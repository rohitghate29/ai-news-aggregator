from typing import List
import feedparser
from typing import Dict
from datetime import datetime, timedelta, timezone
from typing import Optional
import feedparser
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from pydantic import BaseModel



class Transcript(BaseModel):
  text: str

class ChannelVideo(BaseModel):
  title: str
  url: str
  published_at: datetime
  video_id: str
  description: str
  transcript: Optional[str] = None


class YoutubeScrapper:
  def __init__(self):
    self.transcript_api = YouTubeTranscriptApi()

  def get_res_url(self, channel_id: str) -> str:
    return f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"

  def extract_video_id(self, video_url: str) -> str:
    if "youtube.com/watch?v=" in video_url:
      return video_url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in video_url:
      return video_url.split("youtu.be/")[1].split("?")[0]
    return video_url

  def get_latest_videos(self, channel_id: str, hours: int = 24) -> list[Dict]:
    feed = feedparser.parse(self.get_res_url(channel_id))
    if not feed.entries:
      return []

    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    videos = []

    for entry in feed.entries:
      published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

      if published_time >= cutoff_time:
        video_id = self.extract_video_id(entry.link)
        videos.append({
          "title": entry.title,
          "url": entry.link,
          "published_at": published_time,
          "video_id": video_id,
          "description": entry.get("summary", "")
        })
    return videos
      
  def get_transcript(self, video_id: str) -> Optional[Transcript]:
    try:
      ytt_api = YouTubeTranscriptApi()
      transcript = ytt_api.fetch(video_id)
      text = " ".join([entry.text for entry in transcript])
      return Transcript(text=text)
    except (TranscriptsDisabled, NoTranscriptFound):
      return None
    except Exception as e:
      print(f"Error fetching transcript for {video_id}: {e}")
      return None
    
  def scrape_channel(self, channel_id: str, hours: int = 150) -> list[ChannelVideo]:
    videos_data = self.get_latest_videos(channel_id, hours=hours)
    videos = []
    for data in videos_data:
      transcript = self.get_transcript(data["video_id"])
      videos.append(ChannelVideo(
        title=data["title"],
        url=data["url"],
        published_at=data["published_at"],
        video_id=data["video_id"],
        description=data["description"],
        transcript=transcript.text if transcript else None
      ))
    return videos

if __name__ == "__main__":
  scrapper = YoutubeScrapper()
  transcript: Transcript = scrapper.get_transcript("E8zpgNPx8jE")
  print(transcript.text)
  channel_videos: List[ChannelVideo] = scrapper.scrape_channel("UCn8ujwUInbJkBhffxqAPBVQ")

