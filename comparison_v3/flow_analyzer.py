from comparison_v3.utils import Utils


class FlowAnalyzer:
    """
    Flow Analyzer

    Identifies:
    - Happy Flow
    - Unhappy Flow
    - Automation Opportunities
    """

    def __init__(self):

        self.exception_keywords = [
            "if",
            "else",
            "except",
            "exception",
            "error",
            "fail",
            "failed",
            "reject",
            "rejected",
            "return",
            "retry",
            "missing",
            "invalid",
            "cancel",
            "escalate",
            "not approved",
            "unable",
            "stop"
        ]

        self.manual_keywords = [
            "review",
            "check",
            "verify",
            "validate",
            "compare",
            "analyse",
            "analyze",
            "approve",
            "confirm",
            "email",
            "send",
            "copy",
            "update",
            "enter",
            "create",
            "download",
            "upload"
        ]

    # --------------------------------------------------------
    # HAPPY FLOW
    # --------------------------------------------------------

    def happy_flow(self, steps):

        happy = []

        for i, step in enumerate(steps, start=1):

            if isinstance(step, dict):

                activity = (
                    step.get("activity")
                    or step.get("step")
                    or step.get("name")
                    or ""
                )

            else:

                activity = str(step)

            happy.append({

                "step": i,

                "activity": activity

            })

        return happy

    # --------------------------------------------------------
    # UNHAPPY FLOW
    # --------------------------------------------------------

    def unhappy_flow(self, steps):

        unhappy = []

        for i, step in enumerate(steps, start=1):

            if isinstance(step, dict):

                activity = (
                    step.get("activity")
                    or step.get("step")
                    or step.get("name")
                    or ""
                )

            else:

                activity = str(step)

            text = activity.lower()

            for keyword in self.exception_keywords:

                if keyword in text:

                    unhappy.append({

                        "step": i,

                        "trigger": keyword,

                        "activity": activity

                    })

                    break

        return unhappy

    # --------------------------------------------------------
    # AUTOMATION IDEAS
    # --------------------------------------------------------

    def automation(self, steps):

        ideas = []

        for i, step in enumerate(steps, start=1):

            if isinstance(step, dict):

                activity = (
                    step.get("activity")
                    or step.get("step")
                    or step.get("name")
                    or ""
                )

            else:

                activity = str(step)

            text = activity.lower()

            score = 0

            reason = []

            for keyword in self.manual_keywords:

                if keyword in text:

                    score += 15

                    reason.append(keyword)

            score = min(score, 100)

            if score >= 75:

                priority = "High"

            elif score >= 45:

                priority = "Medium"

            else:

                priority = "Low"

            ideas.append({

                "step": i,

                "activity": activity,

                "automation_score": score,

                "priority": priority,

                "reason": ", ".join(reason)

            })

        return ideas

    # --------------------------------------------------------
    # COMPLETE ANALYSIS
    # --------------------------------------------------------

    def analyze(self, steps):

        steps = Utils.remove_empty(steps)

        return {

            "happy_flow": self.happy_flow(steps),

            "unhappy_flow": self.unhappy_flow(steps),

            "automation": self.automation(steps)

        }