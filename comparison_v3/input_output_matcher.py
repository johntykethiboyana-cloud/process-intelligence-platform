from comparison_v3.business_matcher import BusinessMatcher
from comparison_v3.utils import Utils


class InputOutputMatcher:
    """
    Input Output Matcher V3

    Responsibilities
    ----------------
    • Compare Inputs
    • Compare Outputs
    • Find Best Match
    • Missing Items
    • Extra Items
    """

    def __init__(self):

        self.matcher = BusinessMatcher()

        self.threshold = 70

    # ---------------------------------------------------------
    # BEST MATCH
    # ---------------------------------------------------------

    def best_match(self, value, candidates):

        best = None

        best_score = -1

        best_index = -1

        best_details = None

        for index, candidate in enumerate(candidates):

            details = self.matcher.compare(
                value,
                candidate
            )

            if details["score"] > best_score:

                best_score = details["score"]

                best = candidate

                best_index = index

                best_details = details

        return best, best_score, best_index, best_details

    # ---------------------------------------------------------
    # GENERIC COMPARISON
    # ---------------------------------------------------------

    def compare_list(self, left_list, right_list, label):

        left_list = Utils.unique(

            Utils.remove_empty(left_list)

        )

        right_list = Utils.unique(

            Utils.remove_empty(right_list)

        )

        matched = []

        missing = []

        extra = []

        used = set()

        for item in left_list:

            best, score, index, details = self.best_match(

                item,

                right_list

            )

            if score >= self.threshold:

                matched.append({

                    f"l4_{label}": item,

                    f"sop_{label}": best,

                    "score": round(score, 2),

                    "confidence": self.matcher.confidence(score)

                })

                used.add(index)

            else:

                missing.append({

                    f"l4_{label}": item,

                    "best_match": best,

                    "score": round(score, 2)

                })

        for index, item in enumerate(right_list):

            if index not in used:

                extra.append({

                    f"sop_{label}": item

                })

        percentage = Utils.percentage(

            len(matched),

            len(left_list)

        )

        return {

            "percentage": percentage,

            "matched": matched,

            "missing": missing,

            "extra": extra

        }

    # ---------------------------------------------------------
    # INPUTS
    # ---------------------------------------------------------

    def compare_inputs(self, l4_inputs, sop_inputs):

        return self.compare_list(

            l4_inputs,

            sop_inputs,

            "input"

        )

    # ---------------------------------------------------------
    # OUTPUTS
    # ---------------------------------------------------------

    def compare_outputs(self, l4_outputs, sop_outputs):

        return self.compare_list(

            l4_outputs,

            sop_outputs,

            "output"

        )

    # ---------------------------------------------------------
    # COMPLETE COMPARISON
    # ---------------------------------------------------------

    def compare(

        self,

        l4_inputs,

        sop_inputs,

        l4_outputs,

        sop_outputs

    ):

        return {

            "inputs": self.compare_inputs(

                l4_inputs,

                sop_inputs

            ),

            "outputs": self.compare_outputs(

                l4_outputs,

                sop_outputs

            )

        }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    matcher = InputOutputMatcher()

    l4_inputs = [

        "Customer Request",

        "Booking Form",

        "Price File"

    ]

    sop_inputs = [

        "Customer Request Form",

        "Booking Request",

        "Price Sheet"

    ]

    l4_outputs = [

        "Approved Booking",

        "Generated Invoice"

    ]

    sop_outputs = [

        "Booking Approval",

        "Invoice Generated",

        "Email Notification"

    ]

    result = matcher.compare(

        l4_inputs,

        sop_inputs,

        l4_outputs,

        sop_outputs

    )

    print("=" * 80)

    print("INPUT MATCH :", result["inputs"]["percentage"])

    print("OUTPUT MATCH :", result["outputs"]["percentage"])

    print("=" * 80)

    print("\nINPUTS")

    print(result["inputs"])

    print("\nOUTPUTS")

    print(result["outputs"])