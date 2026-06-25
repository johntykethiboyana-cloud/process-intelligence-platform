from comparison_v3.business_matcher import BusinessMatcher
from comparison_v3.utils import Utils


class ApplicationMatcher:
    """
    Application Matcher V3

    Responsibilities
    ----------------
    • Compare L4 Applications with SOP Applications
    • Find Best Match
    • Calculate Match Percentage
    • Identify Missing Applications
    • Identify Extra Applications
    """

    def __init__(self):

        self.matcher = BusinessMatcher()

        self.threshold = 90

    # ---------------------------------------------------------
    # NORMALIZE
    # ---------------------------------------------------------

    def normalize(self, application):

        return self.matcher.normalizer.normalize_application(
            application
        )

    # ---------------------------------------------------------
    # BEST MATCH
    # ---------------------------------------------------------

    def best_match(self, application, candidates):

        best = None
        best_score = -1
        best_index = -1

        for index, candidate in enumerate(candidates):

            left = self.normalize(application)

            right = self.normalize(candidate)

            score = 100 if left == right and left else 0

            if score > best_score:

                best = candidate
                best_score = score
                best_index = index

        return best, best_score, best_index

    # ---------------------------------------------------------
    # COMPARE
    # ---------------------------------------------------------

    def compare(self, l4_applications, sop_applications):

        l4_applications = Utils.unique(

            [self.normalize(x) for x in l4_applications]

        )

        sop_applications = Utils.unique(

            [self.normalize(x) for x in sop_applications]

        )

        l4_applications = Utils.remove_empty(l4_applications)

        sop_applications = Utils.remove_empty(sop_applications)

        matched = []

        missing = []

        extra = []

        used = set()

        for app in l4_applications:

            best, score, index = self.best_match(

                app,

                sop_applications

            )

            if score >= self.threshold:

                matched.append({

                    "l4_application": app,

                    "sop_application": best,

                    "score": score,

                    "confidence": self.matcher.confidence(score)

                })

                used.add(index)

            else:

                missing.append({

                    "l4_application": app

                })

        for index, app in enumerate(sop_applications):

            if index not in used:

                extra.append({

                    "sop_application": app

                })

        percentage = Utils.percentage(

            len(matched),

            len(l4_applications)

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

    matcher = ApplicationMatcher()

    l4 = [

        "SAP",

        "GCSS",

        "ARIS",

        "SharePoint",

        "Power BI"

    ]

    sop = [

        "sap",

        "gcss",

        "Power BI",

        "SharePoint",

        "Excel"

    ]

    result = matcher.compare(

        l4,

        sop

    )

    print("=" * 80)

    print("APPLICATION MATCH :", result["percentage"])

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