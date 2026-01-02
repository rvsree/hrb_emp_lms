# HRB_EMP_LMS Cleanup Plan

## Overview
Incremental cleanup of hrb_emp_lms project organized by use cases/features with checkpoints for rollback.

## Cleanup Stages

### Stage 0: Preparation & Backup
**Goal**: Create backup and baseline before cleanup

**Actions**:
1. Create git checkpoint: `git tag cleanup-stage-0-baseline`
2. Document current state
3. Create test baseline script

**Checkpoint**: `cleanup-stage-0-checkpoint`

---

### Stage 1: Test Scripts & Temporary Files
**Goal**: Remove temporary test scripts and files created during development

**Files to Remove**:
- `test_color_logging.py` (temporary diagnostic script)
- `test_logging_colors.py` (duplicate/old test)
- `fix_color_logging.py` (temporary fix script)
- `COLOR_LOGGING_FIX_SUMMARY.md` (temporary documentation)
- `LOGGING_CONFIGURATION.md` (duplicate - info in main docs)

**Files to Keep**:
- `tests/test_all_tools.py` (legitimate test)
- `tests/test_comprehensive.py` (legitimate test)
- `tools/check_health.py` (utility tool)

**Test**: Run `tests/test_all_tools.py` and `tests/test_comprehensive.py` to ensure no dependencies broken

**Checkpoint**: `cleanup-stage-1-checkpoint`

---

### Stage 2: Configuration Cleanup
**Goal**: Consolidate and clean configuration files

**Files to Review**:
- `src/app/common/config/config.py` - Main config (keep)
- `src/app/common/config/app_logging.py` - Logging config (keep, already cleaned)
- `src/app/common/providers_config/db_config/postgres_db_config.py` - DB config (review for duplicates)

**Actions**:
1. Check for duplicate config functions between `config.py` and `postgres_db_config.py`
2. Consolidate database configuration
3. Remove unused config functions
4. Ensure single source of truth for each setting

**Test**: 
- Application starts successfully
- Health endpoints work
- Database connections work

**Checkpoint**: `cleanup-stage-2-checkpoint`

---

### Stage 3: Database Client Cleanup
**Goal**: Clean up database client code, remove unused functions

**Files to Review**:
- `src/app/common/providers_client/db_client/postgres_db_client.py`
- `src/app/repos/database.py`

**Actions**:
1. Identify unused database functions
2. Remove orphaned LTM/entity memory functions if not used by MCP
3. Keep only functions used by:
   - Health checks
   - Leave balance service
   - Leave request service
   - HITL service

**Test**:
- Health endpoint: `/hrb_emp_lms/health/postgres`
- MCP tools that use database
- All services work correctly

**Checkpoint**: `cleanup-stage-3-checkpoint`

---

### Stage 4: Health Endpoints Cleanup
**Goal**: Ensure health endpoints are clean and minimal

**Files to Review**:
- `src/app/api/admin/health.py`

**Actions**:
1. Remove unused health checks (if any)
2. Ensure consistent response format
3. Remove duplicate health logic

**Test**:
- `GET /hrb_emp_lms/health/app`
- `GET /hrb_emp_lms/health/postgres`

**Checkpoint**: `cleanup-stage-4-checkpoint`

---

### Stage 5: MCP Controller Cleanup
**Goal**: Clean up MCP controller, remove duplicate code

**Files to Review**:
- `src/app/api/controller/mcp_controller.py`

**Actions**:
1. Remove duplicate helper functions
2. Consolidate error handling
3. Remove unused JSON-RPC utilities
4. Ensure consistent logging

**Test**:
- `POST /api/hrb/lms/mcp` with `tools/list`
- `POST /api/hrb/lms/mcp` with `tools/call`
- All MCP tools work correctly

**Checkpoint**: `cleanup-stage-5-checkpoint`

---

### Stage 6: Services Cleanup
**Goal**: Clean up service layer, remove unused code

**Files to Review**:
- `src/app/services/leave_balance_service.py`
- `src/app/services/leave_request_service.py`
- `src/app/services/hitl_service.py`

**Actions**:
1. Remove unused methods
2. Consolidate duplicate logic
3. Ensure consistent error handling
4. Remove orphaned imports

**Test**:
- All MCP tools that use services
- Service methods called by controller
- Error handling works correctly

**Checkpoint**: `cleanup-stage-6-checkpoint`

---

### Stage 7: Models & Repositories Cleanup
**Goal**: Clean up data models and repositories

**Files to Review**:
- `src/app/models/models.py`
- `src/app/repos/database.py`

**Actions**:
1. Remove unused model fields
2. Remove unused repository methods
3. Ensure SQLAlchemy models are minimal and correct

**Test**:
- Database operations work
- Models serialize correctly
- Repository methods work

**Checkpoint**: `cleanup-stage-7-checkpoint`

---

### Stage 8: Exceptions & Utilities Cleanup
**Goal**: Clean up exception handling and utilities

**Files to Review**:
- `src/app/exceptions/exceptions.py`
- Empty/unused directories:
  - `src/app/ai/` (if empty)
  - `src/app/foundry/` (if empty)

**Actions**:
1. Remove unused exception classes
2. Remove empty directories
3. Clean up unused utility functions

**Test**:
- Error handling works
- Exceptions are caught correctly
- No import errors

**Checkpoint**: `cleanup-stage-8-checkpoint`

---

### Stage 9: Documentation Cleanup
**Goal**: Consolidate and clean documentation

**Files to Review**:
- `resources/readme_docs/readme-lms-mcp-server.md`
- `resources/readme_docs/archived/` (review for relevance)
- `IMPLEMENTATION_REVIEW.md`
- `TEST_RESULTS.md`

**Actions**:
1. Keep only current, relevant documentation
2. Archive or remove outdated docs
3. Consolidate duplicate information
4. Update main README if needed

**Checkpoint**: `cleanup-stage-9-checkpoint`

---

### Stage 10: Final Validation
**Goal**: Complete system test and validation

**Actions**:
1. Run all test suites
2. Test all endpoints
3. Verify no broken imports
4. Check for any remaining orphaned code
5. Create final cleanup report

**Test**:
- Full integration test
- All MCP tools
- All health endpoints
- Database operations

**Checkpoint**: `cleanup-stage-10-final`

---

## Rollback Procedure

If issues occur at any stage:

```bash
# Rollback to previous checkpoint
git reset --hard cleanup-stage-{N-1}-checkpoint

# Or rollback to baseline
git reset --hard cleanup-stage-0-baseline
```

## Test Scripts

Each stage will have a corresponding test script:
- `scripts/test_stage_{N}.py` - Validates stage N cleanup

## Progress Tracking

- [ ] Stage 0: Preparation
- [ ] Stage 1: Test Scripts
- [ ] Stage 2: Configuration
- [ ] Stage 3: Database Client
- [ ] Stage 4: Health Endpoints
- [ ] Stage 5: MCP Controller
- [ ] Stage 6: Services
- [ ] Stage 7: Models & Repositories
- [ ] Stage 8: Exceptions & Utilities
- [ ] Stage 9: Documentation
- [ ] Stage 10: Final Validation


