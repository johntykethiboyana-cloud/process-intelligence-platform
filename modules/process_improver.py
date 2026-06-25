class ProcessImprover:

    def analyze(self, opportunities):

        improvements = []

        for item in opportunities:

            # -------------------------
            # Default values
            # -------------------------

            business_impact = item["business_impact"]

            estimated_saving = item["estimated_saving"]

            readiness = item["automation_readiness"]

            difficulty = "Easy"

            if item["manual_steps"] >= 8:
                difficulty = "Medium"

            if item["manual_steps"] >= 15:
                difficulty = "High"

            improvements.append({

                "section": item["section"],

                "manual_steps": item["manual_steps"],

                "activities": item["activities"],

                "solution": item["solution"],

                "priority": item["priority"],

                "business_impact": business_impact,

                "estimated_saving": estimated_saving,

                "automation_readiness": readiness,

                "implementation_difficulty": difficulty

            })

        return improvements