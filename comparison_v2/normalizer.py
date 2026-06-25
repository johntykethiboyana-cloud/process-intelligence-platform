import re


class Normalizer:

    def __init__(self):

        self.stop_words = {

            "the","a","an","to","of","for","and","or",
            "by","on","in","into","under","from","with",
            "that","this","then","once","after","before",
            "when","kindly","please","post","below",
            "above","shown","required","need","needs",
            "will","be","is","are","as","per","it",
            "you","your","there","their","can","could",
            "user","screen","page","window","system",
            "navigate","navigation","go","goto"
        }

        # UI words that should not affect business comparison
        self.ui_words = {

            "click",
            "select",
            "double",
            "press",
            "choose",
            "open",
            "close",
            "expand",
            "collapse",
            "scroll",
            "enter",
            "type",
            "tick",
            "untick",
            "highlight"
        }

        # Business synonyms
        self.synonyms = {

            "review":"validate",
            "verification":"validate",
            "verify":"validate",
            "approval":"approve",
            "authorise":"approve",
            "authorize":"approve",
            "creation":"create",
            "creating":"create",
            "generated":"generate",
            "generation":"generate",
            "modification":"update",
            "modify":"update",
            "editing":"update",
            "remove":"delete",
            "deletion":"delete",
            "uploading":"upload",
            "downloading":"download",
            "mail":"email",
            "e-mail":"email"
        }

    def normalize(self, text):

        text = str(text).lower()

        text = re.sub(r"http\\S+", " ", text)

        text = re.sub(r"[^a-z0-9 ]", " ", text)

        words = []

        for word in text.split():

            if word in self.stop_words:
                continue

            if word in self.ui_words:
                continue

            if word in self.synonyms:
                word = self.synonyms[word]

            words.append(word)

        # remove duplicates while preserving order
        cleaned = []

        seen = set()

        for word in words:

            if word not in seen:

                seen.add(word)

                cleaned.append(word)

        return " ".join(cleaned)