import os
from typing import Optional
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """ You are an expert AI news analyst specialising in summarising technical articles, research papers and video content about artificial intelligence. 
    
Your role is to create concise informative digests that help readers quickly understand the key point and significance of AI-related content.

Guidelines:
- Create a compeling Title (5-10 words) that captures the essence of the content 
- Write a 2-3 sentence summary that highlights the main point and why they matter
- Focus on actionable insights and implications
- Use clear, accessible language while maintaining technical accuracy
- Avoid marketing - Focus on substance
"""

class DigestOutput(BaseModel):
  title: str
  summary: str

class DigestAgent:
  def __init__(self,):
    self.client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"), base_url=os.getenv("GEMINI_BASE_URL"))
    self.model = os.getenv("GEMINI_MODEL")
    self.system_prompt = SYSTEM_PROMPT
    
  def generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]:
    try:
      user_prompt = f"""Create a digest for this {article_type}: \n Title: \n {title} \n Content: 
     \n {content[:8000]}

      provide a title and 2-3 sentence summary."""

      response = self.client.chat.completions.parse(
        model=self.model,
        messages=[
          {"role": "system", "content": self.system_prompt},
          {"role": "user", "content": user_prompt}
        ],
        response_format=DigestOutput,
        temperature=1
      )

      parsed = response.choices[0].message.parsed
      if parsed: 
        return parsed
      
      content_text = response.choices[0].message.content
      if content_text:
        import json
        data = json.loads(content_text)
        return DigestOutput(**data)
      
      return None
    except Exception as e:
      print(f"Error generating digest: {e}")
      return None
