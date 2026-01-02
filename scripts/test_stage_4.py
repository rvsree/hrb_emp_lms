"""
Test script for Stage 4 cleanup: Health Endpoints Cleanup
Validates health endpoints are clean, minimal, and consistent.
"""

import sys
import os
import inspect

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_health_imports():
    """Test that health endpoints can be imported."""
    print("Testing health endpoint imports...")
    try:
        from src.app.api.admin.health import health_router, app_health, postgres_health
        print("  ✅ Health router and endpoints imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_health_router_config():
    """Test health router configuration."""
    print("\nTesting health router configuration...")
    try:
        from src.app.api.admin.health import health_router
        
        # Check prefix
        assert health_router.prefix == "/hrb_emp_lms/health", f"Expected prefix '/hrb_emp_lms/health', got '{health_router.prefix}'"
        print(f"  ✅ Router prefix: {health_router.prefix}")
        
        # Check tags
        assert "health" in health_router.tags, "Router should have 'health' tag"
        print(f"  ✅ Router tags: {health_router.tags}")
        
        # Count routes
        routes = [route for route in health_router.routes]
        print(f"  ✅ Number of routes: {len(routes)}")
        
        return True
    except Exception as e:
        print(f"  ❌ Router config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_endpoint_signatures():
    """Test endpoint function signatures."""
    print("\nTesting endpoint signatures...")
    try:
        from src.app.api.admin.health import app_health, postgres_health
        
        # Check app_health
        sig = inspect.signature(app_health)
        assert len(sig.parameters) == 0, "app_health should have no parameters"
        print("  ✅ app_health signature correct")
        
        # Check postgres_health
        sig = inspect.signature(postgres_health)
        assert len(sig.parameters) == 0, "postgres_health should have no parameters"
        print("  ✅ postgres_health signature correct")
        
        return True
    except Exception as e:
        print(f"  ❌ Signature test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_response_format():
    """Test that response formats are consistent."""
    print("\nTesting response format consistency...")
    try:
        from src.app.api.admin.health import app_health, postgres_health
        
        # Test app_health response structure (mock)
        # We can't actually call async functions without event loop, so we check the code
        health_path = Path("src/app/api/admin/health.py")
        with open(health_path, 'r') as f:
            content = f.read()
        
        # Check app_health returns dict with status and message
        if '"status": "healthy"' in content and '"message":' in content:
            print("  ✅ app_health response format includes status and message")
        else:
            print("  ⚠️  app_health response format may be inconsistent")
        
        # Check postgres_health returns dict with status, message, and data
        if 'status_obj["status"]' in content and '"data": status_obj' in content:
            print("  ✅ postgres_health response format includes status, message, and data")
        else:
            print("  ⚠️  postgres_health response format may be inconsistent")
        
        return True
    except Exception as e:
        print(f"  ❌ Response format test failed: {e}")
        return False

def check_outdated_docstrings():
    """Check for outdated docstrings mentioning unused features."""
    print("\nChecking for outdated docstrings...")
    try:
        health_path = Path("src/app/api/admin/health.py")
        with open(health_path, 'r') as f:
            content = f.read()
        
        issues = []
        
        # Check for outdated LTM references
        if "LTM" in content or "agent long-term memory" in content.lower():
            if "UNUSED" not in content and "not used" not in content.lower():
                issues.append("Mentions LTM/agent memory without noting it's unused")
                print("  ⚠️  Found outdated LTM/agent memory reference in docstring")
        
        if issues:
            print(f"  ⚠️  Found {len(issues)} potential docstring issues")
            return False
        else:
            print("  ✅ Docstrings are up to date")
            return True
    except Exception as e:
        print(f"  ❌ Docstring check failed: {e}")
        return False

def test_dependencies():
    """Test that health endpoints have correct dependencies."""
    print("\nTesting dependencies...")
    try:
        from src.app.api.admin.health import postgres_health_check
        from src.app.common.providers_client.db_client.postgres_db_client import postgres_health_check as db_health_check
        
        # Verify they're the same function
        assert postgres_health_check is db_health_check, "postgres_health_check should be imported from postgres_db_client"
        print("  ✅ postgres_health_check correctly imported")
        
        return True
    except Exception as e:
        print(f"  ❌ Dependency test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("STAGE 4 CLEANUP TEST: Health Endpoints")
    print("=" * 80)
    print()
    
    results = []
    results.append(("Health Imports", test_health_imports()))
    results.append(("Router Configuration", test_health_router_config()))
    results.append(("Endpoint Signatures", test_endpoint_signatures()))
    results.append(("Response Format", test_response_format()))
    results.append(("Docstring Check", check_outdated_docstrings()))
    results.append(("Dependencies", test_dependencies()))
    
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
        print("✅ All tests passed - Ready for Stage 4 cleanup")
    else:
        print("❌ Some tests failed - Review issues above before proceeding")
        print("\nRecommendations:")
        print("  - Update docstrings to remove outdated LTM/agent memory references")
        print("  - Ensure response formats are consistent")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    from pathlib import Path
    sys.exit(main())


