"""
Foundation Tests - Validate base components

Tests for SharedMaximusClient and UI components.

Biblical Foundation:
"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
"""
import pytest
from unittest.mock import Mock, patch
import httpx

from core.maximus_integration.shared_client import (
    SharedMaximusClient,
    MaximusService,
    ServiceResponse,
    get_shared_client
)
from ui.components import (
    create_table,
    show_thinking_stream,
    show_results_box,
    show_error,
    confirm_action,
    format_json
)


class TestSharedMaximusClient:
    """Test SharedMaximusClient functionality"""
    
    def test_client_initialization(self):
        """Test client initializes with settings"""
        client = SharedMaximusClient()
        
        assert client.timeout > 0
        assert client.max_retries > 0
        assert len(client.service_urls) > 0
    
    def test_singleton_pattern(self):
        """Test get_shared_client returns same instance"""
        client1 = get_shared_client()
        client2 = get_shared_client()
        
        assert client1 is client2
    
    def test_service_url_mapping(self):
        """Test service URLs are correctly mapped"""
        client = SharedMaximusClient()
        
        # Check all services have URLs
        for service in MaximusService:
            url = client.get_service_url(service)
            assert url, f"No URL for {service.value}"
            assert url.startswith("http"), f"Invalid URL for {service.value}: {url}"
    
    @patch('httpx.Client')
    def test_successful_request(self, mock_client_class):
        """Test successful HTTP request"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        
        mock_client = Mock()
        mock_client.request.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        # Make request
        client = SharedMaximusClient()
        response = client.request(MaximusService.CORE, "/health")
        
        # Validate
        assert response.success is True
        assert response.data == {"status": "ok"}
        assert response.status_code == 200
        assert response.service == "core"
    
    @patch('httpx.Client')
    def test_failed_request(self, mock_client_class):
        """Test failed HTTP request"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        
        mock_client = Mock()
        mock_client.request.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        # Make request
        client = SharedMaximusClient()
        response = client.request(MaximusService.CORE, "/fail")
        
        # Validate
        assert response.success is False
        assert response.status_code == 500
        assert "500" in response.error
    
    @patch('httpx.Client')
    def test_timeout_handling(self, mock_client_class):
        """Test timeout handling with retry"""
        mock_client = Mock()
        mock_client.request.side_effect = httpx.TimeoutException("Timeout")
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        # Make request
        client = SharedMaximusClient()
        response = client.request(MaximusService.CORE, "/slow", timeout=1)
        
        # Validate
        assert response.success is False
        assert "timeout" in response.error.lower()
        # Should retry max_retries times
        assert mock_client.request.call_count == client.max_retries
    
    @patch('httpx.Client')
    def test_health_check(self, mock_client_class):
        """Test health check method"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "healthy",
            "uptime": "2h 15m",
            "version": "1.0.0"
        }
        
        mock_client = Mock()
        mock_client.request.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client
        
        # Health check
        client = SharedMaximusClient()
        response = client.health_check(MaximusService.CORE)
        
        # Validate
        assert response.success is True
        assert response.data["status"] == "healthy"
        
        # Check correct endpoint was called
        call_args = mock_client.request.call_args
        url_arg = call_args[0][1]  # Second positional arg is URL
        assert "/health" in url_arg


class TestUIComponents:
    """Test UI components"""
    
    def test_create_table(self):
        """Test table creation"""
        table = create_table(
            "Test Table",
            [("Name", "left", "bold"), ("Value", "right", "")],
            [["Row1", "Val1"], ["Row2", "Val2"]]
        )
        
        assert table is not None
        assert table.title == "[bold cyan]Test Table"
        assert len(table.columns) == 2
    
    def test_format_json(self):
        """Test JSON formatting"""
        data = {"key": "value", "number": 42}
        syntax = format_json(data)
        
        assert syntax is not None
        # Syntax object from rich doesn't have lexer_name, just check it's created
        assert hasattr(syntax, 'code')
    
    def test_confirm_action_default_yes(self, monkeypatch):
        """Test confirm action with default yes"""
        # Mock Console.input to return empty string
        from rich.console import Console
        monkeypatch.setattr(Console, 'input', lambda self, prompt: "")
        
        # Should return True (default)
        result = confirm_action("Test?", default=True)
        assert result is True
    
    def test_confirm_action_default_no(self, monkeypatch):
        """Test confirm action with default no"""
        # Mock Console.input to return empty string
        from rich.console import Console
        monkeypatch.setattr(Console, 'input', lambda self, prompt: "")
        
        # Should return False (default)
        result = confirm_action("Test?", default=False)
        assert result is False
    
    def test_confirm_action_explicit_yes(self, monkeypatch):
        """Test confirm action with explicit yes"""
        from rich.console import Console
        monkeypatch.setattr(Console, 'input', lambda self, prompt: "y")
        
        result = confirm_action("Test?", default=False)
        assert result is True
    
    def test_confirm_action_explicit_no(self, monkeypatch):
        """Test confirm action with explicit no"""
        from rich.console import Console
        monkeypatch.setattr(Console, 'input', lambda self, prompt: "n")
        
        result = confirm_action("Test?", default=True)
        assert result is False


class TestServiceResponse:
    """Test ServiceResponse dataclass"""
    
    def test_success_response(self):
        """Test success response creation"""
        response = ServiceResponse(
            success=True,
            data={"key": "value"},
            status_code=200,
            response_time_ms=50.5,
            service="core"
        )
        
        assert response.success is True
        assert response.data == {"key": "value"}
        assert response.error is None
        assert response.status_code == 200
        assert response.response_time_ms == 50.5
        assert response.service == "core"
    
    def test_error_response(self):
        """Test error response creation"""
        response = ServiceResponse(
            success=False,
            error="Connection failed",
            status_code=503,
            service="oraculo"
        )
        
        assert response.success is False
        assert response.data is None
        assert response.error == "Connection failed"
        assert response.status_code == 503
        assert response.service == "oraculo"


# Integration tests (require services running)
@pytest.mark.integration
class TestRealServices:
    """Integration tests with real MAXIMUS services"""
    
    def test_real_health_check(self):
        """Test health check against real service (if available)"""
        client = get_shared_client()
        response = client.health_check(MaximusService.CORE, timeout=5)
        
        # If service is running, should succeed
        # If not, should fail gracefully
        assert isinstance(response, ServiceResponse)
        assert response.service == "core"
    
    def test_real_health_check_all(self):
        """Test health check all services (if available)"""
        client = get_shared_client()
        results = client.health_check_all(timeout=3)
        
        # Should return results for all services
        assert len(results) == len(MaximusService)
        
        # All should be ServiceResponse
        for result in results:
            assert isinstance(result, ServiceResponse)
            assert result.service is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
