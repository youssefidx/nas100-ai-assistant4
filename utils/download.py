import base64
import pandas as pd

def get_table_download_link(df: pd.DataFrame, filename="trade_log.csv"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download Trade Log as CSV</a>'
    return href
