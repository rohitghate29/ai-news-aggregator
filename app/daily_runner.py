from IPython.core.magics import logging
import logging
from datetime import datetime
from  dotenv import load_dotenv

load_dotenv()

from app.runner import run_scrappers
from app.services.process_anthropic import process_anthropic_markdown
from app.services.process_openai import process_openai_markdown
from app.services.process_huggingface import process_huggingface_markdown
from app.services.process_claude import process_claude_markdown
from app.services.process_google_ai import process_google_ai_markdown
from app.services.process_groq import process_groq_markdown
from app.services.process_mistral import process_mistral_markdown
from app.services.process_ollama import process_ollama_markdown
from app.services.process_perplexity import process_perplexity_markdown
from app.services.process_xai import process_xai_markdown
from app.services.process_digest import process_digests
from app.services.process_email import send_digest_email
from app.database.repository import Repository

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def run_daily_pipeline(hours: int = 24, top_n: int = 10) -> dict:
    start_time = datetime.now()
    logger.info("="*60)
    logger.info(f"Starting daily pipeline at {start_time}")
    logger.info("="*60)

    results = {
      "start_time": start_time.isoformat(),
      "scrapping": {},
      "processing": {},
      "digests": {},
      "email": {},
      "success": False
    }

    try:
      # Step 1: Run Scrappers
      logger.info("\nStep 1: Running Scrappers...")
      scrapping_results = run_scrappers(hours=hours)
      results["scrapping"] = {
        "youtube": len(scrapping_results.get("youtube", [])),
        "anthropic": len(scrapping_results.get("anthropic", [])),
        "openai": len(scrapping_results.get("openai", [])),
        "huggingface": len(scrapping_results.get("huggingface", [])),
        "claude": len(scrapping_results.get("claude", [])),
        "google_ai": len(scrapping_results.get("google_ai", [])),
        "groq": len(scrapping_results.get("groq", [])),
        "mistral": len(scrapping_results.get("mistral", [])),
        "ollama": len(scrapping_results.get("ollama", [])),
        "perplexity": len(scrapping_results.get("perplexity", [])),
        "xai": len(scrapping_results.get("xai", [])),
        "digest": len(scrapping_results.get("digest", []))
      }
      logger.info(f"Scrapping completed: YouTube={results['scrapping']['youtube']}")
      logger.info(f"Scrapping completed: Anthropic={results['scrapping']['anthropic']}")
      logger.info(f"Scrapping completed: OpenAI={results['scrapping']['openai']}")
      logger.info(f"Scrapping completed: HuggingFace={results['scrapping']['huggingface']}")
      logger.info(f"Scrapping completed: Claude={results['scrapping']['claude']}")
      logger.info(f"Scrapping completed: GoogleAI={results['scrapping']['google_ai']}")
      logger.info(f"Scrapping completed: Groq={results['scrapping']['groq']}")
      logger.info(f"Scrapping completed: Mistral={results['scrapping']['mistral']}")
      logger.info(f"Scrapping completed: Ollama={results['scrapping']['ollama']}")
      logger.info(f"Scrapping completed: Perplexity={results['scrapping']['perplexity']}")
      logger.info(f"Scrapping completed: XAI={results['scrapping']['xai']}")
      logger.info(f"Scrapping completed: Digest={results['scrapping']['digest']}")

      # Step 2: Process Anthropic
      logger.info("\nStep 2: Processing Anthropic markdown...")
      anthropic_result = process_anthropic_markdown()
      results["processing"]["anthropic"] = anthropic_result
      logger.info(f"Anthropic processing completed: {anthropic_result['processed']} articles processed")
      
      # Step 2b: Process OpenAI
      logger.info("\nStep 2b: Processing OpenAI descriptions...")
      openai_result = process_openai_markdown()
      results["processing"]["openai"] = openai_result
      logger.info(f"OpenAI processing completed: {openai_result['processed']} articles processed")

      # Step 2c: Process Hugging Face
      logger.info("\nStep 2c: Processing Hugging Face articles...")
      huggingface_result = process_huggingface_markdown()
      results["processing"]["huggingface"] = huggingface_result
      logger.info(f"Hugging Face processing completed: {huggingface_result['processed']} articles processed")

      # Step 2d: Process Claude
      logger.info("\nStep 2d: Processing Claude articles...")
      claude_result = process_claude_markdown()
      results["processing"]["claude"] = claude_result
      logger.info(f"Claude processing completed: {claude_result['processed']} articles processed")

      # Step 2e: Process Google AI
      logger.info("\nStep 2e: Processing Google AI articles...")
      google_ai_result = process_google_ai_markdown()
      results["processing"]["google_ai"] = google_ai_result
      logger.info(f"Google AI processing completed: {google_ai_result['processed']} articles processed")

      # Step 2f: Process Groq
      logger.info("\nStep 2f: Processing Groq articles...")
      groq_result = process_groq_markdown()
      results["processing"]["groq"] = groq_result
      logger.info(f"Groq processing completed: {groq_result['processed']} articles processed")

      # Step 2g: Process Mistral
      logger.info("\nStep 2g: Processing Mistral articles...")
      mistral_result = process_mistral_markdown()
      results["processing"]["mistral"] = mistral_result
      logger.info(f"Mistral processing completed: {mistral_result['processed']} articles processed")

      # Step 2h: Process Ollama
      logger.info("\nStep 2h: Processing Ollama articles...")
      ollama_result = process_ollama_markdown()
      results["processing"]["ollama"] = ollama_result
      logger.info(f"Ollama processing completed: {ollama_result['processed']} articles processed")

      # Step 2i: Process Perplexity
      logger.info("\nStep 2i: Processing Perplexity articles...")
      perplexity_result = process_perplexity_markdown()
      results["processing"]["perplexity"] = perplexity_result
      logger.info(f"Perplexity processing completed: {perplexity_result['processed']} articles processed")

      # Step 2j: Process XAI
      logger.info("\nStep 2j: Processing XAI articles...")
      xai_result = process_xai_markdown()
      results["processing"]["xai"] = xai_result
      logger.info(f"XAI processing completed: {xai_result['processed']} articles processed")
      
      # Step 3: Process YouTube
      logger.info("\nStep 3: Processing YouTube transcripts...")
      
      # Step 4: Process Digests
      logger.info("\nStep 4: Processing digests...")
      digest_result = process_digests()
      results["digests"] = digest_result
      logger.info(f"Digest processing completed: {digest_result['processed']} digests created")
      
      # Step 5: Send per-user personalized emails
      logger.info("\nStep 5: Sending personalized emails...")
      repo = Repository()
      users = repo.get_all_user_preferences()

      if not users:
        # No registered users — send one global email to the default address
        logger.info("No registered users found. Sending global email to default address.")
        email_result = send_digest_email(hours=hours, top_n=top_n)
        results["email"] = [email_result]
        if email_result["success"]:
          logger.info(f"Email sent to default: {email_result['subject']}")
        else:
          logger.error(f"Default email failed: {email_result.get('error', 'Unknown error')}")
      else:
        logger.info(f"Sending emails to {len(users)} registered users...")
        email_results = []
        for user in users:
          providers = [p for p in (user.providers or "").split(",") if p] or None
          logger.info(
            f"  → {user.email} | providers: {providers or 'all'}"
          )
          email_result = send_digest_email(
            hours=hours,
            top_n=top_n,
            recipient_email=user.email,
            recipient_name=user.name,
            providers=providers,
          )
          email_results.append(email_result)
          if email_result["success"]:
            logger.info(f"    ✓ Email sent to {user.email}")
          else:
            logger.error(f"    ✗ Failed for {user.email}: {email_result.get('error')}")
        results["email"] = email_results

      # Step 6: Mark as success
      results["success"] = True

      # Step 7: Log summary
      end_time = datetime.now()
      duration = (end_time - start_time).total_seconds()
      results["end_time"] = end_time.isoformat()
      results["duration_seconds"] = duration

      sent_count = sum(1 for e in (results["email"] if isinstance(results["email"], list) else [results["email"]]) if e.get("success"))
      total_emails = len(results["email"]) if isinstance(results["email"], list) else 1

      logger.info("\n" + "="*60)
      logger.info("Daily Pipeline Completed Successfully!")
      logger.info(f"Total duration: {duration:.2f} seconds")
      logger.info("\nSummary:")
      logger.info(f"  Scrapped: {results['scrapping']}")
      logger.info(f"  Processed: {results['processing']}")
      logger.info(f"  Digests created: {results['digests'].get('total_digests', 0)}")
      logger.info(f"  Videos summarized: {results['digests'].get('videos_summarized', 0)}")
      logger.info(f"  Articles summarized: {results['digests'].get('articles_summarized', 0)}")
      logger.info(f"  Emails sent: {sent_count}/{total_emails}")
      logger.info("="*60)

    except Exception as e:
      logger.error(f"\nDaily pipeline failed: {str(e)}", exc_info=True)
      results["success"] = False

    return results


if __name__ == "__main__":
  result = run_daily_pipeline(hours=24, top_n=10)
  exit(0 if result["success"] else 1)