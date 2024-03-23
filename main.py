import os
import pandas as pd

FIRST_INDEX=16990
OUTPUT_PATH='./output.xlsx'
ASTE_PATH='./aste'
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
        if item['Event_ref'] != '' and item['Lot'] != '':
            items.append(item)
    return items

def get_key_from_vehicle(vehicle: dict[str, str]) -> str:
    return vehicle['Event_ref'] + '/' + vehicle['Lot']
def merge_vehicles(old: dict[str, str], new: dict[str, str]) -> dict[str, str]:
    if new['val_min'] == '':
        new['val_min'] = old['val_min']
    if new['val_max'] == '':
        new['val_max'] = old['val_max']
    if old['Index'] != '':
        new['Index'] = old['Index']
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

def get_all_vehicles() -> dict[str, dict[str, str]]:
    vehicles = {}
    aste = get_aste_paths()
    for asta in aste:
        print(asta)
        get_asta_vehicles(vehicles, asta)
    return vehicles
        
def numerate_new_vehicles(vehicles: dict[str, dict[str, str]], max_index: int):
    for key in vehicles:
        if 'Index' not in vehicles[key] or vehicles[key]['Index'] == '':
            vehicles[key]['Index'] = str(max_index)
            max_index += 1
        
def merge_current_and_new_vehicles(current_vehicles: dict[str, dict[str, str]], new_vehicles: dict[str, dict[str, str]], max_index: int) -> dict[str, dict[str, str]]:
    for key in new_vehicles:
        if key in current_vehicles:
            new_vehicles[key] = merge_vehicles(current_vehicles[key], new_vehicles[key])
    for key in current_vehicles:
        if key not in new_vehicles:
            new_vehicles[key] = current_vehicles[key]
    numerate_new_vehicles(new_vehicles, max_index)
    return new_vehicles


    
def save_vehicles(vehicles: dict[str, dict[str, str]], output_path: str):
    vehicles_rows = sorted(list(vehicles.values()), key=lambda x: int(x['Index']))
    df = pd.DataFrame(vehicles_rows)
    df.to_excel(output_path, index=False)
    
if __name__ == '__main__':
    current_vehicles = get_current_vehicles()
    max_index = get_max_index_of_current_vehicles(current_vehicles)
    if (max_index >= FIRST_INDEX):
        raise Exception(f'Max index {max_index} is greater or equal than {FIRST_INDEX}')
    elif (max_index - FIRST_INDEX > 100):
        raise Exception(f'Max index {max_index} is too far from {FIRST_INDEX}')
    vehicles = get_all_vehicles()
    final_vehicles = merge_current_and_new_vehicles(current_vehicles, vehicles, max_index)
    save_vehicles(final_vehicles, OUTPUT_PATH)
