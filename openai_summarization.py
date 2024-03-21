from openai import OpenAI
import os
from dotenv import load_dotenv


class API:
    def __init__(self):
        load_dotenv(".env")

        self.client = OpenAI()
        # OpenAI.api_key = os.getenv('OPENAI')

    def summarize_text(self, input_text):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": "Generate a concise summary of the text while retaining its essence and omitting "
                               "extraneous details." + input_text,
                },
            ],
            temperature=0.4
        )

        summarized_text = completion.choices[0].message.content
        return summarized_text


if __name__ == '__main__':
    app = API()

    text_article = """
        Hi everyone, I hope this email finds you well. As you may know, our company is hosting a special event next week 
        to celebrate a major milestone. We would like to extend an invitation to all employees to join us for this 
        memorable occasion. Please RSVP by the end of this week, indicating whether you will be able to attend. We look
        forward to celebrating together as a team. If you have any dietary restrictions or special requests, please let 
        us know in your response. Thank you, and we hope to see you there!
        """

    print(app.summarize_text(text_article))
