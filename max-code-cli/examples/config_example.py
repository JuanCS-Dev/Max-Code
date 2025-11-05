"""
Example: Centralized Configuration Management

Demonstrates how all clients now use centralized settings from config/settings.py
instead of hardcoded default URLs.

Run: python examples/config_example.py
"""

import sys
sys.path.insert(0, '.')

from config.settings import get_settings
from core.maximus_integration import MaximusClient, PENELOPEClient, NISClient, MABAClient


# =============================================================================
# EXAMPLE 1: Load Settings
# =============================================================================

def example_load_settings():
    print("=" * 70)
    print("EXAMPLE 1: Load Settings")
    print("=" * 70)

    settings = get_settings()

    print(f"✅ Settings loaded successfully")
    print(f"\n📋 MAXIMUS Services Configuration:")
    print(f"   - Core URL: {settings.maximus.core_url}")
    print(f"   - Penelope URL: {settings.maximus.penelope_url}")
    print(f"   - NIS URL: {settings.maximus.nis_url}")
    print(f"   - MABA URL: {settings.maximus.maba_url}")
    print(f"   - Timeout: {settings.maximus.timeout_seconds}s")
    print(f"   - Max Retries: {settings.maximus.max_retries}")

    print()


# =============================================================================
# EXAMPLE 2: Clients Use Settings
# =============================================================================

def example_clients_use_settings():
    print("=" * 70)
    print("EXAMPLE 2: Clients Use Settings (No Hardcoded URLs)")
    print("=" * 70)

    # Create clients WITHOUT providing URLs
    # They will automatically use settings
    maximus = MaximusClient()
    penelope = PENELOPEClient()
    nis = NISClient()
    maba = MABAClient()

    print(f"✅ All clients created without hardcoded URLs\n")

    print(f"📍 MaximusClient:")
    print(f"   - base_url: {maximus.base_url}")
    print(f"   - penelope_url: {maximus.penelope_url}")
    print(f"   - maba_url: {maximus.maba_url}")
    print(f"   - nis_url: {maximus.nis_url}")
    print(f"   - timeout: {maximus.timeout}s")

    print(f"\n📍 PENELOPEClient:")
    print(f"   - url: {penelope.url}")
    print(f"   - timeout: {penelope.timeout}s")

    print(f"\n📍 NISClient:")
    print(f"   - url: {nis.url}")
    print(f"   - timeout: {nis.timeout}s")

    print(f"\n📍 MABAClient:")
    print(f"   - url: {maba.url}")
    print(f"   - timeout: {maba.timeout}s")

    print()


# =============================================================================
# EXAMPLE 3: Override with Custom URLs (Still Possible)
# =============================================================================

def example_override_urls():
    print("=" * 70)
    print("EXAMPLE 3: Override with Custom URLs")
    print("=" * 70)

    # Can still override if needed (e.g., for testing)
    maximus = MaximusClient(base_url="http://custom-server:9000")
    penelope = PENELOPEClient(url="http://test-penelope:8200")

    print(f"✅ Clients can still be overridden for testing\n")

    print(f"📍 MaximusClient (custom):")
    print(f"   - base_url: {maximus.base_url}")

    print(f"\n📍 PENELOPEClient (custom):")
    print(f"   - url: {penelope.url}")

    print()


# =============================================================================
# EXAMPLE 4: Environment Variables
# =============================================================================

def example_environment_variables():
    print("=" * 70)
    print("EXAMPLE 4: Environment Variables Support")
    print("=" * 70)

    print(f"📝 You can override settings via environment variables:\n")

    env_vars = [
        ("MAXIMUS_CORE_URL", "http://localhost:8153"),
        ("MAXIMUS_PENELOPE_URL", "http://localhost:8150"),
        ("MAXIMUS_NIS_URL", "http://localhost:8152"),
        ("MAXIMUS_MABA_URL", "http://localhost:8151"),
        ("MAXIMUS_TIMEOUT", "30"),
        ("MAXIMUS_MAX_RETRIES", "3"),
    ]

    for var, example in env_vars:
        print(f"   export {var}={example}")

    print(f"\n💡 Environment variables override defaults from settings.py")
    print(f"💡 .env file is also supported (see .env.example)")

    print()


# =============================================================================
# EXAMPLE 5: Validate Configuration
# =============================================================================

def example_validate_configuration():
    print("=" * 70)
    print("EXAMPLE 5: Validate Configuration")
    print("=" * 70)

    settings = get_settings()

    is_valid, errors = settings.validate_configuration()

    if is_valid:
        print(f"✅ Configuration is valid!")
    else:
        print(f"❌ Configuration has errors:")
        for error in errors:
            print(f"   - {error}")

    print()


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 12 + "CENTRALIZED CONFIGURATION MANAGEMENT" + " " * 21 + "║")
    print("║" + " " * 24 + "FASE 3.3 Complete" + " " * 27 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")

    example_load_settings()
    example_clients_use_settings()
    example_override_urls()
    example_environment_variables()
    example_validate_configuration()

    print("=" * 70)
    print("✅ All configuration examples completed!")
    print("=" * 70)
    print()

    print("📊 SUMMARY:")
    print("   - Centralized settings in config/settings.py")
    print("   - All 4 clients refactored (MaximusClient, PENELOPEClient, NISClient, MABAClient)")
    print("   - No hardcoded URLs in __init__ signatures")
    print("   - Environment variable support (MAXIMUS_*)")
    print("   - .env file support")
    print("   - Type-safe with Pydantic validation")
    print("   - Can still override for testing")
    print()

    print("Biblical Foundation:")
    print('"Porque com sabedoria se edifica a casa, e com a inteligência ela se firma"')
    print("(Provérbios 24:3)")
    print()


if __name__ == "__main__":
    main()
