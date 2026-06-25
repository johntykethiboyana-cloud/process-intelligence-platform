class SearchEngine:

    def search(self, sections, keyword):

        keyword = keyword.lower()

        results = []

        for heading, content in sections.items():

            heading_found = keyword in heading.lower()

            matched_lines = []

            for line in content:

                if keyword in line.lower():
                    matched_lines.append(line)

            if heading_found or matched_lines:

                results.append({
                    "heading": heading,
                    "matches": matched_lines
                })

        return results