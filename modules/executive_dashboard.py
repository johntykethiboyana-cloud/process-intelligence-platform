class ExecutiveDashboard:

    def generate(self, analysis, quality):

        opportunities = analysis["automation_opportunities"]

        high = 0
        medium = 0
        low = 0

        total_minutes = 0

        for item in opportunities:

            if item["priority"] == "High":
                high += 1
            elif item["priority"] == "Medium":
                medium += 1
            else:
                low += 1

            try:
                minutes = int(item["estimated_saving"].split()[0])
            except:
                minutes = 0

            total_minutes += minutes

        annual_hours = round((total_minutes * 250) / 60)

        automation_readiness = 100

        if len(opportunities) > 0:

            automation_readiness = round(

                sum(int(i["automation_readiness"].replace("%", ""))
                    for i in opportunities)

                / len(opportunities)

            )

        documentation = "Excellent"

        if quality["score"] < 90:
            documentation = "Good"

        if quality["score"] < 70:
            documentation = "Average"

        if quality["score"] < 50:
            documentation = "Poor"

        if len(analysis["risks"]) >= 10:
            business_risk = "High"
        elif len(analysis["risks"]) >= 5:
            business_risk = "Medium"
        else:
            business_risk = "Low"

        print("\n")
        print("=" * 80)
        print("AI PROCESS EXCELLENCE DASHBOARD".center(80))
        print("=" * 80)

        print(f"Overall Health Score         : {quality['score']}/100")
        print(f"Automation Readiness         : {automation_readiness}%")
        print(f"Documentation Quality        : {documentation}")
        print(f"Business Risk                : {business_risk}")

        print()

        print(f"Estimated Time Saving        : {total_minutes} Minutes / Process")
        print(f"Estimated Annual Saving      : {annual_hours} Hours")

        print()

        print(f"Applications Identified      : {len(analysis['applications'])}")
        print(f"Roles Identified             : {len(analysis['roles'])}")
        print(f"Controls Identified          : {len(analysis['controls'])}")
        print(f"Risks Identified             : {len(analysis['risks'])}")

        print()

        print(f"High Priority Processes      : {high}")
        print(f"Medium Priority Processes    : {medium}")
        print(f"Low Priority Processes       : {low}")

        print("=" * 80)