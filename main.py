import os
import pandas as pd
import json

ASTE_PATH='./aste'

def get_aste_folders_paths() -> list[str]:
    return [f.path for f in os.scandir(ASTE_PATH) if f.is_dir()]

def get_aste_files_of_asta(asta_path: str) -> list[str]:
    return [f.path for f in os.scandir(asta_path + '/NuoveAste') if f.is_file() and f.name.endswith('.xlsx')]

if __name__ == '__main__':
    aste = get_aste_folders_paths()
    headers = []
    for asta in aste:
        files = get_aste_files_of_asta(asta)
        first_file = files[0]
        df = pd.read_excel(first_file)
        headers.append(df.columns.tolist())
    # create a csv with 47 columns called "COLONNA_1", "COLONNA_2", ..., "COLONNA_47" and put the headers as data
    df = pd.DataFrame(headers, columns=[f'COLONNA_{i}' for i in range(1, 48)])
    df.to_excel('headers.xlsx', index=False)
    

    