# Name:                                            Renacin Matadeen
# Date:                                               12/10/2020
# Title                                SQLite3 Database That Will Store Scraped Data
#
# ----------------------------------------------------------------------------------------------------------------------
import sqlite3
# ----------------------------------------------------------------------------------------------------------------------


# Create A Class For Our SQL_Lite Database
class SQL_Database:


    # Initial Function, Run When A WebCrawler Object Is Created
    def __init__(self):
        try:
            # Connect To Database Check If It has Data In It
            self.conn = sqlite3.connect(r"/home/pi/Desktop/TPA_Items_DB.db")

            self.conn.execute('''
            CREATE TABLE IF NOT EXISTS TPA_ITEM_DB
            (ITEM_NAME TEXT NOT NULL,
            SKU TEXT NOT NULL,
            CUR_PRICE REAL NOT NULL,
            MIN_UPBID REAL NOT NULL,
            UPBID_PRICE REAL NOT NULL,
            MINUTES_LEFT INT NOT NULL,
            START_DATE TEXT NOT NULL,
            END_DATE TEXT NOT NULL,
            NUM_BIDS INT NOT NULL,
            HIGHEST_BIDR TEXT NOT NULL)
            ;''')

            print("Connected To Database")

        except sqlite3.OperationalError as e:
            print(e)


    # Function To Insert Data Into Database
    def addtoDB(self, data_):
        cursor = self.conn.cursor()

        cursor.execute("""INSERT INTO TPA_ITEM_DB(ITEM_NAME, SKU, CUR_PRICE, MIN_UPBID, UPBID_PRICE, MINUTES_LEFT, START_DATE, END_DATE, NUM_BIDS, HIGHEST_BIDR)
                    VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (data_[0], data_[1], data_[2], data_[3], data_[4], data_[5], data_[6], data_[7], data_[8], data_[9]))

        self.conn.commit()
        cursor.close()


    # Function To Return Number Of Rows In Database
    def rowsinDB(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM TPA_ITEM_DB;")
        print("Rows In DB: {}".format(len(cursor.fetchall())))
        cursor.close()
