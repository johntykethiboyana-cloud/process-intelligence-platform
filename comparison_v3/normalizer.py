import re


class Normalizer:
    """
    Business Process Normalizer V3

    Responsibilities
    ----------------
    1. Clean text
    2. Remove UI words
    3. Remove stop words
    4. Standardize business actions
    5. Standardize applications
    6. Extract comparable business text
    """

    def __init__(self):

        # --------------------------------------------------
        # Stop Words
        # --------------------------------------------------

        self.stop_words = {

            "the", "a", "an",
            "to", "of", "for",
            "and", "or", "by",
            "on", "in", "into",
            "under", "from",
            "with", "without",
            "that", "this",
            "then", "once",
            "after", "before",
            "when", "while",
            "will", "shall",
            "can", "could",
            "should", "would",
            "be", "is", "are",
            "was", "were",
            "as", "per",
            "it", "its",
            "there", "their",
            "your", "our",
            "user", "users",
            "using", "use"
        }

        # --------------------------------------------------
        # UI Words
        # --------------------------------------------------

        self.ui_words = {

            "click",
            "double",
            "right",
            "left",
            "select",
            "choose",
            "navigate",
            "navigation",
            "goto",
            "go",
            "open",
            "close",
            "expand",
            "collapse",
            "scroll",
            "screen",
            "page",
            "window",
            "tab",
            "menu",
            "button",
            "icon",
            "field",
            "textbox",
            "drop",
            "dropdown",
            "radio",
            "checkbox",
            "press",
            "enter",
            "type"
        }

        # --------------------------------------------------
        # Action Synonyms
        # --------------------------------------------------

        self.action_map = {

            "creation": "create",
            "creating": "create",
            "created": "create",

            "modification": "update",
            "modify": "update",
            "modified": "update",
            "editing": "update",
            "edited": "update",

            "deletion": "delete",
            "remove": "delete",
            "removed": "delete",

            "verification": "validate",
            "verify": "validate",
            "verified": "validate",

            "reviewed": "review",

            "approval": "approve",
            "approved": "approve",

            "generated": "generate",
            "generation": "generate",

            "received": "receive",
            "receiving": "receive",

            "submitted": "submit",
            "submission": "submit",

            "uploaded": "upload",
            "uploading": "upload",

            "downloaded": "download",

            "linked": "link",
            "linking": "link",

            "cancelled": "cancel",

            "completed": "complete",
            "completion": "complete"

        }

        # --------------------------------------------------
        # Application Synonyms
        # --------------------------------------------------

        self.application_map = {

            "gcss": "GCSS",

            "sap": "SAP",

            "aris": "ARIS",

            "sharepoint": "SharePoint",

            "excel": "Excel",

            "outlook": "Outlook",

            "powerbi": "Power BI",

            "power bi": "Power BI",

            "servicenow": "ServiceNow",

            "service now": "ServiceNow",

            "salesforce": "Salesforce",

            "athena": "Athena",

            "gpm": "GPM",

            "d365": "Dynamics",

            "dynamics": "Dynamics"

        }

    # --------------------------------------------------
    # Clean Text
    # --------------------------------------------------

    def clean(self, text):

        if text is None:
            return ""

        text = str(text)

        text = text.lower()

        text = re.sub(r"http\S+", " ", text)

        text = re.sub(r"[^a-z0-9 ]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # --------------------------------------------------
    # Normalize Application
    # --------------------------------------------------

    def normalize_application(self, text):

        text = self.clean(text)

        for key, value in self.application_map.items():

            if key in text:

                return value

        return ""

    # --------------------------------------------------
    # Normalize Words
    # --------------------------------------------------

    def normalize_words(self, text):

        text = self.clean(text)

        words = []

        for word in text.split():

            if word in self.stop_words:
                continue

            if word in self.ui_words:
                continue

            word = self.action_map.get(word, word)

            words.append(word)

        return words

    # --------------------------------------------------
    # Remove Duplicates
    # --------------------------------------------------

    def unique(self, words):

        output = []

        seen = set()

        for word in words:

            if word not in seen:

                seen.add(word)

                output.append(word)

        return output

    # --------------------------------------------------
    # Normalize
    # --------------------------------------------------

    def normalize(self, text):

        words = self.normalize_words(text)

        words = self.unique(words)

        return " ".join(words)

    # --------------------------------------------------
    # Extract Keywords
    # --------------------------------------------------

    def keywords(self, text):

        return self.normalize(text).split()

    # --------------------------------------------------
    # Token Similarity Helper
    # --------------------------------------------------

    def common_tokens(self, text1, text2):

        s1 = set(self.keywords(text1))

        s2 = set(self.keywords(text2))

        return s1.intersection(s2)

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    def debug(self, text):

        return {

            "original": text,

            "normalized": self.normalize(text),

            "keywords": self.keywords(text),

            "application": self.normalize_application(text)

        }


# ----------------------------------------------------------
# Test
# ----------------------------------------------------------

if __name__ == "__main__":

    n = Normalizer()

    samples = [

        "Click Create Booking in SAP",

        "Navigate to GCSS and Update Price",

        "Review Booking Request",

        "Verification of Customer Data",

        "Upload document in SharePoint"

    ]

    for sample in samples:

        print("=" * 60)

        print(n.debug(sample))