"""
pytest-recording configuration for E2E tests

VCR.py configuration for recording/replaying HTTP requests to LLM APIs.
"""

import os
import pytest


@pytest.fixture(scope="module")
def vcr_config():
    """
    VCR.py configuration for E2E tests

    - record_mode="once": Record on first run, replay after
    - filter_headers: Remove sensitive auth headers from cassettes
    - decode_compressed_response: Enable reading gzipped responses
    """
    return {
        "record_mode": "once",  # Record cassette once, then replay
        "decode_compressed_response": True,  # Handle gzipped responses
        "filter_headers": [
            ("authorization", "REDACTED"),
            ("x-api-key", "REDACTED"),
        ],
        "match_on": ["method", "scheme", "host", "port", "path", "query"],  # Match criteria
    }


@pytest.fixture(scope="module")
def vcr_cassette_dir(request):
    """
    Custom cassette directory for E2E tests

    Stores all cassettes in tests/fixtures/vcr_cassettes/
    """
    return os.path.join(os.path.dirname(__file__), "..", "fixtures", "vcr_cassettes")
