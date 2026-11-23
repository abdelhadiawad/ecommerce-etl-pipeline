from pathlib import Path
import pandas as pd 



PROJECT_ROOT=Path(__file__).resolve().parent.parent
DATA_PATH=PROJECT_ROOT/"data"/"raw"
BRONZE_PATH=PROJECT_ROOT /"data"/"bronze"
expected_files={'olist_geolocation_dataset.csv', 'olist_orders_dataset.csv', 'olist_customers_dataset.csv', 'olist_order_items_dataset.csv', 'olist_products_dataset.csv', 'olist_sellers_dataset.csv', 'olist_order_payments_dataset.csv', 'product_category_name_translation.csv', 'olist_order_reviews_dataset.csv'}

def discover_csv_files():
    
    if not DATA_PATH.exists():
        raise FileNotFoundError("Source directory not found")

    if not DATA_PATH.is_dir():
        raise NotADirectoryError("Source path is not a directory")

    csv_files=list(DATA_PATH.glob('*.csv'))

    if not csv_files:
        raise ValueError("No CSV files found")

    return csv_files


def validate_csv_files(csv_files):
    
    actual_files = {file.name for file in csv_files}    
    invalid_files=[]

    for file in csv_files:
        
        if not file.is_file() or file.stat().st_size==0:
            invalid_files.append(file.name) 
            continue
    if  len(invalid_files)!=0:
        raise ValueError(f"invalid files: {invalid_files}")

    missing_files=expected_files-actual_files
    unexpected_files=actual_files-expected_files

    if  missing_files:
        raise ValueError(f"missing_files:{missing_files}")
    

    
def extract_to_bronze():


    BRONZE_PATH.mkdir(parents=True,exist_ok=True)

    for file in expected_files:
        df_path = DATA_PATH / file  
        df_csv = pd.read_csv(df_path)
        df_csv.to_parquet(BRONZE_PATH / f'{df_path.stem}.parquet',index=False)
        df_parquet=pd.read_parquet(BRONZE_PATH / f'{df_path.stem}.parquet')
        print(df_csv.equals(df_parquet))
        if not df_csv.equals(df_parquet): raise ValueError(f'the files not equivalent: {file}')



if __name__ == "__main__":
    csv_files = discover_csv_files()
    validate_csv_files(csv_files)
    extract_to_bronze()