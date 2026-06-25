import os

from comparison.excel_reader import ExcelReader
from comparison.l4_parser import L4Parser
from comparison.repository_index import RepositoryIndex
from comparison.repository_cleaner import RepositoryCleaner
from comparison.keyword_extractor import KeywordExtractor
from comparison.intelligent_matcher import IntelligentMatcher

from modules.document_reader import DocumentReader
from modules.sop_parser import SOPParser
from modules.activity_extractor import ActivityExtractor


# ============================================================
# LOAD REPOSITORY
# ============================================================

print("=" * 80)
print("LOADING REPOSITORY")
print("=" * 80)

reader = ExcelReader("L4_Repository/Act_Info.xlsx")

df = reader.load_excel()

parser = L4Parser(df)

repository = parser.build_repository()

index = RepositoryIndex()

knowledge = index.build(repository)

cleaner = RepositoryCleaner()

knowledge = cleaner.clean_repository(knowledge)

print(f"Processes Loaded : {len(knowledge)}")


# ============================================================
# LOAD SOP
# ============================================================

files = [

    f

    for f in os.listdir("SOPs")

    if f.lower().endswith(".docx")

]

print("\n")
print("=" * 80)
print("AVAILABLE SOP FILES")
print("=" * 80)

for i, file in enumerate(files, start=1):

    print(f"{i}. {file}")

choice = int(input("\nSelect SOP Number : "))

selected = files[choice - 1]

print(f"\nLoading SOP : {selected}")

reader = DocumentReader(

    os.path.join(

        "SOPs",

        selected

    )

)

details = reader.get_paragraph_details()

sections = SOPParser(details).build_sections()

extractor = ActivityExtractor()

items = extractor.extract(sections)


# ============================================================
# KEYWORDS
# ============================================================

keyword_engine = KeywordExtractor()

keywords = keyword_engine.extract(items)


# ============================================================
# ACTIVITIES
# ============================================================

activities = [

    item["text"]

    for item in items

    if item["type"] in [

        "ACTIVITY",
        "COMMUNICATION",
        "APPROVAL",
        "VALIDATION"

    ]

]


# ============================================================
# MATCH
# ============================================================

matcher = IntelligentMatcher()

results = matcher.match(

    sop_title=selected,

    sop_keywords=keywords["business"],

    sop_apps=keywords["systems"],

    sop_activities=activities,

    repository_index=knowledge

)


# ============================================================
# REPORT
# ============================================================

print("\n")
print("=" * 110)
print("TOP 10 INTELLIGENT MATCHES")
print("=" * 110)

for i, item in enumerate(results, start=1):

    print(f"\n{i}. {item['process']}")

    print(f"Overall Score      : {item['score']}")

    print(f"Keyword Score      : {item['keyword_score']}")

    print(f"Application Score  : {item['application_score']}")

    print(f"Activity Score     : {item['activity_score']}")

    print(f"Process Name Score : {item['process_score']}")