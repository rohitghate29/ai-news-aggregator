import os
import smtplib
import html
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import markdown

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(
    subject: str,
    body_text: str,
    body_html: str = None,
    recipients: list = None,
    headers: dict = None,
):
    if recipients is None:
        if not MY_EMAIL:
            raise ValueError("MY_EMAIL environment variable is not set")
        recipients = [MY_EMAIL]

    recipients = [r for r in recipients if r is not None]
    if not recipients:
        raise ValueError("No valid recipients provided")

    if not MY_EMAIL:
        raise ValueError("MY_EMAIL environment variable is not set")
    if not APP_PASSWORD:
        raise ValueError("APP_PASSWORD environment variable is not set")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = MY_EMAIL
    msg["To"] = ", ".join(recipients)
    if headers:
        for key, value in headers.items():
            if value:
                msg[key] = value

    part1 = MIMEText(body_text, "plain")
    msg.attach(part1)

    if body_html:
        part2 = MIMEText(body_html, "html")
        msg.attach(part2)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(MY_EMAIL, APP_PASSWORD)
        smtp.sendmail(MY_EMAIL, recipients, msg.as_string())


def markdown_to_html(markdown_text: str) -> str:
    content_html = markdown.markdown(markdown_text, extensions=["extra", "nl2br"])
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            background-color: #f5f7fb;
            color: #202124;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 24px 16px;
        }}
        .email-shell {{
            background-color: #ffffff;
            border: 1px solid #e6e9ef;
            border-radius: 14px;
            margin: 0 auto;
            max-width: 680px;
            padding: 28px 32px;
        }}
        h2, h3 {{
            color: #111827;
            line-height: 1.35;
        }}
        p {{
            color: #3f4654;
        }}
        a {{
            color: #2563eb;
            font-weight: 600;
            text-decoration: none;
        }}
    </style>
</head>
<body>
<div class="email-shell">
{content_html}
</div>
</body>
</html>"""


def digest_to_html(digest_response, unsubscribe_url: str = None) -> str:
    from app.agent.email_agent import EmailDigestResponse

    if not isinstance(digest_response, EmailDigestResponse):
        content = digest_response.to_markdown() if hasattr(digest_response, "to_markdown") else str(digest_response)
        return markdown_to_html(content)

    source_mapping = {
        "youtube": "YouTube",
        "openai": "OpenAI",
        "anthropic": "Anthropic",
        "huggingface": "Hugging Face",
        "claude": "Claude",
        "google_ai": "Google AI",
        "groq": "Groq",
        "mistral": "Mistral AI",
        "ollama": "Ollama",
        "perplexity": "Perplexity Hub",
        "xai": "XAI",
    }

    greeting_html = markdown.markdown(digest_response.introduction.greeting, extensions=["extra", "nl2br"])
    introduction_html = markdown.markdown(digest_response.introduction.introduction, extensions=["extra", "nl2br"])

    html_parts = [
        '<div class="hero">',
        f'<div class="greeting">{greeting_html}</div>',
        f'<div class="introduction">{introduction_html}</div>',
        '</div>',
        '<div class="content">',
    ]

    for article in digest_response.articles:
        summary_html = markdown.markdown(article.summary, extensions=["extra", "nl2br"])
        source_name = source_mapping.get(article.article_type.lower(), article.article_type.title())
        match_score = round(article.relevance_score * 10)
        html_parts.extend([
            '<div class="article-card">',
            '<div class="article-meta">',
            '<div class="meta-left">',
            f'<span class="source-pill">{html.escape(source_name)}</span>',
            '</div>',
            '</div>',
            f'<h3>{html.escape(article.title)}</h3>',
            f'<div class="summary">{summary_html}</div>',
            '<div class="card-footer">',
            '<div class="tags">',
            f'<span>{html.escape(source_name)}</span>',
            '<span>AI News</span>',
            '</div>',
            f'<a href="{html.escape(article.url)}" class="article-link">Read</a>',
            '</div>',
            '</div>',
        ])

    html_parts.append('</div>')

    if unsubscribe_url:
        html_parts.append(
            '<p class="footer">'
            'You are receiving this because you subscribed to AI News Aggregator. '
            f'<a href="{html.escape(unsubscribe_url)}">Unsubscribe</a>'
            '</p>'
        )

    html_content = "\n".join(html_parts)

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            box-sizing: border-box;
        }}
        body {{
            background-color: #f3f5fb;
            color: #080d1d;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.5;
            margin: 0;
            padding: 0;
        }}
        .email-shell {{
            background-color: #f3f5fb;
            margin: 0 auto;
            max-width: 760px;
            overflow: hidden;
        }}
        .preheader {{
            color: transparent;
            display: none;
            max-height: 0;
            opacity: 0;
            overflow: hidden;
        }}
        .hero {{
            padding: 30px 42px 16px 42px;
        }}
        .greeting {{
            color: #080d1d;
            font-size: 22px;
            font-weight: 800;
            line-height: 1.3;
            margin-bottom: 10px;
        }}
        .greeting p,
        .introduction p {{
            margin: 0;
        }}
        .introduction {{
            color: #2f3441;
            font-size: 14px;
            margin: 0;
        }}
        .content {{
            background-color: #f3f5fb;
            padding: 12px 42px 48px 42px;
        }}
        .article-card {{
            background-color: #ffffff;
            border: 1px solid #c9ced9;
            border-radius: 10px;
            margin: 0 0 22px 0;
            padding: 20px 22px 18px 22px;
        }}
        .article-meta {{
            align-items: center;
            display: flex;
            justify-content: space-between;
            margin-bottom: 14px;
        }}
        .meta-left {{
            align-items: center;
            display: flex;
            gap: 10px;
        }}
        .source-icon {{
            color: #0148ff;
            display: inline-block;
            font-size: 10px;
            font-weight: 900;
            letter-spacing: -0.04em;
            line-height: 1;
        }}
        .source-pill {{
            background-color: #eef5ff;
            border-radius: 4px;
            color: #0148ff;
            display: inline-block;
            font-size: 12px;
            font-weight: 500;
            line-height: 1.2;
            padding: 3px 8px;
        }}
        .score {{
            color: #161b27;
            font-size: 12px;
            font-weight: 500;
            white-space: nowrap;
        }}
        h3 {{
            color: #080d1d;
            font-size: 18px;
            font-weight: 800;
            line-height: 1.3;
            margin: 0 0 10px 0;
        }}
        p {{
            color: #242936;
            margin: 8px 0;
        }}
        .summary {{
            color: #242936;
            font-size: 14px;
        }}
        .summary p {{
            margin: 8px 0;
        }}
        strong {{
            color: #111827;
            font-weight: 600;
        }}
        em {{
            color: #596174;
            font-style: italic;
        }}
        a {{
            color: #2563eb;
            font-weight: 500;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .article-link {{
            background-color: #111827;
            border: 1px solid #020716;
            border-radius: 4px;
            color: #ffffff;
            display: inline-block;
            font-size: 12px;
            font-weight: 800;
            line-height: 1;
            min-width: 72px;
            padding: 11px 16px;
            text-align: center;
        }}
        .article-link:hover {{
            color: #ffffff;
            text-decoration: none;
        }}
        .card-footer {{
            border-top: 1px solid #dbe3f2;
            margin-top: 24px;
            padding-top: 16px;
        }}
        .tags {{
            display: inline-block;
            width: 72%;
        }}
        .tags span {{
            background-color: #f5f7fc;
            border-radius: 4px;
            color: #1f2430;
            display: inline-block;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.02em;
            line-height: 1;
            margin: 0 6px 6px 0;
            padding: 7px 9px;
        }}
        .footer {{
            border-top: 1px solid #c9ced9;
            background-color: #f3f5fb;
            color: #5f6470;
            font-size: 12px;
            line-height: 1.5;
            margin: 0;
            padding: 28px 32px 44px 32px;
            text-align: center;
        }}
        .footer a {{
            color: #555;
            text-decoration: underline;
        }}
        @media screen and (max-width: 520px) {{
            body {{
                background-color: #f3f5fb;
                padding: 0;
            }}
            .hero,
            .content,
            .footer {{
                padding-left: 18px;
                padding-right: 18px;
            }}
            .article-meta {{
                display: block;
            }}
            .score {{
                display: block;
                margin-top: 8px;
            }}
            .tags {{
                display: block;
                width: 100%;
            }}
            .article-link {{
                margin-top: 10px;
            }}
        }}
    </style>
</head>
<body>
<div class="preheader">Your personalized AI news digest is ready.</div>
<div class="email-shell">
{html_content}
</div>
</body>
</html>"""


def send_email_to_self(subject: str, body: str):
    if not MY_EMAIL:
        raise ValueError("MY_EMAIL environment variable is not set. Please set it in your .env file.")
    send_email(subject, body, recipients=[MY_EMAIL])


if __name__ == "__main__":
    send_email_to_self("Test from Python", "Hello from my script.")
