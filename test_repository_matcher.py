import os
import json
from datetime import datetime

from comparison.excel_reader import ExcelReader
from comparison.l4_parser import L4Parser
from comparison.repository_matcher import RepositoryMatcher

from intelligence.ai_reasoner import AIReasoner

from modules.document_reader import DocumentReader
from modules.sop_parser import SOPParser
from modules.activity_extractor import ActivityExtractor


# ==========================================================
# SETTINGS
# ==========================================================

L4_FILE = "L4_Repository/Act_Info.xlsx"
SOP_FOLDER = "SOPs"
OUTPUT_FOLDER = "Output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# ==========================================================
# LOAD L4 REPOSITORY
# ==========================================================

print("\n" + "=" * 80)
print("LOADING L4 REPOSITORY")
print("=" * 80)

try:

    reader = ExcelReader(L4_FILE)
    df = reader.load_excel()

    parser = L4Parser(df)
    repository = parser.build_repository()

    print(f"✓ Processes Loaded : {parser.repository_size()}")

except Exception as e:

    print("\nError loading repository")
    print(e)
    exit()


# ==========================================================
# LIST SOP FILES
# ==========================================================

print("\n" + "=" * 80)
print("AVAILABLE SOP FILES")
print("=" * 80)

files = sorted(

    [

        f

        for f in os.listdir(SOP_FOLDER)

        if f.lower().endswith(".docx")

    ]

)

if not files:

    print("No SOP files found.")
    exit()

if len(files) == 1:

    selected = files[0]

else:

    for index, file in enumerate(files, start=1):

        print(f"{index}. {file}")

    while True:

        try:

            choice = int(input("\nSelect SOP Number : "))

            if 1 <= choice <= len(files):

                selected = files[choice - 1]
                break

        except:

            pass

        print("Invalid selection.")


print(f"\nLoading SOP : {selected}")


# ==========================================================
# LOAD SOP
# ==========================================================

reader = DocumentReader(

    os.path.join(

        SOP_FOLDER,

        selected

    )

)

paragraph_details = reader.get_paragraph_details()

sections = SOPParser(

    paragraph_details

).build_sections()


# ==========================================================
# EXTRACT ACTIVITIES
# ==========================================================

extractor = ActivityExtractor()

sop_items = extractor.extract(

    sections

)

print("\n" + "=" * 80)
print("SOP SUMMARY")
print("=" * 80)

print(f"Activities Extracted : {len(sop_items)}")

print("\nSample Activities\n")

for index, item in enumerate(sop_items[:15], start=1):

    print(f"{index:>2}. [{item['type']}] {item['text']}")


# ==========================================================
# MATCH REPOSITORY
# ==========================================================

print("\nSearching repository...")

matcher = RepositoryMatcher()

results = matcher.find_best_matches(

    sop_items,

    repository

)


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

print("\n" + "=" * 80)
print("TOP 10 BEST MATCHING L4 PROCESSES")
print("=" * 80)

for index, item in enumerate(results, start=1):

    print(

        f"{index:>2}. "

        f"{item['process']:<70}"

        f"{item['score']:>6}%"

    )


# ==========================================================
# BEST MATCH
# ==========================================================

best = results[0]

print("\n" + "=" * 80)
print("BEST MATCH")
print("=" * 80)

print(f"Process : {best['process']}")
print(f"Score   : {best['score']}%")


# ==========================================================
# AI REASONING
# ==========================================================

print("\n" + "=" * 80)
print("AI PROCESS REASONING")
print("=" * 80)

reasoner = AIReasoner()

best_process = repository[best["process"]]

report = reasoner.analyze(

    best_process,

    best

)

reasoner.print_report(

    report

)


# ==========================================================
# SAVE RESULTS
# ==========================================================

timestamp = datetime.now().strftime(

    "%Y%m%d_%H%M%S"

)

json_file = os.path.join(

    OUTPUT_FOLDER,

    f"Match_{timestamp}.json"

)

with open(

    json_file,

    "w",

    encoding="utf-8"

) as f:

    json.dump(

        results,

        f,

        indent=4,

        ensure_ascii=False

    )

print(f"\nJSON Saved : {json_file}")

try:

    import pandas as pd

    df = pd.DataFrame(results)

    csv_file = os.path.join(

        OUTPUT_FOLDER,

        f"Match_{timestamp}.csv"

    )

    df.to_csv(

        csv_file,

        index=False

    )

    print(f"CSV Saved  : {csv_file}")

except Exception:

    pass


# ==========================================================
# COMPLETE
# ==========================================================

print("\n" + "=" * 80)
print("PROCESS COMPLETED")
print("=" * 80)