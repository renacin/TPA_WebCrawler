# Name:                                            Renacin Matadeen
# Date:                                               02/15/2021
# Title                         Toronto Police Auctions - Website Parsing: Data Annalytics
#
# ----------------------------------------------------------------------------------------------------------------------
import time
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
# ----------------------------------------------------------------------------------------------------------------------


class prep_data:

    # [FUNCTION #1] Read Data From SQLite Database As Pandas Df
    @staticmethod
    def data_from_db(db_path):

        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM TPA_ITEM_DB;"

        return pd.read_sql_query(query, conn)

    # Function For [FUNCTION #2] Parse Item Type
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

        # Format Time
        df["START_DATE"] = pd.to_datetime(df["START_DATE"], format="%m/%d/%Y")
        df["END_DATE"] = pd.to_datetime(df["END_DATE"], format="%m/%d/%Y")

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

        # Sort Df By Item Name, And Then Time Remaining
        df = df.sort_values(["END_DATE", "ITEM_NAME", "MINUTES_LEFT"], ascending=[True, True, True])
        df = df.drop_duplicates(subset=df.columns.difference(["MINUTES_LEFT"]))

        return df



class create_data:

    # Function For [FUNCTION #1] Identify The Date Observed
    def date_obs_calc(end_date, days_since):

        edl = end_date.split("-")
        edl = list(map(int, edl))
        cleaned_end_date = datetime(edl[0], edl[1], edl[2])

        return (cleaned_end_date - timedelta(days=days_since))


    # [FUNCTION #1] Create Basic Features
    @staticmethod
    def parse_dates(df):

        # Format Time
        end_date_list = df["END_DATE"].tolist()
        df["START_DATE"] = pd.to_datetime(df["START_DATE"], format="%Y-%m-%d")
        df["END_DATE"] = pd.to_datetime(df["END_DATE"], format="%Y-%m-%d")

        df["LIST_DAY"] = df["START_DATE"].dt.day_name()
        df["LIST_MONTH"] = df["START_DATE"].dt.month_name()
        df["MINUTES_SINCE"] = 10080 - df["MINUTES_LEFT"]

        # Create A Date Observed Column
        df["DAYS_SINCE"] = 7 - ((df["MINUTES_SINCE"] // 1440) + 1)
        df["DAYS_SINCE"] = df["DAYS_SINCE"].replace([-1], 0)

        days_since_list = df["DAYS_SINCE"].tolist()
        day_observed = [create_data.date_obs_calc(x, y) for x, y in zip(end_date_list, days_since_list)]
        df["DATE_OBS"] = day_observed

        return df


    # [FUNCTION #2] Create IDs For Type Of Items
    @staticmethod
    def create_ids(df):
        df["TEMP"] = df["END_DATE"].astype(str) + df["SKU"].astype(str)
        df["ID"] = df.groupby(["TEMP"]).grouper.group_info[0]

        return df



class visualize_data:

    # [FUNCTION #1] Visualize Data
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

            plt.close()


# ----------------------------------------------------------------------------------------------------------------------

# Main Function That Will Store Everything
def main():

    # # Data Prep
    # df = prep_data.data_from_db("Data/TPA_Items_DB.db")
    # df = prep_data.clean_columns(df)
    # df = prep_data.remove_redun(df)
    #
    # # Create Deep Copy & Write To CSV
    # cleaned_df = df.copy()
    # cleaned_df.to_csv("CleanedData.csv", index=False)
    # del df, cleaned_df

    # Read Data From CSV & Create New Features
    df = pd.read_csv("Data/CleanedData.csv")
    df = create_data.parse_dates(df)
    df = create_data.create_ids(df)

    # df = visualize_data.scatter_by_sku(df)
    df.to_csv("Data/TPS_Auctions_Data.csv", index=False)

# ----------------------------------------------------------------------------------------------------------------------

# Main Entry Point Into Python Code
if __name__ == "__main__":
    main()
