# aced_queries
Worked examples of ACED queries


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install aced_query_helpers.

```bash
pip install aced_queries
```

## Usage

```python
    import pathlib
    
    from gen3.query import Gen3Query
    
    from aced_queries.auth import Gen3SessionAuth
    from aced_queries.guppy_graph import GuppyGraph

    # assume you've retrieved the access_token from the request
    auth = Gen3SessionAuth(access_token=access_token)
    
    # load our config from the same directory as the script
    config = pathlib.Path(__file__).parent / 'guppy_graph.config.yaml'
    
    # greate a guppy graph
    gg = GuppyGraph(Gen3Query(auth), config)

    # query guppy for aggregation statistics, the first page of data and the keys for all patients 
    aggregation, rows, keys = gg.query('patient')
    patient_aggregations = aggregation._aggregation.patient
    assert sorted(patient_aggregations.keys()) == ['_totalCount', 'extension_0_extension_1_valueString', 'gender',
                                                   'project_id']

    print("How many patients?", {}, patient_aggregations._totalCount, len(keys))
    print("What are their races?", patient_aggregations['extension_0_extension_1_valueString'])
    print(rows.keys())
    print("Number of patients in 1st page", len(rows.patient), "Total number of patients",
          rows._aggregation.patient._totalCount)

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

### Development setup

```commandline
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt 
pip install -r requirements-dev.txt 

```

### Integration test setup

See [Gen3 Service Account]( https://github.com/uc-cdis/fence/blob/master/README.md#register-an-oauth-client-for-a-client-credentials-flow)
Add endpoint, client_id and client_secret to the .env file, alternatively use git secrets

```commandline
$ pytest  --cov=aced_queries --cov-report term-missing
================================================================================ test session starts ================================================================================
platform darwin -- Python 3.9.12, pytest-7.2.0, pluggy-1.0.0
rootdir: /Users/walsbr/aced/query_helpers
plugins: requests-mock-1.10.0, dotenv-0.5.2, cov-4.0.0, anyio-3.6.2, flask-1.2.0
collected 11 items                                                                                                                                                                  

tests/integration/test_guppy_graph.py ....                                                                                                                                    [ 36%]
tests/integration/test_service_account.py .                                                                                                                                   [ 45%]
tests/unit/test_simple.py .                                                                                                                                                   [ 54%]
tests/unit/auth/test_session_auth.py .....                                                                                                                                    [100%]

---------- coverage: platform darwin, python 3.9.12-final-0 ----------
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
aced_queries/__init__.py          0      0   100%
aced_queries/auth.py             31      0   100%
aced_queries/guppy_graph.py      66      0   100%
-----------------------------------------------------------
TOTAL                            97      0   100%


================================================================================ 11 passed in 37.72s
```

## Documentation

To build docs
```commandline

mkdocs serve

```


## License

[MIT](https://choosealicense.com/licenses/mit/)