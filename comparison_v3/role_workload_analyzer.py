from collections import defaultdict


class RoleWorkloadAnalyzer:
    """
    Analyze workload distribution by role.
    """

    def __init__(self):

        self.categories = {
            "Approval": [
                "approve",
                "approval",
                "authorise",
                "authorize",
                "sign off"
            ],
            "Validation": [
                "validate",
                "verify",
                "check",
                "review"
            ],
            "Communication": [
                "email",
                "notify",
                "inform",
                "send",
                "call"
            ],
            "Data Entry": [
                "create",
                "update",
                "enter",
                "upload",
                "download",
                "copy"
            ],
            "Analysis": [
                "analyse",
                "analyze",
                "assess",
                "calculate",
                "evaluate"
            ]
        }

    def detect_category(self, activity):

        text = activity.lower()

        for category, keywords in self.categories.items():

            for keyword in keywords:

                if keyword in text:
                    return category

        return "Other"

    def analyze(self, steps):

        role_summary = defaultdict(lambda: {
            "Role": "",
            "Activities": 0,
            "Steps": 0,
            "Approval": 0,
            "Validation": 0,
            "Communication": 0,
            "Data Entry": 0,
            "Analysis": 0,
            "Other": 0
        })

        for step in steps:

            if isinstance(step, dict):

                role = (
                    step.get("role")
                    or step.get("owner")
                    or "Unassigned"
                )

                activity = (
                    step.get("activity")
                    or step.get("step")
                    or ""
                )

            else:

                role = "Unassigned"
                activity = str(step)

            category = self.detect_category(activity)

            role_summary[role]["Role"] = role
            role_summary[role]["Activities"] += 1
            role_summary[role]["Steps"] += 1
            role_summary[role][category] += 1

        return list(role_summary.values())
    