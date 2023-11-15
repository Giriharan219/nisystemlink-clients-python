"""Implementation of TestMonitorClient Results."""
from typing import Optional

from nisystemlink.clients import core
from nisystemlink.clients.core._uplink._base_client import BaseClient
from nisystemlink.clients.core._uplink._methods import delete, get, post
from nisystemlink.clients.testmonitor import models
from uplink import Path, Query


class TestMonitorClient(BaseClient):
    """Access the Result APIs of TestMonitor."""

    def __init__(self, configuration: Optional[core.HttpConfiguration] = None):
        """Initialize an instance of the TestMonitorClient.

        Args:
            configuration: Defines the web server to connect to and information about
                how to connect. If not provided, an instance of
                :class:`JupyterHttpConfiguration <nisystemlink.clients.core.JupyterHttpConfiguration>` # noqa: W505
                is used.

        Raises:
            ApiException: if unable to communicate with the TestMonitor Service.
        """
        if configuration is None:
            configuration = core.JupyterHttpConfiguration()

        super().__init__(configuration, "/nitestmonitor/v2/")

    # versioning

    @get("")
    def api_info(self) -> models.V2Operations:
        """Get information about available API operations.

        Returns:
            Information about available API operations.
        """
        ...

    # results

    @post("query-results")
    def query_results(
        self, query_filter: models.ResultsAdvancedQuery
    ) -> models.ResultsQueryResponse:
        """Query test results based on filter.

        Args:
            query_filter : Filter to be applied for test results.

        Returns:
            List of test results.
        """
        ...

    @get("results", args=[Query, Query, Query])
    def get_results(
        self,
        continuationToken: Optional[str],
        take: Optional[int],
        returnCount: bool,
    ) -> models.ResultsQueryResponse:
        """Get test result details for multiple results.

        Args:
            continuationToken : Token used to paginate results.
            take : Limit test results list to a specified number.
            returnCount : Total count of test results.

        Returns:
            List of results.
        """
        ...

    @post("results")
    def create_results(
        self, request_body: models.CreateTestResultsRequest
    ) -> models.CreateResultPartialSuccessResponse:
        """Create new test results with given result details.

        Args:
            request_body :  Request body of test results.

        Returns:
            Details of created test results.
        """
        ...

    @get("results/{resultId}")
    def get_result(self, resultId: str) -> models.TestResultResponseObject:
        """Get test result details of a single test result.

        Args:
            resultId : Unique ID of a test result.

        Returns:
            Details of specified test result.
        """
        ...

    @delete("results/{resultId}", args=[Path, Query])
    def delete_result(self, resultId: str, deleteSteps: bool) -> None:
        """Delete a test result.

        Args:
            resultId : Result ID to be deleted.
            deleteSteps : Delete the steps associated with results.

        Returns:
            None
        """
        ...

    @post("query-result-values")
    def query_result_values(
        self, result_query: models.ResultValuesQuery
    ) -> models.QueryResultValuesResponse:
        """Get test result values based on a filter.

        Args:
            result_query : Filter to be applied for test results.

        Returns:
            List of values.
        """
        ...

    @post("update-results")
    def update_results(
        self, request_body: models.UpdateTestResultsRequest
    ) -> models.ResultUpdatePartialSuccessResponse:
        """Update multiple test results.

        Args:
            request_body : Updated details of test results.

        Returns:
            Details of updated test results.
        """
        ...

    @post("delete-results")
    def delete_results(self, request_body: models.DeleteResultsRequest) -> None:
        """Delete multiple test results.

        Args:
            request_body : List of test result IDs to be deleted.

        Returns:
            None
        """
        ...
