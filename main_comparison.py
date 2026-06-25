import os

from comparison.excel_reader import ExcelReader
from comparison.l4_parser import L4Parser
from comparison.comparison_engine import ComparisonEngine

from modules.document_reader import DocumentReader
from modules.sop_parser import SOPParser
from modules.activity_extractor import ActivityExtractor


# ==========================================================
# LOAD L4 REPOSITORY
# ==========================================================

print("\n")
print("=" * 80)
print("LOADING L4 REPOSITORY")
print("=" * 80)

reader = ExcelReader("L4_Repository/Act_Info.xlsx")

df = reader.load_excel()

parser = L4Parser(df)

parser.build_repository()

print(f"Processes Loaded : {parser.repository_size()}")

# ==========================================================
# SEARCH PROCESS
# ==========================================================

print("\n")
print("=" * 80)
print("SEARCH L4 PROCESS")
print("=" * 80)

keyword = input("Search Process : ")

matches = parser.search_process(keyword)

if len(matches) == 0:

    print("\nNo matching process found.")

    exit()

print("\n")

for index, process in enumerate(matches, start=1):

    print(f"{index}. {process}")

choice = int(input("\nSelect Process Number : "))

selected_process = parser.get_process(matches[choice - 1])

print("\nSelected Process :")
print(matches[choice - 1])

# ==========================================================
# LOAD SOP
# ==========================================================

print("\n")
print("=" * 80)
print("AVAILABLE SOP FILES")
print("=" * 80)

files = [

    file

    for file in os.listdir("SOPs")

    if file.lower().endswith(".docx")

]

if len(files) == 0:

    print("No SOP files found.")

    exit()

for index, file in enumerate(files, start=1):

    print(f"{index}. {file}")

choice = int(input("\nSelect SOP Number : "))

selected_sop = files[choice - 1]

print(f"\nLoading SOP : {selected_sop}")

# ==========================================================
# EXTRACT SOP ACTIVITIES
# ==========================================================

doc = DocumentReader(

    os.path.join(

        "SOPs",

        selected_sop

    )

)

details = doc.get_paragraph_details()

sections = SOPParser(details).build_sections()

extractor = ActivityExtractor()

sop_items = extractor.extract(sections)

# ==========================================================
# COMPARE
# ==========================================================

engine = ComparisonEngine()

result = engine.compare(

    selected_process,

    sop_items

)

# ==========================================================
# REPORT
# ==========================================================

print("\n")
print("=" * 80)
print("PROCESS GOVERNANCE REPORT")
print("=" * 80)

print(f"Coverage                : {result['coverage']}%")

print(f"Matched Activities      : {len(result['matched'])}")

print(f"Missing Activities      : {len(result['missing'])}")

print(f"Extra SOP Activities    : {len(result['extra'])}")

print("\n")

print("=" * 80)
print("MATCHED ACTIVITIES")
print("=" * 80)

for item in result["matched"]:

    print(f"\nL4  : {item['l4']}")

    print(f"SOP : {item['sop']}")

    print(f"Match Score : {item['score']}%")

print("\n")
print("=" * 80)
print("MISSING L4 ACTIVITIES")
print("=" * 80)

for item in result["missing"]:

    print("•", item)

print("\n")
print("=" * 80)
print("EXTRA SOP ACTIVITIES")
print("=" * 80)

for item in result["extra"]:

    print("•", item)

print("\n")
print("=" * 80)
print("COMPARISON COMPLETED")
print("=" * 80)