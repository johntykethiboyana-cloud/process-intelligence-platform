import re


class RepositoryIndex:

    def __init__(self):

        self.index = []

    # ---------------------------------------------------------

    def extract_keywords(self, process):

        keywords = set()

        # Process Name
        process_name = process.get("process_name", "")

        words = re.findall(r"[A-Za-z0-9]+", process_name.lower())

        for word in words:

            if len(word) > 2:
                keywords.add(word)

        # Activities

        for activity in process["activities"]:

            words = re.findall(r"[A-Za-z0-9]+", activity.lower())

            for word in words:

                if len(word) > 2:
                    keywords.add(word)

        # Applications

        for app in process["applications"]:

            words = re.findall(r"[A-Za-z0-9]+", app.lower())

            for word in words:

                if len(word) > 2:
                    keywords.add(word)

        return sorted(list(keywords))

    # ---------------------------------------------------------

    def count_activity_types(self, process):

        manual = 0
        supported = 0
        automated = 0

        for activity_type in process.get("activity_types", []):

            activity_type = activity_type.lower()

            if "manual" in activity_type:
                manual += 1

            elif "supported" in activity_type:
                supported += 1

            elif "automated" in activity_type:
                automated += 1

        return manual, supported, automated

    # ---------------------------------------------------------

    def build(self, repository):

        self.index = []

        for process_name, process in repository.items():

            process["process_name"] = process_name

            manual, supported, automated = self.count_activity_types(process)

            self.index.append({

                "process": process_name,

                "l1": process.get("l1", ""),

                "l2": process.get("l2", ""),

                "l3": process.get("l3", ""),

                "owner": process.get("owner", ""),

                "applications": process.get("applications", []),

                "activities": process.get("activities", []),

                "activity_types": process.get("activity_types", []),

                "manual_count": manual,

                "supported_count": supported,

                "automated_count": automated,

                "keywords": self.extract_keywords(process)

            })

        return self.index