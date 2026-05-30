from typing import List
from .config import YOUTUBE_CHANNELS
from .scrappers.anthropic import AnthropicScrapper, AnthropicArticle
from .scrappers.youtube import YoutubeScrapper, ChannelVideo
from .database.repository import Repository

def run_scrappers(hours: int = 24) -> dict:
  youtube_scrapper = YoutubeScrapper()
  anthropic_scrapper = AnthropicScrapper()
  repo = Repository()

  youtube_videos = []
  video_dicts = []

  for channel_id in YOUTUBE_CHANNELS:
    videos = youtube_scrapper.scrape_channel(channel_id, hours)
    youtube_videos.extend(videos)
    video_dicts.extend([
      {
        "video_id": v.video_id,
        "title": v.title,
        "url": v.url,
        "channel_id": channel_id,
        "published_at": v.published_at,
        "description": v.description,
        "transcript": v.transcript,
      }
      for v in videos
    ])
  
  anthropic_articles = anthropic_scrapper.get_articles(hours)

  if video_dicts:
    repo.bulk_create_youtube_videos(video_dicts)

  if anthropic_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in anthropic_articles
    ]
    repo.bulk_create_anthropic_articles(article_dicts)

  return {
    "youtube": youtube_videos,
    "anthropic": anthropic_articles
  }
  
if __name__ == "__main__":
  results = run_scrappers()
  print(f"Youtube Videos: {len(results['youtube'])}")
  print(f"Anthropic Articles: {len(results['anthropic'])}")