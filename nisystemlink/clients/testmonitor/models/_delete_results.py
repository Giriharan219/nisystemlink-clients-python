"""Delete results model."""

# Python Modules
from typing import List

# Third party Modules
from nisystemlink.clients.core._uplink._json_model import JsonModel
from pydantic import Field


class DeleteResultsRequest(JsonModel):
    ids: List[str]
    """
    Array of result ids to delete.
    """
    delete_steps: bool = Field(True, alias='deleteSteps')
    """
    Delete the steps associated with the results.
    """