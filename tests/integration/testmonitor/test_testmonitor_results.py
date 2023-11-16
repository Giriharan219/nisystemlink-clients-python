"""Implementation of test class for results APIs of TestMonitor."""
import uuid
from datetime import datetime
from typing import Callable, List, Optional

import pytest
from nisystemlink.clients.auth import AuthClient
from nisystemlink.clients.core import ApiException
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    CreateTestResultsRequest,
    DeleteResultsRequest,
    ResultQueryOrderByField,
    ResultsAdvancedQuery,
    ResultValuesQuery,
    ResultValuesQueryField,
    StatusObject,
    StatusType,
    TestResultRequestObject,
    TestResultResponseObject,
    TestResultUpdateRequestObject,
    UpdateTestResultsRequest,
)
from tests.integration.testmonitor.constants import (
    CreateResultRequest,
    QueryResults,
    UpdateResults,
)


def get_workspace_id() -> Optional[str]:
    """Get Workspace ID.

    Args:
        None
    Returns:
        str: Id of the workspace.
    """
    api_info = AuthClient().get_auth()
    if api_info.workspaces is not None:
        work_space_id = api_info.workspaces[0].id
        return work_space_id

    return None


@pytest.fixture(scope="class")
def client(enterprise_config):
    """Create TestMonitorClient object."""
    return TestMonitorClient(enterprise_config)


@pytest.fixture(scope="class")
def get_result_uuid():
    """Create result_uuid object for results."""

    def _get_result_uuid():
        result_uuid = uuid.uuid4()
        return result_uuid

    yield _get_result_uuid


@pytest.fixture(scope="class")
def create_result_request(get_result_uuid: Callable):
    """Create a request body object for create results API."""

    def _create_result_request():
        result_uuid = get_result_uuid()

        request_body = TestResultRequestObject(
            part_number=f"{CreateResultRequest.PART_NUMBER_PREFIX}_{result_uuid}",
            program_name=CreateResultRequest.PROGRAM_NAME,
            keywords=CreateResultRequest.TEST_KEYWORD,
            properties=CreateResultRequest.PROPERTY,
            workspace=get_workspace_id(),
            status=StatusObject(
                statusType=StatusType.PASSED, statusName=CreateResultRequest.STATUS_NAME
            ),
        )
        return request_body

    yield _create_result_request


@pytest.fixture(scope="class")
def create_result(client: TestMonitorClient):
    """Return a object that creates results."""
    result_ids = []

    def _create_result(result):
        response = client.create_results(result)
        result_ids.extend([result.id for result in response.results])
        return response

    yield _create_result

    # Delete the created results after the tests are completed.
    request_body = DeleteResultsRequest(ids=result_ids, delete_steps=True)
    client.delete_results(request_body)


@pytest.fixture(scope="class")
def create_test_results(create_result: Callable, create_result_request: Callable):
    """Create a set of test results."""
    test_results = []

    request_objects = [create_result_request() for _ in range(4)]
    request_body = CreateTestResultsRequest(results=request_objects)

    response = create_result(request_body)
    test_results.extend(response.results)

    return test_results


@pytest.fixture(scope="class")
def update_result_request():
    """Create a request body object for update results API."""

    def _update_result_request(
        id,
        name=UpdateResults.UPDATED_NAME,
        keywords=UpdateResults.UPDATED_KEYWORD,
        properties=UpdateResults.UPDATED_PROPERTIES,
        status_name=UpdateResults.UPDATED_STATUS_NAME,
    ):
        result_request_details = TestResultUpdateRequestObject(
            id=id,
            status=StatusObject(statusType=StatusType.PASSED, statusName=status_name),
            program_name=name,
            keywords=keywords,
            properties=properties,
        )

        return result_request_details

    yield _update_result_request


@pytest.mark.enterprise
@pytest.mark.integration
class TestSuiteTestMonitorClientResults:
    """Test methods to test results API of TestMonitor."""

    def test__create_results__complete_success(
        self,
        create_result: Callable,
        create_result_request: Callable,
    ):
        """Test a fully successful create results API case."""
        request_object = [create_result_request()]
        request_body = CreateTestResultsRequest(results=request_object)
        response = create_result(request_body)

        assert response.failed is None
        assert response.error is None

        assert len(response.results) == 1

        requested_result = request_body.results[0]
        created_result = response.results[0]

        assert created_result.part_number == requested_result.part_number
        assert created_result.keywords == requested_result.keywords
        assert created_result.status == requested_result.status
        assert created_result.properties == requested_result.properties
        assert created_result.workspace == requested_result.workspace

    def test__create_results__partial_success(
        self,
        create_result: Callable,
        create_result_request: Callable,
    ):
        """Test a partially successful create results API."""
        valid_result = create_result_request()
        duplicate_result = TestResultRequestObject(
            program_name=CreateResultRequest.PROGRAM_NAME,
            status=StatusObject(status_type=StatusType.PASSED),
            workspace=CreateResultRequest.INVALID_ID,
        )
        request_body = CreateTestResultsRequest(
            results=[valid_result, duplicate_result]
        )
        response = create_result(request_body)

        assert response.error is not None
        assert response.failed is not None
        assert len(response.results) == 1

    def test__get_result(
        self,
        client: TestMonitorClient,
        create_test_results: List[TestResultResponseObject],
    ):
        """Test complete successful get result API."""
        test_result = create_test_results[0]
        test_result_details = client.get_result(test_result.id)

        assert test_result_details.part_number == test_result.part_number
        assert test_result_details.keywords == test_result.keywords
        assert test_result_details.properties == test_result.properties
        assert test_result_details.status == test_result.status

        assert test_result_details.updated_at is not None

        updated_at_timestamp = test_result_details.updated_at.timestamp()
        current_timestamp = datetime.now().timestamp()

        assert updated_at_timestamp == pytest.approx(
            current_timestamp,
            abs=CreateResultRequest.MAX_TIME_DIFF_IN_SECONDS,
        )

    def test__get_result__invalid_id(self, client: TestMonitorClient):
        """Test get result API with invalid id."""
        with pytest.raises(ApiException, match="404 Not Found"):
            client.get_result(CreateResultRequest.INVALID_ID)

    def test__query_results(self, client: TestMonitorClient):
        """Test query results API"""
        result_query_body = ResultsAdvancedQuery(
            filter=QueryResults.FILTER,
            substitutions=QueryResults.SUBSTITUTIONS,
            order_by=ResultQueryOrderByField.PROGRAM_NAME,
            projection=QueryResults.PROJECTION,
            descending=False,
            return_count=True,
        )

        query_response = client.query_results(result_query_body)

        assert query_response.results is not None
        assert query_response.continuation_token is not None
        assert query_response.total_count is not None
        assert query_response.total_count > 0

    def test__get_results(self, client: TestMonitorClient):
        """Test get results API."""
        get_results_response = client.get_results(
            returnCount=True,
            take=QueryResults.TAKE_COUNT,
            continuationToken=None,
        )

        assert get_results_response.total_count is not None
        assert get_results_response.total_count > 0
        assert get_results_response.continuation_token is not None
        assert get_results_response.results is not None
        assert len(get_results_response.results) == QueryResults.TAKE_COUNT

    def test__delete_result(
        self,
        client: TestMonitorClient,
        create_result: Callable,
        create_result_request: Callable,
    ):
        """Test delete result API."""
        result_details = create_result_request()
        request_body = CreateTestResultsRequest(results=[result_details])
        new_result = create_result(request_body)

        id = new_result.results[0].id
        deleted_result_response = client.delete_result(resultId=id, deleteSteps=True)

        assert deleted_result_response is None

        with pytest.raises(ApiException, match="404 Not Found"):
            client.get_result(id)

    def test_delete_results(
        self,
        client: TestMonitorClient,
        create_result: Callable,
        create_result_request: Callable,
    ):
        """Test delete results API."""
        result_details = [create_result_request() for _ in range(3)]
        request_body = CreateTestResultsRequest(results=result_details)
        created_results = create_result(request_body)

        result_ids = [result.id for result in created_results.results]
        delete_results_request = DeleteResultsRequest(ids=result_ids, deleteSteps=True)
        deleted_results_response = client.delete_results(delete_results_request)

        assert deleted_results_response is None

        for result_id in result_ids:
            with pytest.raises(ApiException, match="404 Not Found"):
                client.get_result(result_id)

    def test_update_result_with_replacement(
        self,
        client: TestMonitorClient,
        create_test_results: List[TestResultResponseObject],
        update_result_request: Callable,
    ):
        """Test update result API with replace key."""
        new_result_info = update_result_request(create_test_results[1].id)
        request_body = UpdateTestResultsRequest(results=[new_result_info], replace=True)
        response = client.update_results(request_body)
        updated_result = response.results[0]

        assert updated_result.program_name == UpdateResults.UPDATED_NAME
        assert updated_result.properties == UpdateResults.UPDATED_PROPERTIES
        assert updated_result.keywords == UpdateResults.UPDATED_KEYWORD

        assert updated_result.status is not None
        assert updated_result.status.status_name == UpdateResults.UPDATED_STATUS_NAME

    def test_update_result_without_replacement(
        self,
        client: TestMonitorClient,
        create_test_results: List[TestResultResponseObject],
        update_result_request: Callable,
    ):
        """Test update result API without replace key."""
        existing_result = client.get_result(create_test_results[2].id)
        new_result_info = update_result_request(id=create_test_results[2].id)
        request_body = UpdateTestResultsRequest(
            results=[new_result_info], replace=False, determineStatusFromSteps=False
        )
        response = client.update_results(request_body)
        updated_result = response.results[0]

        assert updated_result.program_name == UpdateResults.UPDATED_NAME
        assert (
            updated_result.keywords is not None and existing_result.keywords is not None
        )
        assert (
            updated_result.properties is not None
            and existing_result.properties is not None
        )
        assert len(updated_result.keywords) == len(existing_result.keywords) + 1
        assert len(updated_result.properties) == len(existing_result.properties) + 1

    def test__update_results__partial_success(
        self,
        client: TestMonitorClient,
        create_test_results: List[TestResultResponseObject],
        update_result_request: Callable,
    ):
        """Test partially successful update results API."""
        valid_result_info = update_result_request(id=create_test_results[3].id)
        invalid_result_info = update_result_request(id=CreateResultRequest.INVALID_ID)

        # Update multiple results with one of the results being invalid and check the response.
        request_body = UpdateTestResultsRequest(
            results=[valid_result_info, invalid_result_info],
            replace=False,
        )

        response = client.update_results(request_body)

        assert len(response.results) == 1
        assert response.failed is not None
        assert response.error is not None

    def test__query_product_values(self, client: TestMonitorClient):
        """Test query result values API."""
        request_body = ResultValuesQuery(
            field=ResultValuesQueryField.PROGRAM_NAME,
            filter=QueryResults.FILTER,
            substitutions=QueryResults.SUBSTITUTIONS,
            starts_with=QueryResults.STARTS_WITH,
        )

        response = client.query_result_values(request_body)
        assert len(response.__root__) == 1
