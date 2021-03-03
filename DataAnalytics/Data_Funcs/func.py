# Name:                                            Renacin Matadeen
# Date:                                               02/20/2021
# Title                           Website Parsing: Data Analytics - Needed Functions
#
# ----------------------------------------------------------------------------------------------------------------------
import glob
import time
import sqlite3
from collections import Counter
from datetime import datetime, timedelta

import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
# ----------------------------------------------------------------------------------------------------------------------


class prep_data:

    # For [FUNCTION #1] Read Databases Turn To Dataframes
    def db_to_df(db_path):
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM TPA_ITEM_DB;"

        return pd.read_sql_query(query, conn)


    # [FUNCTION #1] Read Data From SQLite Database As Pandas Df
    @staticmethod
    def data_from_db(path):

        file_list = glob.glob(path + "*.db")
        all_dfs = [prep_data.db_to_df(filename) for filename in file_list]
        full_df = pd.concat(all_dfs, axis=0, ignore_index=True)

        return full_df

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


# ----------------------------------------------------------------------------------------------------------------------


class create_data:


    def date_obs_calc(end_date, days_since):
        """ Function For [parse_dates] Identify The Date Observed """

        edl = end_date.split("-")
        edl = list(map(int, edl))
        cleaned_end_date = datetime(edl[0], edl[1], edl[2])

        return (cleaned_end_date - timedelta(days=days_since))



    @staticmethod
    def parse_dates(df):
        """ Create Basic Features """

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



    @staticmethod
    def create_ids(df):
        """ Create IDs For Type Of Items """

        df["TEMP"] = df["END_DATE"].astype(str) + df["SKU"].astype(str)
        df["ID"] = df.groupby(["TEMP"]).grouper.group_info[0]

        for col_ in ["TEMP", "UPBID_PRICE"]:
            try:
                del df[col_]

            except KeyError:
                pass

        return df



    @staticmethod
    def last_bids_df(df):
        """ Based On Previous Df Create New DF of Only Rows With Final Bid Price | Similar To Remove Redundant"""

        # Data Should Be Sorted But Just In Case Sort Again
        df = df.sort_values(["END_DATE", "ITEM_NAME", "MINUTES_LEFT"], ascending=[True, True, True])
        cleaned_df = df.drop_duplicates(subset=df.columns.difference(["CUR_PRICE", "MIN_UPBID", "MINUTES_LEFT",
                                                                      "NUM_BIDS", "HIGHEST_BIDR", "MINUTES_SINCE",
                                                                      "DAYS_SINCE", "DATE_OBS"]))

        return cleaned_df



    @staticmethod
    def create_index(df):
        """Created An Index Representing PRICE & NUM_BIDS; Desirability. And Create Col Of Item Type | Laptop, Phone Etc..."""

        # Normalize Columns Of Focus & Create Index Value
        for col_ in ["CUR_PRICE", "NUM_BIDS"]:
            df[col_+"_N"] = (df[col_] - df[col_].min()) / (df[col_].max() - df[col_].min())

        df["DESIRABILITY"] = (df["CUR_PRICE_N"] * 0.30) + (df["NUM_BIDS_N"] * 0.70)

        # Clean Up
        for col_ in ["CUR_PRICE", "NUM_BIDS"]:
            del df[col_+"_N"]

        return df



# ----------------------------------------------------------------------------------------------------------------------


class descriptive:



    @staticmethod
    def central_tendency(df_list, print_data=False):
        """ Describe Data Via Central Tendency Measures | Mean, Median, Mode, Sum, Num Obs"""

        col_name = df_list.name

        col_mean = round(np.mean(df_list), 2)
        col_mode = stats.mode(df_list)
        col_mode = round(col_mode[0][0], 2)
        col_median = round(np.median(df_list), 2)
        col_count = len(df_list)

        if print_data:
            print("{} | Mean: {} | Median: {} | Mode: {} | Count: {}".format(col_name, col_mean, col_median, col_mode, col_count))

        return [col_mean, col_mode, col_median, col_count]



    @staticmethod
    def dispersion(df_list, print_data=False):
        """ Describe Data Via Dispersion Statistics | Std. Dev, Variance, Min, Max"""

        col_name = df_list.name

        col_std = round(np.std(df_list), 2)
        col_var = round(np.var(df_list), 2)
        col_min = df_list.min()
        col_max = df_list.max()

        if print_data:
            print("{} | Stn. Dev: {} | Variance: {} | Min: {} | Max: {}".format(col_name, col_std, col_var, col_min, col_max))

        return [col_std, col_var, col_min, col_max]



    @staticmethod
    def distribution(df_list, print_data=False):
        """ Describe Data Via Distribution Statistics | Skewness, Kurtosis | CAUTION SKEW & KURTOSIS CAN BE DISTORTED"""

        col_name = df_list.name

        # Skewness Should Be 0; Negative Num Means Left Tail Is Long; Posetive Right Tail Is Long
        # Kurtosis Should Be 3; Higher Means Leptokurtic; Lower Means Platykurtic
        col_skew = round(stats.skew(df_list), 2)
        col_kurto = round(stats.kurtosis(df_list), 2)

        if print_data:
            print("{} | Skewness: {} | Kurtosis: {}".format(col_name, col_skew, col_kurto))

        return [col_skew, col_kurto]



    @staticmethod
    def histogram(df_list):
        """ Visualize Data By Histogram | USE ONLY ON RATIO DATA ONLY"""

        # Name Of Column
        col_name = df_list.name

        # Central Distribution Measures
        col_mean, col_mode, col_median, col_count = descriptive.central_tendency(df_list, print_data=True)
        col_std, col_var, col_min, col_max = descriptive.dispersion(df_list, print_data=True)
        col_skew, col_kurto = descriptive.distribution(df_list, print_data=True)

        # Basics Of Histogram
        bins_ = 15
        plt.figure(figsize= (5, 5))
        plt.hist(df_list, bins_, edgecolor="black")
        plt.title("Histogram: {}".format(col_name))
        plt.xlabel("Obersvations Of: {}".format(col_name))
        plt.ylabel("Frequency")

        # Add Line & Text Overlay
        ct_descriptors = {"Mean": col_mean, "Median": col_median, "Mode": col_mode}
        for cent_tend in ct_descriptors:
            plt.axvline(ct_descriptors[cent_tend], color='k', linestyle='dashed', linewidth=1)
            plt.text(ct_descriptors[cent_tend], 10, "{}: {}".format(cent_tend, ct_descriptors[cent_tend]), fontsize=8, color="k", rotation=90)

        print("\n")

        # Plot Standard Deviation Data
        minus_1_std = round(col_mean - col_std, 2)
        plus_1_std = round(col_mean + col_std, 2)

        if (plus_1_std <= col_max) and (minus_1_std >= 0):
            plt.text(minus_1_std, 10, "-1 Standard Dev: {}".format(minus_1_std), fontsize=8, color="k", rotation=90)
            plt.axvline(minus_1_std, color='red', linestyle='dashed', linewidth=1)
            plt.text(plus_1_std, 10, "+1 Standard Dev: {}".format(plus_1_std), fontsize=8, color="k", rotation=90)
            plt.axvline(plus_1_std, color='red', linestyle='dashed', linewidth=1)

        elif (minus_1_std >= 0):
            plt.text(minus_1_std, 10, "-1 Standard Dev: {}".format(minus_1_std), fontsize=8, color="k", rotation=90)
            plt.axvline(minus_1_std, color='red', linestyle='dashed', linewidth=1)

        elif (plus_1_std <= col_max):
            plt.text(plus_1_std, 10, "+1 Standard Dev: {}".format(plus_1_std), fontsize=8, color="k", rotation=90)
            plt.axvline(plus_1_std, color='red', linestyle='dashed', linewidth=1)

        plt.show()



    @staticmethod
    def freqtable(df_list):
        """ Visualize Data By Freq Table | USE ONLY ON NOMINAL"""

        col_name = df_list.name
        len_col =  len(df_list)

        # Create New Dataframe | Replace Names
        obs_df = df_list.value_counts().to_frame()
        obs_df = obs_df.reset_index(drop=False)
        obs_df = obs_df.rename({col_name : "Count"}, axis=1)
        obs_df = obs_df.rename({"index" : col_name}, axis=1)

        # Find Percentage
        obs_df["Percentage"] = (obs_df["Count"] / len_col) * 100

        print(obs_df.head(20))



    @staticmethod
    def line_by_id(df):

        unique_id_ = set(df["ID"].tolist())

        for id_ in unique_id_:
            # Grab By ID
            extract_df = df[df["ID"] == id_]

            # Grab Item Name
            name_list = extract_df["ITEM_NAME"].tolist()
            itemname = str(name_list[0])
            item_name = itemname.replace(" ", "_")

            # Make Copy of Master_Nan List & Replace Price Data By Index Of Time
            item_minutes_observed = extract_df["MINUTES_SINCE"].tolist()
            item_price_observed = extract_df["CUR_PRICE"].tolist()

            plt.plot(item_minutes_observed, item_price_observed, label=item_name)

        # plt.legend()
        plt.show()



# ----------------------------------------------------------------------------------------------------------------------
