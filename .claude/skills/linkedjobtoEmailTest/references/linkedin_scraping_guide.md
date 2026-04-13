# LinkedIn Job Scraping Guide

## Guest API Endpoint

LinkedIn exposes a public guest job search endpoint that does not require login:

```
GET https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search
```

### Key Parameters

| Parameter | Description | Example |
|---|---|---|
| `keywords` | Job title or skills to search | `Microsoft Azure` |
| `location` | City, region, or country | `Sydney, New South Wales, Australia` |
| `f_TPR` | Time filter in seconds (`r` prefix) | `r604800` = past 7 days |
| `start` | Pagination offset | `0`, `10`, `25` |
| `count` | Results per page (max ~25) | `25` |

### Time Filter Values

| Value | Meaning |
|---|---|
| `r3600` | Past hour |
| `r86400` | Past 24 hours |
| `r604800` | Past week (7 days) |
| `r2592000` | Past month |

### Example Request

```python
import requests

url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
params = {
    "keywords": "Microsoft Azure",
    "location": "Sydney, New South Wales, Australia",
    "f_TPR": "r604800",
    "start": 0,
}
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
response = requests.get(url, params=params, headers=headers, timeout=15)
```

## Parsing the Response

The response is an HTML fragment containing `<li>` job cards. Use BeautifulSoup:

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, "html.parser")
cards = soup.find_all("li")

for card in cards:
    title = card.find("h3")
    company = card.find("h4")
    location = card.find("span", class_="job-search-card__location")
    date = card.find("time")
    link = card.find("a", href=True)
    job_id_div = card.find("div", {"data-entity-urn": True})
```

## Anti-Blocking Tips

- Add `time.sleep(2)` between keyword searches
- Use a realistic browser `User-Agent` header
- Keep requests to a reasonable rate (1 search per 2–3 seconds)
- LinkedIn may return 0 results or block if too many requests are made quickly

## Keyword Strategy for Sydney Jobs

Recommended search terms for tech roles in Sydney:

```python
SEARCHES = {
    "Microsoft / Azure": "Microsoft Azure",
    "SAP": "SAP",
    "AI Engineer": "AI Engineer",
    "Machine Learning": "Machine Learning",
    "Data Engineering": "Data Engineer",
    "Cloud": "Cloud Architect Sydney",
}
```
