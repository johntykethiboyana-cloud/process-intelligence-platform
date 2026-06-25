from collections import OrderedDict


class Utils:
    """
    Utility Functions for Comparison Engine V3
    """

    # ----------------------------------------------------
    # SAFE STRING
    # ----------------------------------------------------

    @staticmethod
    def safe_text(value):

        if value is None:
            return ""

        return str(value).strip()

    # ----------------------------------------------------
    # SAFE LOWER
    # ----------------------------------------------------

    @staticmethod
    def safe_lower(value):

        return Utils.safe_text(value).lower()

    # ----------------------------------------------------
    # UNIQUE LIST
    # ----------------------------------------------------

    @staticmethod
    def unique(values):

        result = []
        seen = set()

        for value in values:

            value = Utils.safe_text(value)

            if not value:
                continue

            key = value.lower()

            if key not in seen:

                seen.add(key)

                result.append(value)

        return result

    # ----------------------------------------------------
    # UNIQUE DICTIONARIES
    # ----------------------------------------------------

    @staticmethod
    def unique_dict(items, key):

        output = []
        seen = set()

        for item in items:

            if key not in item:
                continue

            value = Utils.safe_lower(item[key])

            if value in seen:
                continue

            seen.add(value)

            output.append(item)

        return output

    # ----------------------------------------------------
    # SAFE STEP TEXT
    # ----------------------------------------------------

    @staticmethod
    def step_text(step):

        if isinstance(step, dict):

            return (

                step.get("activity")

                or step.get("clean_activity")

                or step.get("text")

                or step.get("description")

                or ""

            )

        return Utils.safe_text(step)

    # ----------------------------------------------------
    # SAFE ROLE
    # ----------------------------------------------------

    @staticmethod
    def role(step):

        if isinstance(step, dict):

            return Utils.safe_text(

                step.get("role")

            )

        return ""

    # ----------------------------------------------------
    # SAFE APPLICATION
    # ----------------------------------------------------

    @staticmethod
    def application(step):

        if isinstance(step, dict):

            return Utils.safe_text(

                step.get("application")

            )

        return ""

    # ----------------------------------------------------
    # SAFE INPUT
    # ----------------------------------------------------

    @staticmethod
    def input_value(step):

        if isinstance(step, dict):

            return Utils.safe_text(

                step.get("input")

            )

        return ""

    # ----------------------------------------------------
    # SAFE OUTPUT
    # ----------------------------------------------------

    @staticmethod
    def output_value(step):

        if isinstance(step, dict):

            return Utils.safe_text(

                step.get("output")

            )

        return ""

    # ----------------------------------------------------
    # PERCENTAGE
    # ----------------------------------------------------

    @staticmethod
    def percentage(matched, total):

        if total == 0:
            return 100.0

        return round(

            (matched / total) * 100,

            2

        )

    # ----------------------------------------------------
    # SORT BY SCORE
    # ----------------------------------------------------

    @staticmethod
    def sort_score(data):

        return sorted(

            data,

            key=lambda x: x.get(

                "score",

                0

            ),

            reverse=True

        )

    # ----------------------------------------------------
    # EMPTY RESULT
    # ----------------------------------------------------

    @staticmethod
    def empty_result():

        return {

            "percentage": 0,

            "matched": [],

            "missing": [],

            "extra": []

        }

    # ----------------------------------------------------
    # MERGE LISTS
    # ----------------------------------------------------

    @staticmethod
    def merge(*lists):

        output = []

        for lst in lists:

            output.extend(lst)

        return Utils.unique(output)

    # ----------------------------------------------------
    # REMOVE EMPTY
    # ----------------------------------------------------

    @staticmethod
    def remove_empty(values):

        return [

            v

            for v in values

            if Utils.safe_text(v)

        ]

    # ----------------------------------------------------
    # DICTIONARY TO LIST
    # ----------------------------------------------------

    @staticmethod
    def dict_values(data):

        if not isinstance(data, dict):

            return []

        output = []

        for value in data.values():

            if isinstance(value, list):

                output.extend(value)

            else:

                output.append(value)

        return output

    # ----------------------------------------------------
    # FLATTEN
    # ----------------------------------------------------

    @staticmethod
    def flatten(values):

        output = []

        for item in values:

            if isinstance(item, list):

                output.extend(

                    Utils.flatten(item)

                )

            else:

                output.append(item)

        return output

    # ----------------------------------------------------
    # REMOVE DUPLICATE ORDER
    # ----------------------------------------------------

    @staticmethod
    def ordered_unique(values):

        return list(

            OrderedDict.fromkeys(

                values

            )

        )

    # ----------------------------------------------------
    # SCORE SUMMARY
    # ----------------------------------------------------

    @staticmethod
    def score_summary(result):

        return {

            "matched":

                len(result.get(

                    "matched",

                    []

                )),

            "missing":

                len(result.get(

                    "missing",

                    []

                )),

            "extra":

                len(result.get(

                    "extra",

                    []

                )),

            "percentage":

                result.get(

                    "percentage",

                    0

                )

        }


# ----------------------------------------------------
# TEST
# ----------------------------------------------------

if __name__ == "__main__":

    sample = [

        "SAP",

        "sap",

        "GCSS",

        "",

        "GCSS"

    ]

    print(Utils.unique(sample))

    print(Utils.percentage(8, 10))