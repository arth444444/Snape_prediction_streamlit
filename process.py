from Parse import deduped_data as dataset
from haversine import haversine, Unit

# Pickup lat long extraction
dataset['pickup_latitude'] = dataset['latitude'].astype(float)
dataset['pickup_longitude'] = dataset['longitude'].astype(float)

laketown = (22.604061, 88.403715)
sector_5 = (22.576222, 88.435053)
rabindrasadan_metro = (22.541297, 88.347389)
howrah = (22.583474, 88.342969)
airport = (22.642434, 88.439351)

def calculate_distance(coords, lat, lon):
    point_coords = (lat, lon)
    return haversine(coords, point_coords, unit=Unit.KILOMETERS)

dataset['aerial_dist_laketown'] = dataset.apply(
    lambda row: calculate_distance(laketown, row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_sector_V'] = dataset.apply(
    lambda row: calculate_distance(sector_5, row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_rabindrasadan_metro'] = dataset.apply(
    lambda row: calculate_distance(rabindrasadan_metro, row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_howrah'] = dataset.apply(
    lambda row: calculate_distance(howrah, row['pickup_latitude'], row['pickup_longitude']), axis=1
)
dataset['aerial_dist_airport'] = dataset.apply(
    lambda row: calculate_distance(airport, row['pickup_latitude'], row['pickup_longitude']), axis=1
)

dataset_rabindrasadan = dataset[dataset['aerial_dist_rabindrasadan_metro'] < 3]
dataset_airport = dataset[dataset['aerial_dist_airport'] < 3]
dataset_laketown = dataset[dataset['aerial_dist_laketown'] < 3]
dataset_howrah = dataset[dataset['aerial_dist_howrah'] < 3]
dataset_sectorV = dataset[dataset['aerial_dist_sector_V'] < 5]

print("processed")