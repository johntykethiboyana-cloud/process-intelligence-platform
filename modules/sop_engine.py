from modules.document_reader import DocumentReader
from modules.sop_parser import SOPParser
from modules.json_exporter import JSONExporter
from modules.ai_engine import AIEngine
from modules.search_engine import SearchEngine
from modules.quality_checker import QualityChecker
from modules.process_analyzer import ProcessAnalyzer
from modules.report_generator import ReportGenerator
from modules.executive_dashboard import ExecutiveDashboard


class SOPEngine:

    def __init__(self, file_path):
        self.file_path = file_path
        self.sections = {}

    def load_document(self):
        reader = DocumentReader(self.file_path)
        details = reader.get_paragraph_details()
        parser = SOPParser(details)
        self.sections = parser.build_sections()
        JSONExporter().export(self.sections, "Output/sop.json")
        print("✓ SOP Loaded Successfully")

    def show_summary(self):
        summary = AIEngine().summarize(self.sections)

        print("\n" + "=" * 80)
        print("AI SUMMARY")
        print("=" * 80)

        for heading, info in summary.items():
            print(f"\n{heading}")
            print(f"Paragraphs : {info['paragraphs']}")
            print(f"Preview    : {info['preview']}")
        print("DEBUG: Returning summary")
        return summary

    def search(self):
        keyword = input("\nEnter keyword to search (Press Enter to skip): ").strip()

        if keyword == "":
            print("\nSearch skipped.")
            return

        results = SearchEngine().search(self.sections, keyword)

        print("\n" + "=" * 80)
        print("SEARCH RESULTS")
        print("=" * 80)

        if not results:
            print("No results found.")
            return

        for result in results:
            print("\n" + "-" * 80)
            print(result["heading"])
            print("-" * 80)

            if not result["matches"]:
                print("Keyword found in heading.")
            else:
                for line in result["matches"]:
                    print(line)

    def quality_report(self):
        quality = QualityChecker().evaluate(self.sections)

        print("\n" + "=" * 80)
        print("QUALITY REPORT")
        print("=" * 80)

        for key, value in quality.items():
            if key != "score":
                print(f"{key:<25}: {'YES' if value else 'NO'}")

        print(f"\nOverall Score : {quality['score']}/100")
        return quality

    def process_analysis(self):
        analysis = ProcessAnalyzer().analyze(self.sections)

        print("\n" + "=" * 80)
        print("PROCESS INTELLIGENCE REPORT")
        print("=" * 80)

        print("\nAPPLICATIONS")
        for app in analysis["applications"]:
            print("✓", app)

        print("\nROLES")
        for role in analysis["roles"]:
            print("✓", role)

        print("\nSTATISTICS")
        for k, v in analysis["statistics"].items():
            print(f"{k:<20}: {v}")

        print("\nSUMMARY")
        print(f"Controls Found      : {len(analysis['controls'])}")
        print(f"Risks Found         : {len(analysis['risks'])}")
        print(f"Approvals Found     : {len(analysis['approvals'])}")
        print(f"Manual Activities   : {len(analysis['manual_steps'])}")

        print("\nRECOMMENDATIONS")
        for r in analysis["recommendations"]:
            print("•", r)

        return analysis

    def executive_dashboard(self, analysis, quality):
        ExecutiveDashboard().generate(analysis, quality)

    def intelligence_scorecard(self, analysis, quality):
        ReportGenerator().generate(analysis, quality)

    def automation_report(self, analysis):
        print("\n" + "=" * 80)
        print("AUTOMATION OPPORTUNITIES")
        print("=" * 80)

        opportunities = analysis["automation_opportunities"]

        if not opportunities:
            print("No automation opportunities found.")
            return

        for i, item in enumerate(opportunities, start=1):
            print(f"\nAutomation Opportunity #{i}")
            print("-" * 80)
            print(f"Section                 : {item['section']}")
            print(f"Manual Steps            : {item['manual_steps']}")
            print(f"Suggested Technology    : {item['solution']}")
            print(f"Estimated Saving        : {item['estimated_saving']}")
            print(f"Business Impact         : {item['business_impact']}")
            print(f"Automation Readiness    : {item['automation_readiness']}")
            print(f"Priority                : {item['priority']}")
            print("\nActivities")
            for act in item["activities"]:
                print(f"  • {act}")

    def get_dashboard(self):

        # Load SOP
        self.load_document()

        # Generate Summary
        summary = AIEngine().summarize(self.sections)

        # Quality Report
        quality = QualityChecker().evaluate(self.sections)

        # Process Analysis
        analysis = ProcessAnalyzer().analyze(self.sections)

        return {
            "summary": summary,
            "quality": quality,
            "analysis": analysis
        }

    def run(self):

        self.load_document()

        self.show_summary()

        self.search()

        quality = self.quality_report()

        analysis = self.process_analysis()

        self.executive_dashboard(analysis, quality)

        self.intelligence_scorecard(analysis, quality)

        self.automation_report(analysis)

        print("\n" + "=" * 80)
        print("PROCESS COMPLETED".center(80))
        print("=" * 80)