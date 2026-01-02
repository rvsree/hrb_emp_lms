"""
Cleanup script for Stage 2: Configuration Cleanup
Consolidates duplicate configuration between config.py and postgres_db_config.py
"""

import os
import shutil
from pathlib import Path

def create_backup():
    """Create backup of config files before modification."""
    backup_dir = Path("backup_stage_2")
    backup_dir.mkdir(exist_ok=True)
    
    files_to_backup = [
        "src/app/common/config/config.py",
        "src/app/common/providers_config/db_config/postgres_db_config.py",
    ]
    
    print(f"Creating backup in {backup_dir}...")
    for file_path in files_to_backup:
        src = Path(file_path)
        if src.exists():
            # Create subdirectory structure
            dst = backup_dir / src.relative_to("src")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"  Backed up: {file_path}")
    
    return backup_dir

def consolidate_config():
    """
    Consolidate configuration by making Settings.database_url use get_postgres_dsn().
    This ensures consistency between SQLAlchemy (database.py) and psycopg (postgres_db_client.py).
    """
    config_path = Path("src/app/common/config/config.py")
    
    if not config_path.exists():
        print(f"❌ Config file not found: {config_path}")
        return False
    
    print("\nConsolidating configuration...")
    
    # Read current config
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Check if already consolidated
    if "from src.app.common.providers_config.db_config.postgres_db_config import get_postgres_dsn" in content:
        print("  ⚠️  Configuration already uses get_postgres_dsn()")
        return True
    
    # Replace database_url property to use get_postgres_dsn()
    old_property = '''    @property
    def database_url(self) -> str:
        """Get database URL."""
        return f"postgresql://{self.postgres_db_user}:{self.postgres_db_password}@{self.postgres_db_host}:{self.postgres_db_port}/{self.postgres_db_name}"
'''
    
    new_property = '''    @property
    def database_url(self) -> str:
        """
        Get database URL.
        Uses get_postgres_dsn() to ensure consistency with postgres_db_client.
        """
        from src.app.common.providers_config.db_config.postgres_db_config import get_postgres_dsn
        return get_postgres_dsn()
'''
    
    if old_property in content:
        content = content.replace(old_property, new_property)
        print("  ✅ Updated database_url property to use get_postgres_dsn()")
    else:
        print("  ⚠️  database_url property not found in expected format")
        # Try to find and replace anyway
        import re
        pattern = r'(@property\s+def database_url\(self\) -> str:.*?return f"postgresql://.*?")'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            content = content.replace(match.group(1), new_property.strip())
            print("  ✅ Updated database_url property (regex match)")
        else:
            print("  ⚠️  Could not find database_url property to update")
            return False
    
    # Write updated config
    with open(config_path, 'w') as f:
        f.write(content)
    
    print("  ✅ Configuration consolidated")
    return True

def remove_unused_postgres_fields():
    """
    Note: We keep postgres_db_* fields in Settings for backward compatibility,
    but database_url now uses get_postgres_dsn() which reads from env vars directly.
    The fields are still used by other parts potentially, so we keep them for now.
    """
    print("\nChecking for unused postgres fields...")
    print("  ℹ️  Keeping postgres_db_* fields in Settings for potential backward compatibility")
    print("  ℹ️  database_url now delegates to get_postgres_dsn() for consistency")
    return True

def main():
    """Main cleanup function."""
    print("=" * 80)
    print("STAGE 2 CLEANUP: Configuration Consolidation")
    print("=" * 80)
    print()
    
    # Create backup
    backup_dir = create_backup()
    print(f"\n✅ Backup created in: {backup_dir}")
    
    # Consolidate config
    success = consolidate_config()
    
    # Check unused fields
    remove_unused_postgres_fields()
    
    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Backup location: {backup_dir}")
    
    if success:
        print("\n✅ Stage 2 cleanup complete")
        print("\nChanges made:")
        print("  - Settings.database_url now uses get_postgres_dsn()")
        print("  - Ensures consistency between SQLAlchemy and psycopg connections")
        print("\nNext steps:")
        print("1. Run: python scripts/test_stage_2.py")
        print("2. Test application startup")
        print("3. Test database connections")
        print("4. If tests pass, create checkpoint: git tag cleanup-stage-2-checkpoint")
        print("5. Proceed to Stage 3")
    else:
        print("\n⚠️  Some operations failed - review before proceeding")
    
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())


