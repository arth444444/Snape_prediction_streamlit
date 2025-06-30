import pandas as pd
from google.cloud import bigquery
from datetime import datetime, timedelta
import os

project_id = 'bigquarry-459611'
client = bigquery.Client(project=project_id)

# Calculate time range
current_datetime = datetime.now()
current_datetime_utc = current_datetime - timedelta(hours=5, minutes=30)
prev_25_hours_utc = current_datetime_utc - timedelta(hours=25)

start_time = prev_25_hours_utc.strftime('%Y-%m-%d %H:%M:%S')
end_time = current_datetime_utc.strftime('%Y-%m-%d %H:%M:%S')

query = f"""
SELECT 
    createdDate,
    ST_Y(pickupGeoLocation) AS latitude,
    ST_X(pickupGeoLocation) AS longitude,
    bookingDate,
    customerNumber
FROM `bigquarry-459611.snape_mongo_data.bookings_rides`
WHERE createdDate >= '{start_time}'
  AND createdDate <= '{end_time}'
ORDER BY createdDate DESC
"""

# Initialize cursor_df so it's accessible globally
cursor_df = pd.DataFrame()

try:
    # cursor_df = client.query(query).to_dataframe()

    # Alternative approach without to_dataframe()
    query_job = client.query(query)
    results = query_job.result()
    # Convert to list of dictionaries first
    rows = [dict(row) for row in results]
    cursor_df = pd.DataFrame(rows)

    if not cursor_df.empty:
        
        cursor_df['customerNumber'] = cursor_df['customerNumber'].astype(str)
        print("Data fetched successfully:")
        print(cursor_df)
    else:
        print("No data found.")

except Exception as e:
    print(f"An error occurred while fetching data: {e}")
