import pytest
import etest
from eshopadmin.db import db_sql_get_recordset_ex


with open(etest.args_file) as file:
    raw_ids = file.read().split('\n')
    query = db_sql_get_recordset_ex('SELECT "ExternalShopId", "ScriptPath" FROM prod."ExternalShopsParsers" '
                                    'WHERE "ExternalShopId" IN ({})'.format(', '.join(raw_ids)))
    ids = {item["ExternalShopId"]: item["ScriptPath"] for item in query}


@pytest.fixture(scope='module', params=ids.items())
def external_parser_data(request):
    yield request.param
