import os
import pandas as pd
import json

FIRST_INDEX=23874
OUTPUT_PATH='./output.xlsx'
ASTE_PATH='./aste'
COMBINED_RESULT_PATH='./combined_result.xlsx'
COMBINED_MAISON_MAPPING = {
    'BringATrailer': 'BringTrailer',
    'CarAndClassic': 'CarsAndClassic',
    'P_CarMarket': 'P CarMarket',
    'Sothebys': 'RmSotheby\'s',
    'H&H Classic': 'H&H'
}
CHARACTERS_TO_PURGE = {
    '\'': '',
    '"': '',
    'à': 'a'
}
COLUMN_MAPPING= column_mapping = {
    'Index': ['Index'],
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

def to_lowercase_purged(s: str) -> str:
    s = s.lower()
    for input, output in CHARACTERS_TO_PURGE.items():
        s = s.replace(input, output)
    return s

def get_aste_paths() -> list[str]:
    return sorted([f.path for f in os.scandir(ASTE_PATH) if f.is_dir()])

def get_snapshots_of_asta(asta_path: str) -> list[str]:
    return sorted([f.path for f in os.scandir(asta_path + '/NuoveAste') if f.is_file() and f.name.endswith('.xlsx')])

def parse_snapshot(snapshot_path: str) -> dict[str, str]:
    df = pd.read_excel(snapshot_path)
    possible_keys = list(COLUMN_MAPPING.keys())
    items = []
    for i in range(len(df)):
        xlsx_row = df.iloc[i]
        item = {}
        for key in possible_keys:
            for column in COLUMN_MAPPING[key]:
                if column in xlsx_row and not pd.isna(xlsx_row[column]):
                    item[key] = str(xlsx_row[column])
                    break
            if key not in item:
                item[key] = ''
        if 'AuctionCode' not in item:
            item['AuctionCode'] = ''
        if item['Event_ref'] != '' and item['PageUrl'] != '':
            items.append(item)
    return items

def fix_combined_maison(maison: str) -> str:
    if maison in COMBINED_MAISON_MAPPING.keys():
        return COMBINED_MAISON_MAPPING[maison]
    return maison

def parse_combined_result() -> dict[str, str]:
    df = pd.read_excel(COMBINED_RESULT_PATH)
    items = []
    for i in range(len(df)):
        xlsx_row = df.iloc[i]
        item = {}
        for column in ['Maison', 'Auction_title', 'Subtitle', 'AuctionCode', 'Auction_internal_code']:
            if column in xlsx_row and not pd.isna(xlsx_row[column]):
                item[column] = str(xlsx_row[column])
                if column == 'Auction_internal_code':
                    item[column] = item[column].replace('.0', '')
            else:
                item[column] = ''
        if item['Maison'] != '' and item['Auction_title'] != '' and item['AuctionCode'] != '':
            item['Maison'] = fix_combined_maison(item['Maison'])
            items.append(item)
    result = {}
    for item in items:
        result[get_key_for_combined(item)] = item['AuctionCode']
        result[get_key_for_combined(item, with_subtitle=True)] = item['AuctionCode']
    return result

def get_key_from_vehicle(vehicle: dict[str, str]) -> str:
    return to_lowercase_purged(vehicle['Event_ref'] + '///' + vehicle['PageUrl'])

def get_key_for_combined(item: dict[str, str], is_vehicle = False, with_subtitle = False) -> str:
    if fix_combined_maison(item['Maison']) == 'Catawiki':
        internal_code = item['Event_ref'] if is_vehicle else item['Auction_internal_code']  
        return to_lowercase_purged('Catawiki_special_case' + '///' + internal_code)

    if fix_combined_maison(item['Maison']) == 'H&H':
        val = item['Event_ref'] if is_vehicle else ('https://www.handh.co.uk/auction/search?au=' + item['Auction_internal_code'])
        return to_lowercase_purged(val)
    
    title = item['Event_ref'] if is_vehicle else (item['Auction_title'] + ' ' + item['Subtitle'] if with_subtitle else item['Auction_title'])
    return to_lowercase_purged(item['Maison'] + '///' + title)

def merge_vehicles(old: dict[str, str], new: dict[str, str]) -> dict[str, str]:
    if new['val_min'] == '':
        new['val_min'] = old['val_min']
    if new['val_max'] == '':
        new['val_max'] = old['val_max']
    if old['Index'] != '':
        new['Index'] = old['Index']
    if old['Lot'] != '':
        new['Lot'] = old['Lot']
    if old['AuctionCode'] != '':
        new['AuctionCode'] = old['AuctionCode']
    return new

def add_vehicles_to_asta(asta_vehicles: dict[str, dict[str, str]], vehicles: dict[str, str]):
    for vehicle in vehicles:
        key = get_key_from_vehicle(vehicle)
        if key not in asta_vehicles:
            asta_vehicles[key] = vehicle
        else:
            asta_vehicles[key] = merge_vehicles(asta_vehicles[key], vehicle)
            
def get_asta_vehicles(vehicles: dict[str, dict[str, str]], asta_path: str):
    snapshots = get_snapshots_of_asta(asta_path)
    for snapshot in snapshots:
        snapshot_vehicles = parse_snapshot(snapshot)
        add_vehicles_to_asta(vehicles, snapshot_vehicles)
        
def get_current_vehicles() -> dict[str, dict[str, str]]:
    try:
        items = parse_snapshot(OUTPUT_PATH)
        vehicles = {}
        for item in items:
            vehicles[get_key_from_vehicle(item)] = item
        return vehicles
    except FileNotFoundError:
        return {}
    
def get_max_index_of_current_vehicles(vehicles: dict[str, dict[str, str]]) -> int:
    max_index = 0
    for key in vehicles:
        if 'Index' in vehicles[key] and vehicles[key]['Index'] != '':
            max_index = max(max_index, int(vehicles[key]['Index']))
    return max_index

def get_all_vehicles(only_some = False) -> dict[str, dict[str, str]]:
    vehicles = {}
    aste = get_aste_paths()
    for asta in (aste[5:6] if only_some else aste):
        print(asta)
        get_asta_vehicles(vehicles, asta)
    return vehicles
        
def numerate_new_vehicles(vehicles: dict[str, dict[str, str]], max_index: int):
    for key in vehicles:
        if 'Index' not in vehicles[key] or vehicles[key]['Index'] == '':
            vehicles[key]['Index'] = str(max_index)
            max_index += 1

def assign_missing_lots(vehicles: dict[str, dict[str, str]]) -> None:
    vehicles_tuples = sorted(list(vehicles.items()), key=lambda x: x[1]['Event_ref'])
    current_event_ref = None
    current_lot_index = 1
    for key, vehicle in vehicles_tuples:
        if current_event_ref != vehicle['Event_ref']:
            current_event_ref = vehicle['Event_ref']
            current_lot_index = 1
        if vehicle['Lot'] == '':
            vehicles[key]['Lot'] = str(current_lot_index)
            current_lot_index += 1

def combine_auction_codes(vehicles: dict[str, dict[str, str]], combined_results: dict[str, str]) -> None:
    for key, vehicle in vehicles.items():
        if vehicle['AuctionCode'] == '':
            combined_key = get_key_for_combined(vehicle, is_vehicle=True)
            if combined_key in combined_results:
                auction_code = combined_results[combined_key]
                vehicles[key]['AuctionCode'] = auction_code
    
def merge_current_and_new_vehicles(current_vehicles: dict[str, dict[str, str]], new_vehicles: dict[str, dict[str, str]], combined_results: dict[str, str], max_index: int) -> dict[str, dict[str, str]]:
    for key in new_vehicles:
        if key in current_vehicles:
            new_vehicles[key] = merge_vehicles(current_vehicles[key], new_vehicles[key])
    for key in current_vehicles:
        if key not in new_vehicles:
            new_vehicles[key] = current_vehicles[key]
    numerate_new_vehicles(new_vehicles, max_index)
    assign_missing_lots(new_vehicles)
    combine_auction_codes(new_vehicles, combined_results)
    return new_vehicles

def save_vehicles(vehicles: dict[str, dict[str, str]], output_path: str):
    vehicles_rows = sorted(list(vehicles.values()), key=lambda x: int(x['Index']))
    df = pd.DataFrame(vehicles_rows)
    df.to_excel(output_path, index=False)
    
if __name__ == '__main__':
    combined_results = parse_combined_result()
    current_vehicles = get_current_vehicles()
    max_index = get_max_index_of_current_vehicles(current_vehicles)
    if (max_index >= FIRST_INDEX):
        raise Exception(f'Max index {max_index} is greater or equal than {FIRST_INDEX}')
    elif (max_index - FIRST_INDEX > 100):
        raise Exception(f'Max index {max_index} is too far from {FIRST_INDEX}')
    vehicles = get_all_vehicles(True)
    final_vehicles = merge_current_and_new_vehicles(current_vehicles, vehicles, combined_results, max_index)
    save_vehicles(final_vehicles, OUTPUT_PATH)
