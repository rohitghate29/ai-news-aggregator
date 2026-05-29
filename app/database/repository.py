from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from .models import YoutubeVideo, OpenAIAtricle, AnthropicArticle
from .connection import get_session

class Repository:
  def __init__(self, session: Optional[Session] = None):
    self.session = session or get_session()

  def create_youtube_video(self, video_id: str, title: str, url: str, channel_id: str, published_at: datetime, description: str = "", transcript: Optional[str] =None) -> YoutubeVideo:
    video = YoutubeVideo(
      video_id=video_id,
      title=title,
      url=url,
      channel_id=channel_id,
      published_at=published_at,
      description=description,
      transcript=transcript
    )
    self.session.merge(video)
    self.session.commit()
    return video

  def create_openai_article(self, guid, title, url, description, published_at, category) -> OpenAIAtricle:
    article = OpenAIAtricle(
      guid=guid,
      title=title,
      url=url,
      description=description,
      published_at=published_at,
      category=category
    )
    self.session.merge(article)
    self.session.commit()
    return article

  def create_anthropic_article(self, guid, title, url, description, published_at, category) -> AnthropicArticle:
    article = AnthropicArticle(
      guid=guid,
      title=title,
      url=url,
      description=description,
      published_at=published_at,
      category=category
    )
    self.session.merge(article)
    self.session.commit()
    return article

  def bulk_create_youtube_videos(self, videos: List[dict]) -> int:
        new_videos = []
        for v in videos:
            existing = self.session.query(YoutubeVideo).filter_by(video_id=v["video_id"]).first()
            if not existing:
                new_videos.append(YoutubeVideo(
                    video_id=v["video_id"],
                    title=v["title"],
                    url=v["url"],
                    channel_id=v.get("channel_id", ""),
                    published_at=v["published_at"],
                    description=v.get("description", ""),
                    transcript=v.get("transcript")
                ))
        if new_videos:
            self.session.add_all(new_videos)
            self.session.commit()
        return len(new_videos)
    
  def bulk_create_openai_articles(self, articles: List[dict]) -> int:
      new_articles = []
      for a in articles:
          existing = self.session.query(OpenAIAtricle).filter_by(guid=a["guid"]).first()
          if not existing:
              new_articles.append(OpenAIAtricle(
                  guid=a["guid"],
                  title=a["title"],
                  url=a["url"],
                  published_at=a["published_at"],
                  description=a.get("description", ""),
                  category=a.get("category")
              ))
      if new_articles:
          self.session.add_all(new_articles)
          self.session.commit()
      return len(new_articles)
    
  def bulk_create_anthropic_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(AnthropicArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(AnthropicArticle(
                guid=a["guid"],
                title=a["title"],
                url=a["url"],
                published_at=a["published_at"],
                description=a.get("description", ""),
                category=a.get("category")
            ))
    if new_articles:
      self.session.add_all(new_articles)
      self.session.commit()
    return len(new_articles)
  
  def anthropic_articles_without_md(self, limit: int = 10) -> list[AnthropicArticle]:
    query = self.session.query(AnthropicArticle).filter(AnthropicArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()
  
  def update_anthropic_article_markdown(self, guid: str, markdown: str) -> bool: 
    article = self.session.query(AnthropicArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False