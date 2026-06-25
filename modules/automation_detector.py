class AutomationDetector:

    def __init__(self):

        self.rules = {

            "copy": ("Python / Power Automate", "High", 3),
            "paste": ("Python / Power Automate", "High", 3),
            "download": ("Power Automate", "Medium", 2),
            "upload": ("Power Automate", "Medium", 2),
            "email": ("Outlook API / Power Automate", "High", 3),
            "mail": ("Outlook API / Power Automate", "High", 3),
            "login": ("RPA", "Low", 1),
            "log in": ("RPA", "Low", 1),
            "enter": ("Python", "Medium", 2),
            "type": ("Python", "Medium", 2),
            "save": ("Power Automate", "Low", 1),
            "update": ("Python", "Medium", 2),
            "search": ("Python", "Low", 1),
            "select": ("RPA", "Low", 1),
            "click": ("RPA", "Low", 1)
        }

    # ------------------------------------------------------------

    def detect(self, sections):

        opportunities = []

        for heading, paragraphs in sections.items():

            activities = []
            technologies = set()
            total_minutes = 0
            priority_score = 0

            for paragraph in paragraphs:

                text = paragraph.lower()

                for keyword, recommendation in self.rules.items():

                    if keyword in text:

                        activities.append(paragraph)

                        technologies.add(recommendation[0])

                        total_minutes += recommendation[2]

                        if recommendation[1] == "High":
                            priority_score += 3
                        elif recommendation[1] == "Medium":
                            priority_score += 2
                        else:
                            priority_score += 1

                        break

            if len(activities) == 0:
                continue

            # ---------------- Priority ----------------

            if priority_score >= 10:
                priority = "High"
                business_impact = "High"
                readiness = "95%"
            elif priority_score >= 5:
                priority = "Medium"
                business_impact = "Medium"
                readiness = "80%"
            else:
                priority = "Low"
                business_impact = "Low"
                readiness = "60%"

            opportunities.append({

                "section": heading,

                "manual_steps": len(activities),

                "activities": activities,

                "solution": ", ".join(sorted(technologies)),

                "priority": priority,

                "estimated_saving": f"{total_minutes} Minutes",

                "business_impact": business_impact,

                "automation_readiness": readiness

            })

        return opportunities