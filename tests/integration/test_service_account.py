from aced_queries.auth import Gen3SessionAuth
from gen3.query import Gen3Query


def test_service_account(access_token):
    """Test that the service account can read the guppy schema."""
    assert access_token, "Should have retrieved an access token"
    auth = Gen3SessionAuth(access_token=access_token)
    guppy_service = Gen3Query(auth)
    response = guppy_service.graphql_query(
        query_string="""
            {
              __schema {
                queryType {
                  name
                  fields {
                    name
                  }
                }
              }
            }
        """
    )

    fields = [f['name'] for f in response['data']['__schema']['queryType']['fields'] if not f['name'].startswith('_')]
    assert len(fields) > 0, response
