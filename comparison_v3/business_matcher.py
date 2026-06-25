import re

from comparison_v3.normalizer import Normalizer
from comparison_v3.similarity import Similarity


class BusinessMatcher:
    """
    Business Matcher V3

    This class understands business activities instead of
    comparing plain text.

    It extracts

    • Action
    • Business Object
    • Application
    • Role
    • Controls
    • Risks
    • Keywords

    and produces a business similarity score.
    """

    def __init__(self):

        self.normalizer = Normalizer()

        self.similarity = Similarity()

        # ----------------------------------------
        # Business Actions
        # ----------------------------------------

        self.actions = {

            "create",

            "update",

            "delete",

            "approve",

            "review",

            "validate",

            "verify",

            "submit",

            "receive",

            "send",

            "generate",

            "assign",

            "cancel",

            "upload",

            "download",

            "link",

            "unlink",

            "complete"

        }

        # ----------------------------------------
        # Applications
        # ----------------------------------------

        self.applications = {

            "SAP",

            "GCSS",

            "ARIS",

            "SharePoint",

            "Outlook",

            "Excel",

            "Power BI",

            "ServiceNow",

            "Salesforce",

            "Athena",

            "GPM",

            "Dynamics"

        }

        # ----------------------------------------
        # Role words
        # ----------------------------------------

        self.roles = {

            "Requester",

            "Approver",

            "Reviewer",

            "Treasury",

            "Finance",

            "Operations",

            "CPM",

            "Manager",

            "Controller",

            "Business",

            "Administrator",

            "Price Setter"

        }

        # ----------------------------------------
        # Control words
        # ----------------------------------------

        self.control_words = {

            "approve",

            "approval",

            "review",

            "validate",

            "verification",

            "mandatory",

            "maker",

            "checker",

            "authorization"

        }

        # ----------------------------------------
        # Risk words
        # ----------------------------------------

        self.risk_words = {

            "risk",

            "duplicate",

            "incorrect",

            "delay",

            "error",

            "failure",

            "exception",

            "missing"

        }

    # --------------------------------------------------
    # ACTION
    # --------------------------------------------------

    def extract_action(self, text):

        text = self.normalizer.normalize(text)

        for word in text.split():

            if word in self.actions:

                return word

        return ""

    # --------------------------------------------------
    # APPLICATION
    # --------------------------------------------------

    def extract_application(self, text):

        return self.normalizer.normalize_application(text)

    # --------------------------------------------------
    # ROLE
    # --------------------------------------------------

    def extract_role(self, text):

        lower = str(text).lower()

        for role in self.roles:

            if role.lower() in lower:

                return role

        return ""

    # --------------------------------------------------
    # CONTROL
    # --------------------------------------------------

    def has_control(self, text):

        lower = str(text).lower()

        return any(

            word in lower

            for word in self.control_words

        )

    # --------------------------------------------------
    # RISK
    # --------------------------------------------------

    def has_risk(self, text):

        lower = str(text).lower()

        return any(

            word in lower

            for word in self.risk_words

        )

    # --------------------------------------------------
    # BUSINESS OBJECT
    # --------------------------------------------------

    def extract_business_object(self, text):

        text = self.normalizer.normalize(text)

        action = self.extract_action(text)

        if not action:

            return text

        pattern = rf"{action}\s+(.*)"

        match = re.search(

            pattern,

            text,

            re.IGNORECASE

        )

        if match:

            return match.group(1).strip()

        return text

    # --------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------

    def extract_keywords(self, text):

        return self.normalizer.keywords(text)

    # --------------------------------------------------
    # BUILD BUSINESS OBJECT
    # --------------------------------------------------

    def analyse(self, text):

        return {

            "text": text,

            "normalized":

                self.normalizer.normalize(text),

            "action":

                self.extract_action(text),

            "business_object":

                self.extract_business_object(text),

            "application":

                self.extract_application(text),

            "role":

                self.extract_role(text),

            "control":

                self.has_control(text),

            "risk":

                self.has_risk(text),

            "keywords":

                self.extract_keywords(text)

        }

    # --------------------------------------------------
    # ACTION SCORE
    # --------------------------------------------------

    def action_score(

        self,

        left,

        right

    ):

        a1 = self.extract_action(left)

        a2 = self.extract_action(right)

        if not a1:

            return 0

        return 100 if a1 == a2 else 0

    # --------------------------------------------------
    # OBJECT SCORE
    # --------------------------------------------------

    def object_score(

        self,

        left,

        right

    ):

        return self.similarity.business_similarity(

            self.extract_business_object(left),

            self.extract_business_object(right)

        ) * 100

    # --------------------------------------------------
    # APPLICATION SCORE
    # --------------------------------------------------

    def application_score(

        self,

        left,

        right

    ):

        app1 = self.extract_application(left)

        app2 = self.extract_application(right)

        if not app1:

            return 0

        return 100 if app1 == app2 else 0




    # --------------------------------------------------
    # ROLE SCORE
    # --------------------------------------------------

    def role_score(self, left, right):

        role1 = self.extract_role(left)

        role2 = self.extract_role(right)

        if not role1:
            return 0

        return 100 if role1 == role2 else 0

    # --------------------------------------------------
    # CONTROL SCORE
    # --------------------------------------------------

    def control_score(self, left, right):

        c1 = self.has_control(left)

        c2 = self.has_control(right)

        return 100 if c1 == c2 else 0

    # --------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------

    def risk_score(self, left, right):

        r1 = self.has_risk(left)

        r2 = self.has_risk(right)

        return 100 if r1 == r2 else 0

    # --------------------------------------------------
    # KEYWORD SCORE
    # --------------------------------------------------

    def keyword_score(self, left, right):

        left_keywords = set(
            self.extract_keywords(left)
        )

        right_keywords = set(
            self.extract_keywords(right)
        )

        if not left_keywords:
            return 0

        common = len(
            left_keywords.intersection(
                right_keywords
            )
        )

        return round(
            common / len(left_keywords) * 100,
            2
        )

    # --------------------------------------------------
    # TEXT SCORE
    # --------------------------------------------------

    def text_score(self, left, right):

        return self.similarity.business_similarity(
            left,
            right
        ) * 100

    # --------------------------------------------------
    # OVERALL BUSINESS SCORE
    # --------------------------------------------------

    def compare(self, left, right):

        action = self.action_score(
            left,
            right
        )

        obj = self.object_score(
            left,
            right
        )

        app = self.application_score(
            left,
            right
        )

        role = self.role_score(
            left,
            right
        )

        control = self.control_score(
            left,
            right
        )

        risk = self.risk_score(
            left,
            right
        )

        keyword = self.keyword_score(
            left,
            right
        )

        text = self.text_score(
            left,
            right
        )

        score = (

            action * 0.20 +

            obj * 0.25 +

            keyword * 0.15 +

            app * 0.10 +

            role * 0.05 +

            control * 0.05 +

            risk * 0.05 +

            text * 0.15

        )

        return {

            "left": left,

            "right": right,

            "score": round(score, 2),

            "action_score": round(action, 2),

            "object_score": round(obj, 2),

            "keyword_score": round(keyword, 2),

            "application_score": round(app, 2),

            "role_score": round(role, 2),

            "control_score": round(control, 2),

            "risk_score": round(risk, 2),

            "text_score": round(text, 2)

        }

    # --------------------------------------------------
    # BEST MATCH
    # --------------------------------------------------

    def best_match(self, source, candidates):

        best = None

        best_result = None

        best_score = -1

        best_index = -1

        for index, candidate in enumerate(candidates):

            result = self.compare(
                source,
                candidate
            )

            if result["score"] > best_score:

                best_score = result["score"]

                best = candidate

                best_result = result

                best_index = index

        return {

            "candidate": best,

            "index": best_index,

            "score": best_score,

            "details": best_result

        }

    # --------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------

    def confidence(self, score):

        if score >= 95:
            return "Excellent"

        if score >= 85:
            return "Very High"

        if score >= 75:
            return "High"

        if score >= 65:
            return "Medium"

        if score >= 50:
            return "Low"

        return "Poor"


# --------------------------------------------------
    # ROLE SCORE
    # --------------------------------------------------

    def role_score(self, left, right):

        role1 = self.extract_role(left)

        role2 = self.extract_role(right)

        if not role1:
            return 0

        return 100 if role1 == role2 else 0

    # --------------------------------------------------
    # CONTROL SCORE
    # --------------------------------------------------

    def control_score(self, left, right):

        c1 = self.has_control(left)

        c2 = self.has_control(right)

        return 100 if c1 == c2 else 0

    # --------------------------------------------------
    # RISK SCORE
    # --------------------------------------------------

    def risk_score(self, left, right):

        r1 = self.has_risk(left)

        r2 = self.has_risk(right)

        return 100 if r1 == r2 else 0

    # --------------------------------------------------
    # KEYWORD SCORE
    # --------------------------------------------------

    def keyword_score(self, left, right):

        left_keywords = set(
            self.extract_keywords(left)
        )

        right_keywords = set(
            self.extract_keywords(right)
        )

        if not left_keywords:
            return 0

        common = len(
            left_keywords.intersection(
                right_keywords
            )
        )

        return round(
            common / len(left_keywords) * 100,
            2
        )

    # --------------------------------------------------
    # TEXT SCORE
    # --------------------------------------------------

    def text_score(self, left, right):

        return self.similarity.business_similarity(
            left,
            right
        ) * 100

    # --------------------------------------------------
    # OVERALL BUSINESS SCORE
    # --------------------------------------------------

    def compare(self, left, right):

        action = self.action_score(
            left,
            right
        )

        obj = self.object_score(
            left,
            right
        )

        app = self.application_score(
            left,
            right
        )

        role = self.role_score(
            left,
            right
        )

        control = self.control_score(
            left,
            right
        )

        risk = self.risk_score(
            left,
            right
        )

        keyword = self.keyword_score(
            left,
            right
        )

        text = self.text_score(
            left,
            right
        )

        score = (

            action * 0.20 +

            obj * 0.25 +

            keyword * 0.15 +

            app * 0.10 +

            role * 0.05 +

            control * 0.05 +

            risk * 0.05 +

            text * 0.15

        )

        return {

            "left": left,

            "right": right,

            "score": round(score, 2),

            "action_score": round(action, 2),

            "object_score": round(obj, 2),

            "keyword_score": round(keyword, 2),

            "application_score": round(app, 2),

            "role_score": round(role, 2),

            "control_score": round(control, 2),

            "risk_score": round(risk, 2),

            "text_score": round(text, 2)

        }

    # --------------------------------------------------
    # BEST MATCH
    # --------------------------------------------------

    def best_match(self, source, candidates):

        best = None

        best_result = None

        best_score = -1

        best_index = -1

        for index, candidate in enumerate(candidates):

            result = self.compare(
                source,
                candidate
            )

            if result["score"] > best_score:

                best_score = result["score"]

                best = candidate

                best_result = result

                best_index = index

        return {

            "candidate": best,

            "index": best_index,

            "score": best_score,

            "details": best_result

        }

    # --------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------

    def confidence(self, score):

        if score >= 95:
            return "Excellent"

        if score >= 85:
            return "Very High"

        if score >= 75:
            return "High"

        if score >= 65:
            return "Medium"

        if score >= 50:
            return "Low"

        return "Poor"


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    matcher = BusinessMatcher()

    left = "Create Ocean Tender in SAP"

    right = "Click Create Ocean Tender in SAP"

    result = matcher.compare(
        left,
        right
    )

    print("=" * 80)

    for key, value in result.items():

        print(f"{key:20} : {value}")

    print()

    print(
        "Confidence :",
        matcher.confidence(
            result["score"]
        )
    )