# Cleanup Execution Guide

## Quick Start

### Step 1: Create Baseline Checkpoint
```bash
cd C:\workspace\poc\MCP\hrb_emp_lms
git add .
git commit -m "Pre-cleanup baseline"
git tag cleanup-stage-0-baseline
```

### Step 2: Run Stage 1 Cleanup (Test Scripts)
```bash
# Test before cleanup
python scripts/test_stage_1.py

# Run cleanup
python scripts/cleanup_stage_1.py

# Test after cleanup
python scripts/test_stage_1.py

# If tests pass, create checkpoint
git add .
git commit -m "Stage 1: Removed temporary test scripts"
git tag cleanup-stage-1-checkpoint
```

## Stage 1: Files to Remove

The cleanup script will remove:
- ✅ `test_color_logging.py` - Temporary diagnostic script
- ✅ `test_logging_colors.py` - Duplicate/old test
- ✅ `fix_color_logging.py` - Temporary fix script
- ✅ `COLOR_LOGGING_FIX_SUMMARY.md` - Temporary documentation
- ✅ `LOGGING_CONFIGURATION.md` - Duplicate (info in main docs)

Files that will be KEPT:
- ✅ `tests/test_all_tools.py` - Legitimate test
- ✅ `tests/test_comprehensive.py` - Legitimate test
- ✅ `tools/check_health.py` - Utility tool

## Rollback Instructions

If something breaks after Stage 1:
```bash
# Rollback to baseline
git reset --hard cleanup-stage-0-baseline

# Or rollback to Stage 1 checkpoint
git reset --hard cleanup-stage-1-checkpoint
```

## Next Stages

After Stage 1 is complete and validated:
1. Review `CLEANUP_PLAN.md` for Stage 2 details
2. Create test script for Stage 2
3. Execute Stage 2 cleanup
4. Test and create checkpoint
5. Repeat for each stage

## Manual Cleanup (Alternative)

If you prefer to clean up manually:

1. **Backup first:**
   ```bash
   mkdir backup_manual
   cp test_color_logging.py backup_manual/
   cp test_logging_colors.py backup_manual/
   cp fix_color_logging.py backup_manual/
   cp COLOR_LOGGING_FIX_SUMMARY.md backup_manual/
   cp LOGGING_CONFIGURATION.md backup_manual/
   ```

2. **Remove files:**
   ```bash
   rm test_color_logging.py
   rm test_logging_colors.py
   rm fix_color_logging.py
   rm COLOR_LOGGING_FIX_SUMMARY.md
   rm LOGGING_CONFIGURATION.md
   ```

3. **Test:**
   ```bash
   python scripts/test_stage_1.py
   ```

4. **Commit:**
   ```bash
   git add .
   git commit -m "Stage 1: Removed temporary test scripts"
   git tag cleanup-stage-1-checkpoint
   ```

## Validation Checklist

After Stage 1 cleanup:
- [ ] All imports work (`python scripts/test_stage_1.py`)
- [ ] Logging works correctly
- [ ] Configuration loads correctly
- [ ] Application starts successfully
- [ ] Health endpoints work
- [ ] MCP endpoints work
- [ ] Git checkpoint created

## Notes

- All cleanup scripts create backups before deletion
- Test scripts validate functionality after each stage
- Git checkpoints allow easy rollback
- Each stage is independent and can be rolled back separately


