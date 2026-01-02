"""
Test script for Stage 1 cleanup: Test Scripts & Temporary Files
Validates that removing temporary files doesn't break functionality.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all main imports still work."""
    print("Testing imports...")
    try:
        from src.app.api.main import app
        from src.app.api.admin.health import health_router
        from src.app.api.controller.mcp_controller import mcp_router
        from src.app.common.config.app_logging import setup_logging, get_logger
        from src.app.common.config.config import settings
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_logging():
    """Test that logging still works."""
    print("Testing logging...")
    try:
        from src.app.common.config.app_logging import setup_logging, get_logger
        setup_logging()
        logger = get_logger("test")
        logger.info("Test log message")
        print("✅ Logging works")
        return True
    except Exception as e:
        print(f"❌ Logging failed: {e}")
        return False

def test_config():
    """Test that configuration loads correctly."""
    print("Testing configuration...")
    try:
        from src.app.common.config.config import settings
        assert settings.server_port > 0
        assert settings.environ in ["dev", "release"]
        print(f"✅ Configuration loaded: port={settings.server_port}, environ={settings.environ}")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("STAGE 1 CLEANUP TEST")
    print("=" * 80)
    print()
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Logging", test_logging()))
    results.append(("Configuration", test_config()))
    
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("✅ All tests passed - Stage 1 cleanup is safe")
        return 0
    else:
        print("❌ Some tests failed - Review before proceeding")
        return 1

if __name__ == "__main__":
    sys.exit(main())


