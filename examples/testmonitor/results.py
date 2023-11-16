"""Functionality of Result APIs."""
# Third party models.
from nisystemlink.clients.testmonitor import TestMonitorClient
from nisystemlink.clients.testmonitor.models import (
    CreateTestResultsRequest,
    ResultQueryOrderByField,
    ResultsAdvancedQuery,
    StatusObject,
    StatusType,
    TestResultRequestObject,
    TestResultUpdateRequestObject,
    UpdateTestResultsRequest,
)

# Constant.
WORK_SPACE_ID = "06791634-40bd-4056-89cf-41e29ca8e022"


# Create the TestMonitorClient object.
client = TestMonitorClient()

# Create a Test result.
results_request = CreateTestResultsRequest(
    results=[
        TestResultRequestObject(
            part_number="abcd_def",
            program_name="example_result",
            status=StatusObject(statusType=StatusType.PASSED, statusName="passed"),
            keywords=["example_keywords"],
            properties={"example_key": "example_value"},
            workspace=WORK_SPACE_ID,
        )
    ]
)

example_result = client.create_results(results_request).results[0]
result_id = example_result.id

print("result Created Successfully.")
print(f"Created result Name: {example_result.program_name}")

# Update the result.
update_result_request = UpdateTestResultsRequest(
    results=[
        TestResultUpdateRequestObject(
            id=result_id,
            program_name="updated_result",
            keywords=["updated_keywords"],
            properties={"updated_key": "updated_value"},
        )
    ],
    replace=False,
)
updated_result = client.update_results(request_body=update_result_request).results[0]

print("Result Updated Successfully.")
print(f"Updated result Name: {updated_result.program_name}")

# Query the result.
query_filter = ResultsAdvancedQuery(
    filter="programName == @0",
    substitutions=["updated_result"],
    order_by=ResultQueryOrderByField.PROGRAM_NAME,
    descending=False,
    continuation_token=None,
    return_count=True,
)
queried_result = client.query_results(query_filter=query_filter).results[0]

print("Result Queried Successfully.")
print(f"Queried result Name: {queried_result.program_name}")

# Delete the result.
client.delete_result(resultId=result_id, deleteSteps=True)
print("Result Deleted Successfully")
