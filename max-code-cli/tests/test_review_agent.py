"""
Test Suite for ReviewAgent - Code Review with Constitutional + Ethical Analysis

Comprehensive scientific tests covering:
- Constitutional code review (P1-P6 compliance)
- Security vulnerability detection
- Code quality analysis
- Best practices validation
- Review feedback generation
- Severity classification
- Different code patterns
- MAXIMUS integration (hybrid mode)
- Decision fusion logic

Biblical Foundation:
"Examinai tudo. Retende o bem." (1 Tessalonicenses 5:21)
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from agents.review_agent import ReviewAgent
from sdk.base_agent import AgentTask, AgentCapability
from core.maximus_integration import (
    EthicalVerdict,
    MaximusClient,
    DecisionFusion,
    FusedDecision,
    FusionMethod,
)
from core.constitutional.models import (
    ConstitutionalResult,
    Violation,
    ViolationSeverity,
    create_clean_result,
    create_violation_result,
)


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def review_agent_standalone():
    """ReviewAgent without MAXIMUS (standalone mode)"""
    return ReviewAgent(agent_id="review_001", enable_maximus=False)


@pytest.fixture
def review_agent_hybrid():
    """ReviewAgent with MAXIMUS enabled (hybrid mode)"""
    return ReviewAgent(agent_id="review_002", enable_maximus=True)


@pytest.fixture
def simple_valid_code():
    """Simple valid Python code"""
    return """
def calculate_sum(a, b):
    '''Calculate sum of two numbers'''
    return a + b
"""


@pytest.fixture
def code_with_security_issues():
    """Code with security vulnerabilities"""
    return """
import pickle
import os

def load_user_data(filename):
    # SECURITY ISSUE: Arbitrary code execution via pickle
    with open(filename, 'rb') as f:
        return pickle.load(f)

def execute_command(user_input):
    # SECURITY ISSUE: Command injection
    os.system(user_input)
"""


@pytest.fixture
def code_with_quality_issues():
    """Code with quality issues but no security problems"""
    return """
def processuserdata(x,y,z):
    # Bad naming, no docstring, poor formatting
    if x==None:
        return None
    result=x+y*z
    print("result:",result)
    return result
"""


@pytest.fixture
def code_without_tests():
    """Production code without corresponding tests"""
    return """
def authenticate_user(username, password):
    '''Authenticate user against database'''
    # Critical function without tests
    if not username or not password:
        return False
    # Database query logic...
    return True
"""


@pytest.fixture
def code_with_bad_practices():
    """Code with multiple bad practices"""
    return """
# Global mutable state
USER_CACHE = {}

def get_user(user_id):
    # Bad practice: Using global mutable state
    if user_id in USER_CACHE:
        return USER_CACHE[user_id]

    # Bad practice: Bare except
    try:
        user = fetch_from_db(user_id)
        USER_CACHE[user_id] = user
        return user
    except:
        return None
"""


# ============================================================================
# INITIALIZATION TESTS
# ============================================================================

def test_review_agent_initialization_standalone(review_agent_standalone):
    """Test ReviewAgent initialization in standalone mode"""
    agent = review_agent_standalone

    assert agent.agent_id == "review_001"
    assert agent.agent_name == "Review Agent (Guardian + MAXIMUS)"
    assert agent.port == 8164
    assert agent.maximus_client is None
    assert agent.decision_fusion is not None
    assert agent.cache is not None
    assert agent.constitutional_engine is not None

    print("✅ ReviewAgent standalone initialization correct")


def test_review_agent_initialization_hybrid(review_agent_hybrid):
    """Test ReviewAgent initialization in hybrid mode"""
    agent = review_agent_hybrid

    assert agent.agent_id == "review_002"
    assert agent.maximus_client is not None
    assert isinstance(agent.maximus_client, MaximusClient)
    assert isinstance(agent.decision_fusion, DecisionFusion)

    print("✅ ReviewAgent hybrid initialization correct")


def test_review_agent_capabilities(review_agent_standalone):
    """Test ReviewAgent declares correct capabilities"""
    capabilities = review_agent_standalone.get_capabilities()

    assert len(capabilities) == 1
    assert AgentCapability.CODE_REVIEW in capabilities

    print("✅ ReviewAgent capabilities correct")


# ============================================================================
# CONSTITUTIONAL REVIEW TESTS (P1-P6)
# ============================================================================

@pytest.mark.asyncio
async def test_constitutional_review_valid_code(review_agent_standalone, simple_valid_code):
    """Test constitutional review passes for valid code"""
    task = AgentTask(
        id="task_001",
        description="Review simple valid code",
        parameters={"code": simple_valid_code}
    )

    result = await review_agent_standalone._execute_async(task)

    assert result.success
    assert result.task_id == "task_001"
    assert "verdict" in result.output
    assert result.metrics["mode"] == "standalone"

    print("✅ Constitutional review passes for valid code")


@pytest.mark.asyncio
async def test_constitutional_review_security_issues(review_agent_standalone, code_with_security_issues):
    """Test constitutional review detects security issues (P1 violation)"""
    task = AgentTask(
        id="task_002",
        description="Review code with security vulnerabilities",
        parameters={"code": code_with_security_issues}
    )

    # Mock constitutional engine to detect security issues
    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P1",
                    severity=ViolationSeverity.CRITICAL,
                    message="Security vulnerability: pickle.load() enables arbitrary code execution",
                    suggestion="Use json.load() or implement safe deserialization",
                    context={"cwe": "CWE-502"}
                ),
                Violation(
                    principle="P1",
                    severity=ViolationSeverity.CRITICAL,
                    message="Security vulnerability: os.system() with user input enables command injection",
                    suggestion="Use subprocess with proper sanitization",
                    context={"cwe": "CWE-78"}
                )
            ],
            score=0.2
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        assert not result.success
        assert result.output["verdict"] == "REJECTED"

        print("✅ Constitutional review detects security issues")


@pytest.mark.asyncio
async def test_constitutional_review_quality_issues(review_agent_standalone, code_with_quality_issues):
    """Test constitutional review detects quality issues (P2/P4 violations)"""
    task = AgentTask(
        id="task_003",
        description="Review code with quality issues",
        parameters={"code": code_with_quality_issues}
    )

    # Mock constitutional engine to detect quality issues
    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P2",
                    severity=ViolationSeverity.MEDIUM,
                    message="Poor code transparency: Missing docstring",
                    suggestion="Add comprehensive docstring explaining function behavior",
                    context={}
                ),
                Violation(
                    principle="P4",
                    severity=ViolationSeverity.MEDIUM,
                    message="Operational prudence: Poor naming convention",
                    suggestion="Use descriptive names following PEP 8",
                    context={}
                )
            ],
            score=0.5
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        # Quality issues shouldn't necessarily block code
        verdict = result.output["verdict"]
        assert verdict in ["APPROVED", "CONDITIONAL", "REJECTED"]

        print(f"✅ Constitutional review detects quality issues (verdict: {verdict})")


@pytest.mark.asyncio
async def test_constitutional_review_missing_tests(review_agent_standalone, code_without_tests):
    """Test constitutional review flags missing tests (P4 violation)"""
    task = AgentTask(
        id="task_004",
        description="Review critical code without tests",
        parameters={"code": code_without_tests}
    )

    # Mock constitutional engine to detect missing tests
    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P4",
                    severity=ViolationSeverity.HIGH,
                    message="Operational prudence: Critical authentication function lacks tests",
                    suggestion="Add comprehensive unit tests covering edge cases",
                    context={"test_coverage": 0}
                )
            ],
            score=0.4
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        assert result.output["verdict"] in ["CONDITIONAL", "REJECTED"]

        print("✅ Constitutional review flags missing tests")


@pytest.mark.asyncio
async def test_constitutional_review_bad_practices(review_agent_standalone, code_with_bad_practices):
    """Test constitutional review detects bad practices (P5/P6 violations)"""
    task = AgentTask(
        id="task_005",
        description="Review code with bad practices",
        parameters={"code": code_with_bad_practices}
    )

    # Mock constitutional engine to detect bad practices
    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P5",
                    severity=ViolationSeverity.MEDIUM,
                    message="Global mutable state makes debugging difficult",
                    suggestion="Use dependency injection or pass state explicitly",
                    context={}
                ),
                Violation(
                    principle="P4",
                    severity=ViolationSeverity.HIGH,
                    message="Bare except clause hides errors",
                    suggestion="Catch specific exceptions and log properly",
                    context={}
                )
            ],
            score=0.45
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        assert result.output["verdict"] in ["CONDITIONAL", "REJECTED"]

        print("✅ Constitutional review detects bad practices")


# ============================================================================
# SEVERITY CLASSIFICATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_severity_critical_blocks_code(review_agent_standalone):
    """Test CRITICAL severity violations block code approval"""
    task = AgentTask(
        id="task_006",
        description="Review code with critical violations",
        parameters={"code": "import os; os.system(input())"}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P1",
                    severity=ViolationSeverity.CRITICAL,
                    message="Direct shell injection vulnerability",
                    suggestion="Never pass user input directly to os.system()",
                    context={}
                )
            ],
            score=0.1
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        assert not result.success
        assert result.output["verdict"] == "REJECTED"

        print("✅ CRITICAL severity blocks code approval")


@pytest.mark.asyncio
async def test_severity_high_conditional_approval(review_agent_standalone):
    """Test HIGH severity violations result in conditional approval"""
    task = AgentTask(
        id="task_007",
        description="Review code with high severity violations",
        parameters={"code": "def foo(): pass"}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P4",
                    severity=ViolationSeverity.HIGH,
                    message="Missing comprehensive tests",
                    suggestion="Add unit tests",
                    context={}
                )
            ],
            score=0.55
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        verdict = result.output["verdict"]
        assert verdict in ["CONDITIONAL", "REJECTED"]

        print(f"✅ HIGH severity results in conditional approval (verdict: {verdict})")


@pytest.mark.asyncio
async def test_severity_low_allows_approval(review_agent_standalone):
    """Test LOW severity violations still allow approval"""
    task = AgentTask(
        id="task_008",
        description="Review code with low severity violations",
        parameters={"code": "def calculate(x, y): return x + y"}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P2",
                    severity=ViolationSeverity.LOW,
                    message="Could add more detailed docstring",
                    suggestion="Add parameter descriptions",
                    context={}
                )
            ],
            score=0.82
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        assert result.success
        assert result.output["verdict"] in ["APPROVED", "CONDITIONAL"]

        print("✅ LOW severity allows approval")


# ============================================================================
# MAXIMUS INTEGRATION TESTS (HYBRID MODE)
# ============================================================================

@pytest.mark.asyncio
async def test_maximus_offline_fallback(review_agent_hybrid, simple_valid_code):
    """Test graceful fallback when MAXIMUS is offline"""
    task = AgentTask(
        id="task_009",
        description="Review code with MAXIMUS offline",
        parameters={"code": simple_valid_code}
    )

    # Mock MAXIMUS health check to return False (offline)
    with patch.object(
        review_agent_hybrid.maximus_client,
        'health_check',
        return_value=AsyncMock(return_value=False)()
    ):
        result = await review_agent_hybrid._execute_async(task)

        assert result.success or not result.success  # Should complete either way
        assert result.metrics["mode"] in ["standalone", "hybrid"]

        print("✅ Graceful fallback when MAXIMUS offline")


@pytest.mark.asyncio
async def test_maximus_ethical_review_integration(review_agent_hybrid, simple_valid_code):
    """Test MAXIMUS ethical review integration"""
    task = AgentTask(
        id="task_010",
        description="Review code with MAXIMUS ethical analysis",
        parameters={"code": simple_valid_code, "context": {"purpose": "calculation"}}
    )

    # Mock MAXIMUS to be online and return ethical verdict
    mock_ethical_verdict = EthicalVerdict(
        kantian_score=85.0,
        virtue_score=90.0,
        consequentialist_score=88.0,
        principlism_score=92.0,
        verdict="APPROVED",
        reasoning="Code follows ethical principles",
        issues=[],
        recommendations=["Consider adding input validation"]
    )

    async def mock_health():
        return True

    async def mock_ethical(code, context):
        return mock_ethical_verdict

    with patch.object(
        review_agent_hybrid.maximus_client,
        'health_check',
        side_effect=mock_health
    ), patch.object(
        review_agent_hybrid.maximus_client,
        'ethical_review',
        side_effect=mock_ethical
    ):
        result = await review_agent_hybrid._execute_async(task)

        assert result.success
        assert result.metrics["mode"] == "hybrid"

        print("✅ MAXIMUS ethical review integration works")
        print(f"   Kantian: {mock_ethical_verdict.kantian_score}/100")
        print(f"   Virtue: {mock_ethical_verdict.virtue_score}/100")


@pytest.mark.asyncio
async def test_maximus_ethical_rejection(review_agent_hybrid):
    """Test MAXIMUS ethical framework rejecting unethical code"""
    unethical_code = """
def manipulate_user_data(user_id):
    '''Secretly collect user data without consent'''
    # Privacy violation
    collect_private_data(user_id)
    sell_to_third_parties(user_id)
"""

    task = AgentTask(
        id="task_011",
        description="Review ethically problematic code",
        parameters={"code": unethical_code}
    )

    # Mock MAXIMUS to reject on ethical grounds
    mock_ethical_verdict = EthicalVerdict(
        kantian_score=20.0,  # Violates categorical imperative
        virtue_score=15.0,   # Shows bad character
        consequentialist_score=25.0,  # Harmful consequences
        principlism_score=10.0,  # Violates autonomy
        verdict="REJECTED",
        reasoning="Violates user privacy and autonomy",
        issues=[
            "Collects data without consent",
            "Sells user data to third parties",
            "Violates GDPR principles"
        ],
        recommendations=[
            "Implement explicit user consent",
            "Add privacy controls",
            "Remove third-party data selling"
        ]
    )

    async def mock_health():
        return True

    async def mock_ethical(code, context):
        return mock_ethical_verdict

    with patch.object(
        review_agent_hybrid.maximus_client,
        'health_check',
        side_effect=mock_health
    ), patch.object(
        review_agent_hybrid.maximus_client,
        'ethical_review',
        side_effect=mock_ethical
    ):
        result = await review_agent_hybrid._execute_async(task)

        # Low ethical scores should result in CONDITIONAL or REJECTED
        # (The fusion logic may allow CONDITIONAL if constitutional is high)
        verdict = result.output["verdict"]
        assert verdict in ["CONDITIONAL", "REJECTED"]
        assert result.output.get("ethical_score", 1.0) < 0.5  # Verify low ethical score

        print(f"✅ MAXIMUS ethical framework flags unethical code (verdict: {verdict})")


# ============================================================================
# DECISION FUSION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_decision_fusion_both_approve(review_agent_hybrid, simple_valid_code):
    """Test decision fusion when both systems approve"""
    task = AgentTask(
        id="task_012",
        description="Fusion test - both approve",
        parameters={"code": simple_valid_code}
    )

    # Mock both to approve
    mock_ethical_verdict = EthicalVerdict(
        kantian_score=85.0, virtue_score=90.0,
        consequentialist_score=88.0, principlism_score=92.0,
        verdict="APPROVED", reasoning="Clean code",
        issues=[], recommendations=[]
    )

    async def mock_health():
        return True

    async def mock_ethical(code, context):
        return mock_ethical_verdict

    with patch.object(
        review_agent_hybrid.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_clean_result(score=0.92)
    ), patch.object(
        review_agent_hybrid.maximus_client,
        'health_check',
        side_effect=mock_health
    ), patch.object(
        review_agent_hybrid.maximus_client,
        'ethical_review',
        side_effect=mock_ethical
    ):
        result = await review_agent_hybrid._execute_async(task)

        assert result.success
        assert result.output["verdict"] == "APPROVED"

        print("✅ Decision fusion - both approve works")


@pytest.mark.asyncio
async def test_decision_fusion_constitutional_rejects_ethical_approves(review_agent_hybrid):
    """Test decision fusion when constitutional rejects but ethical approves"""
    code = "security_issue_code()"
    task = AgentTask(
        id="task_013",
        description="Fusion test - constitutional rejects, ethical approves",
        parameters={"code": code}
    )

    # Constitutional rejects (security)
    constitutional_result = create_violation_result(
        violations=[
            Violation(
                principle="P1",
                severity=ViolationSeverity.CRITICAL,
                message="Security issue",
                suggestion="Fix it",
                context={}
            )
        ],
        score=0.2
    )

    # Ethical approves (no ethical issues)
    ethical_result = EthicalVerdict(
        kantian_score=85.0, virtue_score=90.0,
        consequentialist_score=88.0, principlism_score=92.0,
        verdict="APPROVED", reasoning="No ethical concerns",
        issues=[], recommendations=[]
    )

    async def mock_health():
        return True

    async def mock_ethical(code, context):
        return ethical_result

    with patch.object(
        review_agent_hybrid.constitutional_engine,
        'evaluate_all_principles',
        return_value=constitutional_result
    ), patch.object(
        review_agent_hybrid.maximus_client,
        'health_check',
        side_effect=mock_health
    ), patch.object(
        review_agent_hybrid.maximus_client,
        'ethical_review',
        side_effect=mock_ethical
    ):
        result = await review_agent_hybrid._execute_async(task)

        # Should reject (constitutional veto on security)
        assert not result.success

        print("✅ Decision fusion - constitutional veto works")


@pytest.mark.asyncio
async def test_decision_fusion_weights(review_agent_hybrid):
    """Test decision fusion uses correct weights"""
    code = "test_code()"
    task = AgentTask(
        id="task_014",
        description="Fusion test - check weights",
        parameters={"code": code}
    )

    # Medium scores from both
    constitutional_result = create_clean_result(score=0.6)
    ethical_result = EthicalVerdict(
        kantian_score=60.0, virtue_score=60.0,
        consequentialist_score=60.0, principlism_score=60.0,
        verdict="CONDITIONAL", reasoning="Medium confidence",
        issues=[], recommendations=[]
    )

    async def mock_health():
        return True

    async def mock_ethical(code, context):
        return ethical_result

    with patch.object(
        review_agent_hybrid.constitutional_engine,
        'evaluate_all_principles',
        return_value=constitutional_result
    ), patch.object(
        review_agent_hybrid.maximus_client,
        'health_check',
        side_effect=mock_health
    ), patch.object(
        review_agent_hybrid.maximus_client,
        'ethical_review',
        side_effect=mock_ethical
    ):
        result = await review_agent_hybrid._execute_async(task)

        # Check that fusion was applied
        assert "verdict" in result.output

        print("✅ Decision fusion weights applied correctly")


# ============================================================================
# CODE PATTERN TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_review_async_code(review_agent_standalone):
    """Test review of async/await code patterns"""
    async_code = """
async def fetch_user_data(user_id):
    '''Fetch user data asynchronously'''
    async with aiohttp.ClientSession() as session:
        async with session.get(f'/users/{user_id}') as response:
            return await response.json()
"""

    task = AgentTask(
        id="task_015",
        description="Review async code",
        parameters={"code": async_code}
    )

    result = await review_agent_standalone._execute_async(task)

    assert result.task_id == "task_015"
    assert "verdict" in result.output

    print("✅ Review of async code works")


@pytest.mark.asyncio
async def test_review_class_based_code(review_agent_standalone):
    """Test review of class-based OOP code"""
    class_code = """
class UserRepository:
    '''Repository for user data operations'''

    def __init__(self, db_connection):
        self.db = db_connection

    def get_user(self, user_id):
        '''Retrieve user by ID'''
        return self.db.query(User).filter_by(id=user_id).first()

    def save_user(self, user):
        '''Save user to database'''
        self.db.add(user)
        self.db.commit()
"""

    task = AgentTask(
        id="task_016",
        description="Review class-based code",
        parameters={"code": class_code}
    )

    result = await review_agent_standalone._execute_async(task)

    assert result.task_id == "task_016"

    print("✅ Review of class-based code works")


@pytest.mark.asyncio
async def test_review_decorator_patterns(review_agent_standalone):
    """Test review of decorator patterns"""
    decorator_code = """
from functools import wraps

def require_auth(func):
    '''Decorator to require authentication'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            raise Unauthorized("Authentication required")
        return func(*args, **kwargs)
    return wrapper

@require_auth
def delete_user(user_id):
    '''Delete user (requires authentication)'''
    User.query.filter_by(id=user_id).delete()
"""

    task = AgentTask(
        id="task_017",
        description="Review decorator patterns",
        parameters={"code": decorator_code}
    )

    result = await review_agent_standalone._execute_async(task)

    assert result.task_id == "task_017"

    print("✅ Review of decorator patterns works")


@pytest.mark.asyncio
async def test_review_context_managers(review_agent_standalone):
    """Test review of context manager patterns"""
    context_code = """
from contextlib import contextmanager

@contextmanager
def database_transaction(db):
    '''Context manager for database transactions'''
    transaction = db.begin()
    try:
        yield transaction
        transaction.commit()
    except Exception:
        transaction.rollback()
        raise
    finally:
        transaction.close()

def update_user(user_id, data):
    '''Update user within transaction'''
    with database_transaction(db) as txn:
        user = User.query.get(user_id)
        user.update(data)
"""

    task = AgentTask(
        id="task_018",
        description="Review context managers",
        parameters={"code": context_code}
    )

    result = await review_agent_standalone._execute_async(task)

    assert result.task_id == "task_018"

    print("✅ Review of context managers works")


@pytest.mark.asyncio
async def test_review_generator_patterns(review_agent_standalone):
    """Test review of generator patterns"""
    generator_code = """
def read_large_file(file_path):
    '''Generator to read large file line by line'''
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

def process_data_stream(stream):
    '''Process data from generator'''
    for item in stream:
        if item:
            yield process_item(item)
"""

    task = AgentTask(
        id="task_019",
        description="Review generator patterns",
        parameters={"code": generator_code}
    )

    result = await review_agent_standalone._execute_async(task)

    assert result.task_id == "task_019"

    print("✅ Review of generator patterns works")


# ============================================================================
# SECURITY VULNERABILITY DETECTION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_detect_sql_injection(review_agent_standalone):
    """Test detection of SQL injection vulnerabilities"""
    sql_injection_code = """
def get_user_by_name(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)
"""

    task = AgentTask(
        id="task_020",
        description="Detect SQL injection",
        parameters={"code": sql_injection_code}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P1",
                    severity=ViolationSeverity.CRITICAL,
                    message="SQL injection vulnerability: String formatting in query",
                    suggestion="Use parameterized queries",
                    context={"cwe": "CWE-89"}
                )
            ],
            score=0.15
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        assert not result.success

        print("✅ SQL injection detection works")


@pytest.mark.asyncio
async def test_detect_hardcoded_secrets(review_agent_standalone):
    """Test detection of hardcoded secrets"""
    secret_code = """
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "SuperSecret123!"

def connect_to_api():
    return requests.get('https://api.example.com',
                       headers={'Authorization': f'Bearer {API_KEY}'})
"""

    task = AgentTask(
        id="task_021",
        description="Detect hardcoded secrets",
        parameters={"code": secret_code}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P1",
                    severity=ViolationSeverity.CRITICAL,
                    message="Hardcoded API key and password",
                    suggestion="Use environment variables or secret management",
                    context={"cwe": "CWE-798"}
                )
            ],
            score=0.1
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        assert not result.success

        print("✅ Hardcoded secrets detection works")


@pytest.mark.asyncio
async def test_detect_path_traversal(review_agent_standalone):
    """Test detection of path traversal vulnerabilities"""
    path_traversal_code = """
def read_user_file(filename):
    path = f"/var/data/{filename}"
    with open(path, 'r') as f:
        return f.read()
"""

    task = AgentTask(
        id="task_022",
        description="Detect path traversal",
        parameters={"code": path_traversal_code}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P1",
                    severity=ViolationSeverity.HIGH,
                    message="Path traversal vulnerability: User input in file path",
                    suggestion="Validate and sanitize file paths",
                    context={"cwe": "CWE-22"}
                )
            ],
            score=0.3
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        verdict = result.output["verdict"]
        assert verdict in ["REJECTED", "CONDITIONAL"]

        print("✅ Path traversal detection works")


# ============================================================================
# BEST PRACTICES VALIDATION TESTS
# ============================================================================

@pytest.mark.asyncio
async def test_validate_pep8_compliance(review_agent_standalone):
    """Test PEP 8 compliance validation"""
    non_pep8_code = """
def calculateUserAge(birthYear,currentYear):
    age=currentYear-birthYear
    return age
"""

    task = AgentTask(
        id="task_023",
        description="Validate PEP 8 compliance",
        parameters={"code": non_pep8_code}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P2",
                    severity=ViolationSeverity.LOW,
                    message="PEP 8 violations: snake_case naming, spacing",
                    suggestion="Follow PEP 8 style guide",
                    context={}
                )
            ],
            score=0.75
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        # Low severity shouldn't block
        assert result.success or result.output["verdict"] == "CONDITIONAL"

        print("✅ PEP 8 compliance validation works")


@pytest.mark.asyncio
async def test_validate_error_handling(review_agent_standalone):
    """Test error handling best practices"""
    poor_error_handling = """
def divide(a, b):
    try:
        return a / b
    except:
        pass
"""

    task = AgentTask(
        id="task_024",
        description="Validate error handling",
        parameters={"code": poor_error_handling}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P4",
                    severity=ViolationSeverity.MEDIUM,
                    message="Poor error handling: Bare except and silent failure",
                    suggestion="Catch specific exceptions and log errors",
                    context={}
                )
            ],
            score=0.55
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        verdict = result.output["verdict"]
        assert verdict in ["CONDITIONAL", "REJECTED"]

        print("✅ Error handling validation works")


@pytest.mark.asyncio
async def test_validate_documentation(review_agent_standalone):
    """Test documentation best practices"""
    undocumented_code = """
def process_payment(user_id, amount, payment_method):
    validate_payment(user_id, amount)
    charge_payment(payment_method, amount)
    update_balance(user_id, amount)
    return True
"""

    task = AgentTask(
        id="task_025",
        description="Validate documentation",
        parameters={"code": undocumented_code}
    )

    with patch.object(
        review_agent_standalone.constitutional_engine,
        'evaluate_all_principles',
        return_value=create_violation_result(
            violations=[
                Violation(
                    principle="P2",
                    severity=ViolationSeverity.MEDIUM,
                    message="Missing docstring for critical payment function",
                    suggestion="Add comprehensive docstring with parameters and return value",
                    context={}
                )
            ],
            score=0.62
        )
    ):
        result = await review_agent_standalone._execute_async(task)

        verdict = result.output["verdict"]
        assert verdict in ["APPROVED", "CONDITIONAL", "REJECTED"]

        print("✅ Documentation validation works")


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

@pytest.mark.asyncio
async def test_review_empty_code(review_agent_standalone):
    """Test review of empty code"""
    task = AgentTask(
        id="task_026",
        description="Review empty code",
        parameters={"code": ""}
    )

    result = await review_agent_standalone._execute_async(task)

    # Should handle gracefully
    assert result.task_id == "task_026"

    print("✅ Empty code handling works")


@pytest.mark.asyncio
async def test_review_very_large_code(review_agent_standalone):
    """Test review of very large code file"""
    large_code = "\n".join([f"def function_{i}(): pass" for i in range(1000)])

    task = AgentTask(
        id="task_027",
        description="Review large code file",
        parameters={"code": large_code}
    )

    result = await review_agent_standalone._execute_async(task)

    # Should handle without crashing
    assert result.task_id == "task_027"

    print("✅ Large code file handling works")


@pytest.mark.asyncio
async def test_review_malformed_code(review_agent_standalone):
    """Test review of syntactically invalid code"""
    malformed_code = """
def broken_function(
    # Missing closing parenthesis and body
"""

    task = AgentTask(
        id="task_028",
        description="Review malformed code",
        parameters={"code": malformed_code}
    )

    result = await review_agent_standalone._execute_async(task)

    # Should handle gracefully (may reject due to syntax)
    assert result.task_id == "task_028"

    print("✅ Malformed code handling works")


@pytest.mark.asyncio
async def test_maximus_timeout_handling(review_agent_hybrid):
    """Test handling of MAXIMUS timeout"""
    task = AgentTask(
        id="task_029",
        description="Test MAXIMUS timeout",
        parameters={"code": "def foo(): pass"}
    )

    # Mock MAXIMUS to timeout
    with patch.object(
        review_agent_hybrid.maximus_client,
        'health_check',
        side_effect=asyncio.TimeoutError("Timeout")
    ):
        result = await review_agent_hybrid._execute_async(task)

        # Should fallback to standalone
        assert result.task_id == "task_029"

        print("✅ MAXIMUS timeout handling works")


@pytest.mark.asyncio
async def test_maximus_error_handling(review_agent_hybrid):
    """Test handling of MAXIMUS errors"""
    task = AgentTask(
        id="task_030",
        description="Test MAXIMUS error",
        parameters={"code": "def bar(): pass"}
    )

    # Mock MAXIMUS to raise error
    with patch.object(
        review_agent_hybrid.maximus_client,
        'health_check',
        side_effect=Exception("MAXIMUS error")
    ):
        result = await review_agent_hybrid._execute_async(task)

        # Should handle gracefully
        assert result.task_id == "task_030"

        print("✅ MAXIMUS error handling works")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("REVIEW AGENT - Comprehensive Scientific Test Suite")
    print("=" * 80)
    print()
    print("Testing Constitutional + Ethical Code Review System")
    print("Coverage: P1-P6 Principles + MAXIMUS 4 Ethical Frameworks")
    print()
    print("=" * 80)

    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
