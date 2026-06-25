from comparison_v3.business_matcher import BusinessMatcher
from comparison_v3.utils import Utils


class ActivityMatcher:
    """
    Activity Matcher V3
    """

    def __init__(self):

        self.matcher = BusinessMatcher()

        # Activity match threshold (%)
        self.threshold = 45

    # ---------------------------------------------------------
    # BEST MATCH
    # ---------------------------------------------------------

    def best_match(self, activity, candidates):

        best = None

        best_score = -1

        best_index = -1

        best_details = None

        for index, candidate in enumerate(candidates):

            details = self.matcher.compare(

                activity,

                candidate

            )

            if details["score"] > best_score:

                best = candidate

                best_score = details["score"]

                best_index = index

                best_details = details

        return best, best_score, best_index, best_details

    # ---------------------------------------------------------
    # COMPARE
    # ---------------------------------------------------------

    def compare(self, l4_activities, sop_activities):

        l4_activities = Utils.unique(

            Utils.remove_empty(l4_activities)

        )

        sop_activities = Utils.unique(

            Utils.remove_empty(sop_activities)

        )

        matched = []

        missing = []

        extra = []

        used = set()

        for activity in l4_activities:

            best, score, index, details = self.best_match(

                activity,

                sop_activities

            )

            if score >= self.threshold:

                matched.append({

                    "l4_activity": activity,

                    "sop_activity": best,

                    "score": round(score, 2),

                    "confidence": self.matcher.confidence(score),

                    "status": "Matched"

                })

                used.add(index)

            else:

                missing.append({

                    "l4_activity": activity,

                    "best_match": best,

                    "score": round(score, 2),
                    "status": "Missing"
                    

                })

        for index, activity in enumerate(sop_activities):

            if index not in used:

                extra.append({

                    "sop_activity": activity

                })

        percentage = Utils.percentage(

            len(matched),

            len(l4_activities)

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

            "threshold": self.threshold,

            "percentage": result["percentage"]

        }