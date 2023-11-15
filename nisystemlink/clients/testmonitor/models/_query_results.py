"""Query results models."""

# Python Modules
from typing import List, Optional

# Third party Modules
from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


from ._testmonitor_models import TestResultResponseObject


class ResultsQueryResponse(JsonModel):
    results: List[TestResultResponseObject]
    """
    Array of results.
    """
    continuation_token: str = Field(None, alias="continuationToken")
    """
    A token which allows the user to resume this query at the next item in the matching result set.
    In order to continue paginating a query, pass this token to the service on a subsequent request.
    The service will respond with a new continuation token.
    To paginate a set of results,
    continue sending requests with the newest continuation token provided by the service,
    until this value is null.
    """
    total_count: Optional[int] = Field(None, alias="totalCount")
    """
    The number of matching results, if returnCount is true.
    This value is not present if returnCount is false.
    """


class QueryResultValuesResponse(JsonModel):
    __root__: List[str]
    """
    Array of strings.
    """