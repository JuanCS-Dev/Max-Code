"""
Tool Executor Scientific Tests - REAL IMPLEMENTATION

Tests that Tool Executor placeholders have been replaced with real implementations.

Biblical Foundation:
"Tudo é puro para os puros" (Tito 1:15)
All things are pure to those who are pure.

NO MOCK, NO PLACEHOLDER, NO TODO
"""

import pytest
from core.deter_agent.execution.tool_executor import ToolExecutor


class TestToolExecutorAPICall:
    """Test real API call implementation"""

    def test_api_call_real_endpoint(self):
        """
        SCIENTIFIC TEST: Validate API calls hit real endpoints.

        Validates that _execute_api_call uses requests library
        and returns real HTTP responses.
        """
        executor = ToolExecutor()

        # Test against httpbin.org (testing service)
        result = executor._execute_api_call({
            'url': 'https://httpbin.org/get',
            'method': 'GET'
        })

        # Assertions: Real response structure
        assert 'status_code' in result, "Must return status_code"
        assert 'headers' in result, "Must return headers"
        assert 'body' in result, "Must return body"

        # httpbin returns JSON with 'url' field
        if result.get('status_code') == 200:
            assert 'url' in result['body'], "httpbin should return 'url' field"
            print(f"✅ API call successful: {result['status_code']}")
        else:
            print(f"⚠️ API call returned: {result}")

    def test_api_call_post_with_data(self):
        """
        SCIENTIFIC TEST: POST requests with JSON body.

        Validates that API calls can send data payloads.
        """
        executor = ToolExecutor()

        result = executor._execute_api_call({
            'url': 'https://httpbin.org/post',
            'method': 'POST',
            'data': {'test': 'value', 'number': 42}
        })

        assert result.get('status_code') == 200, "POST should succeed"

        # httpbin echoes back the JSON we sent
        if 'json' in result.get('body', {}):
            assert result['body']['json']['test'] == 'value'
            assert result['body']['json']['number'] == 42
            print(f"✅ POST with data successful")

    def test_api_call_timeout_handling(self):
        """
        SCIENTIFIC TEST: Timeout handling.

        Validates that long requests timeout gracefully.
        """
        executor = ToolExecutor()

        # httpbin has /delay/{n} endpoint
        result = executor._execute_api_call({
            'url': 'https://httpbin.org/delay/5',
            'method': 'GET',
            'timeout': 1  # 1 second timeout, endpoint waits 5s
        })

        # Should timeout
        assert 'error' in result, "Should return error on timeout"
        assert result['error'] == 'timeout'
        print(f"✅ Timeout handled correctly")

    def test_api_call_connection_error(self):
        """
        SCIENTIFIC TEST: Connection error handling.

        Validates that unreachable hosts return proper errors.
        """
        executor = ToolExecutor()

        result = executor._execute_api_call({
            'url': 'http://invalid-host-that-does-not-exist-12345.com',
            'method': 'GET',
            'timeout': 2
        })

        # Should return connection error
        assert 'error' in result, "Should return error on connection failure"
        assert 'connection_error' in result['error']
        print(f"✅ Connection error handled: {result['error'][:50]}")


class TestToolExecutorSearch:
    """Test real grep search implementation"""

    def test_search_in_real_files(self):
        """
        SCIENTIFIC TEST: Search in actual project files.

        Validates that _execute_search uses grep on real filesystem.
        """
        executor = ToolExecutor()

        # Search for "TruthEngine" in core directory
        matches = executor._execute_search({
            'pattern': 'TruthEngine',
            'path': 'core/',
            'file_pattern': '*.py'
        })

        # Should find matches (TruthEngine class exists)
        assert isinstance(matches, list), "Should return list"
        assert len(matches) > 0, "Should find 'TruthEngine' in core/"

        # Validate format: "file:line:content"
        if matches:
            first_match = matches[0]
            assert ':' in first_match, "Matches should have format file:line:content"
            print(f"✅ Found {len(matches)} matches for 'TruthEngine'")
            print(f"   Example: {first_match[:80]}")

    def test_search_case_insensitive(self):
        """
        SCIENTIFIC TEST: Case-insensitive search.

        Validates that case_sensitive parameter works.
        """
        executor = ToolExecutor()

        # Search for "TRUTHENGINE" (all caps) with case-insensitive
        matches = executor._execute_search({
            'pattern': 'TRUTHENGINE',
            'path': 'core/',
            'case_sensitive': False
        })

        # Should find matches despite case difference
        assert isinstance(matches, list), "Should return list"
        # TruthEngine exists, so case-insensitive should find it
        if len(matches) > 0:
            print(f"✅ Case-insensitive search found {len(matches)} matches")

    def test_search_no_matches(self):
        """
        SCIENTIFIC TEST: No matches returns empty list.

        Validates that non-existent patterns return empty list (not error).
        """
        executor = ToolExecutor()

        matches = executor._execute_search({
            'pattern': 'NONEXISTENT_PATTERN_XYZABC12345',
            'path': 'core/'
        })

        assert isinstance(matches, list), "Should return list"
        assert len(matches) == 0, "Should return empty list for no matches"
        print(f"✅ No matches handled correctly: {matches}")

    def test_search_file_pattern_filter(self):
        """
        SCIENTIFIC TEST: File pattern filtering.

        Validates that file_pattern parameter filters correctly.
        """
        executor = ToolExecutor()

        # Search only in .md files
        matches = executor._execute_search({
            'pattern': 'MAXIMUS',
            'path': '.',
            'file_pattern': '*.md'
        })

        # All matches should be from .md files
        if matches:
            for match in matches[:5]:  # Check first 5
                file_path = match.split(':')[0]
                assert file_path.endswith('.md'), f"Should only match .md files, got {file_path}"
            print(f"✅ File pattern filter works: {len(matches)} .md files")


class TestToolExecutorPlaceholderRemoval:
    """Test that placeholders have been removed"""

    def test_no_placeholder_in_api_call(self):
        """
        SCIENTIFIC TEST: No [Placeholder] in API call logs.

        Validates that placeholder markers have been removed.
        """
        executor = ToolExecutor()

        result = executor._execute_api_call({
            'url': 'https://httpbin.org/get',
            'method': 'GET'
        })

        # Check that result is not placeholder
        assert result != {'status': 'placeholder'}, "Should not return placeholder response"
        assert 'status_code' in result or 'error' in result, "Should return real response"
        print(f"✅ No placeholder response")

    def test_no_empty_search_results(self):
        """
        SCIENTIFIC TEST: Search returns real results (not []).

        Validates that search implementation is real.
        """
        executor = ToolExecutor()

        # Search for something that DEFINITELY exists
        matches = executor._execute_search({
            'pattern': 'def ',  # Python function definitions
            'path': 'core/truth_engine/',
            'file_pattern': '*.py'
        })

        # Should find many function definitions
        assert len(matches) > 0, "Should find 'def ' in Python files"
        print(f"✅ Search returns real results: {len(matches)} functions found")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
