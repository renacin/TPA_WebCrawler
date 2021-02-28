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


    # Data Prep
    df = prep_data.data_from_db("Data/")
    df = prep_data.clean_columns(df)
    df = prep_data.remove_redun(df)


    # Create Deep Copy & Write To CSV
    cleaned_df = df.copy()
    cleaned_df.to_csv("CleanedData.csv", index=False)
    del df, cleaned_df


    # Read Data From CSV & Create New Features
    df = pd.read_csv("Data/CleanedData.csv")
    df = create_data.parse_dates(df)
    df_all_data = create_data.create_ids(df)
    df_last_bid = create_data.last_bids_df(df_all_data)


    # Descriptive Statistics For Ratio Data | Using Final Data
    for col_name in ["CUR_PRICE", "NUM_BIDS"]:
        descriptive.histogram(df_last_bid[col_name])


    # Descriptive Statistics For Nominal Data | Using Final Data
    for col_name in ["HIGHEST_BIDR"]:
        descriptive.freqtable(df_last_bid[col_name])


    df_last_bid.to_csv("Data/DataLastBidPrice.csv", index=False)

# ----------------------------------------------------------------------------------------------------------------------

# Main Entry Point Into Python Code
if __name__ == "__main__":
    main()
