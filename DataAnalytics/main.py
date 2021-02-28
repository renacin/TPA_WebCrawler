# Name:                                            Renacin Matadeen
# Date:                                               02/15/2021
# Title                         Toronto Police Auctions - Website Parsing: Data Annalytics
#
# ----------------------------------------------------------------------------------------------------------------------
import pandas as pd
from Data_Funcs.func import *
# ----------------------------------------------------------------------------------------------------------------------


# Main Function That Will Store Everything
def main():


    # Read Data From CSV & Create New Features
    df = pd.read_csv("Data/CleanedData.csv")
    df = create_data.parse_dates(df)
    df_all_data = create_data.create_ids(df)

    df_last_bid = create_data.last_bids_df(df_all_data)

    df_data = create_data.create_index(df_last_bid)

    df_data = df_data[df_data["ITEM_TYPE"] == "Technology"]

    # Descriptive Statistics For Ratio Data | Using Final Data
    for col_name in ["CUR_PRICE", "NUM_BIDS", "DESIRABILITY"]:
        descriptive.histogram(df_data[col_name])

    # Descriptive Statistics For Nominal Data | Using Final Data
    for col_name in ["HIGHEST_BIDR"]:
        descriptive.freqtable(df_data[col_name])


# ----------------------------------------------------------------------------------------------------------------------

# Main Entry Point Into Python Code
if __name__ == "__main__":
    main()
