from difflib import SequenceMatcher
from comparison_v3.normalizer import Normalizer


class Similarity:

    """
    Similarity Engine V3

    Responsible for

    • Text Similarity
    • Token Similarity
    • Keyword Similarity
    • Jaccard Similarity
    • Combined Business Similarity
    """

    def __init__(self):

        self.normalizer = Normalizer()

    # -------------------------------------------------------
    # Character Similarity
    # -------------------------------------------------------

    def text_similarity(self, text1, text2):

        t1 = self.normalizer.normalize(text1)

        t2 = self.normalizer.normalize(text2)

        if not t1 or not t2:
            return 0.0

        return SequenceMatcher(
            None,
            t1,
            t2
        ).ratio()

    # -------------------------------------------------------
    # Token Similarity
    # -------------------------------------------------------

    def token_similarity(self, text1, text2):

        t1 = set(self.normalizer.keywords(text1))

        t2 = set(self.normalizer.keywords(text2))

        if not t1 or not t2:
            return 0.0

        common = t1.intersection(t2)

        return len(common) / max(len(t1), len(t2))

    # -------------------------------------------------------
    # Jaccard Similarity
    # -------------------------------------------------------

    def jaccard_similarity(self, text1, text2):

        t1 = set(self.normalizer.keywords(text1))

        t2 = set(self.normalizer.keywords(text2))

        if not t1 and not t2:
            return 1.0

        if not t1 or not t2:
            return 0.0

        intersection = len(t1 & t2)

        union = len(t1 | t2)

        return intersection / union

    # -------------------------------------------------------
    # Keyword Similarity
    # -------------------------------------------------------

    def keyword_similarity(self, text1, text2):

        k1 = self.normalizer.keywords(text1)

        k2 = self.normalizer.keywords(text2)

        if not k1 or not k2:
            return 0.0

        common = 0

        for word in k1:

            if word in k2:

                common += 1

        return common / len(k1)

    # -------------------------------------------------------
    # Business Similarity
    # -------------------------------------------------------

    def business_similarity(self, text1, text2):

        text_score = self.text_similarity(
            text1,
            text2
        )

        token_score = self.token_similarity(
            text1,
            text2
        )

        keyword_score = self.keyword_similarity(
            text1,
            text2
        )

        jaccard_score = self.jaccard_similarity(
            text1,
            text2
        )

        score = (

            text_score * 0.40 +

            token_score * 0.25 +

            keyword_score * 0.20 +

            jaccard_score * 0.15

        )

        return round(score, 4)

    # -------------------------------------------------------
    # Detailed Result
    # -------------------------------------------------------

    def compare(self, text1, text2):

        text_score = self.text_similarity(
            text1,
            text2
        )

        token_score = self.token_similarity(
            text1,
            text2
        )

        keyword_score = self.keyword_similarity(
            text1,
            text2
        )

        jaccard_score = self.jaccard_similarity(
            text1,
            text2
        )

        business_score = self.business_similarity(
            text1,
            text2
        )

        return {

            "text_similarity":
                round(text_score * 100, 2),

            "token_similarity":
                round(token_score * 100, 2),

            "keyword_similarity":
                round(keyword_score * 100, 2),

            "jaccard_similarity":
                round(jaccard_score * 100, 2),

            "business_similarity":
                round(business_score * 100, 2)

        }


# -------------------------------------------------------
# Test
# -------------------------------------------------------

if __name__ == "__main__":

    engine = Similarity()

    tests = [

        (

            "Click Create Booking in SAP",

            "Create Booking"

        ),

        (

            "Review Customer Request",

            "Validate Customer Request"

        ),

        (

            "Upload Document in SharePoint",

            "Upload File to SharePoint"

        ),

        (

            "Approve Ocean Tender",

            "Approval of Ocean Tender"

        )

    ]

    for t1, t2 in tests:

        print("=" * 70)

        print("TEXT 1 :", t1)

        print("TEXT 2 :", t2)

        print(engine.compare(t1, t2))