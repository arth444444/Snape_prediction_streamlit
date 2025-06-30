from Script_fetch_from_db import cursor_df as dataset
import pandas as pd
#print("Available columns:", dataset.columns)

dataset['date_column'] = pd.to_datetime(dataset['createdDate'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
dataset['date_column'] = dataset['date_column'].fillna(pd.to_datetime(dataset['createdDate'], format='%m/%d/%Y %H:%M', errors='coerce'))

dataset['10min_window'] = dataset['date_column'].dt.floor('10min')
deduped_data = dataset.sort_values(['customerNumber', 'date_column']).drop_duplicates(['customerNumber', '10min_window'], keep='first')
deduped_data['date_column'] += pd.Timedelta(hours=5, minutes=30)


print("Parsed")
