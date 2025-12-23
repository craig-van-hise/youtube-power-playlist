
import os
import google.generativeai as genai

class AIAlyst:
    def __init__(self):
        # Configure the Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def analyze_video_metadata(self, title, description):
        """
        Uses the Gemini API to extract structured data from video metadata.
        """
        prompt = f"""
        Analyze the following video title and description to determine the performance date, primary artist, and context.
        Provide the response in a structured format.

        Title: {title}
        Description: {description}

        Desired output format:
        - performance_date: YYYY-MM-DD (estimate if necessary)
        - is_date_estimated: boolean (true if the date is an approximation)
        - primary_artist: string
        - context: string (e.g., Live, Studio, Interview, Rehearsal, Lesson)
        """

        try:
            response = self.model.generate_content(prompt)
            # Basic parsing of the response (a more robust implementation would use JSON)
            ai_response_text = response.text

            # This is a simplified parser. For a real-world application, 
            # you might ask the model to return JSON directly.
            extracted_data = {
                'performance_date': self._parse_field(ai_response_text, 'performance_date'),
                'is_date_estimated': self._parse_field(ai_response_text, 'is_date_estimated').lower() == 'true',
                'primary_artist': self._parse_field(ai_response_text, 'primary_artist'),
                'context': self._parse_field(ai_response_text, 'context'),
                'ai_confidence_score': 0.9  # Placeholder for confidence scoring
            }
            return extracted_data

        except Exception as e:
            print(f"Error during AI analysis: {e}")
            return {
                'performance_date': None,
                'is_date_estimated': True,
                'primary_artist': 'Unknown',
                'context': 'Unknown',
                'ai_confidence_score': 0.0
            }

    def _parse_field(self, text, field_name):
        """Helper to parse a field from the AI's text response."""
        try:
            return text.split(f"{field_name}: ")[1].split('\n')[0].strip()
        except IndexError:
            return 'Unknown'

if __name__ == '__main__':
    # Example usage:
    ai_analyst = AIAlyst()
    sample_title = "Steve Gadd - Drum Solo in 'Aja' - Live in London 1988"
    sample_description = "Incredible performance by the master drummer Steve Gadd during the 1988 world tour."
    
    analysis_result = ai_analyst.analyze_video_metadata(sample_title, sample_description)
    print(analysis_result)
