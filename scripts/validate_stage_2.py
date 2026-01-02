"""
Quick validation script for Stage 2 cleanup.
Tests that the configuration consolidation works correctly.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_database_url():
    """Test that database_url uses get_postgres_dsn()."""
    print("Testing database_url consolidation...")
    try:
        from src.app.common.config.config import settings
        from src.app.common.providers_config.db_config.postgres_db_config import get_postgres_dsn
        
        # Get URLs from both sources
        settings_url = settings.database_url
        config_dsn = get_postgres_dsn()
        
        # They should match now
        if settings_url == config_dsn:
            print(f"  ✅ database_url matches get_postgres_dsn()")
            print(f"     URL: {settings_url[:60]}...")
            return True
        else:
            print(f"  ❌ Mismatch!")
            print(f"     settings.database_url: {settings_url}")
            print(f"     get_postgres_dsn():   {config_dsn}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test that all imports still work."""
    print("\nTesting imports...")
    try:
        from src.app.common.config.config import settings
        from src.app.repos.database import get_db
        from src.app.common.providers_client.db_client.postgres_db_client import get_postgres_connection
        print("  ✅ All imports successful")
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run validation."""
    print("=" * 80)
    print("STAGE 2 VALIDATION")
    print("=" * 80)
    print()
    
    results = []
    results.append(("Database URL Consolidation", test_database_url()))
    results.append(("Imports", test_imports()))
    
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
        print("✅ Stage 2 cleanup validated successfully")
        return 0
    else:
        print("❌ Validation failed - review errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())


