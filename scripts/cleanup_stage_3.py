"""
Cleanup script for Stage 3: Database Client Cleanup
Marks unused LTM/Entity/Conversation functions as unused (conservative approach).
"""

import os
import shutil
from pathlib import Path

def create_backup():
    """Create backup of postgres_db_client.py before modification."""
    backup_dir = Path("backup_stage_3")
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = [
        "src/app/common/providers_client/db_client/postgres_db_client.py",
    ]
    
    print(f"Creating backup in {backup_dir}...")
    for file_path in files_to_backup:
        src = Path(file_path)
        if src.exists():
            dst = backup_dir / src.name
            shutil.copy2(src, dst)
            print(f"  Backed up: {file_path}")
    
    return backup_dir

def mark_unused_functions():
    """
    Mark unused LTM/Entity/Conversation functions with comments.
    Conservative approach: Add comments rather than delete.
    """
    client_path = Path("src/app/common/providers_client/db_client/postgres_db_client.py")
    
    if not client_path.exists():
        print(f"❌ File not found: {client_path}")
        return False
    
    print("\nMarking unused functions...")
    
    # Read current file
    with open(client_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Functions to mark as unused
    unused_functions = [
        'insert_ltm_memory',
        'query_ltm_memories',
        'delete_ltm_memory',
        'upsert_entity',
        'query_entities',
        'get_entity_by_name',
        'insert_conversation_message',
        'query_conversation_history',
        'delete_conversation_thread',
    ]
    
    # Find and mark functions
    modified = False
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Check if this line starts a function definition
        for func_name in unused_functions:
            if f"def {func_name}(" in line:
                # Check if already marked
                if "# UNUSED:" not in line and "# TODO: Remove if not needed" not in lines[i-1] if i > 0 else True:
                    # Add comment before function
                    indent = len(line) - len(line.lstrip())
                    comment = " " * indent + "# UNUSED: This function is not used by hrb_emp_lms MCP server.\n"
                    comment += " " * indent + "# Services use SQLAlchemy ORM (database.py) instead of direct psycopg.\n"
                    comment += " " * indent + "# TODO: Remove if agent memory features are not planned.\n"
                    new_lines.insert(-1, comment)
                    modified = True
                    print(f"  ✅ Marked {func_name} as unused")
                break
        
        i += 1
    
    if modified:
        # Write updated file
        with open(client_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("  ✅ File updated with unused function markers")
    else:
        print("  ⚠️  No changes needed (functions may already be marked)")
    
    return True

def add_module_docstring_note():
    """Add note to module docstring about unused functions."""
    client_path = Path("src/app/common/providers_client/db_client/postgres_db_client.py")
    
    if not client_path.exists():
        return False
    
    with open(client_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if note already exists
    if "NOTE: LTM/Entity/Conversation functions" in content:
        return True
    
    # Update module docstring
    old_docstring = '''"""
PostgreSQL Database Client for Agent Memory.

This module provides functions for:
- Database connection management
- Schema initialization for agent memory tables
- Long-Term Memory (LTM) CRUD operations
- Entity Memory CRUD operations
- Conversation history operations

Tables managed:
- agent_ltm: Long-term memory storage
- agent_entities: Named entity memory
- agent_conversations: Conversation history (for analytics)
"""'''
    
    new_docstring = '''"""
PostgreSQL Database Client for Agent Memory.

This module provides functions for:
- Database connection management
- Schema initialization for agent memory tables
- Long-Term Memory (LTM) CRUD operations (UNUSED in hrb_emp_lms)
- Entity Memory CRUD operations (UNUSED in hrb_emp_lms)
- Conversation history operations (UNUSED in hrb_emp_lms)

NOTE: LTM/Entity/Conversation functions are marked as UNUSED because:
- hrb_emp_lms MCP server uses SQLAlchemy ORM models (database.py) for data access
- Services (LeaveBalanceService, LeaveRequestService, HitlService) use SQLAlchemy
- Only postgres_health_check() is actively used by the health endpoint

Tables managed:
- agent_ltm: Long-term memory storage (not used by current MCP implementation)
- agent_entities: Named entity memory (not used by current MCP implementation)
- agent_conversations: Conversation history (not used by current MCP implementation)
"""'''
    
    if old_docstring in content:
        content = content.replace(old_docstring, new_docstring)
        with open(client_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✅ Updated module docstring with usage note")
        return True
    
    return False

def main():
    """Main cleanup function."""
    print("=" * 80)
    print("STAGE 3 CLEANUP: Database Client")
    print("=" * 80)
    print()
    
    # Create backup
    backup_dir = create_backup()
    print(f"\n✅ Backup created in: {backup_dir}")
    
    # Mark unused functions
    success1 = mark_unused_functions()
    
    # Update docstring
    success2 = add_module_docstring_note()
    
    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Backup location: {backup_dir}")
    
    if success1 or success2:
        print("\n✅ Stage 3 cleanup complete")
        print("\nChanges made:")
        print("  - Marked LTM/Entity/Conversation functions as UNUSED")
        print("  - Added notes explaining why they're unused")
        print("  - Functions are preserved but clearly marked")
        print("\nNext steps:")
        print("1. Run: python scripts/test_stage_3.py")
        print("2. Test application startup")
        print("3. Test health endpoint")
        print("4. If tests pass, create checkpoint: git tag cleanup-stage-3-checkpoint")
        print("5. Consider removing unused functions in future cleanup if not needed")
    else:
        print("\n⚠️  No changes made - review before proceeding")
    
    return 0 if (success1 or success2) else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())


