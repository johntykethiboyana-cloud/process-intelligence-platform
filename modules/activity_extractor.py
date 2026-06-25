import re


class ActivityExtractor:

    def __init__(self):

        self.action_words = {

            "login", "log", "search", "select", "click",
            "enter", "fill", "update", "create", "delete",
            "approve", "reject", "review", "verify",
            "validate", "submit", "save", "upload",
            "download", "send", "mail", "email",
            "complete", "link", "open", "close",
            "copy", "paste", "check", "assign",
            "execute", "raise", "request",
            "add", "remove", "modify", "amend",
            "inform", "notify", "move",
            "setup", "set", "maintain",
            "choose", "attach", "enter",
            "update", "confirm"
        }

        self.stop_phrases = [

            "once",
            "after",
            "before",
            "kindly",
            "please",
            "below",
            "following",
            "this guide",
            "this document",
            "this sop",
            "the below",
            "in order to",
            "it will",
            "thereafter"

        ]

    # ---------------------------------------------------------

    def clean_text(self, text):

        text = re.sub(r"\s+", " ", text)

        text = text.replace("•", " ")

        return text.strip()

    # ---------------------------------------------------------

    def split_sentences(self, text):

        text = self.clean_text(text)

        sentences = re.split(

            r'(?<=[.!?])\s+|;',

            text

        )

        return [

            s.strip()

            for s in sentences

            if len(s.strip()) > 5

        ]

    # ---------------------------------------------------------

    def remove_stop_phrases(self, text):

        lower = text.lower()

        for phrase in self.stop_phrases:

            if lower.startswith(phrase):

                text = text[len(phrase):].strip(" ,:-")

                lower = text.lower()

        return text

    # ---------------------------------------------------------

    def classify(self, text):

        lower = text.lower()

        if lower.startswith("http"):
            return "URL"

        if "http://" in lower or "https://" in lower:
            return "URL"

        if lower.startswith("note"):
            return "NOTE"

        if "approve" in lower:
            return "APPROVAL"

        if "reject" in lower:
            return "APPROVAL"

        if "verify" in lower or "validate" in lower:
            return "VALIDATION"

        if "email" in lower or "mail" in lower or "notify" in lower:
            return "COMMUNICATION"

        for action in self.action_words:

            if action in lower:
                return "ACTIVITY"

        return "INFORMATION"

    # ---------------------------------------------------------

    def extract(self, sections):

        results = []

        for heading, paragraphs in sections.items():

            for paragraph in paragraphs:

                paragraph = self.clean_text(paragraph)

                sentences = self.split_sentences(paragraph)

                for sentence in sentences:

                    sentence = self.remove_stop_phrases(sentence)

                    if len(sentence) < 5:
                        continue

                    category = self.classify(sentence)

                    results.append({

                        "heading": heading,
                        "text": sentence,
                        "type": category

                    })

        return results