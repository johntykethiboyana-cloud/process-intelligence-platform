from comparison_v3.business_matcher import BusinessMatcher
from comparison_v3.utils import Utils


class ControlMatcher:
    """
    Control Matcher V3

    Responsibilities
    ----------------
    • Compare Controls
    • Find Best Match
    • Calculate Match %
    • Missing Controls
    • Extra Controls
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

    def best_match(self, control, candidates):

        best = None

        best_score = -1

        best_index = -1

        best_details = None

        for index, candidate in enumerate(candidates):

            details = self.matcher.compare(

                control,

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

    def compare(self, l4_controls, sop_controls):

        l4_controls = Utils.unique(

            Utils.remove_empty(l4_controls)

        )

        sop_controls = Utils.unique(

            Utils.remove_empty(sop_controls)

        )

        matched = []

        missing = []

        extra = []

        used = set()

        for control in l4_controls:

            best, score, index, details = self.best_match(

                control,

                sop_controls

            )

            if score >= self.threshold:

                matched.append({

                    "l4_control": control,

                    "sop_control": best,

                    "score": round(score, 2),

                    "confidence": self.matcher.confidence(score)

                })

                used.add(index)

            else:

                missing.append({

                    "l4_control": control,

                    "best_match": best,

                    "score": round(score, 2)

                })

        for index, control in enumerate(sop_controls):

            if index not in used:

                extra.append({

                    "sop_control": control

                })

        percentage = Utils.percentage(

            len(matched),

            len(l4_controls)

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

    matcher = ControlMatcher()

    l4 = [

        "Maker Approval",

        "Checker Validation",

        "Management Review",

        "Mandatory Approval"

    ]

    sop = [

        "Approval by Maker",

        "Checker Validation",

        "Manager Review",

        "Dual Authorization",

        "Risk Assessment"

    ]

    result = matcher.compare(

        l4,

        sop

    )

    print("=" * 80)

    print("CONTROL MATCH :", result["percentage"])

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