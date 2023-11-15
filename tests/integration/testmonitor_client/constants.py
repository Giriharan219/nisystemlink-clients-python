"""Constants to be used for test implementation of Results API."""
from nisystemlink.clients.testmonitor.models import ResultField


class UpdateResults:
    """Update results."""

    UPDATED_NAME = "NewResult"
    UPDATED_KEYWORD = ["NewKeyword"]
    UPDATED_PROPERTIES = {"NewKey": "NewValue"}
    UPDATED_STATUS_NAME = "Done"


class CreateResultRequest:
    """Create result request."""

    PART_NUMBER_PREFIX = "Test"
    PROGRAM_NAME = "_TEST_RESULT"
    TEST_KEYWORD = ["TestKeyword"]
    PROPERTY = {"TestKey": "TestValue"}

    STATUS_NAME = "passed"
    HOST_NAME = "My-Host"
    TOTAL_TIME_IN_SECONDS = 2.7
    INVALID_ID = "invalid_id12323"
    MAX_TIME_DIFF_IN_SECONDS = 20


class QueryResults:
    """Query results."""

    FILTER = "programName == @0"
    SUBSTITUTIONS = [CreateResultRequest.PROGRAM_NAME]
    PROJECTION = [ResultField.PROGRAM_NAME]
    STARTS_WITH = "_T"
    TAKE_COUNT = 1000
