import json
import re
from collections import Counter


class RepositoryDiscovery:

    def __init__(self, repository_file="Output/repository_vocabulary.json"):
        with open(repository_file, "r", encoding="utf-8") as f:
            self.repository = json.load(f)

    def extract_keywords(self, sections):

        text = []

        for content in sections.values():
            for line in content:
                words = re.findall(r"[A-Za-z0-9]+", line.lower())
                text.extend(words)

        return Counter(text)

    def compare(self, sections):

        sop_words = self.extract_keywords(sections)

        scores = {}

        for category, values in self.repository.items():

            score = 0

            for value in values:

                words = re.findall(r"[A-Za-z0-9]+", value.lower())

                for word in words:

                    score += sop_words.get(word, 0)

            scores[category] = score

        return sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )