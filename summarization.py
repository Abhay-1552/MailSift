import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest


class TEXT:
    def __init__(self, text, per=0.5):
        self.text = text
        self.percentage = per

    def summarize(self):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.text)

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

        select_length = int(len(sentence_tokens) * self.percentage)
        summary = nlargest(select_length, sentence_scores, key=sentence_scores.get)
        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)

        return summary

