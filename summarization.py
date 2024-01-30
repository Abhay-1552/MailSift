import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # Get tokens without stop words and punctuation
    tokens = [token.text.lower() for token in doc if
              token.text.lower() not in STOP_WORDS and token.text not in punctuation]

    word_frequencies = {}
    for word in tokens:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

    max_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / max_frequency

    sentence_tokens = [sent for sent in doc.sents]

    sentence_scores = {}
    for sent in sentence_tokens:
        for word, freq in word_frequencies.items():
            if word in sent.text.lower():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = freq
                else:
                    sentence_scores[sent] += freq

    select_length = int(len(sentence_tokens) * per)
    summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)

    return summary


text_article = """
Hello!

Trust you are doing well. We are back with the new product updates in Predis.ai😀 But before we start, 
here is a quick refresher about us- Predis.ai is a powerful combination of ChatGPT, Canvas, and Hoot suite that allows 
you to create almost ready-to-publish but still completely editable social media content in your brand language. We 
are back with new updates!

🚀 Get Ready for Smoother Resizing! We've made some major improvements to our resizing feature, and we can't wait for 
you to try it out. Before, resizing could be a bit of a headache. Templates would often end up looking wonky and 
distorted. Not cool, right? But guess what? We've listened to your feedback and rolled out a much better resizing 
logic. Now, resizing works like a charm in most cases! Whether you're publishing in different sizes or using 
templates for ad creatives , you'll notice a big difference. We're still fine-tuning things, so consider this an 
experiment in progress. But hey, we're all about making things better for you, and this update is just the beginning 
into making multiple ad sizes"""

a = summarize(text_article, 0.5)
print(a)
