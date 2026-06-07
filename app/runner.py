from typing import List
from .scrappers.anthropic import AnthropicScrapper, AnthropicArticle
from .scrappers.openai import OpenAIScrapper, OpenAIArticle
from .scrappers.huggingface import HuggingFaceScrapper, HuggingFaceArticle
from .scrappers.claude import ClaudeScrapper, ClaudeArticle
from .scrappers.google_ai import GoogleAIScrapper, GoogleAIArticle
from .scrappers.groq import GroqScrapper, GroqArticle
from .scrappers.mistral import MistralScrapper, MistralArticle
from .scrappers.ollama import OllamaScrapper, OllamaArticle
from .scrappers.perplexity import PerplexityScrapper, PerplexityArticle
from .scrappers.xai import XAIScrapper, XAIArticle
from .database.repository import Repository


def run_scrappers(hours: int = 24) -> dict:
  anthropic_scrapper = AnthropicScrapper()
  openai_scrapper = OpenAIScrapper()
  huggingface_scrapper = HuggingFaceScrapper()
  claude_scrapper = ClaudeScrapper()
  google_ai_scrapper = GoogleAIScrapper()
  groq_scrapper = GroqScrapper()
  mistral_scrapper = MistralScrapper()
  ollama_scrapper = OllamaScrapper()
  perplexity_scrapper = PerplexityScrapper()
  xai_scrapper = XAIScrapper()
  repo = Repository()

  anthropic_articles = anthropic_scrapper.get_articles(hours)
  openai_articles = openai_scrapper.get_articles(hours)
  huggingface_articles = huggingface_scrapper.get_articles(hours)
  claude_articles = claude_scrapper.get_articles(hours)
  google_ai_articles = google_ai_scrapper.get_articles(hours)
  groq_articles = groq_scrapper.get_articles(hours)
  mistral_articles = mistral_scrapper.get_articles(hours)
  ollama_articles = ollama_scrapper.get_articles(hours)
  perplexity_articles = perplexity_scrapper.get_articles(hours)
  xai_articles = xai_scrapper.get_articles(hours)

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

  if openai_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in openai_articles
    ]
    repo.bulk_create_openai_articles(article_dicts)

  if huggingface_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in huggingface_articles
    ]
    repo.bulk_create_huggingface_articles(article_dicts)

  if claude_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in claude_articles
    ]
    repo.bulk_create_claude_articles(article_dicts)

  if google_ai_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in google_ai_articles
    ]
    repo.bulk_create_google_ai_articles(article_dicts)

  if groq_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in groq_articles
    ]
    repo.bulk_create_groq_articles(article_dicts)

  if mistral_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in mistral_articles
    ]
    repo.bulk_create_mistral_articles(article_dicts)

  if ollama_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in ollama_articles
    ]
    repo.bulk_create_ollama_articles(article_dicts)

  if perplexity_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in perplexity_articles
    ]
    repo.bulk_create_perplexity_articles(article_dicts)

  if xai_articles:
    article_dicts = [
      {
        "guid": a.guid,
        "title": a.title,
        "url": a.url,
        "published_at": a.published_at,
        "description": a.description,
        "category": a.category,
      }
      for a in xai_articles
    ]
    repo.bulk_create_xai_articles(article_dicts)

  return {
    "anthropic": anthropic_articles,
    "openai": openai_articles,
    "huggingface": huggingface_articles,
    "claude": claude_articles,
    "google_ai": google_ai_articles,
    "groq": groq_articles,
    "mistral": mistral_articles,
    "ollama": ollama_articles,
    "perplexity": perplexity_articles,
    "xai": xai_articles
  }


if __name__ == "__main__":
  results = run_scrappers()
  print(f"Anthropic Articles: {len(results.get('anthropic', []))}")
  print(f"OpenAI Articles: {len(results.get('openai', []))}")
  print(f"Hugging Face Articles: {len(results.get('huggingface', []))}")
  print(f"Claude Articles: {len(results.get('claude', []))}")
  print(f"Google AI Articles: {len(results.get('google_ai', []))}")
  print(f"Groq Articles: {len(results.get('groq', []))}")
  print(f"Mistral Articles: {len(results.get('mistral', []))}")
  print(f"Ollama Articles: {len(results.get('ollama', []))}")
  print(f"Perplexity Articles: {len(results.get('perplexity', []))}")
  print(f"XAI Articles: {len(results.get('xai', []))}")