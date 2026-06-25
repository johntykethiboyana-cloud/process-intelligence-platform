import os

from comparison_v2.document_extractor import DocumentExtractor
from comparison_v2.comparison_engine import ComparisonEngine


# ==========================================================
# SELECT FILE
# ==========================================================

def select_file(folder, title):

    print("\n")
    print("=" * 80)
    print(title)
    print("=" * 80)

    files = [

        f

        for f in os.listdir(folder)

        if f.lower().endswith(".docx")

    ]

    if not files:

        print(f"No DOCX files found in {folder}")

        return None

    for i, file in enumerate(files, start=1):

        print(f"{i}. {file}")

    while True:

        try:

            choice = int(input("\nSelect Number : "))

            if 1 <= choice <= len(files):

                return os.path.join(folder, files[choice - 1])

        except:

            pass

        print("Invalid Selection")
# ==========================================================
# MAIN
# ==========================================================

def main():

    print("\n")
    print("=" * 80)
    print("L4 vs SOP COMPARISON ENGINE V2")
    print("=" * 80)

    l4_file = select_file(

        "L4",

        "AVAILABLE L4 FILES"

    )

    if l4_file is None:

        return

    sop_file = select_file(

        "SOPs",

        "AVAILABLE SOP FILES"

    )

    if sop_file is None:

        return

    print("\nLoading Documents...")

    extractor = DocumentExtractor()

    l4_data = extractor.extract(

        l4_file

    )

    sop_data = extractor.extract(

        sop_file

    )

    print("Documents Parsed Successfully")

    print("\nRunning Comparison...")

    engine = ComparisonEngine()

    result = engine.compare(

        l4_data,

        sop_data

    )

    print("\n")
    print("=" * 80)
    print("COMPARISON REPORT")
    print("=" * 80)

    print(f"Overall Match        : {result['overall']}%")
    print(f"Process Name         : {result['process_name']['percentage']}%")
    print(f"Activities           : {result['activities']['percentage']}%")
    print(f"Roles                : {result['roles']['percentage']}%")
    print(f"Applications         : {result['applications']['percentage']}%")
    print(f"Controls             : {result['controls']['percentage']}%")
    print(f"Risks                : {result['risks']['percentage']}%")
    print(f"Inputs               : {result['inputs']['percentage']}%")
    print(f"Outputs              : {result['outputs']['percentage']}%")
    print(f"Steps                : {result['steps']['percentage']}%")
    print(f"Sequence             : {result['sequence']['percentage']}%")

    print("\n")
    print("=" * 80)
    print("MATCHED STEPS")
    print("=" * 80)

    for item in result["steps"]["matched"]:

        print(f"\nL4  : {item['l4']}")
        print(f"SOP : {item['sop']}")
        print(f"Score : {item['score']}%")

    print("\n")
    print("=" * 80)
    print("MISSING L4 STEPS")
    print("=" * 80)

    for item in result["steps"]["missing"]:

        print(f"- {item}")

    print("\n")
    print("=" * 80)
    print("EXTRA SOP STEPS")
    print("=" * 80)

    for item in result["steps"]["extra"]:

        print(f"- {item}")

    print("\n")
    print("=" * 80)
    print("COMPARISON COMPLETED")
    print("=" * 80)


if __name__ == "__main__":

    main()