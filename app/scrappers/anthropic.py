from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel
from docling.document_converter import DocumentConverter

class AnthropicArticle(BaseModel):
  title: str
  description: str
  url: str
  guid: str
  published_at: datetime
  category: Optional[str] = None

class AnthropicScrapper:
  def __init__(self):
    self.rss_url = [
      "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
      "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
      "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml"
      ]
    self.converter = DocumentConverter()

  def get_articles(self, hours: int=24) -> List[AnthropicArticle]:
    now = datetime.now(timezone.utc)
    cutoff_time = now - timedelta(hours=hours)
    articles = []
    seen_guids = set()

    for rss_url in self.rss_url:
      feed = feedparser.parse(rss_url)
      if not feed.entries:
        continue
      for entry in feed.entries:
        published_parsed = getattr(entry, "published_parsed", None)
        if not published_parsed:
          continue
        published_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)
        if published_time < cutoff_time:
          break
        guid = entry.get("id", entry.get("link", ""))
        if guid not in seen_guids:
          seen_guids.add(guid)
          articles.append(AnthropicArticle(
            title=entry.title,
            description=entry.summary,
            url=entry.link,
            guid=entry.id,
            published_at=published_time,
            category=entry.category
          ))

    return articles

  def url_to_markdown(self, url: str) -> str:
    try:
      result = self.converter.convert(url)
      document = result.document
      return document.export_to_markdown()
    except Exception:
      print("Failed to create markdown")
      return None


if __name__ == "__main__":
  scrapper = AnthropicScrapper()
  articles: List[AnthropicArticle] = scrapper.get_articles(hours=24)
  markdown: str = scrapper.url_to_markdown(articles[1].url)
  print(markdown)