class AIReasoner:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def confidence(self, score):

        if score >= 80:
            return "VERY HIGH"

        if score >= 60:
            return "HIGH"

        if score >= 40:
            return "MEDIUM"

        if score >= 20:
            return "LOW"

        return "VERY LOW"

    # ---------------------------------------------------------

    def detect_keywords(self, process):

        keywords = []

        text = (
            process["process_name"] + " " +
            " ".join(process["activities"])
        ).lower()

        mapping = {

            "bank": "Bank Account activities detected",

            "treasury": "Treasury process detected",

            "findur": "FINDUR detected",

            "approval": "Approval workflow detected",

            "approve": "Approval workflow detected",

            "request": "Request workflow detected",

            "master": "Master Data process detected",

            "customer": "Customer related activities",

            "vendor": "Vendor Management",

            "payment": "Payment process",

            "invoice": "Invoice process"

        }

        for word, sentence in mapping.items():

            if word in text:

                keywords.append(sentence)

        return sorted(set(keywords))

    # ---------------------------------------------------------

    def analyze(self, repository_process, match):

        return {

            "process":

                repository_process["process_name"],

            "score":

                match["score"],

            "confidence":

                self.confidence(match["score"]),

            "applications":

                repository_process["applications"],

            "l1":

                repository_process["l1"],

            "l2":

                repository_process["l2"],

            "l3":

                repository_process["l3"],

            "owner":

                repository_process["owner"],

            "reason":

                self.detect_keywords(repository_process)

        }

    # ---------------------------------------------------------

    def print_report(self, report):

        print()

        print("=" * 80)
        print("AI PROCESS REASONING")
        print("=" * 80)

        print()

        print("Best Match")
        print(report["process"])

        print()

        print("Confidence")
        print(report["confidence"])

        print()

        print("Repository Score")
        print(report["score"])

        print()

        print("Business Hierarchy")

        print("L1 :", report["l1"])
        print("L2 :", report["l2"])
        print("L3 :", report["l3"])

        print()

        print("Applications")

        for app in report["applications"]:
            print("✓", app)

        print()

        print("Reason")

        for r in report["reason"]:
            print("✓", r)

        print()

        print("Owner")

        print(report["owner"])