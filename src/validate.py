import pandas as pd
import io
from datetime import datetime

def validate_data(csv_content, cycle_date):
    # Parsing csv content into dataframe
    df = pd.read_csv(io.StringIO(csv_content.decode('utf-8')))

    errors = []
    error_file_path = "data/validation_errors_{}.txt".format(datetime.today().strftime('%Y-%m-%d_%H-%M-%S'))
    expected_col_types = {
        "Loc": "int64",
        "Loc Zn": "object", # String
        "Loc Name": "object",
        "Loc Purp Desc": "object",
        "Loc/QTI": "object",
        "Flow Ind": "object",
        "DC": "float64",    # For some reason, it's considered as float64 instead of int64
        "OPC": "int64",
        "TSQ": "int64",
        "OAC": "int64",
        "IT": "object",
        "Auth Overrun Ind": "object",
        "Nom Cap Exceed Ind": "object",
        "All Qty Avail": "object",
        "Qty Reason": "object"
    }

    # Check if all required columns are present
    missing_columns = [col for col in expected_col_types.keys() if col not in df.columns]
    if missing_columns:
        errors.append(f"CSV is missing one or more columns: {missing_columns}")
    
    # Check if columns are in expected order
    if list(df.columns) != list(expected_col_types.keys()):
        errors.append("Columns are not in the expected order")
    
    # Validate column data type
    for column, expected_dtype in expected_col_types.items():
        if df[column].dtype != expected_dtype:
            errors.append(f"Column '{column}' has incorrect data type. Expected {expected_dtype}, got {df[column].dtype}")

    # If there are errors in column presence, order, or data types, raise them immediately
    if errors:
        with open(error_file_path, "w") as error_file:
            error_file.write("Date and Cycle: " + cycle_date + "\n")
            error_file.write("\n".join(errors))
        raise ValueError(f"Validation errors found. See {error_file_path} for details.")

    ### Row-specific validations ###

    required_cols = [
        "Loc", "Loc Zn", "Loc Name", "Loc Purp Desc", "Loc/QTI", "Flow Ind",
        "IT", "Auth Overrun Ind", "Nom Cap Exceed Ind", "All Qty Avail"
    ]

    numeric_cols = ["DC", "OPC", "TSQ", "OAC"]

    categorical_col_types = {
        "Flow Ind": ["D", "R"],
        "IT": ["Y", "N"],
        "Auth Overrun Ind": ["Y", "N"],
        "Nom Cap Exceed Ind": ["Y", "N"],
        "All Qty Avail": ["Y", "N"]
    }

    # Iterate through each row and perform row-specific validations
    for index, row in df.iterrows():
        row_identifier = f"Loc: {row['Loc']}, Loc Zn: {row['Loc Zn']}, Loc Name: {row['Loc Name']}"

        # Check for missing values in required columns
        for col in required_cols:
            if pd.isna(row[col]):
                errors.append(f"Row {index + 1} ({row_identifier}) has a missing value in column '{col}'")

        # Check for non-null negative values in numeric columns
        for col in numeric_cols:
            if pd.notna(row[col]) and row[col] < 0:
                errors.append(f"Row {index + 1} ({row_identifier}) has a negative value in column '{col}': {row[col]}")

        # Check for invalid values in categorical columns
        for col, allowed_values in categorical_col_types.items():
            if row[col] not in allowed_values:
                errors.append(f"Row {index + 1} ({row_identifier}) has an invalid value in column '{col}': {row[col]}. Allowed values are: {allowed_values}")

    # Raise list of errors, if any, pipe to txt file
    if errors:
        with open(error_file_path, "w") as error_file:
            error_file.write("Date and Cycle: " + cycle_date + "\n")
            error_file.write("\n".join(errors))
        raise ValueError(f"Validation errors found. See {error_file_path} for details.")

    return df