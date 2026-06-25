from collections import defaultdict


class RoleIntelligence:
    """
    Role Intelligence Engine

    Produces:
    - Workload
    - Systems Used
    - Controls
    - Risks
    - Inputs
    - Outputs
    - Work Categories
    - Automation Score
    """

    def __init__(self):

        self.categories = {

            "Approval": [
                "approve",
                "approval",
                "authorize",
                "authorise",
                "sign"
            ],

            "Validation": [
                "review",
                "validate",
                "verify",
                "check"
            ],

            "Analysis": [
                "analyse",
                "analyze",
                "assess",
                "evaluate"
            ],

            "Data Entry": [
                "create",
                "update",
                "enter",
                "upload",
                "download",
                "copy"
            ],

            "Communication": [
                "email",
                "notify",
                "inform",
                "send",
                "call"
            ]

        }

    # ---------------------------------------------------

    def category(self, activity):

        text = activity.lower()

        for cat, words in self.categories.items():

            for word in words:

                if word in text:
                    return cat

        return "Other"

    # ---------------------------------------------------

    def analyze(self, steps):

        roles = defaultdict(lambda: {

            "Role": "",

            "Activities": 0,

            "Applications": set(),

            "Controls": 0,

            "Risks": 0,

            "Inputs": 0,

            "Outputs": 0,

            "Approval": 0,

            "Validation": 0,

            "Analysis": 0,

            "Data Entry": 0,

            "Communication": 0,

            "Other": 0

        })

        total_steps = len(steps)

        for step in steps:

            role = (
        step.get("role")
        or step.get("owner")
        or "Unassigned"
        ).strip()

            activity = step.get("activity", "")

            app = step.get("application", "")

            controls = step.get("controls", [])

            risks = step.get("risks", [])

            inp = step.get("input", "")

            out = step.get("output", "")

            cat = self.category(activity)

            r = roles[role]

            r["Role"] = role

            r["Activities"] += 1

            if app:
                r["Applications"].add(app)

            r["Controls"] += len(controls)

            r["Risks"] += len(risks)

            if inp:
                r["Inputs"] += 1

            if out:
                r["Outputs"] += 1

            r[cat] += 1

        results = []

        for role in roles.values():

            role["Applications"] = len(role["Applications"])

            role["Workload %"] = round(
                role["Activities"] / total_steps * 100,
                2
            ) if total_steps else 0

            score = (

                role["Activities"] * 3

                + role["Controls"] * 2

                + role["Risks"] * 2

                + role["Applications"]

            )

            role["Complexity Score"] = score

            if score >= 40:
                automation = "High"

            elif score >= 20:
                automation = "Medium"

            else:
                automation = "Low"

            role["Automation Potential"] = automation

            results.append(role)

        return {
    "summary": sorted(
        results,
        key=lambda x: x["Activities"],
        reverse=True
    ),
    "details": steps
}