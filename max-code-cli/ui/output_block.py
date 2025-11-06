"""
OutputBlock - Warp-style Visual Blocks

Inspired by Warp terminal's command blocks.
Clean, visual separation of output sections.

Biblical Foundation:
"Tudo, porém, seja feito com decência e ordem" (1 Coríntios 14:40)
Organized, scannable output.

Research findings:
- True collapse requires Textual (TUI mode)
- Rich doesn't have native expand/collapse
- Solution: Visual blocks with clear separation (Warp-style)
- Focus on scannability over interactivity
"""

import logging
from typing import Optional, List, Union
from datetime import datetime
from enum import Enum

from rich.console import Console, RenderableType
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.syntax import Syntax

from ui.constants import NERD_ICONS, NEON_PALETTE

logger = logging.getLogger(__name__)


class BlockType(str, Enum):
    """Block content types."""
    TEXT = "text"
    CODE = "code"
    TABLE = "table"
    ERROR = "error"
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"


class BlockStyle(str, Enum):
    """Block visual styles."""
    DEFAULT = "cyan"
    SUCCESS = "green"
    ERROR = "red"
    WARNING = "yellow"
    INFO = "blue"
    DIM = "dim"


class OutputBlock:
    """
    Warp-style output block.

    Visual block with clear boundaries, title, and content.
    Non-collapsible but highly scannable.

    Example:
        block = OutputBlock(
            title="Code Generation",
            content="Generated 3 files",
            block_type=BlockType.SUCCESS,
            icon="✓"
        )
        console.print(block.render())
    """

    def __init__(
        self,
        title: str,
        content: Union[str, RenderableType],
        block_type: BlockType = BlockType.TEXT,
        style: Optional[BlockStyle] = None,
        icon: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        metadata: Optional[dict] = None
    ):
        """
        Initialize output block.

        Args:
            title: Block title
            content: Block content (string or Rich renderable)
            block_type: Type of block (affects styling)
            style: Override block style
            icon: Optional icon (Nerd Font)
            timestamp: Optional timestamp
            metadata: Optional metadata dict
        """
        self.title = title
        self.content = content
        self.block_type = block_type
        self.icon = icon or self._get_default_icon(block_type)
        self.timestamp = timestamp or datetime.now()
        self.metadata = metadata or {}

        # Auto-detect style from block_type if not provided
        if style is None:
            self.style = self._get_default_style(block_type)
        else:
            self.style = style

        logger.debug(f"OutputBlock created: {title} ({block_type})")

    def _get_default_icon(self, block_type: BlockType) -> str:
        """Get default icon for block type."""
        icons = {
            BlockType.SUCCESS: NERD_ICONS.get('success', '✓'),
            BlockType.ERROR: NERD_ICONS.get('error', '✗'),
            BlockType.WARNING: NERD_ICONS.get('warning', '⚠'),
            BlockType.INFO: NERD_ICONS.get('info', 'ℹ'),
            BlockType.CODE: NERD_ICONS.get('file_code', ''),
            BlockType.TABLE: NERD_ICONS.get('database', ''),
            BlockType.TEXT: NERD_ICONS.get('file', '📄'),
        }
        return icons.get(block_type, '●')

    def _get_default_style(self, block_type: BlockType) -> BlockStyle:
        """Get default style for block type."""
        styles = {
            BlockType.SUCCESS: BlockStyle.SUCCESS,
            BlockType.ERROR: BlockStyle.ERROR,
            BlockType.WARNING: BlockStyle.WARNING,
            BlockType.INFO: BlockStyle.INFO,
            BlockType.CODE: BlockStyle.DEFAULT,
            BlockType.TABLE: BlockStyle.DEFAULT,
            BlockType.TEXT: BlockStyle.DEFAULT,
        }
        return styles.get(block_type, BlockStyle.DEFAULT)

    def _format_title(self) -> str:
        """Format title with icon and timestamp."""
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"{self.icon} {self.title} [dim]({time_str})[/dim]"

    def _render_content(self) -> RenderableType:
        """Render content based on type."""
        # If content is already a Rich renderable, return as-is
        if not isinstance(self.content, str):
            return self.content

        # Handle string content based on block type
        if self.block_type == BlockType.CODE:
            # Auto-detect language from metadata
            lang = self.metadata.get('language', 'python')
            return Syntax(
                self.content,
                lang,
                theme="monokai",
                line_numbers=True
            )

        elif self.block_type == BlockType.ERROR:
            # Style error text
            text = Text(self.content, style="red")
            return text

        else:
            # Plain text
            return Text(self.content)

    def render(self) -> Panel:
        """
        Render block as Rich Panel.

        Returns:
            Panel with styled content
        """
        content = self._render_content()

        return Panel(
            content,
            title=self._format_title(),
            title_align="left",
            border_style=self.style.value,
            padding=(1, 2)
        )


class BlockManager:
    """
    Manages multiple OutputBlocks.

    Provides convenien methods for adding and displaying blocks.

    Example:
        manager = BlockManager()
        manager.add_success("Tests Passed", "All 10 tests passed")
        manager.add_error("Build Failed", "Compilation error in main.py")
        manager.print_all()
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize block manager.

        Args:
            console: Rich Console instance
        """
        self.console = console or Console()
        self.blocks: List[OutputBlock] = []

        logger.info("BlockManager initialized")

    def add_block(self, block: OutputBlock):
        """Add block to manager."""
        self.blocks.append(block)
        logger.debug(f"Block added: {block.title}")

    def add_text(
        self,
        title: str,
        content: str,
        icon: Optional[str] = None
    ):
        """Add text block (convenience)."""
        block = OutputBlock(
            title=title,
            content=content,
            block_type=BlockType.TEXT,
            icon=icon
        )
        self.add_block(block)

    def add_success(
        self,
        title: str,
        content: str,
        icon: Optional[str] = None
    ):
        """Add success block (convenience)."""
        block = OutputBlock(
            title=title,
            content=content,
            block_type=BlockType.SUCCESS,
            icon=icon
        )
        self.add_block(block)

    def add_error(
        self,
        title: str,
        content: str,
        icon: Optional[str] = None
    ):
        """Add error block (convenience)."""
        block = OutputBlock(
            title=title,
            content=content,
            block_type=BlockType.ERROR,
            icon=icon
        )
        self.add_block(block)

    def add_warning(
        self,
        title: str,
        content: str,
        icon: Optional[str] = None
    ):
        """Add warning block (convenience)."""
        block = OutputBlock(
            title=title,
            content=content,
            block_type=BlockType.WARNING,
            icon=icon
        )
        self.add_block(block)

    def add_info(
        self,
        title: str,
        content: str,
        icon: Optional[str] = None
    ):
        """Add info block (convenience)."""
        block = OutputBlock(
            title=title,
            content=content,
            block_type=BlockType.INFO,
            icon=icon
        )
        self.add_block(block)

    def add_code(
        self,
        title: str,
        code: str,
        language: str = "python",
        icon: Optional[str] = None
    ):
        """Add code block (convenience)."""
        block = OutputBlock(
            title=title,
            content=code,
            block_type=BlockType.CODE,
            icon=icon,
            metadata={'language': language}
        )
        self.add_block(block)

    def clear(self):
        """Clear all blocks."""
        self.blocks = []
        logger.debug("All blocks cleared")

    def print_all(self, spacing: int = 1):
        """
        Print all blocks to console.

        Args:
            spacing: Number of blank lines between blocks
        """
        for block in self.blocks:
            self.console.print(block.render())

            # Add spacing
            for _ in range(spacing):
                self.console.print()

    def get_blocks(self) -> List[OutputBlock]:
        """Get all blocks."""
        return self.blocks


# Convenience function
def create_block_manager(console: Optional[Console] = None) -> BlockManager:
    """
    Create block manager instance.

    Args:
        console: Rich Console instance

    Returns:
        BlockManager instance
    """
    return BlockManager(console=console)


# Demo code
if __name__ == "__main__":
    print("=" * 70)
    print("OUTPUT BLOCKS DEMO (Warp-style)")
    print("=" * 70)
    print()

    manager = create_block_manager()

    # Add various blocks
    manager.add_success(
        "Configuration Loaded",
        "Successfully loaded .env configuration with 12 variables"
    )

    manager.add_info(
        "Analyzing Codebase",
        "Found 45 Python files, 12,543 lines of code"
    )

    manager.add_code(
        "Generated Function",
        '''def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two numbers."""
    return a + b''',
        language="python"
    )

    manager.add_warning(
        "Deprecated API",
        "Function 'old_method()' is deprecated. Use 'new_method()' instead."
    )

    manager.add_error(
        "Test Failed",
        "test_authentication.py::test_login FAILED\nAssertionError: Expected 200, got 401"
    )

    # Print all blocks
    manager.print_all(spacing=0)

    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
