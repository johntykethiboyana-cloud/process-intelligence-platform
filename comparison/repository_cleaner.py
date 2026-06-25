import re


class RepositoryCleaner:

    def __init__(self):

        # Common English words to ignore
        self.stop_words = {

            "the", "and", "for", "from", "into", "with", "without",
            "using", "used", "use", "user", "users",
            "this", "that", "these", "those",
            "process", "processing",
            "create", "creating",
            "update", "updating",
            "delete", "deleting",
            "check", "checking",
            "review", "reviewing",
            "approve", "approval",
            "validate", "validation",
            "generate", "generated",
            "copy", "copied",
            "click", "select", "enter",
            "open", "close",
            "new", "old",
            "required", "request",
            "information", "details",
            "activity", "activities",
            "step", "steps",
            "perform", "performed",
            "based", "type",
            "management", "manage",
            "system", "systems",
            "support", "supported",
            "manual", "automated",
            "as", "is", "to", "of", "on",
            "in", "by", "or", "be", "an",
            "a", "at", "it", "if"
        }

    # -----------------------------------------------------

    def clean_keywords(self, keywords):

        cleaned = set()

        for word in keywords:

            word = word.lower().strip()

            # Remove punctuation
            word = re.sub(r"[^a-zA-Z0-9]", "", word)

            if len(word) < 3:
                continue

            if word in self.stop_words:
                continue

            cleaned.add(word)

        return sorted(cleaned)

    # -----------------------------------------------------

    def clean_repository(self, repository_index):

        for process in repository_index:

            process["keywords"] = self.clean_keywords(
                process["keywords"]
            )

        return repository_index