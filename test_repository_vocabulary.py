from comparison.excel_reader import ExcelReader
from comparison.repository_vocabulary import RepositoryVocabulary

print("=" * 80)
print("BUILDING ENTERPRISE VOCABULARY")
print("=" * 80)

reader = ExcelReader("L4_Repository/Act_Info.xlsx")

df = reader.load_excel()

builder = RepositoryVocabulary()

vocabulary = builder.build(df)

builder.save("Output/repository_vocabulary.json")

print()

print("Applications   :", len(vocabulary["applications"]))
print("L1             :", len(vocabulary["l1"]))
print("L2             :", len(vocabulary["l2"]))
print("L3             :", len(vocabulary["l3"]))
print("Owners         :", len(vocabulary["owners"]))
print("Activity Types :", len(vocabulary["activity_types"]))
print("Keywords       :", len(vocabulary["keywords"]))

print("\nSample Applications")

for app in vocabulary["applications"][:15]:
    print("•", app)

print("\nSample Keywords")

for word in vocabulary["keywords"][:30]:
    print("•", word)