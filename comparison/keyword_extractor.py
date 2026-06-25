import re


class KeywordExtractor:

    def __init__(self):

        self.system_keywords = {

            "findur",
            "trax",
            "citrix",
            "sharepoint",
            "swift",
            "fasweb",
            "sap",
            "excel",
            "outlook",
            "servicenow",
            "aris",
            "fin"
        }

        self.business_keywords = {

            "treasury",
            "bank",
            "account",
            "nostro",
            "vostro",
            "ssi",
            "cash",
            "settlement",
            "payment",
            "approval",
            "counterparty",
            "business",
            "legal",
            "entity",
            "whitelisting",
            "cms"
        }

    # ------------------------------------------------------

    def extract(self, sop_items):

        systems = set()

        business = set()

        for item in sop_items:

            text = item["text"].lower()

            words = re.findall(r"[a-zA-Z0-9]+", text)

            for word in words:

                if word in self.system_keywords:

                    systems.add(word.upper())

                if word in self.business_keywords:

                    business.add(word.capitalize())

        return {

            "systems": sorted(list(systems)),

            "business": sorted(list(business))

        }