"""Create and update result models."""
from typing import List, Optional

from nisystemlink.clients.core._uplink._json_model import JsonModel

from ._testmonitor_models import (
    Error,
    TestResultRequestObject,
    TestResultResponseObject,
    TestResultUpdateFailureObject,
)


class CreateTestResultsRequest(JsonModel):
    results: List[TestResultRequestObject]
    """
    Array of results to be created.
    """


class CreateResultPartialSuccessResponse(JsonModel):
    results: List[TestResultResponseObject]
    """
    Array of created results.
    """
    failed: Optional[List[TestResultRequestObject]]
    """
    Array of failed results.
    """
    error: Optional[Error]
    """
    Default error model.
    """


class ResultUpdatePartialSuccessResponse(JsonModel):
    results: List[TestResultResponseObject]
    """
    Array of results created or updated.
    """
    failed: Optional[List[TestResultUpdateFailureObject]]
    """
    Array of failed results.
    """
    error: Optional[Error]
    """
    Default error model.
    """
