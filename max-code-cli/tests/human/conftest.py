"""
Conftest for Human-Like Tests - User Behavior Simulation Fixtures

Provides realistic user behavior patterns and edge cases.
"""

import pytest
import random
from unittest.mock import Mock
from sdk.base_agent import AgentTask, AgentResult


# ============================================================================
# TYPO GENERATORS - Realistic Human Errors
# ============================================================================

@pytest.fixture
def typo_generator():
    """Generates realistic typos like humans make"""

    def make_typo(text: str, typo_rate: float = 0.1) -> str:
        """
        Introduces realistic typos:
        - Missing letters
        - Swapped adjacent letters
        - Duplicate letters
        - Wrong case
        """
        if not text or random.random() > typo_rate:
            return text

        chars = list(text)
        typo_type = random.choice(["missing", "swap", "duplicate", "case"])

        if typo_type == "missing" and len(chars) > 1:
            # Remove random letter
            chars.pop(random.randint(0, len(chars) - 1))

        elif typo_type == "swap" and len(chars) > 1:
            # Swap adjacent letters
            i = random.randint(0, len(chars) - 2)
            chars[i], chars[i + 1] = chars[i + 1], chars[i]

        elif typo_type == "duplicate":
            # Duplicate random letter
            i = random.randint(0, len(chars) - 1)
            chars.insert(i, chars[i])

        elif typo_type == "case" and chars:
            # Random case change
            i = random.randint(0, len(chars) - 1)
            chars[i] = chars[i].swapcase()

        return "".join(chars)

    return make_typo


@pytest.fixture
def realistic_typos():
    """Common typos developers actually make"""
    return {
        "function": ["functon", "funciton", "functoin", "funciton", "fucntion"],
        "calculate": ["calulate", "calcualte", "calculte", "caculate"],
        "return": ["retrun", "retur", "retrn", "retunr"],
        "import": ["improt", "imoprt", "imprt", "imort"],
        "print": ["pirnt", "prnit", "prnt", "pritn"],
        "variable": ["varaible", "varialbe", "varieble", "varible"],
        "parameter": ["paramter", "paramater", "parmeter", "paarameter"],
        "algorithm": ["algorythm", "algorith", "algoritm", "algorthm"],
    }


# ============================================================================
# VAGUE REQUEST GENERATORS
# ============================================================================

@pytest.fixture
def vague_requests():
    """Ultra-vague requests users actually send"""
    return [
        "help",
        "fix it",
        "make it work",
        "do the thing",
        "???",
        "not working",
        "error",
        "broken",
        "halp",  # Classic typo
        "pls fix",
        "urgent!!!",
        "it crashed again",
        "same problem",
        "still not working",
    ]


@pytest.fixture
def contradictory_requests():
    """Requests with built-in contradictions"""
    return [
        "make it fast but with lots of features that will slow it down",
        "simple but comprehensive",
        "quick and dirty but production-ready",
        "minimal dependencies but use all the latest frameworks",
        "secure but no authentication needed",
        "REST API... no wait, GraphQL... actually, just use WebSockets",
    ]


# ============================================================================
# IMPATIENT USER SIMULATOR
# ============================================================================

@pytest.fixture
def impatient_user():
    """Simulates user who spams requests"""

    class ImpatientUser:
        def __init__(self):
            self.request_count = 0
            self.spam_threshold = 3  # Spams after 3 rapid requests

        def make_request(self, agent, description: str):
            """Make a request, potentially spamming"""
            self.request_count += 1

            # Add urgency markers if impatient
            if self.request_count >= self.spam_threshold:
                description = f"URGENT!!! {description} NOW!!!"

            from sdk.base_agent import create_agent_task
            task = create_agent_task(description)
            return agent.execute(task)

        def is_spamming(self) -> bool:
            return self.request_count >= self.spam_threshold

    return ImpatientUser()


# ============================================================================
# CHAOTIC INPUT GENERATORS
# ============================================================================

@pytest.fixture
def chaotic_inputs():
    """Edge case inputs that break things"""
    return {
        "empty": "",
        "whitespace": "   \n\t  ",
        "punctuation": "!@#$%^&*()",
        "emoji": "🚀💻✨🔥💯",
        "unicode": "создай función für العربية 日本語",
        "sql_injection": "'; DROP TABLE users; --",
        "xss_attempt": "<script>alert('xss')</script>",
        "path_traversal": "../../etc/passwd",
        "very_long": "x" * 10000,
        "all_caps": "CREATE A FUNCTION THAT DOES STUFF!!!",
        "mixed_case": "CrEaTe A fUnCtIoN",
        "no_spaces": "createafunctionthatdoesstuff",
        "lots_of_spaces": "create     a     function",
    }


@pytest.fixture
def copy_paste_disasters():
    """Realistic copy-paste mistakes"""
    return {
        "with_line_numbers": """
1. def calculate_sum(a, b):
2.     return a + b
3.
4. print(calculate_sum(5, 3))
""",
        "with_markdown": """```python
def foo():
    print('hi')
```""",
        "with_blog_comments": """
# From: https://stackoverflow.com/questions/12345
# Asked by: user123

def solution():
    pass
""",
        "mixed_indentation": """
def foo():
\tif True:  # tab
        return 1  # spaces
\t\tprint('hi')  # tabs
""",
        "trailing_whitespace": "def foo():    \n    return 1    \n",
    }


# ============================================================================
# LANGUAGE MIXERS
# ============================================================================

@pytest.fixture
def mixed_language_requests():
    """PT/EN/ES mixed requests (real Brazilian dev behavior)"""
    return [
        "cria uma function que faz um loop",
        "faz um código que retorna o result",
        "create uma função para calcular o sum",
        "preciso de uma function que does authentication",
        "implementa um algoritmo que calcula o average",
        "escreve código para fazer o parsing do JSON",
    ]


# ============================================================================
# REALISTIC USER SESSIONS
# ============================================================================

@pytest.fixture
def realistic_session():
    """Simulates a full user session with natural flow"""

    class UserSession:
        def __init__(self):
            self.history = []
            self.context = {}
            self.mood = "neutral"  # neutral, frustrated, impatient

        def add_interaction(self, request: str, response):
            self.history.append({
                "request": request,
                "response": response,
                "mood": self.mood
            })

            # Mood deteriorates with failures
            if not response.success:
                if self.mood == "neutral":
                    self.mood = "frustrated"
                elif self.mood == "frustrated":
                    self.mood = "impatient"

        def get_mood_modifier(self) -> str:
            """Adds mood-appropriate text to requests"""
            if self.mood == "frustrated":
                return " (please work this time)"
            elif self.mood == "impatient":
                return " URGENT!!! WHY ISN'T THIS WORKING???"
            return ""

        def make_typo_if_frustrated(self, text: str) -> str:
            """Frustrated users make more typos"""
            if self.mood == "frustrated" and random.random() < 0.3:
                # 30% chance of typo when frustrated
                chars = list(text)
                if len(chars) > 3:
                    i = random.randint(1, len(chars) - 2)
                    chars[i], chars[i + 1] = chars[i + 1], chars[i]
                return "".join(chars)
            return text

    return UserSession()


print("✅ Human-like test fixtures created: tests/human/conftest.py")
