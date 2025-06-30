import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime, timedelta
import json
import streamlit as st

# ✅ Set up credentials from secrets
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
credentials = service_account.Credentials.from_service_account_info(creds_dict)

# ✅ Initialize BigQuery client
client = bigquery.Client(credentials=credentials, project=credentials.project_id)

# ⏳ Calculate time range (UTC)
current_datetime = datetime.now()
current_datetime_utc = current_datetime - timedelta(hours=5, minutes=30)
prev_25_hours_utc = current_datetime_utc - timedelta(hours=25)

start_time = prev_25_hours_utc.strftime('%Y-%m-%d %H:%M:%S')
end_time = current_datetime_utc.strftime('%Y-%m-%d %H:%M:%S')

# 🧠 Your SQL query
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

# 📦 Global variable to be used elsewhere
cursor_df = pd.DataFrame()

# 🚀 Execute query
try:
    query_job = client.query(query)
    results = query_job.result()

    rows = [dict(row) for row in results]
    cursor_df = pd.DataFrame(rows)

    if not cursor_df.empty:
        cursor_df['customerNumber'] = cursor_df['customerNumber'].astype(str)
        print("✅ Data fetched successfully.")
        print(cursor_df)
    else:
        print("⚠️ No data found in the given time range.")

except Exception as e:
    print(f"❌ An error occurred while fetching data: {e}")
