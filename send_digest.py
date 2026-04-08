"""
Daily News Digest — SBS News
Sends a formatted HTML email digest to sapetech@hotmail.com

Usage:
  python3 send_digest.py

You will be prompted for your sender email and password (app password).
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

# ── Config ────────────────────────────────────────────────────────────────────
TO_EMAIL = "sapetech@hotmail.com"
SUBJECT  = f"📰 Your Daily News Digest — {date.today().strftime('%d %B %Y')}"

# ── HTML Digest Content ───────────────────────────────────────────────────────
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Daily Digest</title>
<style>
  body { margin:0; padding:0; background:#f4f4f5; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; color:#1a1a2e; }
  .wrapper { max-width:640px; margin:32px auto; background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 4px 24px rgba(0,0,0,0.08); }
  .header { background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%); padding:36px 40px; text-align:center; }
  .header h1 { margin:0 0 6px; font-size:26px; font-weight:700; color:#ffffff; letter-spacing:-0.5px; }
  .header p  { margin:0; font-size:13px; color:#94a3b8; }
  .section { padding:28px 40px 0; }
  .section-title { display:flex; align-items:center; gap:10px; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:#64748b; margin-bottom:16px; border-bottom:1px solid #f1f5f9; padding-bottom:10px; }
  .article { margin-bottom:22px; }
  .article h3 { margin:0 0 6px; font-size:16px; font-weight:600; color:#0f172a; line-height:1.4; }
  .article h3 a { color:#0f172a; text-decoration:none; }
  .article h3 a:hover { color:#f97316; }
  .article .summary { margin:0 0 6px; font-size:14px; color:#475569; line-height:1.6; }
  .article .why { margin:0 0 8px; font-size:13px; color:#64748b; line-height:1.5; font-style:italic; }
  .article .tag { display:inline-block; font-size:11px; font-weight:600; padding:3px 10px; border-radius:20px; }
  .tag-war      { background:#fee2e2; color:#991b1b; }
  .tag-rates    { background:#dbeafe; color:#1e40af; }
  .tag-property { background:#dcfce7; color:#166534; }
  .tag-china    { background:#fef9c3; color:#854d0e; }
  .divider { height:1px; background:#f1f5f9; margin:4px 0 18px; }
  .no-result { font-size:14px; color:#94a3b8; font-style:italic; padding:8px 0 20px; }
  .footer { background:#f8fafc; padding:24px 40px; text-align:center; font-size:12px; color:#94a3b8; border-top:1px solid #e2e8f0; }
  .footer a { color:#f97316; text-decoration:none; }
</style>
</head>
<body>
<div class="wrapper">

  <!-- Header -->
  <div class="header">
    <h1>📰 Your Daily Digest</h1>
    <p>Curated from <strong style="color:#f97316;">SBS News</strong> &nbsp;·&nbsp; {date}</p>
  </div>

  <!-- WAR & CONFLICT -->
  <div class="section">
    <div class="section-title">💣 &nbsp;War &amp; Conflict</div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/podcast-episode/strait-of-hormuz-to-reopen-after-iran-us-ceasefire-midday-news-bulletin-8-april-2026/r4mnycurw">Strait of Hormuz to reopen after Iran-US ceasefire</a></h3>
      <p class="summary">The US and Iran have agreed to a two-week ceasefire deal, with the Strait of Hormuz set to reopen to global shipping.</p>
      <p class="why">Why it matters: The Strait of Hormuz carries ~20% of the world's oil — its reopening will ease fuel prices hitting Australian families.</p>
      <span class="tag tag-war">War</span>
    </div>
    <div class="divider"></div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/article/israel-issues-fresh-warning-as-tehran-synagogue-completely-destroyed-by-us-israeli-strikes/5xndiizea">Israel issues fresh warning as Tehran synagogue 'completely destroyed'</a></h3>
      <p class="summary">US-Israeli airstrikes destroyed a Tehran synagogue; the Israeli military issued new warnings to Iranian civilians about train routes.</p>
      <p class="why">Why it matters: Escalating Israel-Iran conflict raises global security fears and affects Australia's foreign policy stance in the region.</p>
      <span class="tag tag-war">War</span>
    </div>
    <div class="divider"></div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/article/australian-federal-police-arrest-army-reservist-charged-with-fighting-in-ukraine/lzvh635lv">Australian Army reservist charged with joining Ukrainian war effort granted bail</a></h3>
      <p class="summary">An Australian Army reservist allegedly worked as a drone operator in Ukraine before returning home — now facing serious charges.</p>
      <p class="why">Why it matters: Highlights the legal risks for Australians involved in foreign conflicts and growing engagement with the Ukraine war.</p>
      <span class="tag tag-war">War</span>
    </div>
  </div>

  <!-- HOME LOANS & INTEREST RATES -->
  <div class="section" style="padding-top:28px;">
    <div class="section-title">🏦 &nbsp;Home Loans &amp; Interest Rates</div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/podcast-episode/rate-cuts-what-rate-cuts-home-prices-have-eaten-them-alive/4kduj363b">Rate cuts? What rate cuts — Home prices have eaten them alive</a></h3>
      <p class="summary">Despite interest rate cuts, Australian home prices have surged so much that buyers are no better off than before the cuts.</p>
      <p class="why">Why it matters: Rate relief hasn't translated to affordability — buyers are still being squeezed by record prices.</p>
      <span class="tag tag-rates">Interest Rates</span>
    </div>
    <div class="divider"></div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/article/banks-warning-could-mean-renewed-cost-of-living-crisis/bmw0vwr4u">Fears of further financial pain as major banks forecast renewed pressure</a></h3>
      <p class="summary">Australia's big four banks are signalling potential rate increases early in the year, worsening cost-of-living pressures.</p>
      <p class="why">Why it matters: Higher rates mean bigger monthly mortgage repayments — a $1M loan could cost $150 more per month.</p>
      <span class="tag tag-rates">Interest Rates</span>
    </div>
  </div>

  <!-- PROPERTY PRICES -->
  <div class="section" style="padding-top:28px;">
    <div class="section-title">🏠 &nbsp;Property Prices</div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/article/2026-australian-property-market-predictions/7zupc0y3o">Where will prices grow the most? This year's property market predictions</a></h3>
      <p class="summary">Australian house prices are tipped to reach record highs in 2026, with national growth of around 5% predicted after 8% in 2025.</p>
      <p class="why">Why it matters: If you're buying or selling this year, prices are still climbing — knowing where growth is strongest can shape decisions.</p>
      <span class="tag tag-property">Property</span>
    </div>
    <div class="divider"></div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/article/summer-rental-property-market-heating-up/cgrp2mvbv">Inside Australia's rental crunch — and what the numbers say about 2026</a></h3>
      <p class="summary">Renters continue to face rising costs and a tight market, with restricted supply and high demand keeping rents elevated nationwide.</p>
      <p class="why">Why it matters: Renters face ongoing affordability stress, with little relief expected despite government schemes.</p>
      <span class="tag tag-property">Property</span>
    </div>
  </div>

  <!-- CHINA NEWS -->
  <div class="section" style="padding-top:28px; padding-bottom:32px;">
    <div class="section-title">🇨🇳 &nbsp;China News</div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/article/how-australia-could-benefit-from-a-us-china-trade-war/ke7ub7mzj">How Australia could benefit from a US-China trade war</a></h3>
      <p class="summary">As the US-China trade war escalates with fresh tariffs, analysts say Australia may gain from redirected Chinese demand for commodities.</p>
      <p class="why">Why it matters: Australia's export economy — iron ore, agriculture, wine — could see a boost if China pivots away from US suppliers.</p>
      <span class="tag tag-china">China</span>
    </div>
    <div class="divider"></div>

    <div class="article">
      <h3><a href="https://www.sbs.com.au/news/article/australian-detained-in-china-hit-with-another-deeply-troubling-verdict-delay/yxu44t294">Australian detained in China hit with another 'troubling' verdict delay</a></h3>
      <p class="summary">An Australian citizen detained in China faces yet another unexplained delay in their trial verdict, drawing concern from Australian officials.</p>
      <p class="why">Why it matters: Raises ongoing concerns about consular access and the safety of Australians traveling or living in China.</p>
      <span class="tag tag-china">China</span>
    </div>
  </div>

  <!-- Footer -->
  <div class="footer">
    Source: <a href="https://www.sbs.com.au/news">SBS News</a> &nbsp;·&nbsp;
    Curated by your Daily Digest skill &nbsp;·&nbsp;
    Run <strong>/daily-digest</strong> in Claude Code for a fresh update
  </div>

</div>
</body>
</html>
""".replace("{date}", date.today().strftime("%d %B %Y"))


# ── Send Email ────────────────────────────────────────────────────────────────
def send_email(from_email: str, password: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"]    = from_email
    msg["To"]      = TO_EMAIL
    msg.attach(MIMEText(HTML, "html"))

    # Detect SMTP server from sender domain
    domain = from_email.split("@")[-1].lower()
    if "gmail" in domain:
        smtp_host, smtp_port = "smtp.gmail.com", 587
    elif "hotmail" in domain or "outlook" in domain or "live" in domain:
        smtp_host, smtp_port = "smtp.office365.com", 587
    elif "yahoo" in domain:
        smtp_host, smtp_port = "smtp.mail.yahoo.com", 587
    else:
        smtp_host = input("SMTP host (e.g. smtp.gmail.com): ").strip()
        smtp_port = 587

    print(f"\nConnecting to {smtp_host}:{smtp_port} ...")
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, TO_EMAIL, msg.as_string())

    print(f"✅ Digest sent to {TO_EMAIL}")


if __name__ == "__main__":
    import getpass
    print("── Daily Digest Email Sender ──")
    print(f"Sending to: {TO_EMAIL}\n")
    from_email = input("Your email address (sender): ").strip()
    password   = getpass.getpass("App password (input hidden): ")
    send_email(from_email, password)
