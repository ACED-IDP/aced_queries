import pathlib
import csv
from gen3.query import Gen3Query
from gen3.auth import get_access_token_with_client_credentials
from aced_queries.auth import Gen3SessionAuth
from dotenv import load_dotenv
import os
import pandas as pd
from aced_queries.guppy_graph import GuppyGraph

def guppy_graph():
      load_dotenv()
      token = get_access_token_with_client_credentials(os.getenv('GEN3_ENDPOINT'),(os.getenv('GEN3_CLIENT_ID'),os.getenv('GEN3_CLIENT_SECRET')),"openid user")
      auth = Gen3SessionAuth(access_token=token)
      
      # load our config from the same directory as the script
      config = pathlib.Path(__file__).parent / 'guppy_graph.config.yaml'

      # greate a guppy graph
      gg = GuppyGraph(Gen3Query(auth), config)
      return gg

def csv_data_observations(gg):
      name_1 = "dict_written_encounter.csv" 
      name_2 = "dict_written.csv"

      obs_aggregation, obs_rows, obs_keys = gg.query('observation')
      observation_aggregations = obs_aggregation._aggregation.observation
      print(sorted(observation_aggregations.keys()))

      assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code', 'predicted_phenotype', 'project_id']

      code_display_counts =  observation_aggregations['code']
      dictdisplay  = code_display_counts.to_dict()

      with open(name_2, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['key','count'])
            writer.writeheader()
            for data in dictdisplay['histogram']:
                  writer.writerow(data)


      code_display_counts =  observation_aggregations['category']
      dictdisplay  = code_display_counts.to_dict()

      with open(name_1, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['key','count'])
            writer.writeheader()
            for data in dictdisplay['histogram']:
                  writer.writerow(data)

      return name_2,name_1



# query guppy for aggregation statistics, the first page of data and the keys for all patients 

gg= guppy_graph()
csv_data_observations(gg)
aggregation, rows, keys = gg.query('patient')
patient_aggregations = aggregation._aggregation.patient
print("SORTED KEYS" ,sorted(patient_aggregations.keys()))
assert sorted(patient_aggregations.keys()) == ['_totalCount', 'gender', 'project_id', 'us_core_race']

print("How many patients?", {}, patient_aggregations._totalCount, len(keys))
print("What are their races?", patient_aggregations['us_core_race'])
print(rows.keys())
print("Number of patients in 1st page", len(rows.patient), "Total number of patients",
      rows._aggregation.patient._totalCount)

print(" ")
print(" ")

file_aggregation, file_rows, file_keys = gg.query('file')
file_aggregations = file_aggregation._aggregation.file
assert sorted(file_aggregations.keys()) == ['_totalCount', 'data_format', 'data_type', 'project_id']

print("How many files?", {}, file_aggregations._totalCount, len(file_keys))
print("what was the data format?", file_aggregations['data_format'])
print(file_rows.keys())
print("Number of patients in 1st page", len(file_rows.file), "Total number of files",
      file_rows._aggregation.file._totalCount)


