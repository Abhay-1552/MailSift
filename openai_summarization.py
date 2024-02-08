import openai
import os
from dotenv import load_dotenv


class API:
    def __init__(self):
        load_dotenv(".env")

        openai.api_key = os.getenv('OPENAI')

    @staticmethod
    def summarize_text(input_text):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Summarize the text while removing unnecessary things and preserving the text meaning" + input_text,
            max_tokens=75
        )

        summarized_text = response.choices[0].text.strip()
        return summarized_text


if __name__ == '__main__':
    app = API()

    text_article = """
        Hello!

        Trust you are doing well. We are back with the new product updates in Predis.ai😀 But before we start,
        here is a quick refresher about us- Predis.ai is a powerful combination of ChatGPT, Canvas, and Hoot suite that
        allows you to create almost ready-to-publish but still completely editable social media content in your brand
        language. We are back with new updates!

        🚀 Get Ready for Smoother Resizing! We've made some major improvements to our resizing feature, and we can't wait
        for you to try it out. Before, resizing could be a bit of a headache. Templates would often end up looking wonky
        and distorted. Not cool, right? But guess what? We've listened to your feedback and rolled out a much better
        resizing logic. Now, resizing works like a charm in most cases! Whether you're publishing in different sizes or
        using templates for ad creatives , you'll notice a big difference. We're still fine-tuning things, so consider
        this an experiment in progress. But hey, we're all about making things better for you, and this update is just
        the beginning into making multiple ad sizes.
        """

    print(app.summarize_text(text_article))

