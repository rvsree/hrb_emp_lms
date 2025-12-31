"""Test script to verify logging colors are working in hrb_emp_lms."""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.app.common.config.app_logging import setup_logging, get_logger

# Setup logging
setup_logging(level=20)  # INFO level
logger = get_logger("test_colors")

print("\n" + "="*80)
print("Testing hrb_emp_lms Logging Colors")
print("="*80)
print()

# Test different log levels
logger.info("[MCP] This is an MCP log message - should be ORANGE")
logger.info("[AUTH] API key verified - should be ORANGE")
logger.info("[REQUEST] Incoming request - should be ORANGE")
logger.info("[TOOLS] Listing tools - should be ORANGE")
logger.info("[TOOL_CALL] Executing tool - should be ORANGE")
logger.info("[TOOL_EXEC] Tool execution - should be ORANGE")
logger.info("[TOOL_RESULT] Tool result - should be ORANGE")
logger.info("[RESPONSE] Response sent - should be ORANGE")

logger.info("[SUCCESS] Operation completed - should be GREEN")
logger.info("status=success - should be GREEN")

logger.warning("[WARNING] This is a warning - should be MAGENTA")

logger.error("[ERROR] This is an error - should be RED")
logger.critical("[CRITICAL] This is critical - should be RED")

print("\n" + "="*80)
print("Color Test Complete")
print("="*80)
print()
print("Expected Colors:")
print("  - [MCP], [AUTH], [REQUEST], etc. -> BRIGHT_ORANGE")
print("  - [SUCCESS] -> GREEN")
print("  - [WARNING] -> MAGENTA")
print("  - [ERROR], [CRITICAL] -> RED")
print("  - Entire line -> Gray/White (default)")
print()

