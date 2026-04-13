"""
Weekly LinkedIn job digest — scrapes public LinkedIn guest API and sends
a formatted HTML email via Gmail SMTP.

Required environment variables:
  GMAIL_USER          sender Gmail address
  GMAIL_APP_PASSWORD  16-char Gmail app password
  RECIPIENT_EMAIL     destination email address
"""

import os
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from bs4 import BeautifulSoup

LOCATION = "Sydney, New South Wales, Australia"
DAYS = 7  # "past week" filter
TIME_FILTER = f"r{DAYS * 86400}"  # LinkedIn uses seconds

SEARCHES = {
    "Microsoft / Azure": "Microsoft Azure",
    "SAP": "SAP",
    "AI Engineer": "AI Engineer",
    "Machine Learning": "Machine Learning",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def search_linkedin_jobs(query: str, location: str = LOCATION, days: int = DAYS) -> list[dict]:
    """Fetch job listings from LinkedIn guest search API for one query."""
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    params = {
        "keywords": query,
        "location": location,
        "f_TPR": f"r{days * 86400}",
        "start": 0,
    }

    jobs = []
    try:
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  Warning: request failed for '{query}': {e}")
        return jobs

    soup = BeautifulSoup(resp.text, "html.parser")
    cards = soup.find_all("li")

    for card in cards:
        job_id_tag = card.find("div", {"data-entity-urn": True})
        title_tag = card.find("h3")
        company_tag = card.find("h4")
        location_tag = card.find("span", class_="job-search-card__location")
        date_tag = card.find("time")
        link_tag = card.find("a", href=True)

        if not title_tag:
            continue

        job_id = ""
        if job_id_tag:
            urn = job_id_tag.get("data-entity-urn", "")
            job_id = urn.split(":")[-1]

        jobs.append({
            "id": job_id,
            "title": title_tag.get_text(strip=True),
            "company": company_tag.get_text(strip=True) if company_tag else "",
            "location": location_tag.get_text(strip=True) if location_tag else location,
            "date": date_tag.get("datetime", "") if date_tag else "",
            "url": link_tag["href"].split("?")[0] if link_tag else "",
        })

    return jobs


def deduplicate(jobs_by_category: dict[str, list[dict]]) -> dict[str, list[dict]]:
    """Remove jobs that appear in multiple category results, keeping the first occurrence."""
    seen_ids: set[str] = set()
    seen_titles: set[str] = set()
    result = {}

    for category, jobs in jobs_by_category.items():
        unique = []
        for job in jobs:
            key = job["id"] if job["id"] else job["title"].lower() + job["company"].lower()
            if key not in seen_ids and key not in seen_titles:
                seen_ids.add(key)
                seen_titles.add(job["title"].lower() + job["company"].lower())
                unique.append(job)
        result[category] = unique

    return result


def build_html_email(jobs_by_category: dict[str, list[dict]]) -> str:
    """Render an HTML email body from grouped job listings."""
    today = datetime.utcnow().strftime("%d %B %Y")
    total = sum(len(v) for v in jobs_by_category.values())

    sections = ""
    for category, jobs in jobs_by_category.items():
        if not jobs:
            rows = "<tr><td colspan='4' style='color:#888;padding:8px 0'>No new listings this week.</td></tr>"
        else:
            rows = ""
            for job in jobs:
                date_display = job["date"][:10] if job["date"] else ""
                url = job["url"] or "#"
                rows += f"""
                <tr>
                  <td style="padding:6px 8px;border-bottom:1px solid #eee">
                    <a href="{url}" style="color:#0073b1;text-decoration:none">{job['title']}</a>
                  </td>
                  <td style="padding:6px 8px;border-bottom:1px solid #eee">{job['company']}</td>
                  <td style="padding:6px 8px;border-bottom:1px solid #eee">{job['location']}</td>
                  <td style="padding:6px 8px;border-bottom:1px solid #eee;color:#666">{date_display}</td>
                </tr>"""

        sections += f"""
        <h2 style="color:#0073b1;font-size:16px;margin:24px 0 8px">{category} ({len(jobs)} jobs)</h2>
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <thead>
            <tr style="background:#f3f3f3">
              <th style="text-align:left;padding:6px 8px">Title</th>
              <th style="text-align:left;padding:6px 8px">Company</th>
              <th style="text-align:left;padding:6px 8px">Location</th>
              <th style="text-align:left;padding:6px 8px">Posted</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>"""

    return f"""
    <html><body style="font-family:Arial,sans-serif;max-width:900px;margin:auto;padding:24px">
      <h1 style="color:#0073b1">LinkedIn Job Digest — {today}</h1>
      <p style="color:#444">
        {total} new job(s) found in <strong>Sydney, Australia</strong>
        across {len(jobs_by_category)} categories this week.
      </p>
      {sections}
      <hr style="margin-top:32px;border:none;border-top:1px solid #ddd">
      <p style="color:#999;font-size:12px">
        Auto-generated by the LinkedIn Job Digest workflow.
        Search location: {LOCATION}.
      </p>
    </body></html>
    """


def send_email(html: str, subject: str) -> None:
    """Send an HTML email via Gmail SMTP."""
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = recipient
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg.as_string())

    print(f"Email sent to {recipient}")


def main() -> None:
    print(f"Starting LinkedIn job digest — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

    jobs_by_category: dict[str, list[dict]] = {}
    for category, query in SEARCHES.items():
        print(f"Searching: {query} in {LOCATION} ...")
        jobs = search_linkedin_jobs(query)
        jobs_by_category[category] = jobs
        print(f"  Found {len(jobs)} listing(s)")
        time.sleep(2)  # be polite to LinkedIn

    jobs_by_category = deduplicate(jobs_by_category)

    total = sum(len(v) for v in jobs_by_category.values())
    print(f"Total unique jobs after deduplication: {total}")

    html = build_html_email(jobs_by_category)
    today = datetime.utcnow().strftime("%d %b %Y")
    subject = f"LinkedIn Job Digest — {today} ({total} new jobs in Sydney)"

    send_email(html, subject)


if __name__ == "__main__":
    main()
