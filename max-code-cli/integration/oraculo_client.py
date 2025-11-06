"""
Oraculo Service Client - Predictions & Foresight

Production HTTP client for Oraculo Predictive Analytics Service.
Based on real API endpoints from services/oraculo/api.py

Endpoints:
- GET  /health                    # Health check
- GET  /capabilities              # Service capabilities
- POST /predict                   # Generate predictions
- POST /analyze_code              # Code analysis
- POST /auto_implement            # Auto-implement code

Port: 8156 (Docker) | localhost:8156 (dev)
"""

import logging
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

try:
    import httpx
    HTTPX_AVAILABLE = True
except ImportError:
    HTTPX_AVAILABLE = False
    logging.warning("httpx not installed. Install: pip install httpx")

from integration.base_client import BaseHTTPClient

logger = logging.getLogger(__name__)


# Request Models (matching real API)
class PredictionRequest(BaseModel):
    """POST /predict request."""
    data: Dict[str, Any] = Field(..., description="Data to analyze for predictions")
    prediction_type: str = Field(..., description="Type of prediction (e.g., 'threat_level', 'resource_demand')")
    time_horizon: str = Field(..., description="Time horizon for prediction (e.g., '24h', '7d')")


class CodeAnalysisRequest(BaseModel):
    """POST /analyze_code request."""
    code: str = Field(..., description="Code snippet to analyze")
    language: str = Field(..., description="Programming language")
    analysis_type: str = Field(..., description="Type of analysis (e.g., 'vulnerability', 'performance', 'refactoring')")


class ImplementationRequest(BaseModel):
    """POST /auto_implement request."""
    task_description: str = Field(..., description="Description of coding task")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context or existing code")
    target_language: str = Field(..., description="Target programming language")


# Response Models
class HealthStatusResponse(BaseModel):
    """GET /health response."""
    status: str
    service: str
    version: str
    capabilities: List[str]
    degradations: List[str] = []
    apv_stream_manager: Optional[Dict[str, Any]] = None


class CapabilitiesResponse(BaseModel):
    """GET /capabilities response."""
    capabilities: List[str]
    configuration: Dict[str, Any]


class PredictionResult(BaseModel):
    """Prediction result data."""
    prediction_type: str
    confidence: float
    forecast: Dict[str, Any]
    suggestions: List[str] = []


class PredictionResponse(BaseModel):
    """POST /predict response."""
    status: str
    timestamp: str
    prediction: PredictionResult


class CodeAnalysisResult(BaseModel):
    """Code analysis result data."""
    issues_found: int
    severity_breakdown: Dict[str, int]
    recommendations: List[str]
    details: Dict[str, Any]


class CodeAnalysisResponse(BaseModel):
    """POST /analyze_code response."""
    status: str
    timestamp: str
    analysis_result: CodeAnalysisResult


class ImplementationResult(BaseModel):
    """Auto-implementation result data."""
    generated_code: str
    language: str
    implementation_notes: List[str]
    confidence: float
    test_cases: Optional[List[str]] = []


class ImplementationResponse(BaseModel):
    """POST /auto_implement response."""
    status: str
    timestamp: str
    implementation_result: ImplementationResult


if HTTPX_AVAILABLE:
    class OraculoClient(BaseHTTPClient):
        """
        Oraculo Service Client - Predictive Analytics & Foresight.

        Example:
            client = OraculoClient()

            # Get prediction
            prediction = client.predict(
                data={"metric": "cpu_usage", "values": [0.3, 0.5, 0.7]},
                prediction_type="resource_demand",
                time_horizon="24h"
            )
            print(f"Prediction: {prediction.prediction.forecast}")

            # Analyze code
            analysis = client.analyze_code(
                code="def foo(): pass",
                language="python",
                analysis_type="vulnerability"
            )
            print(f"Issues found: {analysis.analysis_result.issues_found}")
        """

        def __init__(self, base_url: str = "http://localhost:8156", **kwargs):
            super().__init__(base_url=base_url, **kwargs)

        def get_health(self) -> HealthStatusResponse:
            """
            Get service health status.

            Returns:
                HealthStatusResponse with status and capabilities
            """
            response = self.get("/health")
            return HealthStatusResponse(**response.json())

        def get_capabilities(self) -> CapabilitiesResponse:
            """
            Get service capabilities and feature flags.

            Returns:
                CapabilitiesResponse with capabilities and configuration
            """
            response = self.get("/capabilities")
            return CapabilitiesResponse(**response.json())

        def predict(
            self,
            data: Dict[str, Any],
            prediction_type: str,
            time_horizon: str
        ) -> PredictionResponse:
            """
            Generate predictive insights based on provided data.

            Args:
                data: Data to analyze for predictions
                prediction_type: Type of prediction (e.g., 'threat_level', 'resource_demand')
                time_horizon: Time horizon for prediction (e.g., '24h', '7d')

            Returns:
                PredictionResponse with prediction results and confidence

            Example:
                result = client.predict(
                    data={"metric": "cpu_usage", "values": [0.3, 0.5, 0.7]},
                    prediction_type="resource_demand",
                    time_horizon="24h"
                )
            """
            request = PredictionRequest(
                data=data,
                prediction_type=prediction_type,
                time_horizon=time_horizon
            )
            response = self.post("/predict", json=request.model_dump())
            return PredictionResponse(**response.json())

        def analyze_code(
            self,
            code: str,
            language: str,
            analysis_type: str
        ) -> CodeAnalysisResponse:
            """
            Analyze code for vulnerabilities, performance issues, or refactoring opportunities.

            Args:
                code: Code snippet to analyze
                language: Programming language (e.g., 'python', 'javascript')
                analysis_type: Type of analysis ('vulnerability', 'performance', 'refactoring')

            Returns:
                CodeAnalysisResponse with analysis results

            Example:
                result = client.analyze_code(
                    code="def foo(): pass",
                    language="python",
                    analysis_type="vulnerability"
                )
            """
            request = CodeAnalysisRequest(
                code=code,
                language=language,
                analysis_type=analysis_type
            )
            response = self.post("/analyze_code", json=request.model_dump())
            return CodeAnalysisResponse(**response.json())

        def auto_implement(
            self,
            task_description: str,
            target_language: str,
            context: Optional[Dict[str, Any]] = None
        ) -> ImplementationResponse:
            """
            Request automated code implementation based on task description.

            Args:
                task_description: Description of coding task
                target_language: Target programming language (e.g., 'python', 'typescript')
                context: Optional additional context or existing code

            Returns:
                ImplementationResponse with generated code

            Example:
                result = client.auto_implement(
                    task_description="Create a function to validate email addresses",
                    target_language="python"
                )
            """
            request = ImplementationRequest(
                task_description=task_description,
                context=context,
                target_language=target_language
            )
            response = self.post("/auto_implement", json=request.model_dump())
            return ImplementationResponse(**response.json())

else:
    class OraculoClient:
        def __init__(self, *args, **kwargs):
            raise ImportError("httpx required: pip install httpx")
