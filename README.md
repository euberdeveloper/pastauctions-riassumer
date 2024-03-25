# pastauctions-riassumer
A python script that takes the vehicles of the auctions of the last days and handles the data to achieve an output excel

## Purpose

There are many auctions scrapings that are done by pastauctions. For each maison, there is a periodical scraping that creates multiple excel files. This script merges all those scraping files into a unique file, by assigning also an id. Those data will be then added to the database.

## How to use

### Requirements

Pipenv should be installed.
The auctions folder should contain a folder for each maison and each of those folders a folder "NuoveAste" with all the excel files, ordered from the oldest to the newest.

### Steps

1. Clone the repository
2. Install the requirements with `pipenv install` and start a shell with `pipenv shell`
3. Run the script with `python main.py`

### Options

In the script `main.py` there are some constants that can be adjusted:
- **FIRST_INDEX**: the smallest index that will be assigned to the constructed vehicles
- **OUTPUT_PATH**: the path to the output excel file
- **ASTE_PATH**: the path to the folder containing the auction files
- **COLUMN_MAPPING**: an object doing the mapping between wanted properties (keys) and possible column names in the scraped auction files (array of strings)

## How does it work

1. If it exists, the current "output" excel file is loaded
2. The max index of the current output is found and compared to the constant provided one. If it is not ok, an error is thrown
3. For each maison, the auction files are detected (dir walking) and loaded via the mapping
4. They are grouped by "Event_ref" and "Lot". If the lot does not exist, it becomes the hash of the "PageUrl". Rows withou "Event_ref" or "PageUrl" are discarded
5. Rows that end in the same group are merged, with the newest data overwriting the oldest, a part from "val_min" and "val_max" that are taken from the old in case the newest is empty.
6. The rows are then added to the current loaded file. If the vehicles already exist, they are updated and the id remains the same, otherwise the vehicle is added with an incremental id starting from FIRST_INDEX
