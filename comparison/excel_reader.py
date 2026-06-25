import pandas as pd


class ExcelReader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_excel(self):

        self.df = pd.read_excel(self.file_path)

        return self.df

    def repository_summary(self):

        print("\n")
        print("=" * 70)
        print("ARIS REPOSITORY SUMMARY")
        print("=" * 70)

        print(f"Total Rows              : {len(self.df)}")
        print(f"Total L4 Models         : {self.df['L4 Model Name'].nunique()}")
        print(f"Total Activities        : {self.df['Activity'].count()}")

        print(f"Manual Activities       : {len(self.df[self.df['Type of Activity'] == 'Manual Activity'])}")

        print(f"Supported Activities    : {len(self.df[self.df['Type of Activity'] == 'Supported Activity'])}")

        print(f"Automated Activities    : {len(self.df[self.df['Type of Activity'] == 'Automated Activity'])}")

        print(f"Applications            : {self.df['Application'].nunique()}")

        print("=" * 70)