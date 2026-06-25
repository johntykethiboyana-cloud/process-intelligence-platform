import json
import re


class RepositoryVocabulary:

    def __init__(self):

        self.vocabulary = {

            "applications": set(),

            "l1": set(),

            "l2": set(),

            "l3": set(),

            "owners": set(),

            "activity_types": set(),

            "keywords": set()

        }

    # ------------------------------------------------------------

    def clean(self, value):

        if value is None:
            return ""

        value = str(value).strip()

        return value

    # ------------------------------------------------------------

    def add_keywords(self, text):

        words = re.findall(r"[A-Za-z0-9]+", text.lower())

        for word in words:

            if len(word) >= 3:

                self.vocabulary["keywords"].add(word)

    # ------------------------------------------------------------

    def build(self, dataframe):

        for _, row in dataframe.iterrows():

            # ---------- L1 ----------

            l1 = self.clean(row.get("L1"))

            if l1:
                self.vocabulary["l1"].add(l1)

            # ---------- L2 ----------

            l2 = self.clean(row.get("L2"))

            if l2:
                self.vocabulary["l2"].add(l2)

            # ---------- L3 ----------

            l3 = self.clean(row.get("L3"))

            if l3:
                self.vocabulary["l3"].add(l3)

            # ---------- Owner ----------

            owner = self.clean(row.get("FPO"))

            if owner:
                self.vocabulary["owners"].add(owner)

            # ---------- Activity Type ----------

            activity_type = self.clean(row.get("Type of Activity"))

            if activity_type:
                self.vocabulary["activity_types"].add(activity_type)

            # ---------- Application ----------

            application = self.clean(row.get("Application"))

            if application:
                self.vocabulary["applications"].add(application)

            # ---------- Keywords ----------

            self.add_keywords(l1)

            self.add_keywords(l2)

            self.add_keywords(l3)

            self.add_keywords(application)

            self.add_keywords(owner)

            self.add_keywords(activity_type)

            activity = self.clean(row.get("Activity"))

            self.add_keywords(activity)

            process = self.clean(row.get("L4 Model Name"))

            self.add_keywords(process)

        # Convert sets to sorted lists

        for key in self.vocabulary:

            self.vocabulary[key] = sorted(

                list(

                    self.vocabulary[key]

                )

            )

        return self.vocabulary

    # ------------------------------------------------------------

    def save(self, filepath):

        with open(

            filepath,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.vocabulary,

                file,

                indent=4,

                ensure_ascii=False

            )