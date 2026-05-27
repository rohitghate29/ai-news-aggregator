from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

def get_transcript(video_id: str) -> Optional[str]:
  try:
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    return " ".join([entry.text for entry in transcript])
  except (TranscriptsDisabled, NoTranscriptFound):
    return None
  except Exception as e:
    print(f"Error fetching transcript for {video_id}: {e}")
    return None
    
if __name__ == "__main__":
  print(get_transcript(video_id="E8zpgNPx8jE"))
