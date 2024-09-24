# %%
from multiprocessing import Value
import folium
import json
import geojson as gj
from pprint import pprint
import pandas as pd

interested_site_lat = 34.7700834
interested_site_lng = 138.0114131
# %%

with open('N02-20_RailroadSection.geojson', mode = 'r') as f :
    rail_lines_dict:dict = json.load(f)
# %%

list_key:list = ['type','name','crs']
rail_lines_settings:dict = {key:value for key,value in rail_lines_dict.items() if key in list_key}
rail_lines_features_tenhama:list[dict] = [feature for feature in rail_lines_dict["features"] if feature["properties"]["N02_003"] == "天竜浜名湖線" ]
rail_lines_tenhama:dict = rail_lines_settings | {"features":rail_lines_features_tenhama}
# %%
rail_lines_json:str = json.dumps(rail_lines_dict)
rail_lines_tenhama_json:str = json.dumps(rail_lines_tenhama)

pprint(rail_lines_tenhama_json)

# %%
gps_data_path:str = "/home/iori/daxue/bache_thesis/20240629_down_Futamata_to_Shinjohara/gps.csv"
df_gps = pd.read_csv(gps_data_path)

# %%
fmap1 = folium.Map(
    location=[interested_site_lat, interested_site_lng],
    tiles = "OpenStreetMap",
    zoom_start = 16, # 描画時の倍率 1〜20
    width = 800, height = 800 # 地図のサイズ
) 
folium.GeoJson(rail_lines_tenhama_json).add_to(fmap1)
# %%
markers = []
for index,row in df_gps.iterrows():
    speed = row["speed"]
    lat = row["latitude"]
    lon = row["longitude"]
    

# %%
fmap1
# %%
