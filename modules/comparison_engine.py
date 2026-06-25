from difflib import SequenceMatcher


class ComparisonEngine:

    def __init__(self):
        pass

    # -------------------------------------------------------
    # Main Comparison
    # -------------------------------------------------------

    def compare(self, l4_data, sop_data):

        result = {}

        result["process_name"] = self.compare_text(
            l4_data["process_name"],
            sop_data["process_name"]
        )

        result["activities"] = self.compare_lists(
            l4_data["activities"],
            sop_data["activities"]
        )

        result["applications"] = self.compare_lists(
            l4_data["applications"],
            sop_data["applications"]
        )

        result["roles"] = self.compare_lists(
            l4_data["roles"],
            sop_data["roles"]
        )

        result["controls"] = self.compare_lists(
            l4_data["controls"],
            sop_data["controls"]
        )

        result["risks"] = self.compare_lists(
            l4_data["risks"],
            sop_data["risks"]
        )

        result["inputs"] = self.compare_lists(
            l4_data["inputs"],
            sop_data["inputs"]
        )

        result["outputs"] = self.compare_lists(
            l4_data["outputs"],
            sop_data["outputs"]
        )

        result["sequence"] = self.compare_sequence(
            l4_data["activities"],
            sop_data["activities"]
        )

        scores = [

            result["process_name"]["percentage"],
            result["activities"]["percentage"],
            result["applications"]["percentage"],
            result["roles"]["percentage"],
            result["controls"]["percentage"],
            result["risks"]["percentage"],
            result["inputs"]["percentage"],
            result["outputs"]["percentage"],
            result["sequence"]["percentage"]

        ]

        result["overall_score"] = round(
            sum(scores) / len(scores),
            2
        )

        return result

    # -------------------------------------------------------

    def compare_text(self, l4, sop):

        score = round(
            SequenceMatcher(
                None,
                l4.lower(),
                sop.lower()
            ).ratio() * 100,
            2
        )

        return {

            "percentage": score,

            "l4": l4,

            "sop": sop

        }

    # -------------------------------------------------------

    def compare_lists(self, l4_items, sop_items):

        l4_clean = [i.strip() for i in l4_items]
        sop_clean = [i.strip() for i in sop_items]

        matched = []
        missing = []
        extra = []

        used = set()

        for item in l4_clean:

            best_score = 0
            best_index = None

            for index, sop_item in enumerate(sop_clean):

                if index in used:
                    continue

                score = SequenceMatcher(
                    None,
                    item.lower(),
                    sop_item.lower()
                ).ratio()

                if score > best_score:
                    best_score = score
                    best_index = index

            if best_score >= 0.75:

                matched.append({

                    "l4": item,
                    "sop": sop_clean[best_index],
                    "score": round(best_score * 100, 2)

                })

                used.add(best_index)

            else:

                missing.append(item)

        for index, item in enumerate(sop_clean):

            if index not in used:
                extra.append(item)

        if len(l4_clean):

            percentage = round(
                len(matched) / len(l4_clean) * 100,
                2
            )

        else:

            percentage = 100

        return {

            "percentage": percentage,

            "matched": matched,

            "missing": missing,

            "extra": extra

        }

    # -------------------------------------------------------

    def compare_sequence(self, l4_steps, sop_steps):

        l4 = " ".join(l4_steps)
        sop = " ".join(sop_steps)

        score = round(
            SequenceMatcher(
                None,
                l4.lower(),
                sop.lower()
            ).ratio() * 100,
            2
        )

        return {

            "percentage": score

        }