import pandas as pd

def export_to_files(records, csv_path="output.csv", xlsx_path="output.xlsx"):
    if not records:
        return
    df = pd.DataFrame(records)
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)
