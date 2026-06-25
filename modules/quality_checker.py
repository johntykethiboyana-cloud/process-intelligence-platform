class QualityChecker:

    def evaluate(self, sections):

        report = {}

        score = 0

        # --------------------------------------------
        # Basic Statistics
        # --------------------------------------------

        total_sections = len(sections)

        total_paragraphs = sum(len(content) for content in sections.values())

        report["Sections Available"] = total_sections >= 5
        report["Enough Paragraphs"] = total_paragraphs >= 20

        if report["Sections Available"]:
            score += 20

        if report["Enough Paragraphs"]:
            score += 20

        # --------------------------------------------
        # Check Applications
        # --------------------------------------------

        applications = [
            "SAP",
            "SharePoint",
            "Excel",
            "Outlook",
            "ARIS",
            "Swift",
            "ServiceNow",
            "Citrix",
            "FIN"
        ]

        found_application = False

        # --------------------------------------------
        # Check Risks
        # --------------------------------------------

        risks = [
            "risk",
            "error",
            "exception",
            "incorrect",
            "missing",
            "failure"
        ]

        found_risk = False

        # --------------------------------------------
        # Check Controls
        # --------------------------------------------

        controls = [
            "approve",
            "review",
            "verify",
            "mandatory",
            "control",
            "checker"
        ]

        found_control = False

        # --------------------------------------------
        # Scan all paragraphs
        # --------------------------------------------

        for content in sections.values():

            for line in content:

                text = line.lower()

                if any(app.lower() in text for app in applications):
                    found_application = True

                if any(risk in text for risk in risks):
                    found_risk = True

                if any(control in text for control in controls):
                    found_control = True

        report["Applications Mentioned"] = found_application
        report["Risks Mentioned"] = found_risk
        report["Controls Mentioned"] = found_control

        if found_application:
            score += 20

        if found_risk:
            score += 20

        if found_control:
            score += 20

        report["score"] = score

        return report