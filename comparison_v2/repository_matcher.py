from difflib import SequenceMatcher
import re

from comparison.normalizer import Normalizer


class RepositoryMatcher:

    def __init__(self):

        self.normalizer = Normalizer()

        self.stop_words = {
            "the", "a", "an", "to", "of", "for", "and",
            "in", "on", "with", "by", "is", "be", "are",
            "this", "that", "from", "into", "or", "as",
            "at", "it", "its", "your"
        }

        self.action_words = {
            "create",
            "update",
            "delete",
            "approve",
            "review",
            "validate",
            "verify",
            "submit",
            "open",
            "close",
            "send",
            "receive",
            "search",
            "select",
            "assign",
            "link",
            "request",
            "execute",
            "upload",
            "download"
        }

    # ---------------------------------------------------------

    def tokenize(self, text):

        text = self.normalizer.normalize(text)

        words = re.findall(r"[a-zA-Z0-9]+", text)

        return {

            w

            for w in words

            if len(w) > 2

            and w not in self.stop_words

        }

    # ---------------------------------------------------------

    def similarity(self, text1, text2):

        n1 = self.normalizer.normalize(text1)
        n2 = self.normalizer.normalize(text2)

        sequence_score = SequenceMatcher(

            None,

            n1,

            n2

        ).ratio()

        words1 = self.tokenize(text1)
        words2 = self.tokenize(text2)

        # Keyword overlap

        if len(words1 | words2):

            keyword_score = len(

                words1 & words2

            ) / len(

                words1 | words2

            )

        else:

            keyword_score = 0

        # Action word bonus

        action1 = words1 & self.action_words
        action2 = words2 & self.action_words

        if action1 == action2 and len(action1):

            action_bonus = 1

        else:

            action_bonus = 0

        final_score = (

            sequence_score * 0.40 +

            keyword_score * 0.50 +

            action_bonus * 0.10

        )

        return final_score

    # ---------------------------------------------------------

    def score_process(self, sop_items, process):

        sop_activities = [

            item["text"]

            for item in sop_items

            if item["type"] in [

                "ACTIVITY",

                "COMMUNICATION",

                "APPROVAL",

                "VALIDATION"

            ]

        ]

        if not sop_activities:

            return {

                "score": 0,

                "matched_activities": 0

            }

        total_score = 0

        matched = 0

        for sop in sop_activities:

            best = 0

            for l4 in process["activities"]:

                score = self.similarity(

                    sop,

                    l4

                )

                if score > best:

                    best = score

            total_score += best

            if best >= 0.60:

                matched += 1

        final_score = (

            total_score /

            len(sop_activities)

        ) * 100

        return {

            "score": round(final_score, 2),

            "matched_activities": matched

        }

    # ---------------------------------------------------------

    def find_best_matches(self, sop_items, repository):

        results = []

        for process_name, process in repository.items():

            result = self.score_process(

                sop_items,

                process

            )

            results.append({

                "process": process_name,

                "score": result["score"],

                "matched": result["matched_activities"]

            })

        results.sort(

            key=lambda x: (

                x["score"],

                x["matched"]

            ),

            reverse=True

        )

        return results[:10]