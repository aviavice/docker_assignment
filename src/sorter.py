import pandas as pd
import argparse
from .utils import DATE_FORMAT

def sort_csv(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv,
                     usecols=['# Timestamp','MMSI','Latitude','Longitude',
                              'Navigational status','SOG','ETA'],
                     na_values=['',' ','Unknown value'])
    df['# Timestamp'] = pd.to_datetime(df['# Timestamp'],
                                       format=DATE_FORMAT,
                                       errors='coerce')
    df.sort_values(['MMSI','# Timestamp'], inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"Sorted CSV saved to {output_csv}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Sort AIS CSV')
    parser.add_argument('--in',  dest='input_csv',  required=True,
                        help='Input CSV file to sort')
    parser.add_argument('--out', dest='output_csv', default='data/extracted_files/sorted.csv',
                        help='Output sorted CSV path')
    args = parser.parse_args()
    sort_csv(args.input_csv, args.output_csv)
