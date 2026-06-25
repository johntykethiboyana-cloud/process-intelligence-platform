import os

from modules.document_reader import DocumentReader
from modules.sop_parser import SOPParser
from modules.activity_extractor import ActivityExtractor

from comparison.keyword_extractor import KeywordExtractor


files = [

    f

    for f in os.listdir("SOPs")

    if f.lower().endswith(".docx")

]

reader = DocumentReader(

    os.path.join(

        "SOPs",

        files[0]

    )

)

details = reader.get_paragraph_details()

sections = SOPParser(details).build_sections()

activities = ActivityExtractor().extract(sections)

keywords = KeywordExtractor().extract(activities)

print("\n")
print("=" * 70)
print("SOP KEYWORDS")
print("=" * 70)

print("\nSYSTEMS")

for item in keywords["systems"]:

    print("•", item)

print("\nBUSINESS TERMS")

for item in keywords["business"]:

    print("•", item)