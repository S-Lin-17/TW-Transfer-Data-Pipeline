import pandas as pd
import io

def validate_data(csv_content):
    # Parsing csv content into dataframe
    df = pd.read_csv(io.StringIO(csv_content.decode('utf-8')))

    column_names = ["Loc","Loc Zn","Loc Name","Loc Purp Desc","Loc/QTI","Flow Ind",
                    "DC","OPC","TSQ","OAC","IT","Auth Overrun Ind","Nom Cap Exceed Ind",
                    "All Qty Avail","Qty Reason"]

    # Check if all required columns are present
    if not all(column in df.columns for column in column_names):
        raise ValueError("CSV is missing one or more columns")
    
    # Check if...

    return df