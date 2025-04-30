import pandas as pd
import argparse
import json

def summarize(csv_path: str) -> dict:
    """
    Read the sorted AIS CSV and compute high-level statistics.

    Returns a dict with:
     - total_records
     - unique_vessels
     - time_span (as string)
     - speed stats (mean, median, min, max)
     - navigational_status_counts
    """
    df = pd.read_csv(
        csv_path,
        usecols=['# Timestamp', 'MMSI', 'SOG', 'Navigational status'],
        parse_dates=['# Timestamp'],
        na_values=['', ' ', 'Unknown value'],
        low_memory=False,
        dtype={
            'Navigational status': 'string'
        }
    )

    total_records = len(df)
    unique_vessels = df['MMSI'].nunique()

    times = df['# Timestamp'].dropna()
    if not times.empty:
        time_span = (times.max() - times.min())
    else:
        time_span = pd.Timedelta(0)

    speeds = df['SOG'].dropna()
    speed_stats = {
        'mean': speeds.mean(),
        'median': speeds.median(),
        'min': speeds.min(),
        'max': speeds.max()
    }

    status_counts = df['Navigational status'].fillna('Unknown').value_counts().to_dict()

    return {
        'total_records': total_records,
        'unique_vessels': unique_vessels,
        'time_span': str(time_span),
        'speed_stats': speed_stats,
        'navigational_status_counts': status_counts
    }

def main():
    parser = argparse.ArgumentParser(description='Simple AIS data summary')
    parser.add_argument('--csv', required=True,
                        help='Path to the sorted AIS CSV file')
    parser.add_argument('--out', default=None,
                        help='If provided, write JSON summary to this file')
    args = parser.parse_args()

    summary = summarize(args.csv)

    if args.out:
        with open(args.out, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"Summary written to {args.out}")
    else:
        print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()