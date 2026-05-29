from app.runner import run_scrappers

def main(hours: int = 24):
  results = run_scrappers(hours)

  print(f"\n=== Scrapping Results (last ({hours} hours) ===")
  print(f"Youtube Videos: {len(results['youtube'])}")
  print(f"Anthropic Articles: {len(results['anthropic'])}")

  return results


if __name__ == "__main__":
  import sys
  hours = int(sys.argv[1]) if len(sys.argv) > 1 else 24
  main(hours)