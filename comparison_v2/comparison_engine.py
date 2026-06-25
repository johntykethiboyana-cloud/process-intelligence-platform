from comparison_v2.intelligent_matcher import IntelligentMatcher


class ComparisonEngine:

    """
    Comparison Engine V2
    Compatible with the new IntelligentMatcher.
    """

    def __init__(self):
        self.matcher = IntelligentMatcher()

    # ---------------------------------------------------------

    def _safe_step_text(self, step):
        if isinstance(step, dict):
            return (
                step.get("activity")
                or step.get("clean_text")
                or step.get("text")
                or step.get("original_text")
                or ""
            )
        return str(step)

    # ---------------------------------------------------------

    def compare(self, l4_data, sop_data):

        result = {}

        # Process Name
        result["process_name"] = self.matcher.match_text(
            l4_data.get("process_name", ""),
            sop_data.get("process_name", "")
        )

        # Simple list comparisons
        for key in [
            "activities",
            "roles",
            "applications",
            "controls",
            "risks",
            "inputs",
            "outputs"
        ]:
            result[key] = self.matcher.match_lists(
                l4_data.get(key, []),
                sop_data.get(key, [])
            )

        # Step comparison
        l4_steps = [
            self._safe_step_text(s)
            for s in l4_data.get("steps", [])
        ]

        sop_steps = [
            self._safe_step_text(s)
            for s in sop_data.get("steps", [])
        ]

        result["steps"] = self.matcher.match_lists(
            l4_steps,
            sop_steps
        )

        result["sequence"] = self.matcher.match_sequence(
            l4_steps,
            sop_steps
        )

        # Weighted overall score
        weights = {
            "process_name":0.10,
            "activities":0.20,
            "roles":0.05,
            "applications":0.10,
            "controls":0.05,
            "risks":0.05,
            "inputs":0.05,
            "outputs":0.05,
            "steps":0.25,
            "sequence":0.10
        }

        overall = 0
        for k,w in weights.items():
            overall += result[k]["percentage"] * w

        result["overall"] = round(overall,2)

        return result
