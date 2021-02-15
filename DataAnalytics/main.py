# Name:                                            Renacin Matadeen
# Date:                                               02/15/2021
# Title                         Toronto Police Auctions - Website Parsing: Data Annalytics
#
# ----------------------------------------------------------------------------------------------------------------------
import sqlite3
import pandas as pd
# ----------------------------------------------------------------------------------------------------------------------

class prep_data:

    # Read Data From SQLite Database As Pandas Df
    @staticmethod
    def data_from_db(db_path):

        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM TPA_ITEM_DB;"

        return pd.read_sql_query(query, conn)

    # Clean Datetime Columns & Create A Date Obsserved Column
    @staticmethod
    def clean_dates(df):

        df['START_DATE'] = pd.to_datetime(df['START_DATE'], format='%m/%d/%Y')
        df['END_DATE'] = pd.to_datetime(df['END_DATE'], format='%m/%d/%Y')

        return df



# Main Function That Will Store Everything
def main():
    df = prep_data.data_from_db("TPA_Items_DB.db")
    df = prep_data.clean_dates(df)

    print(df.head(100))

# ----------------------------------------------------------------------------------------------------------------------

# Main Entry Point Into Python Code
if __name__ == "__main__":
    main()
