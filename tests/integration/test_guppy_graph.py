import pathlib

import pytest
import requests
from gen3.auth import Gen3Auth
from gen3.query import Gen3Query

from aced_queries.auth import Gen3SessionAuth
from aced_queries.guppy_graph import GuppyGraph


def _run_bad_queries(auth):
    """Query a missing guppy vertices."""
    config = pathlib.Path(__file__).parent / 'guppy_graph.config.yaml'
    gg = GuppyGraph(Gen3Query(auth), config)
    with pytest.raises(Exception):
        _, _, _ = gg.query('foo')


def _run_queries(auth):
    """Query guppy vertices."""
    config = pathlib.Path(__file__).parent / 'guppy_graph.config.yaml'
    gg = GuppyGraph(Gen3Query(auth), config)
    print(f"\n********* {auth.endpoint}")
    print("********* All")
    aggregation, rows, keys = gg.query('patient')
    patient_aggregations = aggregation._aggregation.patient
    assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                                   'project_id']
    print("How many patients?", {}, patient_aggregations._totalCount, len(keys))
    print("What are there races?", patient_aggregations['extension_0_extension_1_valueString'])
    print(rows.keys())
    print("Number of patients in 1st page", len(rows.patient), "Total number of patients",
          rows._aggregation.patient._totalCount)
    aggregation, rows, keys = gg.query('observation')
    observation_aggregations = aggregation._aggregation.observation
    assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code_display', 'encounter_type',
                                                       'project_id']
    print("How many observation 'categories' do they have?", observation_aggregations['category'])
    print("Number of observation in 1st page", len(rows.observation), "Total number of observations",
          rows._aggregation.observation._totalCount)
    print("********* Female")
    patient_filter = {
        "filter": {
            "AND": [
                {"IN": {"gender": ["female"]}}
            ]
        }
    }
    aggregation, rows, keys = gg.query('patient', patient_filter)
    patient_aggregations = aggregation._aggregation.patient
    assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                                   'project_id']
    print("How many patients do we have with 'female' gender?", patient_filter, patient_aggregations._totalCount,
          len(keys))
    print("What are there races?", patient_aggregations['extension_0_extension_1_valueString'])
    print(rows.keys())
    print("Number of patients in 1st page", len(rows.patient), "Total number of patients",
          rows._aggregation.patient._totalCount)
    aggregation, rows, keys = gg.query('observation')
    observation_aggregations = aggregation._aggregation.observation
    assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code_display', 'encounter_type',
                                                       'project_id']
    print("How many observation 'categories' do they have?", observation_aggregations['category'])
    print("Number of observation in 1st page", len(rows.observation), "Total number of observations",
          rows._aggregation.observation._totalCount)
    print("********* laboratory Observations for female patients")
    observation_filter = {"filter": {"AND": [{"IN": {"category": ["laboratory"]}}]}}
    # note we are querying observation first
    aggregation, rows, keys = gg.query('observation', observation_filter)
    observation_aggregations = aggregation._aggregation.observation
    assert sorted(observation_aggregations.keys()) == ['_totalCount', 'category', 'code_display', 'encounter_type',
                                                       'project_id']
    print("How many observation 'categories' do they have?", observation_aggregations['category'])
    # print(json.dumps(observation_filter))
    print("Number of observation in 1st page", len(rows.observation), "Total number of observations",
          rows._aggregation.observation._totalCount)
    # print(rows)
    # patient_filter = {"filter": {'AND': []}}
    aggregation, rows, keys = gg.query('patient')
    patient_aggregations = aggregation._aggregation.patient
    assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                                   'project_id']
    print("How many patients do we have?", {}, patient_aggregations._totalCount, len(keys))
    print("What are there races?", patient_aggregations['extension_0_extension_1_valueString'])
    print(rows.keys())
    print("Number of patients in 1st page", len(rows.patient), "Total number of patients",
          rows._aggregation.patient._totalCount)

    aggregation, rows, keys = gg.query('file')
    file_aggregations = aggregation._aggregation.file
    assert sorted(file_aggregations.keys()) == ['_totalCount', 'data_format', 'data_type', 'project_id']
    print("How many files do they have?", {}, file_aggregations._totalCount, len(keys))
    print("Number of files in 1st page", len(rows.file), "Total number of files",
          rows._aggregation.file._totalCount)


def _check_arborist(access_token, endpoint):
    """Query arborist to get access list."""
    print('\n', access_token)
    arborist_response = requests.get(f'{endpoint}/authz/mapping',
                                     headers={'Authorization': f'bearer {access_token}'})
    arborist_response.raise_for_status()
    print(arborist_response.json())
    assert len(arborist_response.json().keys()) > 0, "should have access to something"


def test_check_arborist(access_token, endpoint):
    """Validate that the service account token has access."""
    print('\n', access_token)
    _check_arborist(access_token, endpoint)


def test_check_arborist_auth(endpoint, client_id, client_secret):
    """Create token using new Gen3Auth parameters.  See https://github.com/uc-cdis/gen3sdk-python/pull/167"""
    auth = Gen3Auth(endpoint=endpoint, client_credentials=(client_id, client_secret))
    access_token = auth.get_access_token()
    _check_arborist(access_token, endpoint)


def test_ok(access_token):
    """Simple test of the guppy graph using access token."""
    auth = Gen3SessionAuth(access_token=access_token)
    _run_queries(auth)


# def test_ok_auth(endpoint, client_id, client_secret):
#     """Simple test of the guppy graph using client_credentials."""
#     auth = Gen3Auth(endpoint=endpoint, client_credentials=(client_id, client_secret))
#     _run_queries(auth)


def test_no_vertex(access_token):
    """Simple test of the guppy graph using access token."""
    auth = Gen3SessionAuth(access_token=access_token)
    _run_bad_queries(auth)
