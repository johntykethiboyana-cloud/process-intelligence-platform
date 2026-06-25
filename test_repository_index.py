from comparison.excel_reader import ExcelReader
from comparison.l4_parser import L4Parser
from comparison.repository_index import RepositoryIndex

print("=" * 80)
print("BUILDING REPOSITORY INDEX")
print("=" * 80)

reader = ExcelReader("L4_Repository/Act_Info.xlsx")

df = reader.load_excel()

parser = L4Parser(df)

repository = parser.build_repository()

index = RepositoryIndex()

knowledge = index.build(repository)

print(f"\nProcesses Indexed : {len(knowledge)}")

print("\n")

print("=" * 80)
print("FIRST PROCESS")
print("=" * 80)

first = knowledge[0]

print("\nProcess")

print(first["process"])

print("\nApplications")

for app in first["applications"]:

    print("•", app)

print("\nFirst 25 Keywords")

for word in first["keywords"][:25]:

    print("•", word)