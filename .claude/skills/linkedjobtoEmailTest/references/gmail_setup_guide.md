# Gmail App Password Setup Guide

## Prerequisites

- A Google account with **2-Step Verification** enabled
- If 2-Step Verification is not enabled, go to: Google Account → Security → 2-Step Verification → Turn On

## Steps to Generate an App Password

1. Go to **myaccount.google.com**
2. Click **Security** in the left sidebar
3. Under "How you sign in to Google", click **2-Step Verification**
4. Scroll to the bottom and click **App passwords**
5. Under "App name", type a label (e.g. `GitHub Actions Job Digest`)
6. Click **Create**
7. Copy the 16-character password shown (e.g. `abcd efgh ijkl mnop`)

## Using the App Password

- Remove spaces when storing it: `abcdefghijklmnop`
- Store it as the `GMAIL_APP_PASSWORD` GitHub secret (never commit it to code)
- Use port **587** with **STARTTLS** (not port 465 with SSL)

## Common Errors

| Error | Cause | Fix |
|---|---|---|
| `SMTPAuthenticationError: 534 Application-specific password required` | Using regular Gmail password instead of app password | Generate an app password as above |
| `SMTPAuthenticationError: 535 Bad credentials` | App password is wrong or has expired | Regenerate the app password |
| App Passwords option not visible | 2-Step Verification not enabled | Enable 2-Step Verification first |

## SMTP Settings Reference

```
Host:     smtp.gmail.com
Port:     587
Security: STARTTLS
Username: your-email@gmail.com
Password: 16-char app password
```
