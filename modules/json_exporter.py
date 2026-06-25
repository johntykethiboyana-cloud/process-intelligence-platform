import json

class JSONExporter:

    def export(self, sections, output_file):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sections, f, indent=4, ensure_ascii=False)

        print(f"JSON exported to {output_file}")