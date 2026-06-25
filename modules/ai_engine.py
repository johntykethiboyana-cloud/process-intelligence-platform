class AIEngine:

    def summarize(self, sections):

        summary = {}

        for heading, content in sections.items():

            if len(content) == 0:
                continue

            summary[heading] = {
                "paragraphs": len(content),
                "preview": content[0][:200]
            }

        return summary