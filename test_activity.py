import os

from modules.document_reader import DocumentReader
from modules.sop_parser import SOPParser
from modules.activity_extractor import ActivityExtractor


# --------------------------------------------------------
# Find all SOP files
# --------------------------------------------------------

sop_folder = "SOPs"

files = [

    file for file in os.listdir(sop_folder)

    if file.lower().endswith(".docx")

]

if len(files) == 0:

    print("No SOP files found in SOPs folder.")

    exit()

# --------------------------------------------------------
# If only one SOP exists, load automatically
# --------------------------------------------------------

if len(files) == 1:

    selected_file = files[0]

else:

    print("\n")
    print("=" * 70)
    print("AVAILABLE SOP FILES")
    print("=" * 70)

    for index, file in enumerate(files, start=1):

        print(f"{index}. {file}")

    choice = int(input("\nSelect SOP Number : "))

    selected_file = files[choice - 1]

# --------------------------------------------------------

print(f"\nLoading SOP : {selected_file}")

reader = DocumentReader(os.path.join(sop_folder, selected_file))

details = reader.get_paragraph_details()

parser = SOPParser(details)

sections = parser.build_sections()

extractor = ActivityExtractor()

activities = extractor.extract(sections)

print("\n")
print("=" * 70)
print("SOP ACTIVITIES")
print("=" * 70)

print(f"Activities Found : {len(activities)}")

print("\n")

for index, activity in enumerate(activities, start=1):

    print(f"{index}. [{activity['type']}] {activity['text']}")