
import os
import json
import google.generativeai as genai

class AIAlyst:
    def __init__(self):
        # Configure the Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        
        # Use gemini-flash-latest which is available
        self.model = genai.GenerativeModel('gemini-flash-latest')
        print(f"DEBUG: Initialized AIAlyst with model: gemini-flash-latest")

    def analyze_video_metadata(self, title, description):
        """
        Uses the Gemini API to extract structured data from video metadata.
        Returns JSON with tldr, original_date, and tags.
        """
        prompt = f"""
        You are a Metadata Librarian for a video archive.
        I will give you a Video Title and Description.
        Your goal is to extract structured metadata.

        Title: {title}
        Description: {description}

        Return ONLY valid JSON in this format:
        {{
          "tldr": "A 15-word max engaging summary of what this video is actually about.",
          "original_date": "YYYY-MM-DD" (or null if you cannot infer a specific recording/broadcast date from context. If year only, use YYYY-01-01),
          "tags": ["tag1", "tag2", "tag3", "tag4"] (Max 5 tags, lowercase, relevant topics)
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            text = response.text
            # Clean markdown code blocks if present
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            return json.loads(text.strip())

        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return {
                'tldr': f"Analysis failed: {str(e)}",
                'original_date': None,
                'tags': []
            }

if __name__ == '__main__':
    # Example usage:
    ai_analyst = AIAlyst()
    sample_title = "Steve Gadd - Drum Solo in 'Aja' - Live in London 1988"
    sample_description = "Incredible performance by the master drummer Steve Gadd during the 1988 world tour."
    
    analysis_result = ai_analyst.analyze_video_metadata(sample_title, sample_description)
    print(json.dumps(analysis_result, indent=2))
