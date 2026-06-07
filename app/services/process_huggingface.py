from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.scrappers.huggingface import HuggingFaceScrapper
from app.database.repository import Repository

def process_huggingface_markdown(limit: Optional[int] = None) -> dict:
  scrapper = HuggingFaceScrapper()
  repo = Repository()

  articles = repo.huggingface_articles_without_md(limit)
  processed = 0
  failed = 0

  for article in articles:
    markdown = scrapper.url_to_markdown(article.url)
    try: 
      if markdown:
        repo.update_huggingface_article_markdown(article.guid, markdown)
        processed += 1
      else:
        failed += 1
    except Exception as e:
      failed += 1
      print(f"Error Processing article {article.guid}: {str(e)}")
      continue

  return {
    "total": len(articles),
    "processed": processed,
    "failed": failed
  }

if __name__ == "__main__":
  result = process_huggingface_markdown(2)
  print(f"Total: {result['total']}")
  print(f"Processed: {result['processed']}")
  print(f"Failed: {result['failed']}")
