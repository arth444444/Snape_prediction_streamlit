from backend.dataprocess import *


for lag in [1, 8, 12, 24]:
    hourly_demand[f'lag_{lag}'] = hourly_demand['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_airpot[f'lag_{lag}'] = hourly_demand_airpot['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_laketown[f'lag_{lag}'] = hourly_demand_laketown['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_howrah[f'lag_{lag}'] = hourly_demand_howrah['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_rabindrasadan[f'lag_{lag}'] = hourly_demand_rabindrasadan['y'].shift(lag)

for lag in [1, 8, 12, 24]:
    hourly_demand_sectorV[f'lag_{lag}'] = hourly_demand_sectorV['y'].shift(lag)

hourly_demand= hourly_demand.tail(1)

hourly_demand_airpot= hourly_demand_airpot.tail(1)
hourly_demand_laketown= hourly_demand_laketown.tail(1)
hourly_demand_howrah= hourly_demand_howrah.tail(1)
hourly_demand_rabindrasadan= hourly_demand_rabindrasadan.tail(1)
hourly_demand_sectorV= hourly_demand_sectorV.tail(1)



print("city",hourly_demand)
print("laketown",hourly_demand_laketown)
print("airpor",hourly_demand_airpot)
print('howrah',hourly_demand_howrah)
print('rabindrasadan',hourly_demand_rabindrasadan)
print('sector5',hourly_demand_sectorV)