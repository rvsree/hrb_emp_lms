"""
Test script for Stage 2 cleanup: Configuration Cleanup
Validates configuration consolidation and identifies duplicate/unused functions.
"""

import sys
import os
import inspect

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_config_imports():
    """Test that config imports work."""
    print("Testing config imports...")
    try:
        from src.app.common.config.config import settings
        from src.app.common.providers_config.db_config.postgres_db_config import (
            get_postgres_host,
            get_postgres_port,
            get_postgres_name,
            get_postgres_user,
            get_postgres_password,
            get_postgres_dsn,
        )
        print("✅ All config imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_class():
    """Test Settings class functionality."""
    print("\nTesting Settings class...")
    try:
        from src.app.common.config.config import settings
        
        # Test basic properties
        assert hasattr(settings, 'postgres_db_host')
        assert hasattr(settings, 'postgres_db_port')
        assert hasattr(settings, 'server_port')
        assert hasattr(settings, 'api_key')
        assert hasattr(settings, 'environ')
        
        # Test database_url property
        db_url = settings.database_url
        assert db_url.startswith('postgresql://')
        print(f"  ✅ database_url: {db_url[:50]}...")
        
        # Test log level methods
        log_level = settings.get_log_level()
        assert log_level in [10, 20, 30, 40, 50]  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        print(f"  ✅ get_log_level(): {log_level}")
        
        component_levels = settings.get_component_log_levels()
        assert isinstance(component_levels, dict)
        assert 'uvicorn' in component_levels
        assert 'mcp_controller' in component_levels
        print(f"  ✅ get_component_log_levels(): {len(component_levels)} components")
        
        print("✅ Settings class works correctly")
        return True
    except Exception as e:
        print(f"❌ Settings test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_postgres_config_functions():
    """Test postgres_db_config functions."""
    print("\nTesting postgres_db_config functions...")
    try:
        from src.app.common.providers_config.db_config.postgres_db_config import (
            get_postgres_host,
            get_postgres_port,
            get_postgres_name,
            get_postgres_user,
            get_postgres_password,
            get_postgres_dsn,
        )
        
        host = get_postgres_host()
        port = get_postgres_port()
        name = get_postgres_name()
        user = get_postgres_user()
        password = get_postgres_password()
        dsn = get_postgres_dsn()
        
        assert isinstance(host, str)
        assert isinstance(port, int)
        assert isinstance(name, str)
        assert isinstance(user, str)
        assert dsn.startswith('postgresql://')
        
        print(f"  ✅ get_postgres_host(): {host}")
        print(f"  ✅ get_postgres_port(): {port}")
        print(f"  ✅ get_postgres_name(): {name}")
        print(f"  ✅ get_postgres_user(): {user}")
        print(f"  ✅ get_postgres_dsn(): {dsn[:50]}...")
        
        print("✅ postgres_db_config functions work correctly")
        return True
    except Exception as e:
        print(f"❌ postgres_db_config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def identify_duplicates():
    """Identify duplicate configuration between config.py and postgres_db_config.py."""
    print("\nIdentifying duplicate configuration...")
    try:
        from src.app.common.config.config import settings
        from src.app.common.providers_config.db_config.postgres_db_config import (
            get_postgres_host,
            get_postgres_port,
            get_postgres_name,
            get_postgres_user,
            get_postgres_password,
            get_postgres_dsn,
        )
        
        # Compare values
        settings_host = settings.postgres_db_host
        config_host = get_postgres_host()
        
        settings_port = settings.postgres_db_port
        config_port = get_postgres_port()
        
        settings_name = settings.postgres_db_name
        config_name = get_postgres_name()
        
        settings_user = settings.postgres_db_user
        config_user = get_postgres_user()
        
        settings_password = settings.postgres_db_password
        config_password = get_postgres_password()
        
        settings_url = settings.database_url
        config_dsn = get_postgres_dsn()
        
        print("\n  Comparison:")
        print(f"    Host: settings={settings_host}, config={config_host}, match={settings_host == config_host}")
        print(f"    Port: settings={settings_port}, config={config_port}, match={settings_port == config_port}")
        print(f"    Name: settings={settings_name}, config={config_name}, match={settings_name == config_name}")
        print(f"    User: settings={settings_user}, config={config_user}, match={settings_user == config_user}")
        print(f"    Password: settings={'*'*len(settings_password) if settings_password else 'None'}, config={'*'*len(config_password) if config_password else 'None'}, match={settings_password == config_password}")
        print(f"    URL/DSN: match={settings_url == config_dsn}")
        
        if settings_url != config_dsn:
            print(f"      Settings URL: {settings_url}")
            print(f"      Config DSN:   {config_dsn}")
        
        print("\n  ⚠️  DUPLICATE CONFIGURATION DETECTED:")
        print("     - config.py has: postgres_db_host, postgres_db_port, etc.")
        print("     - postgres_db_config.py has: get_postgres_host(), get_postgres_port(), etc.")
        print("     - Both read from same environment variables")
        print("     - Recommendation: Consolidate to single source of truth")
        
        return True
    except Exception as e:
        print(f"❌ Duplicate identification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_usage():
    """Test where each config is used."""
    print("\nAnalyzing config usage...")
    try:
        # Check if postgres_db_client uses postgres_db_config
        import importlib.util
        client_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'app', 'common', 'providers_client', 'db_client', 'postgres_db_client.py')
        if os.path.exists(client_path):
            with open(client_path, 'r') as f:
                content = f.read()
                if 'from src.app.common.providers_config.db_config.postgres_db_config import' in content:
                    print("  ✅ postgres_db_client.py uses postgres_db_config")
                else:
                    print("  ⚠️  postgres_db_client.py may not use postgres_db_config")
        
        # Check if main.py uses settings
        main_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'app', 'api', 'main.py')
        if os.path.exists(main_path):
            with open(main_path, 'r') as f:
                content = f.read()
                if 'from src.app.common.config.config import settings' in content:
                    print("  ✅ main.py uses settings from config.py")
                else:
                    print("  ⚠️  main.py may not use settings")
        
        return True
    except Exception as e:
        print(f"❌ Usage analysis failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("STAGE 2 CLEANUP TEST: Configuration")
    print("=" * 80)
    print()
    
    results = []
    results.append(("Config Imports", test_config_imports()))
    results.append(("Settings Class", test_settings_class()))
    results.append(("Postgres Config Functions", test_postgres_config_functions()))
    results.append(("Duplicate Identification", identify_duplicates()))
    results.append(("Config Usage Analysis", test_config_usage()))
    
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
        print("✅ All tests passed - Ready for Stage 2 cleanup")
        print("\nNext steps:")
        print("1. Review duplicate configuration identified above")
        print("2. Consolidate config.py and postgres_db_config.py")
        print("3. Remove unused functions")
        print("4. Test again after cleanup")
    else:
        print("❌ Some tests failed - Fix issues before proceeding")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())


