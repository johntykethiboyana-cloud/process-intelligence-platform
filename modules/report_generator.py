class ReportGenerator:

    def generate(self, analysis, quality):

        quality_score = quality["score"]

        controls = len(analysis["controls"])
        risks = len(analysis["risks"])
        approvals = len(analysis["approvals"])
        manual = len(analysis["manual_steps"])
        applications = len(analysis["applications"])
        roles = len(analysis["roles"])

        # ----------------------------------------------------
        # Automation Score
        # ----------------------------------------------------

        if manual >= 20:
            automation_score = 40
            automation = "HIGH"
        elif manual >= 10:
            automation_score = 70
            automation = "MEDIUM"
        else:
            automation_score = 95
            automation = "LOW"

        # ----------------------------------------------------
        # Risk Coverage Score
        # ----------------------------------------------------

        if risks == 0:
            risk_score = 40
            risk_status = "Poor"
        elif risks <= 3:
            risk_score = 75
            risk_status = "Good"
        else:
            risk_score = 95
            risk_status = "Excellent"

        # ----------------------------------------------------
        # Control Coverage Score
        # ----------------------------------------------------

        if controls == 0:
            control_score = 40
            control_status = "Poor"
        elif controls <= 3:
            control_score = 75
            control_status = "Good"
        else:
            control_score = 95
            control_status = "Excellent"

        # ----------------------------------------------------
        # Documentation Score
        # ----------------------------------------------------

        documentation_score = quality_score

        # ----------------------------------------------------
        # Overall Intelligence Score
        # ----------------------------------------------------

        intelligence_score = round(
            (
                quality_score +
                automation_score +
                risk_score +
                control_score
            ) / 4
        )

        # ----------------------------------------------------
        # Overall Rating
        # ----------------------------------------------------

        if intelligence_score >= 90:
            rating = "★★★★★ Excellent"
        elif intelligence_score >= 80:
            rating = "★★★★☆ Very Good"
        elif intelligence_score >= 70:
            rating = "★★★☆☆ Good"
        elif intelligence_score >= 60:
            rating = "★★☆☆☆ Average"
        else:
            rating = "★☆☆☆☆ Needs Improvement"

        # ----------------------------------------------------
        # Report
        # ----------------------------------------------------

        print("\n")
        print("=" * 80)
        print("SOP INTELLIGENCE SCORECARD".center(80))
        print("=" * 80)

        print(f"Overall Intelligence Score : {intelligence_score}/100")
        print(f"Overall Rating             : {rating}")

        print("\n")
        print("-" * 80)
        print("QUALITY METRICS")
        print("-" * 80)

        print(f"Quality Score              : {quality_score}/100")
        print(f"Documentation              : {documentation_score}/100")
        print(f"Automation Potential       : {automation}")
        print(f"Risk Coverage              : {risk_status}")
        print(f"Control Coverage           : {control_status}")

        print("\n")
        print("-" * 80)
        print("PROCESS METRICS")
        print("-" * 80)

        print(f"Applications               : {applications}")
        print(f"Roles                      : {roles}")
        print(f"Controls                   : {controls}")
        print(f"Risks                      : {risks}")
        print(f"Approvals                  : {approvals}")
        print(f"Manual Activities          : {manual}")

        print("\n")
        print("-" * 80)
        print("BUSINESS RECOMMENDATIONS")
        print("-" * 80)

        if quality_score >= 90:
            print("✓ SOP is well documented.")
        else:
            print("• Improve SOP documentation quality.")

        if manual >= 10:
            print("• High number of manual activities detected.")
            print("  Consider Power Automate, Python or RPA.")
        else:
            print("✓ Manual activities are within acceptable limits.")

        if approvals > 0:
            print("✓ Approval workflow detected.")
        else:
            print("• No approval workflow detected.")

        if controls > 0:
            print("✓ Process controls are documented.")
        else:
            print("• Process controls should be added.")

        if applications > 0:
            print("✓ Business applications identified.")
        else:
            print("• Applications are not clearly mentioned.")

        print("\n")
        print("=" * 80)