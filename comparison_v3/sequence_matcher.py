from comparison_v3.business_matcher import BusinessMatcher
from comparison_v3.utils import Utils


class SequenceMatcher:
    """
    Sequence Matcher V3

    Responsibilities
    ----------------
    • Compare process sequence
    • Compare step order
    • Detect moved activities
    • Calculate sequence score
    """

    def __init__(self):

        self.matcher = BusinessMatcher()

        self.threshold = 70

    # ---------------------------------------------------------
    # SAFE STEP
    # ---------------------------------------------------------

    def step_text(self, step):

        return Utils.step_text(step)

    # ---------------------------------------------------------
    # BUILD SEQUENCE
    # ---------------------------------------------------------

    def build_sequence(self, steps):

        sequence = []

        for step in steps:

            sequence.append(

                self.step_text(step)

            )

        return sequence

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
    # COMPARE SEQUENCE
    # ---------------------------------------------------------

    def compare(self, l4_steps, sop_steps):

        l4_sequence = self.build_sequence(

            l4_steps

        )

        sop_sequence = self.build_sequence(

            sop_steps

        )

        matched = []

        moved = []

        missing = []

        extra = []

        used = set()

        for l4_index, activity in enumerate(l4_sequence):

            best, score, sop_index, details = self.best_match(

                activity,

                sop_sequence

            )

            if score >= self.threshold:

                used.add(sop_index)

                movement = abs(

                    l4_index - sop_index

                )

                if movement == 0:

                    status = "Correct"

                elif movement <= 2:

                    status = "Moved"

                else:

                    status = "Out of Sequence"

                matched.append({

                    "l4_step": l4_index + 1,

                    "sop_step": sop_index + 1,

                    "l4_activity": activity,

                    "sop_activity": best,

                    "score": round(score, 2),

                    "status": status

                })

                if status != "Correct":

                    moved.append({

                        "l4_step": l4_index + 1,

                        "sop_step": sop_index + 1,

                        "activity": activity,

                        "status": status

                    })

            else:

                missing.append({

                    "step": l4_index + 1,

                    "activity": activity

                })

        for index, activity in enumerate(sop_sequence):

            if index not in used:

                extra.append({

                    "step": index + 1,

                    "activity": activity

                })

        percentage = Utils.percentage(

            len(matched),

            len(l4_sequence)

        )

        return {

            "percentage": percentage,

            "matched": matched,

            "moved": moved,

            "missing": missing,

            "extra": extra

        }

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    def summary(self, result):

        return {

            "matched":

                len(result["matched"]),

            "moved":

                len(result["moved"]),

            "missing":

                len(result["missing"]),

            "extra":

                len(result["extra"]),

            "percentage":

                result["percentage"]

        }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    matcher = SequenceMatcher()

    l4 = [

        {"activity": "Create Booking"},

        {"activity": "Validate Booking"},

        {"activity": "Approve Booking"},

        {"activity": "Generate Invoice"},

        {"activity": "Send Email"}

    ]

    sop = [

        {"activity": "Create Booking"},

        {"activity": "Approve Booking"},

        {"activity": "Validate Booking"},

        {"activity": "Generate Invoice"},

        {"activity": "Send Email"}

    ]

    result = matcher.compare(

        l4,

        sop

    )

    print("=" * 80)

    print("SEQUENCE MATCH :", result["percentage"])

    print("=" * 80)

    print()

    print("MATCHED")

    for row in result["matched"]:

        print(row)

    print()

    print("MOVED")

    for row in result["moved"]:

        print(row)

    print()

    print("MISSING")

    for row in result["missing"]:

        print(row)

    print()

    print("EXTRA")

    for row in result["extra"]:

        print(row)