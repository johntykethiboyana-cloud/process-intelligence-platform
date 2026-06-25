class AutomationDetector:

    def detect(self, activities):

        opportunities = []

        keywords = [
            "download",
            "upload",
            "send",
            "email",
            "copy",
            "paste",
            "update",
            "enter",
            "save",
            "review",
            "check",
            "approve"
        ]

        for activity in activities:

            text = str(activity).lower()

            score = 0

            for keyword in keywords:

                if keyword in text:
                    score += 1

            if score > 0:

                opportunities.append({
                    "Activity": activity,
                    "Automation Potential": "HIGH"
                })

        return opportunities