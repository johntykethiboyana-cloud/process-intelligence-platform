from encodings import aliases

from comparison_v3.business_matcher import BusinessMatcher
from comparison_v3.utils import Utils


class RoleMatcher:
    """
    Role Matcher V3

    Responsibilities
    ----------------
    • Compare L4 Roles vs SOP Roles
    • Find Best Match
    • Identify Missing Roles
    • Identify Extra Roles
    • Calculate Percentage
    """

    def __init__(self):

        self.matcher = BusinessMatcher()

        self.threshold = 40

    # ---------------------------------------------------------
    # NORMALIZE
    # ---------------------------------------------------------

    def normalize(self, role):

        return str(role).strip()

        aliases = {

        "CPM": "Contract Product Manager",
        "CEN": "Customer Experience Network",
        "CCA": "Customer Care Agent",
        "SCM": "Supply Chain Manager",
        "OPS": "Operations",
        "CSR": "Customer Service Representative",
        "CSM": "Customer Service Manager",
        "FIN": "Finance",
        "MGR": "Manager",
        "TL": "Team Leader"

    }

        return aliases.get(role.upper(), role)

    # ---------------------------------------------------------
    # BEST MATCH
    # ---------------------------------------------------------

    def best_match(self, role, candidates):

        best = None

        best_score = -1

        best_index = -1

        best_details = None

        for index, candidate in enumerate(candidates):

            details = self.matcher.compare(

                role,

                candidate

            )

            if details["score"] > best_score:

                best_score = details["score"]

                best = candidate

                best_index = index

                best_details = details

        return best, best_score, best_index, best_details

    # ---------------------------------------------------------
    # MAIN COMPARISON
    # ---------------------------------------------------------

    def compare(self, l4_roles, sop_roles):

        l4_roles = Utils.unique(

            Utils.remove_empty(l4_roles)

        )

        sop_roles = Utils.unique(

            Utils.remove_empty(sop_roles)

        )

        matched = []

        missing = []

        extra = []

        used = set()

        for role in l4_roles:

            best, score, index, details = self.best_match(

                role,

                sop_roles

            )

            if score >= self.threshold:

                matched.append({

                    "l4_role": role,

                    "sop_role": best,

                    "score": round(score, 2),

                    "confidence": self.matcher.confidence(score)

                })

                used.add(index)

            else:

                missing.append({

                    "l4_role": role,

                    "best_match": best,

                    "score": round(score, 2)

                })

        for index, role in enumerate(sop_roles):

            if index not in used:

                extra.append({

                    "sop_role": role

                })

        percentage = Utils.percentage(

            len(matched),

            len(l4_roles)

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

    matcher = RoleMatcher()

    l4 = [

        "CPM",

        "Treasury",

        "Finance",

        "Requester",

        "Approver"

    ]

    sop = [

        "Contract Product Manager",

        "Finance",

        "Treasury",

        "Approver",

        "Operations"

    ]

    result = matcher.compare(

        l4,

        sop

    )

    print("=" * 80)

    print("ROLE MATCH :", result["percentage"])

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
       