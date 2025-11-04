"""
Test Configuration System

Tests for Pydantic settings, profile management, and validation.
"""

import sys
sys.path.insert(0, '/media/juan/DATA1/projects/MAXIMUS AI/max-code-cli')

import os
from pathlib import Path
from config.settings import Settings, get_settings, MaximusServiceConfig, ClaudeConfig
from config.profiles import Profile, ProfileManager, PROFILES


def test_default_settings():
    """Test default settings load correctly."""
    print("Test 1: Default settings")

    settings = Settings()

    assert settings.app_name == "Max-Code CLI"
    assert settings.version == "1.0.0"
    assert settings.environment in ['development', 'production', 'local']

    print("  ✓ Default settings loaded")


def test_maximus_config():
    """Test MAXIMUS service configuration."""
    print("\nTest 2: MAXIMUS configuration")

    config = MaximusServiceConfig()

    assert config.core_url == "http://localhost:8150"
    assert config.penelope_url == "http://localhost:8154"
    assert config.orchestrator_url == "http://localhost:8027"
    assert config.timeout_seconds == 30
    assert config.max_retries == 3

    print("  ✓ MAXIMUS config valid")


def test_claude_config():
    """Test Claude API configuration."""
    print("\nTest 3: Claude configuration")

    config = ClaudeConfig()

    assert config.model == "claude-sonnet-4-5-20250929"
    assert 0 <= config.temperature <= 1
    assert config.max_tokens > 0

    print("  ✓ Claude config valid")


def test_settings_validation():
    """Test settings validation."""
    print("\nTest 4: Settings validation")

    settings = Settings()
    is_valid, errors = settings.validate_configuration()

    # May have errors (like missing API key) but should not crash
    print(f"  - Valid: {is_valid}")
    if errors:
        print(f"  - Errors: {len(errors)}")
        for error in errors:
            print(f"    • {error}")
    else:
        print("  ✓ No validation errors")


def test_profile_manager():
    """Test profile manager."""
    print("\nTest 5: Profile manager")

    # Use temporary config dir for testing
    test_dir = Path("/tmp/max-code-test-config")
    test_dir.mkdir(parents=True, exist_ok=True)

    manager = ProfileManager(config_dir=test_dir)

    # Test profile listing
    profiles = manager.list_profiles()
    assert len(profiles) == 3
    assert Profile.DEVELOPMENT in profiles
    assert Profile.PRODUCTION in profiles
    assert Profile.LOCAL in profiles

    print("  ✓ Profiles listed")

    # Test profile setting
    manager.set_profile(Profile.DEVELOPMENT)
    assert manager.get_current_profile() == Profile.DEVELOPMENT
    assert manager.profile_exists()
    assert manager.env_file_exists()

    print("  ✓ Profile set and persisted")

    # Cleanup
    import shutil
    shutil.rmtree(test_dir, ignore_errors=True)


def test_profile_configs():
    """Test profile configurations."""
    print("\nTest 6: Profile configurations")

    for profile in Profile:
        config = PROFILES[profile]

        assert config.name == profile.value
        assert config.description
        assert isinstance(config.settings, dict)
        assert len(config.settings) > 0

        print(f"  ✓ {profile.value} profile valid")


def test_singleton_settings():
    """Test settings singleton pattern."""
    print("\nTest 7: Settings singleton")

    settings1 = get_settings()
    settings2 = get_settings()

    assert settings1 is settings2  # Same instance

    print("  ✓ Singleton pattern working")


def main():
    """Run all config tests."""
    print("=" * 80)
    print("CONFIG SYSTEM TESTS")
    print("=" * 80)

    try:
        test_default_settings()
        test_maximus_config()
        test_claude_config()
        test_settings_validation()
        test_profile_manager()
        test_profile_configs()
        test_singleton_settings()

        print("\n" + "=" * 80)
        print("✅ ALL CONFIG TESTS PASSED!")
        print("=" * 80)

        return True
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
