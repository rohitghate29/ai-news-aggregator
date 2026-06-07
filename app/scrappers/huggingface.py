from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel
from docling.document_converter import DocumentConverter


class HuggingFaceArticle(BaseModel):
  title: str
  description: str
  url: str
  guid: str
  published_at: datetime
  category: Optional[str] = None


class HuggingFaceScrapper:
  def __init__(self):
    self.rss_url = [
      "https://huggingface.co/blog/feed.xml"
    ]
    self.converter = DocumentConverter()

  def get_articles(self, hours: int=24) -> List[HuggingFaceArticle]:
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
          # Hugging Face RSS entries don't have a 'summary' or 'description' attribute,
          # so we set it to an empty string. The markdown parser will fetch the full content.
          description = getattr(entry, "summary", "")
          articles.append(HuggingFaceArticle(
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


if __name__ == "__main__":
  scrapper = HuggingFaceScrapper()
  articles = scrapper.get_articles(hours=72)
  print(f"Found {len(articles)} articles from the last 72 hours.")
  if articles:
    print(f"Title: {articles[0].title}")
    print(f"URL: {articles[0].url}")
