# Name:                                            Renacin Matadeen
# Date:                                               02/15/2021
# Title                         Toronto Police Auctions - Website Parsing: Data Annalytics
#
# ----------------------------------------------------------------------------------------------------------------------
import time
import sqlite3
import datetime
import pandas as pd
import matplotlib.pyplot as plt
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

        # Basic Formating & Feature Creation
        df["ITEM_TYPE"] = [prep_data.item_type(x) for x in df["SKU"]]

        # Drop Items Where Type Is N/A, MINUTES_LEFT Is N/A, And Num Bids Is Zero
        df = df[df["MINUTES_LEFT"] != "N/A"]
        df = df[df["ITEM_TYPE"] != "N/A"]
        df = df[df["NUM_BIDS"] != 0]

        return df


    # [FUNCTION #3] Remove Redundant Rows
    @staticmethod
    def remove_redun(df):

        # Create Dataframe That Will Store Data
        cleaned_df_dict = {}
        for col in df.columns:
            cleaned_df_dict[col] = []

        cleaned_df = pd.DataFrame.from_dict(cleaned_df_dict)

        # Loop Through Unique SKUs, Remove Redundant Rows, & Append To new Df
        unique_sku = set(df["SKU"].tolist())
        for sku in unique_sku:
            extract_df = df[df["SKU"] == sku]
            extract_df = extract_df.sort_values(by="MINUTES_LEFT")
            extract_df = extract_df.drop_duplicates(subset=extract_df.columns.difference(["MINUTES_LEFT"]))

            # Merge Extracted Data With External Dataframe
            cleaned_df = pd.concat([cleaned_df, extract_df])

        return cleaned_df


class visualize_data:

    # [FUNCTION #1] Create Basic Features
    @staticmethod
    def create_columns(df):

        # Format Time
        df["START_DATE"] = pd.to_datetime(df["START_DATE"], format="%m/%d/%Y")
        df["END_DATE"] = pd.to_datetime(df["END_DATE"], format="%m/%d/%Y")

        df["LIST_DAY"] = df["START_DATE"].dt.day_name()
        df["LIST_MONTH"] = df["START_DATE"].dt.month_name()
        df["MINUTES_SINCE"] = 10080 - df["MINUTES_LEFT"]

        return df


    # [FUNCTION #2] Visualize Data
    @staticmethod
    def scatter_by_sku(df):
        unique_sku = set(df["SKU"].tolist())
        for sku in unique_sku:
            extract_df = df[df["SKU"] == sku]

            name_list = extract_df["ITEM_NAME"].tolist()
            item_name = str(name_list[0])

            plt.scatter(extract_df.MINUTES_SINCE, extract_df.CUR_PRICE)
            plt.title(item_name)
            plt.xlabel("Minutes Since")
            plt.ylabel("Current Price")
            plt.show()

            time.sleep(5)

            plt.close()


# ----------------------------------------------------------------------------------------------------------------------


# Main Function That Will Store Everything
def main():

    # # Data Prep
    # df = prep_data.data_from_db("TPA_Items_DB.db")
    # df = prep_data.clean_columns(df)
    # df = prep_data.remove_redun(df)
    #
    # # Create Deep Copy & Write To CSV
    # cleaned_df = df.copy()
    # cleaned_df.to_csv("CleanedData.csv", index=False)
    # del df

    # Read Data From CSV
    df = pd.read_csv("CleanedData.csv")
    df = visualize_data.create_columns(df)
    df = visualize_data.scatter_by_sku(df)

    df.to_csv("Test.csv", index=False)


# ----------------------------------------------------------------------------------------------------------------------

# Main Entry Point Into Python Code
if __name__ == "__main__":
    main()
