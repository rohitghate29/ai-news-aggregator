from sqlalchemy import null
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class YoutubeVideo(Base):
  __tablename__ = "youtube_videos"

  video_id = Column(String, primary_key=True, index=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  channel_id = Column(String, nullable=False)
  published_at = Column(DateTime, nullable=False)
  description = Column(Text)
  transcript = Column(Text, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)

class OpenAIAtricle(Base):
  __tablename__ = "openai_article"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  markdown = Column(Text, nullable=True)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

class AnthropicArticle(Base):
  __tablename__ = "anthropic_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)
  
class HuggingFaceArticle(Base):
  __tablename__ = "huggingface_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)
class ClaudeArticle(Base):
  __tablename__ = "claude_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

class GoogleAIArticle(Base):
  __tablename__ = "google_ai_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

class GroqArticle(Base):
  __tablename__ = "groq_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

class MistralArticle(Base):
  __tablename__ = "mistral_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

class OllamaArticle(Base):
  __tablename__ = "ollama_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

class PerplexityArticle(Base):
  __tablename__ = "perplexity_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

class XAIArticle(Base):
  __tablename__ = "xai_articles"

  guid = Column(String, primary_key=True)
  title = Column(String, nullable=False)
  url = Column(String, nullable=False)
  description = Column(Text)
  published_at = Column(DateTime, nullable=False)
  category = Column(String, nullable=True)
  markdown = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

class UserPreference(Base):
  __tablename__ = "user_preferences"

  id = Column(String, primary_key=True)          # UUID
  email = Column(String, unique=True, nullable=False, index=True)
  name = Column(String, nullable=False)
  # Comma-separated provider keys e.g. "openai,anthropic,google_ai"
  # NULL means "all providers" (no filter applied)
  providers = Column(Text, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)
  updated_at = Column(DateTime, default=datetime.utcnow)

class Digest(Base):
  __tablename__ = "digests"

  id = Column(String, primary_key=True)
  article_type = Column(String, nullable=False)
  article_id = Column(String, nullable=False)
  url = Column(String, nullable=False)
  title = Column(Text, nullable=False)
  summary = Column(Text, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
