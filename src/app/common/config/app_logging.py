"""
Enhanced logging configuration with color schemes for text within [square brackets] and success keywords.

Color Scheme:
- Entire line: Gray/White (default colorlog colors - preserved exactly)
- Text within [square brackets] in MESSAGE part only: Colored with specified colors
  - WHITE: FOUNDRY, CONTEXT
  - BLUE: Agents (ORCHESTRATOR, SUPERVISOR, REVIEWER, ENGINE, REACT_ENGINE, REACT_AGENT, SINGLE_AGENT, MULTI_AGENT)
  - GOLD: NLP (CLASSIFIER, COT_THOUGHT, WORKFLOW, HITL, PROACTIVE)
  - BRIGHT_ORANGE/GOLD: MCP keywords (MCP_AGENT, HRB_SERVICE, MCP, MCP_SERVER, MCP_PROTOCOL, LEAVE_MCP, FUNCTION_TOOL, LLM_TOOL, TOOL)
  - YELLOW: REST_API_MCP, Database calls (REPO, DB, DATABASE, POSTGRES, SQLITE, CHROMADB, HR_CHATBOT_DB, STM_DB, LTM_DB)
  - CYAN: NLP (INTENT, UNDERSTAND, DECOMPOSE, ENHANCE, ROUTER)
  - GREEN: Success (SUCCESS, TRACE ✓, brackets containing "200" or "success", and text containing "status=success" or "| 200 |")
  - RED: Errors (ERROR, CRITICAL, FAILED, FAILURE)
  - MAGENTA: Warnings (WARNING, WARN, FALLBACK, RETRY, TIMEOUT)
  - MILD PURPLE: LLM_DEBUG

IMPORTANT: Only colorizes brackets in the MESSAGE part, not in formatted parts like [%(name)s] or [%(levelname)s]
Also skips ANSI codes like [37m, [0m, [31m, etc.
Also colorizes success keywords in text (status=success, | 200 |) even if not in brackets.
"""

import logging
import sys
import re
from typing import Optional

try:
    import colorlog
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False


class EnhancedColoredFormatter(colorlog.ColoredFormatter if COLORLOG_AVAILABLE else logging.Formatter):
    """
    Enhanced colored formatter that colors only text within [square brackets] in the MESSAGE part,
    and success keywords in text, while keeping the rest of the line in default gray/white colors from colorlog.
    """
    
    # ANSI color codes - specified colors
    GREEN = '\033[38;5;77m'      # Soft green (gentle) - Success
    BLUE = '\033[38;5;75m'       # Soft blue (gentle) - Agents
    MAGENTA = '\033[38;5;171m'   # Soft magenta (gentle) - Warnings
    YELLOW = '\033[38;2;128;113;102m'  # Custom color #807166 - REST_API_MCP, Database calls
    GOLD = '\033[38;2;138;112;55m'  # Custom color #8A7037 - NLP (CLASSIFIER, COT_THOUGHT, WORKFLOW, HITL, PROACTIVE)
    BRIGHT_ORANGE = '\033[38;5;208m'  # Bright orange - MCP keywords
    BROWN = '\033[38;5;130m'     # Brown (gentle) - Backend Services/Tools (replaced with BRIGHT_ORANGE)
    RED = '\033[38;5;203m'       # Soft red (gentle) - Errors
    CYAN = '\033[38;5;87m'       # Soft cyan (gentle) - NLP (INTENT, UNDERSTAND, DECOMPOSE, ENHANCE, ROUTER)
    WHITE = '\033[97m'           # White - FOUNDRY, CONTEXT
    PURPLE = '\033[38;5;141m'    # Mild purple (gentle) - LLM_DEBUG
    RESET = '\033[0m'
    
    # Patterns for text within [square brackets] - RED
    ERROR_BRACKET_PATTERNS = [
        r"\[ERROR\]",
        r"\[CRITICAL\]",
        r"\[EXCEPTION\]",
        r"\[FAILED\]",
        r"\[FAILURE\]",
    ]
    
    # Patterns for text within [square brackets] - MAGENTA (Warnings)
    WARNING_BRACKET_PATTERNS = [
        r"\[WARNING\]",
        r"\[WARN\]",
        r"\[FAILED TO\]",
        r"\[UNABLE TO\]",
        r"\[MISSING\]",
        r"\[NOT FOUND\]",
        r"\[NOT AVAILABLE\]",
        r"\[FALLBACK\]",
        r"\[RETRY\]",
        r"\[TIMEOUT\]",
        r"\[EMPTY\]",
    ]
    
    # Patterns for text within [square brackets] - BLUE (Agents only)
    AGENT_BRACKET_PATTERNS = [
        r"\[ORCHESTRATOR\]",
        r"\[SUPERVISOR\]",
        r"\[REVIEWER\]",
        r"\[ENGINE\]",
        r"\[REACT_ENGINE\]",
        r"\[REACT_AGENT\]",
        r"\[SINGLE_AGENT\]",
        r"\[MULTI_AGENT\]",
    ]
    
    # Patterns for text within [square brackets] - WHITE (FOUNDRY, CONTEXT)
    WHITE_BRACKET_PATTERNS = [
        r"\[FOUNDRY\]",
        r"\[CONTEXT\]",
    ]
    
    # Patterns for text within [square brackets] - GOLD (NLP - CLASSIFIER, COT_THOUGHT, WORKFLOW, HITL, PROACTIVE)
    GOLD_BRACKET_PATTERNS = [
        r"\[CLASSIFIER\]",
        r"\[COT_THOUGHT\]",
        r"\[WORKFLOW\]",
        r"\[HITL\]",
        r"\[PROACTIVE\]",
    ]
    
    # Patterns for text within [square brackets] - CYAN (NLP - INTENT, UNDERSTAND, DECOMPOSE, ENHANCE, ROUTER)
    NLP_BRACKET_PATTERNS = [
        r"\[INTENT\]",
        r"\[UNDERSTAND\]",
        r"\[DECOMPOSE\]",
        r"\[ENHANCE\]",
        r"\[ROUTER\]",
    ]
    
    # Patterns for text within [square brackets] - BRIGHT_ORANGE (MCP keywords)
    MCP_BRACKET_PATTERNS = [
        r"\[MCP_AGENT\]",
        r"\[HRB_SERVICE\]",
        r"\[MCP\]",
        r"\[MCP_SERVER\]",
        r"\[MCP_PROTOCOL\]",
        r"\[LEAVE_MCP\]",
        r"\[FUNCTION_TOOL\]",
        r"\[LLM_TOOL\]",
        r"\[TOOL\]",
        r"\[REQUEST\]",
        r"\[TOOL_CALL\]",
        r"\[TOOL_EXEC\]",
        r"\[TOOL_RESULT\]",
        r"\[RESPONSE\]",
        r"\[AUTH\]",
        r"\[TOOLS\]",
    ]
    
    # Patterns for text within [square brackets] - YELLOW (REST_API_MCP, Database calls)
    YELLOW_BRACKET_PATTERNS = [
        r"\[REST_API_MCP\]",
        r"\[REPO\]",
        r"\[DB\]",
        r"\[DATABASE\]",
        r"\[POSTGRES\]",
        r"\[SQLITE\]",
        r"\[CHROMADB\]",
        r"\[HR_CHATBOT_DB\]",
        r"\[STM_DB\]",
        r"\[LTM_DB\]",
    ]
    
    # Patterns for text within [square brackets] - PURPLE (LLM_DEBUG)
    PURPLE_BRACKET_PATTERNS = [
        r"\[LLM_DEBUG\]",
    ]
    
    # Patterns for text within [square brackets] - GREEN (Success only)
    SUCCESS_BRACKET_PATTERNS = [
        r"\[TRACE\].*✓",
        r"\[SUCCESS\]",
        r"\[.*SUCCESS.*\]",  # Any bracket containing "SUCCESS"
        r"\[.*200.*\]",       # Any bracket containing "200" (HTTP status code)
        r"\[.*success.*\]",   # Any bracket containing "success" (case-insensitive)
        r"\[.*status.*success.*\]",  # Any bracket containing "status" and "success"
        r"\[.*200.*status.*\]",      # Any bracket containing "200" and "status"
    ]
    
    # Patterns for success keywords in text (not in brackets) - GREEN
    SUCCESS_TEXT_PATTERNS = [
        r'\bstatus\s*=\s*success\b',  # status=success
        r'\|\s*200\s*\|',              # | 200 |
        r'\b200\s+OK\b',                # 200 OK
        r'\bstatus\s*:\s*success\b',   # status: success
    ]
    
    def _colorize_brackets(self, text: str) -> str:
        """
        Colorize ONLY UPPER CASE text within [square brackets] in the MESSAGE part.
        Preserves colorlog's default grey/white formatting for the rest of the line.
        Skips ANSI codes, formatted parts, and lowercase text.
        
        THUMB RULE: Only colorize UPPER CASE text in brackets, preserve grey/white for everything else.
        """
        # IMPORTANT: Protect ANSI escape sequences from being matched as brackets
        # ANSI escape sequences are: \033[ followed by numbers and 'm'
        # We'll temporarily replace them with placeholders before bracket matching
        
        # Pattern to match ANSI escape sequences: \033[ followed by digits, semicolons, and 'm'
        ansi_pattern = r'\033\[[0-9;]*m'
        ansi_placeholders = {}
        placeholder_counter = 0
        
        def replace_ansi_with_placeholder(match):
            nonlocal placeholder_counter
            placeholder = f"__ANSI_PLACEHOLDER_{placeholder_counter}__"
            ansi_placeholders[placeholder] = match.group(0)
            placeholder_counter += 1
            return placeholder
        
        # Replace all ANSI codes with placeholders before bracket matching
        text_protected = re.sub(ansi_pattern, replace_ansi_with_placeholder, text)
        
        # Pattern to match [anything] in the text (now safe from ANSI codes)
        bracket_pattern = r'\[([^\]]+)\]'
        
        def replace_bracket(match):
            bracket_content = match.group(0)  # Full match including brackets: [CONTENT]
            content = match.group(1)  # Content inside brackets: CONTENT
            
            # THUMB RULE: Only colorize UPPER CASE text in brackets
            # Skip if content is not UPPER CASE (preserve grey/white for lowercase)
            if not content.isupper():
                return bracket_content
            
            # Skip ANSI color codes (like [37m, [0m, [31m, [1m, [38;5;77m, etc.)
            # ANSI codes are:
            # - Simple: digits followed by 'm' (like [37m, [0m, [31m)
            # - Complex: digits with semicolons and optional digits/letters ending in 'm' (like [38;5;77m)
            if re.match(r'^\d+[a-z;:]*m$', content) or re.match(r'^\d+[a-z;:]*$', content):
                return bracket_content
            
            # Skip common log levels from format string (INFO, DEBUG, WARNING, ERROR, CRITICAL)
            # These are already colored by colorlog, so preserve them
            if content in ['INFO', 'DEBUG', 'WARNING', 'ERROR', 'CRITICAL']:
                return bracket_content
            
            # Determine color based on content (case-insensitive matching)
            # Order matters - check more specific patterns first
            color = None
            
            # Check WHITE patterns first (FOUNDRY, CONTEXT) - highest priority
            for pattern in self.WHITE_BRACKET_PATTERNS:
                if re.search(pattern, bracket_content, re.IGNORECASE):
                    color = self.WHITE
                    break
            
            # Check SUCCESS patterns early (high priority - 200, success keywords)
            # This should be checked before other patterns to ensure success indicators are colored green
            if not color:
                for pattern in self.SUCCESS_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.GREEN
                        break
            
            # Check ERROR patterns
            if not color:
                for pattern in self.ERROR_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.RED
                        break
            
            # Check WARNING patterns
            if not color:
                for pattern in self.WARNING_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.MAGENTA
                        break
            
            # Check PURPLE patterns (LLM_DEBUG)
            if not color:
                for pattern in self.PURPLE_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.PURPLE
                        break
            
            # Check AGENT patterns (Agents - BLUE)
            if not color:
                for pattern in self.AGENT_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.BLUE
                        break
            
            # Check GOLD patterns (NLP - CLASSIFIER, COT_THOUGHT, WORKFLOW, HITL, PROACTIVE)
            if not color:
                for pattern in self.GOLD_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.GOLD
                        break
            
            # Check CYAN patterns (NLP - INTENT, UNDERSTAND, DECOMPOSE, ENHANCE, ROUTER)
            if not color:
                for pattern in self.NLP_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.CYAN
                        break
            
            # Check YELLOW patterns (REST_API_MCP, Database calls)
            if not color:
                for pattern in self.YELLOW_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.YELLOW
                        break
            
            # Check MCP patterns (MCP keywords - BRIGHT_ORANGE)
            if not color:
                for pattern in self.MCP_BRACKET_PATTERNS:
                    if re.search(pattern, bracket_content, re.IGNORECASE):
                        color = self.BRIGHT_ORANGE
                        break
            
            # If color determined, apply it; otherwise return original
            if color:
                return color + bracket_content + self.RESET
            else:
                return bracket_content
        
        # Replace all [brackets] with colored versions (on protected text)
        result = re.sub(bracket_pattern, replace_bracket, text_protected)
        
        # Restore ANSI escape sequences from placeholders
        for placeholder, ansi_code in ansi_placeholders.items():
            result = result.replace(placeholder, ansi_code)
        
        # THUMB RULE: Do NOT colorize text outside brackets
        # Preserve grey/white combination for all non-bracket text
        # Removed success keyword coloring in text - only UPPER CASE brackets get colored
        
        # Clean up any double RESET codes that might occur
        # But preserve colorlog's RESET codes - only remove duplicates
        result = re.sub(r'\033\[0m\033\[0m', self.RESET, result)
        
        return result
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with default gray/white colors for the line,
        but color only text within [square brackets] in the MESSAGE part and success keywords.
        """
        # First, let colorlog format the message with default colors (gray/white for INFO)
        if COLORLOG_AVAILABLE:
            formatted = super().format(record)
        else:
            formatted = logging.Formatter.format(self, record)
        
        # Ensure colorlog's default colors are preserved
        # colorlog applies colors via %(log_color)s and %(reset)s in the format string
        # The formatted string should already have ANSI color codes from colorlog
        # We need to preserve these while adding our custom colors to brackets
        
        # Now colorize only the [brackets] and success keywords in the formatted message
        # This preserves colorlog's default formatting for the rest of the line
        # colorlog's RESET codes are preserved to maintain gray/white line colors
        formatted = self._colorize_brackets(formatted)
        
        return formatted


def setup_logging(level: int = logging.INFO, use_colors: bool = True) -> None:
    """
    Setup enhanced logging with color schemes for [brackets] only.
    Preserves colorlog's default gray/white formatting for entire lines.
    
    Args:
        level: Logging level (default: INFO)
        use_colors: Enable color output (default: True)
    """
    root_logger = logging.getLogger()
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Remove handlers from uvicorn loggers
    for logger_name in ['uvicorn', 'uvicorn.access', 'uvicorn.error', 'fastapi']:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        logger.propagate = True
    
    if COLORLOG_AVAILABLE and use_colors:
        handler = colorlog.StreamHandler(sys.stdout)
        handler.setFormatter(
            EnhancedColoredFormatter(
                "%(log_color)s%(asctime)s [%(name)s] [%(levelname)s]%(reset)s %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "white",  # Default white for INFO (gray/white appearance)
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
                secondary_log_colors={},
                style="%",
            )
        )
        root_logger.addHandler(handler)
        root_logger.setLevel(level)
        
        # Configure uvicorn loggers
        for logger_name in ['uvicorn', 'uvicorn.access', 'uvicorn.error']:
            logger = logging.getLogger(logger_name)
            logger.setLevel(level)
            logger.propagate = True
    else:
        # Fallback to basic logging
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        root_logger.setLevel(level)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger with the given name.
    
    Args:
        name: Logger name (default: "agentic_ai")
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name or "agentic_ai")
