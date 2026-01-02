"""
Cleanup script for Stage 1: Remove temporary test scripts and files.
"""

import os
import shutil
from pathlib import Path

# Files to remove
FILES_TO_REMOVE = [
    "test_color_logging.py",
    "test_logging_colors.py",
    "fix_color_logging.py",
    "COLOR_LOGGING_FIX_SUMMARY.md",
    "LOGGING_CONFIGURATION.md",  # Info is in main docs
]

# Files to keep (for reference)
FILES_TO_KEEP = [
    "tests/test_all_tools.py",
    "tests/test_comprehensive.py",
    "tools/check_health.py",
]

def create_backup():
    """Create backup of files before deletion."""
    backup_dir = Path("backup_stage_1")
    backup_dir.mkdir(exist_ok=True)
    
    print(f"Creating backup in {backup_dir}...")
    for file_path in FILES_TO_REMOVE:
        src = Path(file_path)
        if src.exists():
            dst = backup_dir / src.name
            shutil.copy2(src, dst)
            print(f"  Backed up: {file_path}")
    
    return backup_dir

def remove_files():
    """Remove temporary files."""
    print("\nRemoving temporary files...")
    removed = []
    not_found = []
    
    for file_path in FILES_TO_REMOVE:
        path = Path(file_path)
        if path.exists():
            path.unlink()
            removed.append(file_path)
            print(f"  ✅ Removed: {file_path}")
        else:
            not_found.append(file_path)
            print(f"  ⚠️  Not found: {file_path}")
    
    return removed, not_found

def verify_kept_files():
    """Verify that files we want to keep still exist."""
    print("\nVerifying kept files...")
    all_exist = True
    
    for file_path in FILES_TO_KEEP:
        path = Path(file_path)
        if path.exists():
            print(f"  ✅ Kept: {file_path}")
        else:
            print(f"  ⚠️  Missing: {file_path}")
            all_exist = False
    
    return all_exist

def main():
    """Main cleanup function."""
    print("=" * 80)
    print("STAGE 1 CLEANUP: Test Scripts & Temporary Files")
    print("=" * 80)
    print()
    
    # Create backup
    backup_dir = create_backup()
    print(f"\n✅ Backup created in: {backup_dir}")
    
    # Remove files
    removed, not_found = remove_files()
    
    # Verify kept files
    all_kept = verify_kept_files()
    
    # Summary
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Removed: {len(removed)} files")
    print(f"Not found: {len(not_found)} files")
    print(f"Backup location: {backup_dir}")
    
    if all_kept:
        print("\n✅ Stage 1 cleanup complete")
        print("\nNext steps:")
        print("1. Run: python scripts/test_stage_1.py")
        print("2. If tests pass, create checkpoint: git tag cleanup-stage-1-checkpoint")
        print("3. Proceed to Stage 2")
    else:
        print("\n⚠️  Some expected files are missing - review before proceeding")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())


