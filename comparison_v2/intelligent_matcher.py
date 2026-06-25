from difflib import SequenceMatcher
import re
from comparison_v2.normalizer import Normalizer


class IntelligentMatcher:
    """
    Intelligent Matcher V2
    """

    ACTION_WEIGHT = 0.10
    OBJECT_WEIGHT = 0.10
    APP_WEIGHT = 0.10
    KEYWORD_WEIGHT = 0.20
    TEXT_WEIGHT = 0.50

    def __init__(self):
        self.normalizer = Normalizer()
        self.threshold = 0.65

    # ---------------------------------------------------------

    def normalize(self, text):
        return self.normalizer.normalize(str(text or ""))

    def similarity(self, text1, text2):
        return SequenceMatcher(
            None,
            self.normalize(text1),
            self.normalize(text2)
        ).ratio()

    # ---------------------------------------------------------

    def extract_action(self, text):
        actions = [
    "create",
    "generate",
    "add",
    "open",
    "click",
    "select",
    "update",
    "modify",
    "edit",
    "delete",
    "remove",
    "approve",
    "review",
    "validate",
    "verify",
    "submit",
    "save",
    "search",
    "assign",
    "upload",
    "download",
    "link",
    "unlink",
    "close",
    "cancel",
    "receive",
    "send"
]
        t = self.normalize(text)
        for a in actions:
            if re.search(rf"\b{re.escape(a)}\b", t):
                return a
        return ""

    def extract_application(self, text):
        apps = [
    "gcss",
    "sap",
    "aris",
    "sharepoint",
    "outlook",
    "excel",
    "salesforce",
    "power bi",
    "teams",
    "gpm",
    "mdm",
    "oracle",
    "d365",
    "dynamics",
    "compass",
    "athena",
    "citrix",
    "servicenow"
]
        t = self.normalize(text)
        for a in apps:
            if a in t:
                return a
        return ""

    def extract_keywords(self, text):
        words = re.findall(r"[A-Za-z0-9]+", self.normalize(text))
        stop = {
            "the","and","for","with","from","into",
            "please","kindly","then","now","step",
            "click","select","open"
        }
        return sorted(
    set(
        w
        for w in words
        if len(w) > 2 and w not in stop
    )
)

    def extract_business_object(self, text):
        action = self.extract_action(text)
        t = self.normalize(text)
        if action:
            m = re.search(rf"{action}\s+(.*)", t)
            if m:
                return m.group(1)
        return t

    # ---------------------------------------------------------

    def detailed_score(self, l4_text, sop_text):

        semantic = self.similarity(l4_text, sop_text)

        action1 = self.extract_action(l4_text)
        action2 = self.extract_action(sop_text)

        object1 = self.extract_business_object(l4_text)
        object2 = self.extract_business_object(sop_text)

        app1 = self.extract_application(l4_text)
        app2 = self.extract_application(sop_text)

        kw1 = set(self.extract_keywords(l4_text))
        kw2 = set(self.extract_keywords(sop_text))

        action_score = 1.0 if action1 and action1 == action2 else 0.0
        object_score = self.similarity(object1, object2)
        app_score = 1.0 if app1 and app1 == app2 else 0.0

        if kw1:
            keyword_score = len(kw1 & kw2) / len(kw1)
        else:
            keyword_score = 0

        final = (
            semantic * self.TEXT_WEIGHT +
            action_score * self.ACTION_WEIGHT +
            object_score * self.OBJECT_WEIGHT +
            app_score * self.APP_WEIGHT +
            keyword_score * self.KEYWORD_WEIGHT
        )

        return {
            "semantic": round(semantic * 100, 2),
            "action": round(action_score * 100, 2),
            "object": round(object_score * 100, 2),
            "application": round(app_score * 100, 2),
            "keyword": round(keyword_score * 100, 2),
            "score": round(final * 100, 2)
        }
    # ---------------------------------------------------------

    def match_text(self, text1, text2):

        details = self.detailed_score(text1, text2)

        return {

            "l4": text1,

            "sop": text2,

            "percentage": details["score"],

            **details

        }    
    # ---------------------------------------------------------

    def best_match(self, value, candidates):
        best = None
        best_score = -1
        best_index = -1

        for i, candidate in enumerate(candidates):
            details = self.detailed_score(value, candidate)
            if details["score"] > best_score:
                best = candidate
                best_score = details["score"]
                best_index = i
                best_details = details

        return best, best_details, best_index

    # ---------------------------------------------------------

    def match_lists(self, l4_list, sop_list):

        matched = []
        missing = []
        extra = []
        used = set()

        for item in l4_list:
            sop, details, idx = self.best_match(item, sop_list)

            if details["score"] >= self.threshold * 100:
                matched.append({
                    "l4": item,
                    "sop": sop,
                    **details
                })
                used.add(idx)
            else:
                missing.append(item)

        for idx, item in enumerate(sop_list):
            if idx not in used:
                extra.append(item)

        percentage = round(
            (len(matched) / len(l4_list) * 100)
            if l4_list else 100,
            2
        )

        return {
            "percentage": percentage,
            "matched": matched,
            "missing": missing,
            "extra": extra
        }
        # ---------------------------------------------------------

    def match_sequence(self, l4_steps, sop_steps):

        l4 = " ".join(l4_steps)

        sop = " ".join(sop_steps)

        score = self.similarity(

            l4,

            sop

        )

        return {

            "percentage": round(score * 100, 2)

        }

    # ---------------------------------------------------------

    def repository_match(
        self,
        sop_title,
        sop_keywords,
        sop_apps,
        sop_activities,
        repository_index
    ):
        results = []

        for process in repository_index:

            title_score = self.similarity(
                sop_title,
                process["process"]
            )

            activity = self.match_lists(
                sop_activities,
                process["activities"]
            )

            app = self.match_lists(
                sop_apps,
                process["applications"]
            )

            keyword_overlap = (
                len(set(sop_keywords) & set(process["keywords"]))
                / max(1, len(sop_keywords))
            )

            final = (
                title_score * 0.20 +
                activity["percentage"] / 100 * 0.50 +
                app["percentage"] / 100 * 0.15 +
                keyword_overlap * 0.15
            )

            results.append({
                "process": process["process"],
                "score": round(final * 100, 2),
                "title_score": round(title_score * 100, 2),
                "activity_score": activity["percentage"],
                "application_score": app["percentage"],
                "keyword_score": round(keyword_overlap * 100, 2)
            })

        return sorted(results, key=lambda x: x["score"], reverse=True)
