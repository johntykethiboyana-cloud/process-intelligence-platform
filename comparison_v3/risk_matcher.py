from comparison_v3.business_matcher import BusinessMatcher
from comparison_v3.utils import Utils


class RiskMatcher:
    """
    Risk Matcher V3

    Responsibilities
    ----------------
    • Compare Risks
    • Find Best Match
    • Calculate Match %
    • Identify Missing Risks
    • Identify Extra Risks
    """

    def __init__(self):

        self.matcher = BusinessMatcher()

        self.threshold = 75

    # ---------------------------------------------------------
    # NORMALIZE
    # ---------------------------------------------------------

    def normalize(self, text):

        return self.matcher.normalizer.normalize(text)

    # ---------------------------------------------------------
    # BEST MATCH
    # ---------------------------------------------------------

    def best_match(self, risk, candidates):

        best = None

        best_score = -1

        best_index = -1

        best_details = None

        for index, candidate in enumerate(candidates):

            details = self.matcher.compare(

                risk,

                candidate

            )

            if details["score"] > best_score:

                best = candidate

                best_score = details["score"]

                best_index = index

                best_details = details

        return best, best_score, best_index, best_details

    # ---------------------------------------------------------
    # MAIN COMPARISON
    # ---------------------------------------------------------

    def compare(self, l4_risks, sop_risks):

        l4_risks = Utils.unique(

            Utils.remove_empty(l4_risks)

        )

        sop_risks = Utils.unique(

            Utils.remove_empty(sop_risks)

        )

        matched = []

        missing = []

        extra = []

        used = set()

        for risk in l4_risks:

            best, score, index, details = self.best_match(

                risk,

                sop_risks

            )

            if score >= self.threshold:

                matched.append({

                    "l4_risk": risk,

                    "sop_risk": best,

                    "score": round(score, 2),

                    "confidence": self.matcher.confidence(score)

                })

                used.add(index)

            else:

                missing.append({

                    "l4_risk": risk,

                    "best_match": best,

                    "score": round(score, 2)

                })

        for index, risk in enumerate(sop_risks):

            if index not in used:

                extra.append({

                    "sop_risk": risk

                })

        percentage = Utils.percentage(

            len(matched),

            len(l4_risks)

        )

        return {

            "percentage": percentage,

            "matched": matched,

            "missing": missing,

            "extra": extra

        }

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    def summary(self, result):

        return {

            "matched": len(result["matched"]),

            "missing": len(result["missing"]),

            "extra": len(result["extra"]),

            "percentage": result["percentage"]

        }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    matcher = RiskMatcher()

    l4 = [

        "Duplicate Booking",

        "Incorrect Customer Data",

        "Delayed Approval",

        "Missing Documentation"

    ]

    sop = [

        "Duplicate Record",

        "Incorrect Customer Information",

        "Approval Delay",

        "Missing Supporting Documents",

        "System Failure"

    ]

    result = matcher.compare(

        l4,

        sop

    )

    print("=" * 80)

    print("RISK MATCH :", result["percentage"])

    print("=" * 80)

    print()

    print("MATCHED")

    for row in result["matched"]:

        print(row)

    print()

    print("MISSING")

    for row in result["missing"]:

        print(row)

    print()

    print("EXTRA")

    for row in result["extra"]:

        print(row)