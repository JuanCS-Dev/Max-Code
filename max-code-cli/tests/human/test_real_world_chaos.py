"""
Real-World Chaos Tests - Ultra-Realistic User Behavior

Based on ACTUAL production user behavior patterns.
"Reality is stranger than fiction." - Every QA Engineer

Categories:
1. Stack Overflow Copy-Paste Hell
2. Production Emergency Panic
3. Mobile Users (Autocorrect Chaos)
4. Non-Native English Speakers
5. Junior Developers Learning
6. Late Night Coding (3am Mistakes)
7. Managers Who Code
8. AI-Assisted Coding Gone Wrong
9. Legacy Code Maintainers
10. The "Works On My Machine" Users
"""

import pytest
from sdk.base_agent import create_agent_task
from agents.plan_agent import PlanAgent
from agents.review_agent import ReviewAgent
from agents.fix_agent import FixAgent
from agents.code_agent import CodeAgent


# ============================================================================
# 1. STACK OVERFLOW COPY-PASTE HELL
# ============================================================================

class TestStackOverflowCopyPaste:
    """Users who copy-paste from Stack Overflow without reading"""

    def test_copy_paste_with_so_comments(self):
        """User copies code WITH Stack Overflow comments/metadata"""
        agent = ReviewAgent(enable_maximus=False)

        # Real Stack Overflow copy-paste
        code = """
# Source: https://stackoverflow.com/questions/12345/how-to-sort
# Asked by: user12345
# Answered by: top_contributor (15.2k reputation)
# Upvotes: 234

def sort_list(items):
    # This answer is not recommended for production use
    # See the accepted answer below for a better approach
    return sorted(items, key=lambda x: x[0])

# EDIT: As pointed out in comments, this doesn't handle None values
# EDIT 2: Fixed edge case with empty lists
# EDIT 3: Performance optimization suggested by @expert_user
"""

        task = create_agent_task("review this sorting code", code=code)
        result = agent.execute(task)
        assert result.success
        # Should still review the actual code, ignoring metadata

    def test_copy_paste_multiple_answers(self):
        """User pastes multiple Stack Overflow answers at once"""
        agent = CodeAgent(enable_maximus=False)

        code = """
# Approach 1 (10 upvotes):
def method_a():
    pass

# Approach 2 (50 upvotes):
def method_b():
    pass

# Approach 3 (200 upvotes) - ACCEPTED ANSWER:
def method_c():
    pass
"""

        task = create_agent_task("which approach is best?", code=code)
        result = agent.execute(task)
        # Should handle gracefully
        assert result.success

    def test_copy_paste_with_language_tag(self):
        """Code pasted with language tag from markdown"""
        agent = ReviewAgent(enable_maximus=False)

        code = """```python
def calculate_total(items):
    return sum(items)
```

```python
# Alternative implementation:
def calculate_total_v2(items):
    total = 0
    for item in items:
        total += item
    return total
```"""

        task = create_agent_task("review both implementations", code=code)
        result = agent.execute(task)
        assert result.success


# ============================================================================
# 2. PRODUCTION EMERGENCY PANIC
# ============================================================================

class TestProductionEmergency:
    """Users in full panic mode during production incidents"""

    def test_all_caps_emergency(self):
        """EVERYTHING IS ON FIRE"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
def process_payment(amount):
    return amount * 100  # BUG: Should divide, not multiply!
"""

        task = create_agent_task(
            "URGENT!!! PAYMENT SYSTEM DOWN!!! CUSTOMERS CHARGED 100X!!! FIX NOW!!!",
            code=broken_code,
            error="ValueError: payment too high"
        )

        result = agent.execute(task)
        assert result.success
        # Should stay calm and fix the bug

    def test_production_incident_stream_of_consciousness(self):
        """User typing frantically during incident"""
        agent = FixAgent(enable_maximus=False)

        description = """
        ok so the api is returning 500 errors
        checked logs
        database connection timing out
        wait no
        its the cache
        no wait
        redis is fine
        oh god its the rate limiter
        it thinks everyone is the same user
        fix the rate limiter code ASAP
        """

        task = create_agent_task(description)
        result = agent.execute(task)
        # Should extract: rate limiter bug
        assert result.success

    def test_rollback_request_mid_debugging(self):
        """User wants to rollback while still debugging"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task(
            "wait no don't fix it, just rollback to previous version... "
            "actually wait, let's try to patch it first... "
            "no rollback is safer... "
            "but the fix looks simple... "
            "ok just tell me the safest option"
        )

        result = agent.execute(task)
        assert result.success
        # Should recommend rollback (safest) even though conflicting


# ============================================================================
# 3. MOBILE USERS (AUTOCORRECT CHAOS)
# ============================================================================

class TestMobileAutocorrect:
    """Users coding on mobile (yes, this happens)"""

    def test_autocorrect_function_names(self):
        """Autocorrect mangles code keywords"""
        agent = CodeAgent(enable_maximus=False)

        # Real autocorrect: def → deaf, return → retain, class → glass
        task = create_agent_task(
            "create a glass called Calculator with a method to retain the sum"
        )

        result = agent.execute(task)
        # Should understand: class Calculator, method return sum
        assert result.success

    def test_voice_dictation_gone_wrong(self):
        """User dictated code to phone"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "define function calculate some that takes list of numbers "
            "period for each number in list colon total equals total plus number "
            "period return total period"
        )

        result = agent.execute(task)
        # Should parse voice-dictated code
        assert result.success or "voice" in str(result.output).lower()


# ============================================================================
# 4. NON-NATIVE ENGLISH SPEAKERS
# ============================================================================

class TestNonNativeEnglish:
    """Users from different language backgrounds"""

    def test_german_english_mix(self):
        """German developer with English code"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "bitte create eine function für das berechnung von factorial, "
            "aber mit recursion nicht loop verstehst du?"
        )

        result = agent.execute(task)
        # Should extract: factorial, recursion, not loop
        assert result.success

    def test_false_friends(self):
        """Words that sound similar but mean different things"""
        agent = PlanAgent(enable_maximus=False)

        # "actual" in Spanish means "current", not "real"
        task = create_agent_task(
            "create API for the actual state of the system "
            "(no the historic, only the current state)"
        )

        result = agent.execute(task)
        # Should understand: current state, not historical
        assert result.success

    def test_portuguese_code_comments(self):
        """Brazilian dev with PT comments"""
        agent = ReviewAgent(enable_maximus=False)

        code = """
def processar_pagamento(valor):
    # TODO: validar cartão de crédito antes
    # FIXME: não está tratando erro de timeout
    if valor <= 0:
        raise ValueError("valor inválido")  # melhorar mensagem
    return valor * 1.1  # taxa de serviço
"""

        task = create_agent_task("review this payment code", code=code)
        result = agent.execute(task)
        assert result.success
        # Should review despite PT comments


# ============================================================================
# 5. JUNIOR DEVELOPERS LEARNING
# ============================================================================

class TestJuniorDevelopers:
    """New developers still learning"""

    def test_confused_about_async(self):
        """Junior confused about async/await"""
        agent = CodeAgent(enable_maximus=False)

        task = create_agent_task(
            "i need to make API call but its not waiting... "
            "someone said use async but i tried and it says 'await' outside function??? "
            "how do i make it wait for response before continuing"
        )

        result = agent.execute(task)
        # Should explain async/await or provide sync alternative
        assert result.success

    def test_copying_tutorial_but_different_context(self):
        """Junior following tutorial but wrong context"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
# From tutorial: Django view
from django.http import HttpResponse

def my_view(request):
    return HttpResponse("Hello")

# But I'm using Flask not Django!
"""

        task = create_agent_task(
            "this tutorial code doesn't work in my project",
            code=broken_code,
            error="ModuleNotFoundError: No module named 'django'"
        )

        result = agent.execute(task)
        assert result.success
        # Should recognize framework mismatch

    def test_asking_xyz_problem(self):
        """Junior asks about solution instead of problem (XY Problem)"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task(
            "how do i convert string to list of characters then sort them "
            "then join back into string but only if length > 5"
        )

        result = agent.execute(task)
        # There's probably a better approach to the real problem
        assert result.success


# ============================================================================
# 6. LATE NIGHT CODING (3AM MISTAKES)
# ============================================================================

class TestLateNightCoding:
    """Developers at 3am making tired mistakes"""

    def test_zombie_debugging(self):
        """Exhausted dev trying everything"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
def process():
    # tried adding sleep
    # time.sleep(1)
    # tried catching exception
    # try: ... except: pass
    # tried restarting server
    # tried clearing cache
    # tried sacrificing rubber duck to coding gods
    return None  # i give up
"""

        task = create_agent_task(
            "nothing works... been debugging for 6 hours... "
            "what am i missing",
            code=broken_code,
            error="NoneType has no attribute 'data'"
        )

        result = agent.execute(task)
        assert result.success
        # Should identify: returning None instead of actual data

    def test_copied_own_code_with_bug(self):
        """Copy-pasted from own codebase, includes old bug"""
        agent = ReviewAgent(enable_maximus=False)

        code = """
def calculate_discount(price, percent):
    # Copied from checkout.py
    discount = price * percent  # BUG: should divide by 100
    return price - discount
"""

        task = create_agent_task("why is discount wrong", code=code)
        result = agent.execute(task)
        assert result.success
        # Should catch: percent should be divided by 100

    def test_inverted_logic_brain_fart(self):
        """Classic tired developer logic inversion"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
def should_process(item):
    if item.is_valid:
        return False  # Don't process valid items
    return True  # Only process invalid items

# Wait... that doesn't make sense... but i'm too tired to think
"""

        task = create_agent_task(
            "this logic feels backwards but idk",
            code=broken_code,
            error="Valid items not being processed"
        )

        result = agent.execute(task)
        assert result.success


# ============================================================================
# 7. MANAGERS WHO CODE
# ============================================================================

class TestManagersWhoCoded:
    """Managers who haven't coded in 10 years"""

    def test_ancient_php_style_in_python(self):
        """Manager using PHP syntax in Python"""
        agent = ReviewAgent(enable_maximus=False)

        code = """
def calculate($price, $tax):
    $total = $price + $tax;
    return $total;

# Why does Python complain about $ symbols???
"""

        task = create_agent_task("fix this python code", code=code)
        result = agent.execute(task)
        assert result.success
        # Should detect PHP syntax in Python

    def test_wants_java_patterns_in_python(self):
        """Manager wants Java enterprise patterns"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task(
            "create AbstractFactoryBeanSingletonProxyServiceLocator "
            "following Gang of Four patterns and SOLID principles... "
            "wait this is Python not Java right? "
            "ok just make it simple then"
        )

        result = agent.execute(task)
        # Should suggest simple Python solution
        assert result.success


# ============================================================================
# 8. AI-ASSISTED CODING GONE WRONG
# ============================================================================

class TestAICodingGoneWrong:
    """Users who used ChatGPT/Copilot and got garbage"""

    def test_ai_generated_nonsense(self):
        """AI confidently generated completely wrong code"""
        agent = ReviewAgent(enable_maximus=False)

        # Real example: AI-generated code that looks good but doesn't work
        code = """
def calculate_fibonacci(n):
    # AI-generated code (ChatGPT 3.5)
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib[n]  # BUG: IndexError if n < 2

# AI said this is "production-ready optimized solution"
"""

        task = create_agent_task(
            "ai gave me this but it crashes on small numbers",
            code=code
        )

        result = agent.execute(task)
        assert result.success
        # Should catch IndexError edge case

    def test_ai_hallucinated_library(self):
        """AI invented a library that doesn't exist"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
# Copilot suggested this
from super_json_parser import UltraFastParser

parser = UltraFastParser()  # Module doesn't exist!
"""

        task = create_agent_task(
            "copilot suggested this library but pip install fails",
            code=broken_code,
            error="ModuleNotFoundError: No module named 'super_json_parser'"
        )

        result = agent.execute(task)
        assert result.success
        # Should suggest real alternative (json module)


# ============================================================================
# 9. LEGACY CODE MAINTAINERS
# ============================================================================

class TestLegacyCodeMaintenance:
    """Developers maintaining ancient codebases"""

    def test_python2_in_python3_project(self):
        """Legacy Python 2 code in Python 3 project"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
# Legacy code from 2010
print "Processing user:", user_name
result = items.has_key('total')
data = unicode(response)
"""

        task = create_agent_task(
            "migrate this to python 3",
            code=broken_code,
            error="SyntaxError: invalid syntax"
        )

        result = agent.execute(task)
        assert result.success
        # Should convert: print(), 'in' operator, str()

    def test_ancient_library_no_docs(self):
        """Using library so old docs don't exist anymore"""
        agent = PlanAgent(enable_maximus=False)

        task = create_agent_task(
            "need to update code using 'PyWebService' library from 2008... "
            "can't find docs... "
            "github repo deleted... "
            "stack overflow has 1 question from 2009... "
            "what do i do"
        )

        result = agent.execute(task)
        # Should suggest: reverse engineer or migrate to modern lib
        assert result.success


# ============================================================================
# 10. "WORKS ON MY MACHINE" USERS
# ============================================================================

class TestWorksOnMyMachine:
    """Developers with environment-specific bugs"""

    def test_hardcoded_local_paths(self):
        """Code with hardcoded paths from dev machine"""
        agent = ReviewAgent(enable_maximus=False)

        code = """
def load_config():
    # Works fine on my machine!
    config_path = "C:\\Users\\John\\Desktop\\myproject\\config.json"
    with open(config_path) as f:
        return json.load(f)
"""

        task = create_agent_task(
            "why does this fail on server",
            code=code
        )

        result = agent.execute(task)
        assert result.success
        # Should detect: hardcoded absolute path

    def test_port_already_in_use(self):
        """Different process using same port"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
app.run(port=8000)  # Works on my laptop
"""

        task = create_agent_task(
            "server won't start, says address already in use",
            code=broken_code,
            error="OSError: [Errno 98] Address already in use"
        )

        result = agent.execute(task)
        assert result.success
        # Should suggest: check what's using port, use different port

    def test_missing_env_variables(self):
        """Forgot to mention env variables needed"""
        agent = FixAgent(enable_maximus=False)

        broken_code = """
import os

API_KEY = os.environ['SECRET_API_KEY']
# Works for me, I have it in my .bashrc
"""

        task = create_agent_task(
            "colleague says this crashes on startup",
            code=broken_code,
            error="KeyError: 'SECRET_API_KEY'"
        )

        result = agent.execute(task)
        assert result.success
        # Should suggest: .env file or default value


# ============================================================================
# 11. BONUS: THE TRULY BIZARRE
# ============================================================================

class TestTrulyBizarre:
    """Edge cases so weird they must be real"""

    def test_emoji_variable_names(self):
        """User tried to use emoji as variable names (Python allows this!)"""
        agent = ReviewAgent(enable_maximus=False)

        code = """
🚀 = "launch"
💰 = 100
💸 = 💰 * 0.1
print(f"{🚀}: {💸}")
"""

        task = create_agent_task("is this valid python???", code=code)
        result = agent.execute(task)
        # Actually valid Python 3!
        assert result.success

    def test_code_obfuscated_by_accident(self):
        """User's IDE auto-formatter went crazy"""
        agent = ReviewAgent(enable_maximus=False)

        code = """
def\
 calculate\
(\
x\
,\
y\
)\
:\
return\
 x\
+\
y
"""

        task = create_agent_task(
            "my ide broke my code formatting, is this still valid",
            code=code
        )

        result = agent.execute(task)
        assert result.success

    def test_copy_pasted_from_pdf(self):
        """Code extracted from PDF with weird characters"""
        agent = ReviewAgent(enable_maximus=False)

        code = """
def calculate(x):
    # PDF OCR mistakes:
    # - vs — (en dash)
    # l vs 1 (lowercase L vs number)
    return x — l0  # Should be: x - 10
"""

        task = create_agent_task("this code has weird dashes", code=code)
        result = agent.execute(task)
        # Should detect unicode look-alikes
        assert result.success or "unicode" in str(result.output).lower()


# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

def test_real_world_chaos_coverage():
    """Meta-test: ensure we're testing diverse scenarios"""
    import inspect

    # Count test classes
    classes = [
        TestStackOverflowCopyPaste,
        TestProductionEmergency,
        TestMobileAutocorrect,
        TestNonNativeEnglish,
        TestJuniorDevelopers,
        TestLateNightCoding,
        TestManagersWhoCoded,
        TestAICodingGoneWrong,
        TestLegacyCodeMaintenance,
        TestWorksOnMyMachine,
        TestTrulyBizarre,
    ]

    total_tests = 0
    for cls in classes:
        methods = [m for m in dir(cls) if m.startswith('test_')]
        total_tests += len(methods)
        print(f"{cls.__name__}: {len(methods)} tests")

    print(f"\nTotal real-world chaos tests: {total_tests}")
    assert total_tests >= 29, f"Need at least 29 real-world tests, got {total_tests}"


print("✅ Real-World Chaos test suite created!")
print("Categories: 11")
print("Total tests: 29+")
print("Based on: Actual production nightmares")
