"""
Eval suite for the linkedjobtoEmailTest skill.

Tests the four core functions in scripts/job_digest.py without making
real HTTP requests or sending real emails.

Run from the repo root:
    pip install requests beautifulsoup4
    python .claude/skills/linkedjobtoEmailTest/eval/eval.py
"""

import os
import sys
import textwrap
import unittest
from unittest.mock import MagicMock, patch

# Allow importing from scripts/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../../scripts"))
from job_digest import build_html_email, deduplicate, search_linkedin_jobs, send_email


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_JOB_HTML = textwrap.dedent("""
    <ul>
      <li>
        <div data-entity-urn="urn:li:jobPosting:111"></div>
        <h3>Azure Cloud Engineer</h3>
        <h4>Microsoft</h4>
        <span class="job-search-card__location">Sydney, NSW, Australia</span>
        <time datetime="2026-04-10"></time>
        <a href="https://www.linkedin.com/jobs/view/111?refId=abc">View</a>
      </li>
      <li>
        <div data-entity-urn="urn:li:jobPosting:222"></div>
        <h3>SAP Functional Consultant</h3>
        <h4>Accenture</h4>
        <span class="job-search-card__location">Sydney, NSW, Australia</span>
        <time datetime="2026-04-09"></time>
        <a href="https://www.linkedin.com/jobs/view/222?refId=def">View</a>
      </li>
      <li>
        <!-- card with no title — should be skipped -->
        <h4>SomeCompany</h4>
      </li>
    </ul>
""")


# ---------------------------------------------------------------------------
# 1. search_linkedin_jobs
# ---------------------------------------------------------------------------

class TestSearchLinkedinJobs(unittest.TestCase):

    @patch("job_digest.requests.get")
    def test_parses_jobs_correctly(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = SAMPLE_JOB_HTML
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        jobs = search_linkedin_jobs("Azure")

        self.assertEqual(len(jobs), 2, "Should parse 2 valid job cards (skip the one with no title)")
        self.assertEqual(jobs[0]["title"], "Azure Cloud Engineer")
        self.assertEqual(jobs[0]["company"], "Microsoft")
        self.assertEqual(jobs[0]["id"], "111")
        self.assertEqual(jobs[0]["date"], "2026-04-10")
        self.assertEqual(jobs[0]["url"], "https://www.linkedin.com/jobs/view/111")

    @patch("job_digest.requests.get")
    def test_returns_empty_list_on_request_error(self, mock_get):
        import requests as req
        mock_get.side_effect = req.RequestException("timeout")

        jobs = search_linkedin_jobs("Azure")
        self.assertEqual(jobs, [], "Should return empty list on network error")

    @patch("job_digest.requests.get")
    def test_passes_correct_params(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.text = "<ul></ul>"
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        search_linkedin_jobs("SAP", location="Melbourne, VIC, Australia", days=3)

        _, kwargs = mock_get.call_args
        params = kwargs["params"]
        self.assertEqual(params["keywords"], "SAP")
        self.assertEqual(params["location"], "Melbourne, VIC, Australia")
        self.assertEqual(params["f_TPR"], "r259200")  # 3 * 86400


# ---------------------------------------------------------------------------
# 2. deduplicate
# ---------------------------------------------------------------------------

class TestDeduplicate(unittest.TestCase):

    def _job(self, id_, title, company):
        return {"id": id_, "title": title, "company": company, "location": "", "date": "", "url": ""}

    def test_removes_duplicate_by_id(self):
        jobs = {
            "Azure": [self._job("111", "Cloud Eng", "Microsoft")],
            "AI":    [self._job("111", "Cloud Eng", "Microsoft")],  # same ID
        }
        result = deduplicate(jobs)
        self.assertEqual(len(result["Azure"]), 1)
        self.assertEqual(len(result["AI"]), 0, "Duplicate by ID should be removed from second category")

    def test_removes_duplicate_by_title_company(self):
        jobs = {
            "Azure": [self._job("", "Cloud Eng", "Microsoft")],
            "AI":    [self._job("", "Cloud Eng", "Microsoft")],  # same title+company, no ID
        }
        result = deduplicate(jobs)
        self.assertEqual(len(result["AI"]), 0, "Duplicate by title+company should be removed")

    def test_keeps_unique_jobs_across_categories(self):
        jobs = {
            "Azure": [self._job("111", "Cloud Eng", "Microsoft")],
            "SAP":   [self._job("222", "SAP Consultant", "Accenture")],
        }
        result = deduplicate(jobs)
        self.assertEqual(len(result["Azure"]), 1)
        self.assertEqual(len(result["SAP"]), 1)

    def test_empty_categories_preserved(self):
        jobs = {"Azure": [], "SAP": []}
        result = deduplicate(jobs)
        self.assertIn("Azure", result)
        self.assertIn("SAP", result)


# ---------------------------------------------------------------------------
# 3. build_html_email
# ---------------------------------------------------------------------------

class TestBuildHtmlEmail(unittest.TestCase):

    def setUp(self):
        self.jobs = {
            "Azure": [
                {"id": "1", "title": "Cloud Eng", "company": "Microsoft",
                 "location": "Sydney", "date": "2026-04-10", "url": "https://example.com/1"},
            ],
            "SAP": [],
        }

    def test_returns_html_string(self):
        html = build_html_email(self.jobs)
        self.assertIsInstance(html, str)
        self.assertIn("<html>", html)

    def test_contains_job_title_as_link(self):
        html = build_html_email(self.jobs)
        self.assertIn("Cloud Eng", html)
        self.assertIn("https://example.com/1", html)

    def test_contains_category_headings(self):
        html = build_html_email(self.jobs)
        self.assertIn("Azure", html)
        self.assertIn("SAP", html)

    def test_empty_category_shows_no_listings_message(self):
        html = build_html_email(self.jobs)
        self.assertIn("No new listings this week", html)

    def test_total_count_in_summary(self):
        html = build_html_email(self.jobs)
        self.assertIn("1 new job(s)", html)

    def test_date_truncated_to_10_chars(self):
        html = build_html_email(self.jobs)
        self.assertIn("2026-04-10", html)


# ---------------------------------------------------------------------------
# 4. send_email
# ---------------------------------------------------------------------------

class TestSendEmail(unittest.TestCase):

    @patch("job_digest.smtplib.SMTP")
    def test_sends_with_correct_credentials(self, mock_smtp_cls):
        mock_server = MagicMock()
        mock_smtp_cls.return_value.__enter__ = MagicMock(return_value=mock_server)
        mock_smtp_cls.return_value.__exit__ = MagicMock(return_value=False)

        env = {
            "GMAIL_USER": "sender@gmail.com",
            "GMAIL_APP_PASSWORD": "testapppassword",
            "RECIPIENT_EMAIL": "recipient@gmail.com",
        }
        with patch.dict(os.environ, env):
            send_email("<html>test</html>", "Test Subject")

        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("sender@gmail.com", "testapppassword")
        mock_server.sendmail.assert_called_once()
        args = mock_server.sendmail.call_args[0]
        self.assertEqual(args[0], "sender@gmail.com")
        self.assertEqual(args[1], "recipient@gmail.com")

    def test_raises_if_env_vars_missing(self):
        for var in ("GMAIL_USER", "GMAIL_APP_PASSWORD", "RECIPIENT_EMAIL"):
            env = {
                "GMAIL_USER": "a@gmail.com",
                "GMAIL_APP_PASSWORD": "pwd",
                "RECIPIENT_EMAIL": "b@gmail.com",
            }
            env.pop(var)
            with self.assertRaises(KeyError, msg=f"Should raise KeyError when {var} is missing"):
                with patch.dict(os.environ, env, clear=True):
                    send_email("<html></html>", "Subject")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Running linkedjobtoEmailTest eval...\n")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for cls in (TestSearchLinkedinJobs, TestDeduplicate, TestBuildHtmlEmail, TestSendEmail):
        suite.addTests(loader.loadTestsFromTestCase(cls))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
