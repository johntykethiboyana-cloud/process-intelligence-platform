from comparison.excel_reader import ExcelReader
from comparison.l4_parser import L4Parser


reader = ExcelReader("L4_Repository/Act_Info.xlsx")

df = reader.load_excel()

parser = L4Parser(df)

parser.build_repository()

print("\n")
print("=" * 70)
print("ARIS PROCESS SEARCH")
print("=" * 70)

keyword = input("Search Process : ")

matches = parser.search_process(keyword)

if len(matches) == 0:

    print("\nNo matching process found.")

else:

    print(f"\nFound {len(matches)} matching processes\n")

    for i, process in enumerate(matches, start=1):

        print(f"{i}. {process}")

    choice = int(input("\nSelect Process Number : "))

    process_name = matches[choice - 1]

    process = parser.get_process(process_name)

    print("\n")
    print("=" * 70)
    print(process_name)
    print("=" * 70)

    print(f"Owner                 : {process['owner']}")
    print(f"Activities            : {len(process['activities'])}")
    print(f"Applications          : {len(process['applications'])}")
    print(f"Manual Activities     : {process['manual']}")
    print(f"Supported Activities  : {process['supported']}")
    print(f"Automated Activities  : {process['automated']}")

    print("\nAPPLICATIONS")
    print("-" * 70)

    for app in process["applications"]:
        print("•", app)

    print("\nACTIVITIES")
    print("-" * 70)

    for i, activity in enumerate(process["activities"], start=1):
        print(f"{i}. {activity}")