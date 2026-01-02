"""
Test script for Stage 3 cleanup: Database Client Cleanup
Identifies unused database functions and validates what's actually needed.
"""

import sys
import os
import ast
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def get_all_functions_in_file(file_path):
    """Extract all function names from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read(), filename=file_path)
        
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
        return functions
    except Exception as e:
        print(f"  ⚠️  Error parsing {file_path}: {e}")
        return []

def find_function_usage(function_name, search_dir):
    """Find all usages of a function in the codebase."""
    usages = []
    for root, dirs, files in os.walk(search_dir):
        # Skip __pycache__ and .git
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'backup_*']]
        
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if function_name in content:
                            # Check if it's actually used (not just in a comment)
                            lines = content.split('\n')
                            for i, line in enumerate(lines, 1):
                                if function_name in line and not line.strip().startswith('#'):
                                    usages.append((file_path, i, line.strip()[:80]))
                except Exception:
                    pass
    return usages

def analyze_postgres_db_client():
    """Analyze postgres_db_client.py to find unused functions."""
    print("Analyzing postgres_db_client.py...")
    
    client_path = Path("src/app/common/providers_client/db_client/postgres_db_client.py")
    if not client_path.exists():
        print("  ❌ postgres_db_client.py not found")
        return {}
    
    # Get all functions
    functions = get_all_functions_in_file(str(client_path))
    print(f"  Found {len(functions)} functions in postgres_db_client.py")
    
    # Functions that should be kept (used by health or core functionality)
    core_functions = {
        'get_postgres_connection',
        'postgres_session',
        'postgres_health_check',
        '_table_exists',  # Used by init_agent_memory_schema
        'init_agent_memory_schema',  # May be used for initialization
        '_load_postgres_queries',  # Internal helper
        '_ensure_queries_loaded',  # Internal helper
        '_sql',  # Internal helper
    }
    
    # Functions that are likely unused (LTM/Entity/Conversation - not used by MCP services)
    potentially_unused = {
        'insert_ltm_memory',
        'query_ltm_memories',
        'delete_ltm_memory',
        'upsert_entity',
        'query_entities',
        'get_entity_by_name',
        'insert_conversation_message',
        'query_conversation_history',
        'delete_conversation_thread',
    }
    
    # Search for usages
    src_dir = Path("src")
    usage_map = {}
    
    print("\n  Checking function usage...")
    for func in functions:
        if func.startswith('_'):  # Skip private functions for now
            continue
        
        usages = find_function_usage(func, str(src_dir))
        # Filter out self-references
        usages = [u for u in usages if 'postgres_db_client.py' not in u[0]]
        usage_map[func] = usages
        
        if usages:
            print(f"    ✅ {func}: Used in {len(usages)} location(s)")
            for file_path, line_num, line_content in usages[:3]:  # Show first 3
                rel_path = os.path.relpath(file_path, "src")
                print(f"       - {rel_path}:{line_num}")
        else:
            if func in core_functions:
                print(f"    ⚠️  {func}: No external usage (but may be core function)")
            elif func in potentially_unused:
                print(f"    ❌ {func}: UNUSED (LTM/Entity/Conversation - not used by MCP)")
            else:
                print(f"    ❓ {func}: Unknown usage status")
    
    return usage_map

def test_health_endpoint():
    """Test that health endpoint still works."""
    print("\nTesting health endpoint dependency...")
    try:
        from src.app.api.admin.health import health_router
        from src.app.common.providers_client.db_client.postgres_db_client import postgres_health_check
        
        # Check if health.py imports postgres_health_check
        health_path = Path("src/app/api/admin/health.py")
        with open(health_path, 'r') as f:
            content = f.read()
            if 'postgres_health_check' in content:
                print("  ✅ Health endpoint uses postgres_health_check")
                return True
            else:
                print("  ⚠️  Health endpoint may not use postgres_health_check")
                return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_services_dependencies():
    """Test what database access services use."""
    print("\nAnalyzing service dependencies...")
    
    services = [
        "src/app/services/leave_balance_service.py",
        "src/app/services/leave_request_service.py",
        "src/app/services/hitl_service.py",
    ]
    
    uses_postgres_client = False
    uses_sqlalchemy = False
    
    for service_path in services:
        path = Path(service_path)
        if not path.exists():
            continue
        
        with open(path, 'r') as f:
            content = f.read()
            if 'postgres_db_client' in content:
                uses_postgres_client = True
                print(f"  ⚠️  {path.name} uses postgres_db_client")
            if 'from src.app.repos.database import' in content or 'Session' in content:
                uses_sqlalchemy = True
                print(f"  ✅ {path.name} uses SQLAlchemy (database.py)")
    
    if not uses_postgres_client and uses_sqlalchemy:
        print("  ✅ Services use SQLAlchemy, not postgres_db_client (except health check)")
        return True
    else:
        print("  ⚠️  Mixed usage detected")
        return False

def main():
    """Run all tests."""
    print("=" * 80)
    print("STAGE 3 CLEANUP TEST: Database Client")
    print("=" * 80)
    print()
    
    results = []
    usage_map = analyze_postgres_db_client()
    results.append(("Function Analysis", len(usage_map) > 0))
    results.append(("Health Endpoint", test_health_endpoint()))
    results.append(("Service Dependencies", test_services_dependencies()))
    
    print()
    print("=" * 80)
    print("ANALYSIS SUMMARY")
    print("=" * 80)
    
    # Identify unused functions
    unused_functions = []
    for func, usages in usage_map.items():
        if not usages and func not in ['get_postgres_connection', 'postgres_session', 'postgres_health_check', '_table_exists', 'init_agent_memory_schema']:
            unused_functions.append(func)
    
    if unused_functions:
        print("\n❌ POTENTIALLY UNUSED FUNCTIONS (LTM/Entity/Conversation):")
        for func in unused_functions:
            print(f"   - {func}")
        print("\n  These functions are for agent memory (LTM/Entity/Conversation)")
        print("  but hrb_emp_lms MCP server uses SQLAlchemy ORM models instead.")
        print("  Recommendation: Remove if not needed for future agent features.")
    else:
        print("\n✅ No unused functions identified")
    
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
        print("✅ Analysis complete - Ready for Stage 3 cleanup")
        print("\nRecommendation:")
        print("  - Keep: get_postgres_connection, postgres_session, postgres_health_check")
        print("  - Consider removing: LTM/Entity/Conversation functions (if not needed)")
        print("  - Keep: init_agent_memory_schema (may be needed for initialization)")
    else:
        print("❌ Some tests failed - Review before proceeding")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())


