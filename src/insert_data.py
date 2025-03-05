def insert_data(df, connection):
    cursor = connection.cursor()
    sqlinsert_file_path = "insert_data.sql"
    with open(sqlinsert_file_path, "r") as sql_file:
        sql_query = sql_file.read()

    for _, row in df.iterrows():
        cursor.execute(sql_query, 
            (
                row["Gas Day"],
                row["Cycle"],
                row["Loc"],
                row["Loc Zn"],
                row["Loc Name"],
                row["Loc Purp Desc"],
                row["Loc/QTI"],
                row["Flow Ind"],
                row["DC"],
                row["OPC"],
                row["TSQ"],
                row["OAC"],
                row["IT"],
                row["Auth Overrun Ind"],
                row["Nom Cap Exceed Ind"],
                row["All Qty Avail"],
                row["Qty Reason"]
            )
        )
    
    connection.commit()