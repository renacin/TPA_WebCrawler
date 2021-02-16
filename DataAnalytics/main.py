# Name:                                            Renacin Matadeen
# Date:                                               02/15/2021
# Title                         Toronto Police Auctions - Website Parsing: Data Annalytics
#
# ----------------------------------------------------------------------------------------------------------------------
import sqlite3
import datetime
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------

class prep_data:


    # [FUNCTION #1] Read Data From SQLite Database As Pandas Df
    @staticmethod
    def data_from_db(db_path):

        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM TPA_ITEM_DB;"

        return pd.read_sql_query(query, conn)


    # Function For  [FUNCTION #2] Parse Item Type
    def item_type(sku):
        if sku[-1] == "F":
            return "Jewelry"

        elif sku[-1] == "B":
            return "Technology"

        elif sku[-1] == "C":
            return "Antique"

        return "N/A"


    # [FUNCTION #2] Clean Datetime Columns & Create A Date Obsserved Column
    @staticmethod
    def clean_columns(df):

        df["START_DATE"] = pd.to_datetime(df["START_DATE"], format="%m/%d/%Y")
        df["END_DATE"] = pd.to_datetime(df["END_DATE"], format="%m/%d/%Y")
        df["LIST_DAY"] = df["START_DATE"].dt.day_name()
        df["LIST_MONTH"] = df["START_DATE"].dt.month_name()
        df["ITEM_TYPE"] = [prep_data.item_type(x) for x in df["SKU"]]

        # Drop Items Where Type Is N/A & Num Bids Is Zero
        df = df[df["ITEM_TYPE"] != "N/A"]
        df = df[df["NUM_BIDS"] != 0]

        return df


    # [FUNCTION #3] Remove Redundant Rows
    @staticmethod
    def remove_redun(df):

        return df



# Main Function That Will Store Everything
def main():
    df = prep_data.data_from_db("TPA_Items_DB.db")
    df = prep_data.clean_columns(df)
    df = prep_data.remove_redun(df)

    df.to_csv("DEBUG.csv", index=False)


# ----------------------------------------------------------------------------------------------------------------------

# Main Entry Point Into Python Code
if __name__ == "__main__":
    main()
