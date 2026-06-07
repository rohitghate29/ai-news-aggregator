from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel
from docling.document_converter import DocumentConverter


class OllamaArticle(BaseModel):
  title: str
  description: str
  url: str
  guid: str
  published_at: datetime
  category: Optional[str] = None


class OllamaScrapper:
  def __init__(self):
    self.rss_urls = [
      "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_ollama.xml"
    ]
    self.converter = DocumentConverter()

  def get_articles(self, hours: int = 24) -> List[OllamaArticle]:
    now = datetime.now(timezone.utc)
    cutoff_time = now - timedelta(hours=hours)
    articles = []
    seen_guids = set()

    for rss_url in self.rss_urls:
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
          description = entry.get("summary", entry.get("description", ""))
          articles.append(OllamaArticle(
            title=entry.title,
            description=description,
            url=entry.link,
            guid=guid,
            published_at=published_time,
            category=getattr(entry, "category", None)
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
