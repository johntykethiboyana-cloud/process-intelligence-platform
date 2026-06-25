import re


class Normalizer:

    def __init__(self):

        self.stop_words = {

            "the", "a", "an", "to", "of", "for", "and",
            "or", "by", "on", "in", "into", "under",
            "from", "with", "that", "this", "then",
            "once", "after", "before", "when",
            "kindly", "please", "post", "below",
            "above", "shown", "required", "need",
            "needs", "will", "be", "is", "are",
            "as", "per", "it", "you", "your",
            "there", "their", "can", "could"
        }

    # -----------------------------------------------------

    def normalize(self, text):

        # Lower case
        text = text.lower()

        # Remove URLs
        text = re.sub(r"http\S+", "", text)

        # Remove punctuation
        text = re.sub(r"[^a-z0-9 ]", " ", text)

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        words = []

        for word in text.split():

            if word not in self.stop_words:

                words.append(word)

        return " ".join(words)