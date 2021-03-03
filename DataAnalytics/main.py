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

    # Create Needed Columns
    df_last_bid = create_data.last_bids_df(df_all_data)
    df_data = create_data.create_index(df_last_bid)

    # Filter Data
    focus_df = df_all_data[df_all_data["ITEM_NAME"].str.contains("phone")]

    # Visualize Data
    descriptive.line_by_id(focus_df)

    # Export Data For Analysis
    # focus_df.to_csv("Data/Data2Analyze.csv", index=False)


# ----------------------------------------------------------------------------------------------------------------------

# Main Entry Point Into Python Code
if __name__ == "__main__":
    main()
