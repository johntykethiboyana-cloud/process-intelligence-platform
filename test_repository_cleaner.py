from comparison.excel_reader import ExcelReader
from comparison.l4_parser import L4Parser
from comparison.repository_index import RepositoryIndex
from comparison.repository_cleaner import RepositoryCleaner

reader = ExcelReader("L4_Repository/Act_Info.xlsx")

df = reader.load_excel()

parser = L4Parser(df)

repository = parser.build_repository()

index = RepositoryIndex()

knowledge = index.build(repository)

cleaner = RepositoryCleaner()

knowledge = cleaner.clean_repository(knowledge)

print("=" * 80)
print("FIRST PROCESS")
print("=" * 80)

first = knowledge[0]

print("\nProcess")
print(first["process"])

print("\nClean Keywords")

for word in first["keywords"][:30]:
    print("•", word)