from modules.automation_detector import AutomationDetector
from modules.process_improver import ProcessImprover

import re


class ProcessAnalyzer:

    def __init__(self):

        self.automation_detector = AutomationDetector()
        self.process_improver = ProcessImprover()

        # --------------------------------------------------
        # Applications
        # --------------------------------------------------

        self.application_keywords = [

            "Citrix",
            "SharePoint",
            "Outlook",
            "Excel",
            "FIN",
            "SAP",
            "ARIS",
            "ServiceNow",
            "Swift",
            "FASWeb",
            "FINDUR",
            "TRAX",
            "Power BI",
            "Teams",
            "Oracle",
            "MS Forms"

        ]

        # --------------------------------------------------
        # Roles
        # --------------------------------------------------

        self.role_keywords = [

            "Requestor",
            "Requester",
            "Bank Administration",
            "Treasury",
            "Finance",
            "Approver",
            "Reviewer",
            "Operations",
            "Maker",
            "Checker",
            "User",
            "Administrator",
            "Processor",
            "Manager"

        ]

        # --------------------------------------------------
        # Controls
        # --------------------------------------------------

        self.control_keywords = [

            "approve",
            "approval",
            "verify",
            "validation",
            "review",
            "mandatory",
            "control",
            "maker",
            "checker",
            "authorize",
            "authorise"

        ]

        # --------------------------------------------------
        # Risks
        # --------------------------------------------------

        self.risk_keywords = [

            "risk",
            "failure",
            "incorrect",
            "missing",
            "duplicate",
            "delay",
            "error",
            "exception"

        ]

        # --------------------------------------------------
        # Manual Activities
        # --------------------------------------------------

        self.manual_keywords = [

            "copy",
            "paste",
            "login",
            "log in",
            "download",
            "upload",
            "email",
            "mail",
            "send",
            "enter",
            "type",
            "click",
            "select",
            "search",
            "save"

        ]

        self.approval_keywords = [

            "approve",
            "approval",
            "approved",
            "authorise",
            "authorize",
            "review"

        ]

    # ======================================================
    # Generic Detector
    # ======================================================

    def detect_keywords(self, sections, keywords):

        results = set()

        for content in sections.values():

            for line in content:

                txt = line.lower()

                for keyword in keywords:

                    if keyword.lower() in txt:
                        results.add(keyword)

        return sorted(results)

    # ======================================================
    # Activities
    # ======================================================

    def detect_activities(self, sections):

        activities = []

        verbs = [

            "create",
            "update",
            "delete",
            "validate",
            "verify",
            "review",
            "approve",
            "reject",
            "check",
            "submit",
            "receive",
            "send",
            "upload",
            "download",
            "complete",
            "enter",
            "select",
            "search",
            "close",
            "open",
            "link"

        ]

        for content in sections.values():

            for line in content:

                text = line.strip()

                if len(text) < 5:
                    continue

                first_word = text.split()[0].lower()

                if first_word in verbs:
                    activities.append(text)

        return sorted(list(set(activities)))

    # ======================================================
    # Applications
    # ======================================================

    def detect_applications(self, sections):

        return self.detect_keywords(
            sections,
            self.application_keywords
        )

    # ======================================================
    # Roles
    # ======================================================

    def detect_roles(self, sections):

        return self.detect_keywords(
            sections,
            self.role_keywords
        )

    # ======================================================
    # Inputs
    # ======================================================

    def detect_inputs(self, sections):

        inputs = []

        patterns = [

            "request",
            "form",
            "instruction",
            "email",
            "ticket",
            "document"

        ]

        for content in sections.values():

            for line in content:

                txt = line.lower()

                if any(word in txt for word in patterns):
                    inputs.append(line)

        return sorted(list(set(inputs)))

    # ======================================================
    # Outputs
    # ======================================================

    def detect_outputs(self, sections):

        outputs = []

        patterns = [

            "completed",
            "confirmation",
            "created",
            "updated",
            "closed",
            "approved",
            "rejected"

        ]

        for content in sections.values():

            for line in content:

                txt = line.lower()

                if any(word in txt for word in patterns):
                    outputs.append(line)

        return sorted(list(set(outputs)))

    # ======================================================
    # Line Detector
    # ======================================================

    def detect_lines(self, sections, keywords):

        lines = []

        for content in sections.values():

            for line in content:

                txt = line.lower()

                if any(word in txt for word in keywords):
                    lines.append(line)

        return lines

    # ======================================================
    # Statistics
    # ======================================================

    def calculate_statistics(self, sections):

        paragraphs = sum(len(v) for v in sections.values())

        words = 0

        for content in sections.values():

            for line in content:
                words += len(line.split())

        return {

            "Sections": len(sections),
            "Paragraphs": paragraphs,
            "Words": words

        }

    # ======================================================
    # Recommendations
    # ======================================================

    def generate_recommendations(self, analysis):

        recommendations = []

        if len(analysis["manual_steps"]) > 10:

            recommendations.append(
                "Large number of manual activities detected."
            )

        if len(analysis["controls"]) == 0:

            recommendations.append(
                "No controls identified."
            )

        if len(analysis["risks"]) == 0:

            recommendations.append(
                "No risks documented."
            )

        if len(analysis["applications"]) == 0:

            recommendations.append(
                "No applications detected."
            )

        if len(recommendations) == 0:

            recommendations.append(
                "No major issues detected."
            )

        return recommendations

    # ======================================================
    # Main Analysis
    # ======================================================

    def analyze(self, sections):

        analysis = {}

        analysis["applications"] = self.detect_applications(sections)
        analysis["roles"] = self.detect_roles(sections)
        analysis["activities"] = self.detect_activities(sections)
        analysis["inputs"] = self.detect_inputs(sections)
        analysis["outputs"] = self.detect_outputs(sections)

        analysis["controls"] = self.detect_lines(
            sections,
            self.control_keywords
        )

        analysis["risks"] = self.detect_lines(
            sections,
            self.risk_keywords
        )

        analysis["approvals"] = self.detect_lines(
            sections,
            self.approval_keywords
        )

        analysis["manual_steps"] = self.detect_lines(
            sections,
            self.manual_keywords
        )

        analysis["keywords"] = sorted(

            list(

                set(

                    analysis["applications"] +
                    analysis["roles"]

                )

            )

        )

        analysis["statistics"] = self.calculate_statistics(sections)

        opportunities = self.automation_detector.detect(sections)

        analysis["automation_opportunities"] = opportunities

        analysis["process_improvements"] = self.process_improver.analyze(
            opportunities
        )

        analysis["recommendations"] = self.generate_recommendations(
            analysis
        )

        return analysis