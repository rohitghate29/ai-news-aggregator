from typing import Dict, Any
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
import uuid
from .models import YoutubeVideo, OpenAIAtricle, AnthropicArticle, HuggingFaceArticle, ClaudeArticle, GoogleAIArticle, GroqArticle, MistralArticle, OllamaArticle, PerplexityArticle, XAIArticle, Digest, UserPreference
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

  def create_huggingface_article(self, guid, title, url, description, published_at, category) -> HuggingFaceArticle:
    article = HuggingFaceArticle(
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

  def create_claude_article(self, guid, title, url, description, published_at, category) -> ClaudeArticle:
    article = ClaudeArticle(
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

  def create_google_ai_article(self, guid, title, url, description, published_at, category) -> GoogleAIArticle:
    article = GoogleAIArticle(
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

  def create_groq_article(self, guid, title, url, description, published_at, category) -> GroqArticle:
    article = GroqArticle(
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

  def create_mistral_article(self, guid, title, url, description, published_at, category) -> MistralArticle:
    article = MistralArticle(
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

  def create_ollama_article(self, guid, title, url, description, published_at, category) -> OllamaArticle:
    article = OllamaArticle(
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

  def create_perplexity_article(self, guid, title, url, description, published_at, category) -> PerplexityArticle:
    article = PerplexityArticle(
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

  def create_xai_article(self, guid, title, url, description, published_at, category) -> XAIArticle:
    article = XAIArticle(
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

  def bulk_create_huggingface_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(HuggingFaceArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(HuggingFaceArticle(
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

  def huggingface_articles_without_md(self, limit: int = 10) -> list[HuggingFaceArticle]:
    query = self.session.query(HuggingFaceArticle).filter(HuggingFaceArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_huggingface_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(HuggingFaceArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False

  def bulk_create_claude_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(ClaudeArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(ClaudeArticle(
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

  def claude_articles_without_md(self, limit: int = 10) -> list[ClaudeArticle]:
    query = self.session.query(ClaudeArticle).filter(ClaudeArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_claude_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(ClaudeArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False

  def bulk_create_google_ai_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(GoogleAIArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(GoogleAIArticle(
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

  def google_ai_articles_without_md(self, limit: int = 10) -> list[GoogleAIArticle]:
    query = self.session.query(GoogleAIArticle).filter(GoogleAIArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_google_ai_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(GoogleAIArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False

  def bulk_create_groq_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(GroqArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(GroqArticle(
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

  def groq_articles_without_md(self, limit: int = 10) -> list[GroqArticle]:
    query = self.session.query(GroqArticle).filter(GroqArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_groq_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(GroqArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False

  def bulk_create_mistral_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(MistralArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(MistralArticle(
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

  def mistral_articles_without_md(self, limit: int = 10) -> list[MistralArticle]:
    query = self.session.query(MistralArticle).filter(MistralArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_mistral_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(MistralArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False

  def bulk_create_ollama_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(OllamaArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(OllamaArticle(
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

  def ollama_articles_without_md(self, limit: int = 10) -> list[OllamaArticle]:
    query = self.session.query(OllamaArticle).filter(OllamaArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_ollama_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(OllamaArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False

  def bulk_create_perplexity_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(PerplexityArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(PerplexityArticle(
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

  def perplexity_articles_without_md(self, limit: int = 10) -> list[PerplexityArticle]:
    query = self.session.query(PerplexityArticle).filter(PerplexityArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_perplexity_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(PerplexityArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False

  def bulk_create_xai_articles(self, articles: List[dict]) -> int:
    new_articles = []
    for a in articles:
        existing = self.session.query(XAIArticle).filter_by(guid=a["guid"]).first()
        if not existing:
            new_articles.append(XAIArticle(
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

  def xai_articles_without_md(self, limit: int = 10) -> list[XAIArticle]:
    query = self.session.query(XAIArticle).filter(XAIArticle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_xai_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(XAIArticle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False
  
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

  def openai_articles_without_description(self, limit: int = 10) -> list[OpenAIAtricle]:
    query = self.session.query(OpenAIAtricle).filter(OpenAIAtricle.markdown.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()

  def update_openai_article_markdown(self, guid: str, markdown: str) -> bool:
    article = self.session.query(OpenAIAtricle).filter_by(guid=guid).first()
    if article:
      article.markdown = markdown
      self.session.commit()
      return True
    return False
  
  def get_youtube_videos_without_transcript(self, limit: Optional[int] = None) -> List[YoutubeVideo]:
    query = self.session.query(YoutubeVideo).filter(YoutubeVideo.transcript.is_(None))
    if limit:
      query = query.limit(limit)
    return query.all()
    
  def update_youtube_video_transcript(self, video_id: str, transcript: str) -> bool:
    video = self.session.query(YoutubeVideo).filter_by(video_id=video_id).first()
    if video:
      video.transcript = transcript
      self.session.commit()
      return True
    return False

  # ------------------------------------------------------------------ #
  #  User Preference CRUD                                               #
  # ------------------------------------------------------------------ #

  def create_user_preference(self, email: str, name: str, providers: List[str]) -> UserPreference:
    """Create or update a user preference record (upsert by email)."""
    print("Creating user")
    existing = self.session.query(UserPreference).filter_by(email=email).first()
    print("Existing check", existing)
    providers_str = ",".join(p.strip().lower() for p in providers) if providers else None
    print("Providers string", providers_str)
    if existing:
      print("Updating user")
      existing.name = name
      existing.providers = providers_str
      existing.updated_at = datetime.utcnow()
      self.session.commit()
      return existing
    print("Creating new user")
    preference = UserPreference(
      id=str(uuid.uuid4()),
      email=email,
      name=name,
      providers=providers_str
    )
    print("Adding to session", preference)
    self.session.add(preference)
    print("Committing")
    self.session.commit()
    print("Committed")
    return preference

  def get_user_preference(self, email: str) -> Optional[UserPreference]:
    """Fetch a single user preference by email."""
    return self.session.query(UserPreference).filter_by(email=email).first()

  def get_all_user_preferences(self) -> List[UserPreference]:
    """Fetch all registered users."""
    return self.session.query(UserPreference).all()

  def update_user_providers(self, email: str, providers: List[str]) -> Optional[UserPreference]:
    """Update only the providers list for a user."""
    preference = self.session.query(UserPreference).filter_by(email=email).first()
    if not preference:
      return None
    preference.providers = ",".join(p.strip().lower() for p in providers) if providers else None
    preference.updated_at = datetime.utcnow()
    self.session.commit()
    return preference

  def delete_user_preference(self, email: str) -> bool:
    """Delete a user preference record. Returns True if deleted."""
    preference = self.session.query(UserPreference).filter_by(email=email).first()
    if not preference:
      return False
    self.session.delete(preference)
    self.session.commit()
    return True

  def get_articles_without_digest(self, limit: Optional[int] = None, providers: Optional[List[str]] = None) -> List[Dict[str, Any]]:
      articles = []
      seen_ids = set()

      # Normalise the provider filter. None / empty = all sources.
      active_providers = set(p.strip().lower() for p in providers) if providers else None

      def _include(source: str) -> bool:
          """Return True if this source should be queried for this user."""
          return active_providers is None or source in active_providers

      digests = self.session.query(Digest).all()
      for d in digests:
          seen_ids.add(f"{d.article_type}:{d.article_id}")

      if _include("youtube"):
          youtube_videos = self.session.query(YoutubeVideo).filter(
              YoutubeVideo.transcript.isnot(None),
              YoutubeVideo.transcript != "__UNAVAILABLE__"
          ).all()
          for video in youtube_videos:
              key = f"youtube:{video.video_id}"
              if key not in seen_ids:
                  articles.append({

                  "type": "youtube",
                  "id": video.video_id,
                  "title": video.title,
                  "url": video.url,
                  "content": video.transcript or video.description or "",
                  "published_at": video.published_at
              })

      if _include("openai"):
          openai_articles = self.session.query(OpenAIAtricle).filter(
              OpenAIAtricle.markdown.isnot(None)
          ).all()
          openai_added = 0
          for article in openai_articles:
              if openai_added >= 3:
                  break
              key = f"openai:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "openai",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or "",
                      "published_at": article.published_at
                  })
                  openai_added += 1

      if _include("anthropic"):
          anthropic_articles = self.session.query(AnthropicArticle).filter(
              AnthropicArticle.markdown.isnot(None)
          ).all()
          anthropic_added = 0
          for article in anthropic_articles:
              if anthropic_added >= 3:
                  break
              key = f"anthropic:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "anthropic",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  anthropic_added += 1

      if _include("huggingface"):
          huggingface_articles = self.session.query(HuggingFaceArticle).filter(
              HuggingFaceArticle.markdown.isnot(None)
          ).all()
          huggingface_added = 0
          for article in huggingface_articles:
              if huggingface_added >= 3:
                  break
              key = f"huggingface:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "huggingface",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  huggingface_added += 1

      if _include("claude"):
          claude_articles = self.session.query(ClaudeArticle).filter(
              ClaudeArticle.markdown.isnot(None)
          ).all()
          claude_added = 0
          for article in claude_articles:
              if claude_added >= 3:
                  break
              key = f"claude:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "claude",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  claude_added += 1

      if _include("google_ai"):
          google_ai_articles = self.session.query(GoogleAIArticle).filter(
              GoogleAIArticle.markdown.isnot(None)
          ).all()
          google_ai_added = 0
          for article in google_ai_articles:
              if google_ai_added >= 3:
                  break
              key = f"google_ai:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "google_ai",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  google_ai_added += 1

      if _include("groq"):
          groq_articles = self.session.query(GroqArticle).filter(
              GroqArticle.markdown.isnot(None)
          ).all()
          groq_added = 0
          for article in groq_articles:
              if groq_added >= 3:
                  break
              key = f"groq:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "groq",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  groq_added += 1

      if _include("mistral"):
          mistral_articles = self.session.query(MistralArticle).filter(
              MistralArticle.markdown.isnot(None)
          ).all()
          mistral_added = 0
          for article in mistral_articles:
              if mistral_added >= 3:
                  break
              key = f"mistral:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "mistral",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  mistral_added += 1

      if _include("ollama"):
          ollama_articles = self.session.query(OllamaArticle).filter(
              OllamaArticle.markdown.isnot(None)
          ).all()
          ollama_added = 0
          for article in ollama_articles:
              if ollama_added >= 3:
                  break
              key = f"ollama:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "ollama",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  ollama_added += 1

      if _include("perplexity"):
          perplexity_articles = self.session.query(PerplexityArticle).filter(
              PerplexityArticle.markdown.isnot(None)
          ).all()
          perplexity_added = 0
          for article in perplexity_articles:
              if perplexity_added >= 3:
                  break
              key = f"perplexity:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "perplexity",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  perplexity_added += 1

      if _include("xai"):
          xai_articles = self.session.query(XAIArticle).filter(
              XAIArticle.markdown.isnot(None)
          ).all()
          xai_added = 0
          for article in xai_articles:
              if xai_added >= 3:
                  break
              key = f"xai:{article.guid}"
              if key not in seen_ids:
                  articles.append({
                      "type": "xai",
                      "id": article.guid,
                      "title": article.title,
                      "url": article.url,
                      "content": article.markdown or article.description or "",
                      "published_at": article.published_at
                  })
                  xai_added += 1

      if limit:
          articles = articles[:limit]

      return articles


  def create_digest(self, article_type: str, article_id: str, url: str, title: str, summary: str, published_at: Optional[datetime] = None) -> Optional[Digest]:
        digest_id = f"{article_type}:{article_id}"
        existing = self.session.query(Digest).filter_by(id=digest_id).first()
        if existing:
            return None
        
        if published_at:
            if published_at.tzinfo is None:
                published_at = published_at.replace(tzinfo=timezone.utc)
            created_at = published_at
        else:
            created_at = datetime.now(timezone.utc)
        
        digest = Digest(
            id=digest_id,
            article_type=article_type,
            article_id=article_id,
            url=url,
            title=title,
            summary=summary,
            created_at=created_at
        )
        self.session.add(digest)
        self.session.commit()
        return digest
    
  def get_recent_digests(self, hours: int = 24) -> List[Dict[str, Any]]:
      cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
      digests = self.session.query(Digest).filter(
          Digest.created_at >= cutoff_time
      ).order_by(Digest.created_at.desc()).all()
      
      return [
          {
              "id": d.id,
              "article_type": d.article_type,
              "article_id": d.article_id,
              "url": d.url,
              "title": d.title,
              "summary": d.summary,
              "created_at": d.created_at
          }
          for d in digests
      ]