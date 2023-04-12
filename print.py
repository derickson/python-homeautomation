import os
import copy
import json
from requests import get
from datetime import datetime
from elasticsearch import Elasticsearch

nowiso = datetime.utcnow().isoformat()

## Get Home Assistant State
token = os.getenv('HASS_BEARERTOKEN', 'ERROR')
hass_url = os.getenv('HASS_URL', 'http://localhost:8123')
url = "{}/api/states".format(hass_url)

headers = {
    "Authorization": "Bearer {}".format(token),
    "content-type": "application/json",
}
response = get(url, headers=headers)

## Get JSON state objects I'm interested in loaded into a dictionary
## do some transformation as well
rj = response.json()

# print(json.dumps(rj, indent=4))

entitiesToExtract = ["person.dave_3",
                    #  "sun.sun",
                    #  "light.officesmartwallswitch",
                    #  "binary_sensor.presence_3",
                    #  "binary_sensor.water1",
                    #  "binary_sensor.water2",
                    #  "number.motion_sensor_duration",
                    #  "switch.officesmartwallswitch",
                    #  "sensor.davephone_activity",
                    #  "sensor.davephone_distance",
                    #  "sensor.davephone_floors_ascended",
                    #  "sensor.davephone_floors_descended",
                    #  "sensor.davephone_steps",
                    #  "sensor.davephone_average_active_pace",
                    #  "sensor.davephone_battery_level",
                    #  "sensor.davephone_battery_state",
                    #  "sensor.davephone_geocoded_location",
                    #  "light.hue_smart_plug_1",
                    #  "light.bedroom",
                    #  "device_tracker.davephone",
                    #  "weather.home",
                    #  "light.porchlights",
                    #  "sensor.ipad_16_battery_level",
                    #  "sensor.ipad_16_battery_state",
                    #  "binary_sensor.vibrationwasher",
                    #  "sensor.humidity_9",  #office
                    #  "sensor.temperature_10", #office
                    #  "sensor.temperature1", #pressure #office
                    #  "sensor.humidity_12", #livingroom
                    #  "sensor.temperature_13", #livingroom
                    #  "sensor.temperature2", #pressure #livingroom
                    #  "sensor.humidity_15", #basementfront
                    #  "sensor.temperature_16", #basementfront
                    #  "sensor.temperature3", #pressure #basementfront
                    #  "sensor.house_temperature",
                    #  "sensor.house_humidity",
                    #  "climate.house"
                     ]
numericState = ["number.motion_sensor_duration",
                "sensor.davephone_distance",
                "sensor.davephone_floors_ascended",
                "sensor.davephone_floors_descended",
                "sensor.davephone_steps",
                "sensor.davephone_average_active_pace",
                "sensor.davephone_battery_level",
                "sensor.ipad_16_battery_level",
                "sensor.humidity_9",  #office
                "sensor.temperature_10", #office
                "sensor.temperature1", #pressure #office
                "sensor.humidity_12", #livingroom
                "sensor.temperature_13", #livingroom
                "sensor.temperature2", #pressure #livingroom
                "sensor.humidity_15", #basementfront
                "sensor.temperature_16", #basementfront
                "sensor.temperature3", #pressure #basementfront
                "sensor.house_temperature",
                "sensor.house_humidity"
                ]
geoState = ["person.dave_3",
            "device_tracker.davephone"]
sensorRename = {
    "sensor.humidity_9":        "sensor.office_humidity",
    "sensor.temperature_10":    "sensor.office_temp",
    "sensor.temperature1":      "sensor.office_pressure",
    "sensor.humidity_12":       "sensor.livingroom_humidity",
    "sensor.temperature_13":    "sensor.livingroom_temp",
    "sensor.temperature2":      "sensor.livingroom_pressure",
    "sensor.humidity_15":       "sensor.basementfront_humidity",
    "sensor.temperature_16":    "sensor.basementfront_temp",
    "sensor.temperature3":      "sensor.basementfront_pressure"
}
entityMap = {}
for obj in rj:
    entityid = obj['entity_id']
    if entityid in entitiesToExtract:
        objcopy = copy.deepcopy(obj)
        ## always type the state
        objcopy['state_str'] = objcopy['state']
        ## Transform the state to a nubmer if the object is known
        if entityid in numericState:
            objcopy['state_num'] = float(objcopy['state'])
        ## Transform the state to a geo_point if the object is known
        if entityid in geoState:
            objcopy['state_geo'] = [objcopy['attributes']['longitude'], objcopy['attributes']['latitude']]
        ## we don't use the genetic state label
        del objcopy['state']
        if entityid in sensorRename:
            objcopy['entity_id'] = sensorRename[entityid]
        entityMap[objcopy['entity_id']] = objcopy

# print(json.dumps(entityMap, indent=4))

# Define the Elasticsearch index name
# index_name = "hass_sensor_events"
# es_url = os.getenv('ES_URL', 'https://localhost:9200')
# es_user = os.getenv('ES_USER', 'USER')
# es_password = os.getenv('ES_PASS', 'CHANGEME')
# # Define the Elasticsearch client
# es = Elasticsearch(
#     [es_url],
#     basic_auth=(es_user, es_password),
#     verify_certs=True
# )

# Check the connection by getting the cluster health
# health = es.cluster.health()
# print(health)

# Check if the index mapping exists
# if not es.indices.exists(index=index_name):
#     # Define the index mapping
#     index_mapping = {
#         "properties": {
#             "@timestamp": {"type": "date"},
#             "entity_id": {"type": "keyword"},
#             "state_str": {"type": "keyword"},
#             "state_num": {"type": "float"},
#             "state_geo": {"type": "geo_point"},
#             "attributes": {"type": "object"},
#             "last_changed": {"type": "date"},
#             "last_updated": {"type": "date"},
#             "context": {"type": "object"}
#         }
#     }
#     # Create the index with the defined mapping
#     es.indices.create(index=index_name, mappings=index_mapping)


for doc_id in entityMap:
    doc = entityMap[doc_id]
    doc['@timestamp'] = nowiso
    # es.index(index=index_name, document=doc)
    print(json.dumps(doc,indent=4))


# print(json.dumps(entityMap, indent=4))