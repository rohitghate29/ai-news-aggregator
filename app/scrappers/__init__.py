from .youtube import YoutubeScrapper, ChannelVideo, Transcript

def scrape_channel(channel_id: str, hours: int = 150) -> list[ChannelVideo]:
    """Helper function to instantiate YoutubeScrapper and scrape a channel."""
    return YoutubeScrapper().scrape_channel(channel_id, hours=hours)

__all__ = ["YoutubeScrapper", "ChannelVideo", "Transcript", "scrape_channel"]



