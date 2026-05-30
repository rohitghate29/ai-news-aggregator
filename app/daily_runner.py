from IPython.core.magics import logging
import logging
from datetime import datetime
from  dotenv import load_dotenv

load_dotenv()

from app.runner import run_scrappers
from app.services.process_anthropic import process_anthropic_markdown
from app.services.process_youtube import process_youtube_transcripts
from app.services.process_digest import process_digests
from app.services.process_email import send_digest_email

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
        "digest": len(scrapping_results.get("digest", []))
      }
      logger.info(f"Scrapping completed: YouTube={results['scrapping']['youtube']}")
      logger.info(f"Scrapping completed: Anthropic={results['scrapping']['anthropic']}")
      logger.info(f"Scrapping completed: Digest={results['scrapping']['digest']}")

      # Step 2: Process Anthropic
      logger.info("\nStep 2: Processing Anthropic markdown...")
      anthropic_result = process_anthropic_markdown()
      results["processing"]["anthropic"] = anthropic_result
      logger.info(f"Anthropic processing completed: {anthropic_result['processed']} articles processed")
      
      # Step 3: Process YouTube
      logger.info("\nStep 3: Processing YouTube transcripts...")
      youtube_result = process_youtube_transcripts()
      results["processing"]["youtube"] = youtube_result
      logger.info(f"YouTube processing completed: {youtube_result['processed']} videos processed")
      
      # Step 4: Process Digests
      logger.info("\nStep 4: Processing digests...")
      digest_result = process_digests()
      results["digests"] = digest_result
      logger.info(f"Digest processing completed: {digest_result['processed']} digests created")
      
      # Step 5: Send Email
      logger.info("\nStep 5: Sending email...")
      email_result = send_digest_email(hours=hours, top_n=top_n)
      results["email"] = email_result

      if email_result["success"]:
        logger.info(f"Email sent successfully: {email_result['subject']} with {email_result['articles_count']} articles")
      else:
        logger.error(f"Email sending failed: {email_result.get('error', 'Unknown error')}")
      
      # Step 6: Mark as success
      results["success"] = True
      
      # Step 7: Log summary
      end_time = datetime.now()
      duration = (end_time - start_time).total_seconds()
      results["end_time"] = end_time.isoformat()
      results["duration_seconds"] = duration
      
      logger.info("\n" + "="*60)
      logger.info("Daily Pipeline Completed Successfully!")
      logger.info(f"Total duration: {duration:.2f} seconds")
      logger.info("\nSummary:")
      logger.info(f"  Scrapped: {results['scrapping']}")
      logger.info(f"  Processed: {results['processing']}")
      logger.info(f"  Digests created: {results['digests'].get('total_digests', 0)}")
      logger.info(f"  Videos summarized: {results['digests'].get('videos_summarized', 0)}")
      logger.info(f"  Articles summarized: {results['digests'].get('articles_summarized', 0)}")
      logger.info(f"  Email sent: {results['email'].get('success', False)}")
      logger.info(f"  Email stats: {results['email'].get('stats', {})}")
      logger.info("="*60)
      
    except Exception as e:
      logger.error(f"\nDaily pipeline failed: {str(e)}", exc_info=True)
      results["success"] = False
    
    return results
      
        
if __name__ == "__main__":
  result = run_daily_pipeline(hours=24, top_n=10)
  exit(0 if result["success"] else 1)