from datetime import datetime, timedelta
import pandas as pd
from process import *

########## Overall############
dataset['date'] = dataset['date_column'].dt.date
dataset['hour'] = dataset['date_column'].dt.hour
hourly_demand = dataset.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand['ds'] = hourly_demand.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand = hourly_demand.drop(columns=['date', 'hour'])
hourly_demand['ds'] = pd.to_datetime(hourly_demand['ds'])

all_hours = pd.date_range(start=hourly_demand['ds'].min(), end=hourly_demand['ds'].max(), freq='H')
hourly_demand = hourly_demand.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand = hourly_demand.rename(columns={'index': 'ds'})
hourly_demand = hourly_demand.set_index('ds')


############ Airport #########
dataset_airport['date'] = dataset_airport['date_column'].dt.date
dataset_airport['hour'] = dataset_airport['date_column'].dt.hour
hourly_demand_airpot = dataset_airport.groupby(['date', 'hour']).size().reset_index(name='y')
#hourly_demand_airpot['ds'] = hourly_demand_airpot.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_airpot['ds'] = hourly_demand_airpot.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1).apply(lambda x: x)
hourly_demand_airpot = hourly_demand_airpot.drop(columns=['date', 'hour'])
hourly_demand_airpot['ds'] = pd.to_datetime(hourly_demand_airpot['ds'])



all_hours = pd.date_range(start=hourly_demand_airpot['ds'].min(), end=hourly_demand_airpot['ds'].max(), freq='H')
hourly_demand_airpot = hourly_demand_airpot.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_airpot = hourly_demand_airpot.rename(columns={'index': 'ds'})
hourly_demand_airpot= hourly_demand_airpot.set_index('ds')


########### Rabindrasadan ##########
dataset_rabindrasadan['date'] = dataset_rabindrasadan['date_column'].dt.date
dataset_rabindrasadan['hour'] = dataset_rabindrasadan['date_column'].dt.hour
hourly_demand_rabindrasadan = dataset_rabindrasadan.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_rabindrasadan['ds'] = hourly_demand_rabindrasadan.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_rabindrasadan = hourly_demand_rabindrasadan.drop(columns=['date', 'hour'])
hourly_demand_rabindrasadan['ds'] = pd.to_datetime(hourly_demand_rabindrasadan['ds'])

all_hours = pd.date_range(start=hourly_demand_rabindrasadan['ds'].min(), end=hourly_demand_rabindrasadan['ds'].max(), freq='H')
hourly_demand_rabindrasadan = hourly_demand_rabindrasadan.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_rabindrasadan = hourly_demand_rabindrasadan.rename(columns={'index': 'ds'})
hourly_demand_rabindrasadan = hourly_demand_rabindrasadan.set_index('ds')

############## Howrah #########
dataset_howrah['date'] = dataset_howrah['date_column'].dt.date
dataset_howrah['hour'] = dataset_howrah['date_column'].dt.hour
hourly_demand_howrah = dataset_howrah.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_howrah['ds'] = hourly_demand_howrah.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_howrah = hourly_demand_howrah.drop(columns=['date', 'hour'])
hourly_demand_howrah['ds'] = pd.to_datetime(hourly_demand_howrah['ds'])

all_hours = pd.date_range(start=hourly_demand_howrah['ds'].min(), end=hourly_demand_howrah['ds'].max(), freq='H')
hourly_demand_howrah = hourly_demand_howrah.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_howrah = hourly_demand_howrah.rename(columns={'index': 'ds'})
hourly_demand_howrah = hourly_demand_howrah.set_index('ds')


########## laketown ###########
dataset_laketown['date'] = dataset_laketown['date_column'].dt.date
dataset_laketown['hour'] = dataset_laketown['date_column'].dt.hour
hourly_demand_laketown = dataset_laketown.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_laketown['ds'] = hourly_demand_laketown.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_laketown = hourly_demand_laketown.drop(columns=['date', 'hour'])
hourly_demand_laketown['ds'] = pd.to_datetime(hourly_demand_laketown['ds'])

all_hours = pd.date_range(start=hourly_demand_laketown['ds'].min(), end=hourly_demand_laketown['ds'].max(), freq='H')
hourly_demand_laketown = hourly_demand_laketown.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_laketown = hourly_demand_laketown.rename(columns={'index': 'ds'})
hourly_demand_laketown = hourly_demand_laketown.set_index('ds')


########### Sector V ###########
dataset_sectorV['date'] = dataset_sectorV['date_column'].dt.date
dataset_sectorV['hour'] = dataset_sectorV['date_column'].dt.hour
hourly_demand_sectorV = dataset_sectorV.groupby(['date', 'hour']).size().reset_index(name='y')
hourly_demand_sectorV['ds'] = hourly_demand_sectorV.apply(lambda row: datetime.combine(row['date'], datetime.min.time()) + timedelta(hours=row['hour']), axis=1)
hourly_demand_sectorV = hourly_demand_sectorV.drop(columns=['date', 'hour'])
hourly_demand_sectorV['ds'] = pd.to_datetime(hourly_demand_sectorV['ds'])

all_hours = pd.date_range(start=hourly_demand_sectorV['ds'].min(), end=hourly_demand_sectorV['ds'].max(), freq='H')
hourly_demand_sectorV = hourly_demand_sectorV.set_index('ds').reindex(all_hours, fill_value=0).reset_index()
hourly_demand_sectorV = hourly_demand_sectorV.rename(columns={'index': 'ds'})
hourly_demand_sectorV = hourly_demand_sectorV.set_index('ds')

print("data processed")
