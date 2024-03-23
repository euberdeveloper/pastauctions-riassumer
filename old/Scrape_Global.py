"""
scraping globale di tutte le urls e dettagli veicolo
poi, fa merging di tutti i risultati precedenti
aggiornare ad ogni creazione nuovo script_maison.py
"""
import subprocess
import pandas as pd
import os
import glob
import shutil
from datetime import datetime

def run_script(script_name, max_urls, function_name):
    try:
        print(f"Running {function_name} in {script_name} with limit {max_urls}")
        subprocess.run(['python', script_name, str(max_urls)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {script_name}: {e}")

def standardize_column_names(df, column_mapping):
    for standard_col, variants in column_mapping.items():
        for variant in variants:
            if variant in df.columns:
                df.rename(columns={variant: standard_col}, inplace=True)
    return df


def find_newest_files(file_patterns):
    newest_files = {}
    destination_folder = '/Users/gianfrancostefani/Downloads/Ultimi/A_ScrapeGlobal/VerifyLastDownloadedFiles/'
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)  # Crea la cartella se non esiste

    for pattern_info in file_patterns:
        pattern = pattern_info['file_path']
        files = glob.glob(pattern)
        if files:  # se la lista non è vuota
            newest_file = max(files, key=os.path.getctime)
            newest_files[pattern] = newest_file
            # Copia il file più recente nella cartella di destinazione
            shutil.copy2(newest_file, destination_folder)
        else:
            newest_files[pattern] = None  # o qualche indicazione che non sono stati trovati file
    return newest_files


def main():
    url_limits = {
        # 'ScrapeCollectingCar_extractUrlsController.py': 99,  # Manual from urlsController
        # 'ScrapeHermans_extractUrl.py': 10,

        'ScrapeTheMarket_extractUrl.py': 99,
        'ScrapeCatawiki_extractUrls.py': 99,  # Double for car and motorcycle
        'ScrapeBonhams_extractUrl.py': 99,
        'ScrapeSotheby_extractVehiclesUrl.py': 99,
        'ScrapeHH_extractUrl.py': 10,
        'ScrapeBrightwells_extractUrl.py': 99,
        'ScrapeBringTrailer_extractUrls.py': 99,
        'ScrapeMecum_extractUrlEvent.py': 99,
        'ScrapeMecum_extractUrlVehicle.py': 99,
        'ScrapeBarrettJack_extractUrlVehicle.py': 99,
        'ScrapeCarAndClassic_extractUrl.py': 99,
        'ScrapeVavato_extractUrls.py': 99,
        'ScrapeP_CarMarket_extractUrl_Live.py': 99,
        'ScrapeP_CarMarket_extractUrl_Closed.py': 10,
    }

    # Step 1: Run URL scraping scripts
    url_scripts = [
        # 'ScrapeCollectingCar_extractUrlsController.py',
        # 'ScrapeHermans_extractUrl.py',

        'ScrapeTheMarket_extractUrl.py',
        'ScrapeCatawiki_extractUrls.py',
        'ScrapeBonhams_extractUrl.py',
        'ScrapeSotheby_extractVehiclesUrl.py',
        'ScrapeHH_extractUrl.py',
        'ScrapeBrightwells_extractUrl.py',
        'ScrapeBringTrailer_extractUrls.py',
        'ScrapeMecum_extractUrlEvent.py',
        'ScrapeMecum_extractUrlVehicle.py',
        'ScrapeBarrettJack_extractUrlVehicle.py',
        'ScrapeCarAndClassic_extractUrl.py',
        'ScrapeVavato_extractUrls.py',
        'ScrapeP_CarMarket_extractUrl_Live.py',
        'ScrapeP_CarMarket_extractUrl_Closed.py',
    ]

    for script in url_scripts:
        max_urls = url_limits.get(script, 10)  # Default to 10 if not specified
        run_script(script, max_urls, "URL Scraping")

    # Step 2: Run data scraping scripts
    data_scripts = [
        # 'ScrapeCollectingCar_extractDatas.py',
        # 'ScrapeHermans_extractDatasLive.py',
        # 'ScrapeHermans_extractDatasClosed.py',

        'ScrapeTheMarket_extractData.py',
        'ScrapeCatawiki_extractDatasCar.py',
        'ScrapeCatawiki_extractDatasMoto.py',
        'ScrapeBonhams_extracDatas.py',
        'ScrapeSotheby_extractVehiclesDatas.py',
        'ScrapeSotheby_extractVehiclesDatasSealed.py',
        'ScrapeHH_extractDatas.py',
        'ScrapeBrightwells_extractDatas.py',
        'ScrapeBringTrailer_extractDatas.py',
        'ScrapeMecum_extractDatas.py',
        'ScrapeBarrettJack_extractDatas.py',
        'ScrapeCarAndClassic_extractDatasLive.py',
        'ScrapeCarAndClassic_extractDatasSold.py',
        'ScrapeCarAndClassic_extractDatasUpcoming.py',
        'ScrapeVavato_extractDatas_Closed.py',
        'ScrapeVavato_extractDatas_Upcoming.py',
        'ScrapeP_CarMarket_extractDatas_Live.py',
        'ScrapeP_CarMarket_extractDatas_Closed.py',


        ## fai girare estrazione Events
        # 'ScrapeCollectingCar_extractDatasEvent.py',

        'ScrapeTheMarket_extractDataEvent.py',
        'ScrapeSotheby_extractEventsDatas.py',
        'ScrapeSotheby_extractEventsDatasSealed.py',
        'ScrapeBringTrailer_extractDatasEvent.py',
        'ScrapeMecum_extractUrlEvent.py',
        'ScrapeCarAndClassic_extractDatasEvent.py',
    ]

    for script in data_scripts:
        run_script(script, 10, "Data Scraping")  # Assuming no limit for data scraping

    def find_newest_files(file_patterns):
        newest_files = {}
        for pattern_info in file_patterns:
            pattern = pattern_info['file_path']
            files = glob.glob(pattern)
            if files:  # if list is not empty
                newest_files[pattern] = max(files, key=os.path.getctime)
            else:
                newest_files[pattern] = None  # or some indication that no files were found
        return newest_files

    # Step 3: Combine Excel files
    file_patterns = [
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_TheMarket/NuoveAste/Themarket_CombinedResult_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Catawiki/NuoveAste/catawiki_CarResult_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Catawiki/NuoveAste/catawiki_MotoResult_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Bonhams/NuoveAste/ScrapedResult_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Sotheby/NuoveAste/scraped_vehicleSealed_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Sotheby/NuoveAste/scraped_vehicle_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_HH/NuoveAste/HH_VehiclesData_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Brightwells/NuoveAste/Gen_Brightwells_VehiclesData_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_CollectingCars/NuoveAste/results_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_BringATrailer/NuoveAste/scraped_data_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Mecum/NuoveAste/mecum_result_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_BJ/NuoveAste/BJ_VehiclesData_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_CarAndClassic/NuoveAste/CarAndClassic_VehiclesData_Upcoming_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_CarAndClassic/NuoveAste/CarAndClassic_VehiclesData_Live_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_CarAndClassic/NuoveAste/CarAndClassic_VehiclesData_Result_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Vavato/NuoveAste/Vavato_VehicleUrls_Upcoming_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Vavato/NuoveAste/Vavato_VehicleUrls_Closed_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Hermans/NuoveAste/Hermans_VehicleDetail_Live_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_Hermans/NuoveAste/Hermans_VehicleDetail_Closed_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_PCarMarket/NuoveAste/P_CarMarket_VehicleDatas_Live_*.xlsx'},
        {'file_path': '/Users/gianfrancostefani/Downloads/Ultimi/Gen_PCarMarket/NuoveAste/P_CarMarket_VehicleDatas_Closed_*.xlsx'},
    ]

    # Finding the newest files for each pattern
    newest_files = find_newest_files(file_patterns)
    print("Newest files found:", newest_files)

    column_mapping = {
        'Maison': ['Maison'],
        'Event_ref': ['Event_ref', 'AuctionName'],
        'PageUrl_extract': ['PageUrl_extract'],
        'PageUrl': ['PageUrl'],
        'PhotoUrl': ['PhotoUrl', 'Image URLs', 'ImageURLs'],
        'Lot': ['Lot', 'Lotto'],
        'Title': ['Title', 'Item Title'],
        'Targa': ['Targa'],
        'Chassis': ['Chassis', 'Chassis number'],
        'Engine': ['Engine'],
        'Body': ['Body'],
        'RearFrame': ['RearFrame'],
        'Crankcase': ['Crankcase'],
        'RiferAuction': ['RiferAuction'],
        'km': ['km', 'Km', 'Mileage', 'Odometer', 'Mileage (Km)', 'Mileage (Mi)'],
        'Cilindrata': ['Cilindrata'],
        'TipoCambio': ['TipoCambio', 'Transmission'],
        'ColorEst': ['ColorEst', 'Est_Color'],
        'ColorInt': ['ColorInt', 'Int_Color'],
        'TipoCarrozz': ['TipoCarrozz'],
        'val_min': ['val_min'],
        'val_max': ['val_max'],
        'SalePrice Bid': ['Price', 'SalePrice', 'SalePrice Bid', 'SalesPrice'],
        'SaleStatus': ['SaleStatus'],
        'PriceReserve': ['PriceReserve'],
        'BidStart': ['BidStart'],
        'BidEnd': ['BidEnd'],
        'Subtitle': ['Subtitle'],
        'Year': ['Year'],
        'Brand': ['Brand'],
        'Model': ['Model'],
        'ModelType': ['ModelType'],
        'Cilindri': ['Cilindri'],
        'Eng_Tecnico': ['Eng_Tecnico'],
        'Eng_Note': ['Eng_Note'],
        'Eng_Veicolo': ['Description', 'Item Description', 'Eng_Veicolo'],
        'GalleryPhoto': ['GalleryPhoto'],
        'Bids': ['Bids'],
        'Located in': ['Location', 'CountrySeller', 'Located in', 'SellerLocated'],
        'Seller': ['Seller'],
        'DriveSide': [''],
        'Alimentation': [''],
        'SourceDate': [''],
    }

    # Finding the newest files for each pattern
    newest_files = find_newest_files(file_patterns)
    print("Newest files found:", newest_files)

    dataframes = []
    for pattern_info in newest_files.values():
        file_path = pattern_info  # Extract the file path from the dict
        if file_path and os.path.exists(file_path):  # Ensure file path exists
            try:
                df = pd.read_excel(file_path)
                df = standardize_column_names(df, column_mapping)
                dataframes.append(df)
            except Exception as e:
                print(f"An error occurred while reading {file_path}: {e}")
        else:
            print(f"File not found or no file for pattern: {pattern_info}")

    if dataframes:
        # Reset index for each DataFrame and remove duplicates if necessary
        cleaned_dataframes = []
        for df in dataframes:
            df = df.reset_index(drop=True)  # Reset the index to ensure it's unique
            df = df.drop_duplicates()  # Remove duplicate rows, if they exist
            cleaned_dataframes.append(df)

        # Combine all cleaned DataFrames
        try:
            combined_df = pd.concat(cleaned_dataframes, ignore_index=True)
            combined_df.to_excel('/Users/gianfrancostefani/Downloads/Ultimi/A_ScrapeGlobal/CombinedResults.xlsx',
                                 index=False)
            print("Combined Excel file has been created successfully.")
        except Exception as e:
            print(f"An error occurred while combining dataframes: {e}")
    else:
        print("No dataframes to combine.")


if __name__ == "__main__":
    main()
