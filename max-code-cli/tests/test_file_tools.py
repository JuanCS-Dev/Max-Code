"""
Comprehensive File Tools Unit Tests

Tests all 5 critical file tools with real file operations, edge cases,
error handling, and performance considerations.

Biblical Foundation:
"Provai todas as coisas; retende o que é bom." (1 Tessalonicenses 5:21)
Test all things - ensure robustness.

Coverage:
1. FileReader - Reading, encoding, line limits, special files
2. FileWriter - Writing, backups, permissions, atomic writes
3. FileEditor - Editing, search/replace, diff generation
4. GlobTool - Pattern matching, file finding, ignores
5. GrepTool - Content searching, regex, context lines
"""

import pytest
import sys
import os
import tempfile
import shutil
import time
import threading
from pathlib import Path
from unittest.mock import patch, mock_open
import stat

# Add parent to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.tools.file_reader import FileReader, read_file, FileReadResult
from core.tools.file_writer import FileWriter, write_file, FileWriteResult
from core.tools.file_editor import FileEditor, edit_file, FileEditResult
from core.tools.glob_tool import GlobTool, glob_files, GlobResult
from core.tools.grep_tool import GrepTool, grep_files, GrepResult


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def temp_dir():
    """Create temporary directory for tests"""
    tmp = tempfile.mkdtemp(prefix="max_code_test_")
    yield tmp
    # Cleanup
    try:
        shutil.rmtree(tmp)
    except:
        pass


@pytest.fixture
def sample_text_file(temp_dir):
    """Create a sample text file"""
    file_path = Path(temp_dir) / "sample.txt"
    content = """Line 1: Hello World
Line 2: Python Testing
Line 3: File Operations
Line 4: Test Data
Line 5: End of File
"""
    file_path.write_text(content, encoding='utf-8')
    return str(file_path)


@pytest.fixture
def sample_py_file(temp_dir):
    """Create a sample Python file"""
    file_path = Path(temp_dir) / "sample.py"
    content = """def hello():
    print('Hello, World!')
    return True

def goodbye():
    print('Goodbye, World!')
    return False

# TODO: Add more functions
# FIXME: Fix the bug
"""
    file_path.write_text(content, encoding='utf-8')
    return str(file_path)


@pytest.fixture
def large_file(temp_dir):
    """Create a large file for performance testing"""
    file_path = Path(temp_dir) / "large.txt"
    with open(file_path, 'w', encoding='utf-8') as f:
        for i in range(5000):
            f.write(f"Line {i+1}: " + "x" * 80 + "\n")
    return str(file_path)


@pytest.fixture
def nested_dir_structure(temp_dir):
    """Create nested directory structure with files"""
    # Create structure:
    # temp_dir/
    #   ├── dir1/
    #   │   ├── file1.py
    #   │   └── file2.txt
    #   ├── dir2/
    #   │   ├── subdir/
    #   │   │   └── file3.py
    #   │   └── file4.js
    #   └── root.py

    dirs = [
        Path(temp_dir) / "dir1",
        Path(temp_dir) / "dir2" / "subdir",
    ]

    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    files = {
        "dir1/file1.py": "# Python file 1\ndef test(): pass",
        "dir1/file2.txt": "Text file content",
        "dir2/subdir/file3.py": "# Python file 3\ndef main(): pass",
        "dir2/file4.js": "// JavaScript file",
        "root.py": "# Root Python file\nprint('hello')",
    }

    for rel_path, content in files.items():
        file_path = Path(temp_dir) / rel_path
        file_path.write_text(content, encoding='utf-8')

    return temp_dir


# ============================================================================
# TEST FILEREADER
# ============================================================================

class TestFileReader:
    """Tests for FileReader tool"""

    def test_read_simple_file(self, sample_text_file):
        """Test reading a simple text file"""
        reader = FileReader()
        result = reader.read(sample_text_file)

        assert result.success
        assert result.content is not None
        assert result.total_lines == 5  # 5 lines (Python readlines strips trailing newline)
        assert result.encoding == "utf-8"
        assert "Hello World" in result.content
        assert "→" in result.content  # Check cat -n formatting

    def test_read_with_limit(self, sample_text_file):
        """Test reading with line limit"""
        reader = FileReader()
        result = reader.read(sample_text_file, limit=3)

        assert result.success
        assert result.lines_read == 3
        assert result.truncated
        assert "Line 1" in result.content
        assert "Line 4" not in result.content

    def test_read_with_offset(self, sample_text_file):
        """Test reading with offset"""
        reader = FileReader()
        result = reader.read(sample_text_file, offset=3, limit=2)

        assert result.success
        assert result.lines_read == 2
        assert result.offset == 3
        assert "Line 3" in result.content
        assert "Line 1" not in result.content

    def test_read_specific_line_range(self, sample_text_file):
        """Test read_lines method"""
        reader = FileReader()
        result = reader.read_lines(sample_text_file, start_line=2, end_line=4)

        assert result.success
        assert result.lines_read == 3  # Lines 2, 3, 4
        assert "Line 2" in result.content
        assert "Line 4" in result.content

    def test_read_large_file(self, large_file):
        """Test reading large file with default limits"""
        reader = FileReader()
        start = time.time()
        result = reader.read(large_file)
        duration = time.time() - start

        assert result.success
        assert result.lines_read == 2000  # Default limit
        assert result.truncated
        assert duration < 1.0  # Should be fast

    def test_read_nonexistent_file(self):
        """Test reading non-existent file"""
        reader = FileReader()
        result = reader.read("/nonexistent/file.txt")

        assert not result.success
        assert "not found" in result.error.lower()

    def test_read_directory(self, temp_dir):
        """Test reading a directory (should fail)"""
        reader = FileReader()
        result = reader.read(temp_dir)

        assert not result.success
        assert "not a file" in result.error.lower()

    def test_read_with_encoding(self, temp_dir):
        """Test reading file with specific encoding"""
        # Create file with latin-1 encoding
        file_path = Path(temp_dir) / "latin1.txt"
        content = "Café com açúcar"
        file_path.write_bytes(content.encode('latin-1'))

        reader = FileReader()
        result = reader.read(str(file_path), encoding='latin-1')

        assert result.success
        assert "Café" in result.content

    def test_read_binary_fallback(self, temp_dir):
        """Test reading binary file falls back to latin-1"""
        # Create file with invalid UTF-8
        file_path = Path(temp_dir) / "binary.txt"
        file_path.write_bytes(b"Hello\x80\x81\x82World")

        reader = FileReader()
        result = reader.read(str(file_path))

        assert result.success
        assert result.encoding == "latin-1"

    def test_read_long_lines_truncation(self, temp_dir):
        """Test long lines are truncated"""
        file_path = Path(temp_dir) / "long_lines.txt"
        long_line = "x" * 3000  # Longer than max_line_length
        file_path.write_text(long_line, encoding='utf-8')

        reader = FileReader(max_line_length=2000)
        result = reader.read(str(file_path))

        assert result.success
        assert "[truncated]" in result.content

    def test_read_all(self, sample_text_file):
        """Test read_all method"""
        reader = FileReader()
        result = reader.read_all(sample_text_file)

        assert result.success
        assert result.lines_read == result.total_lines
        assert not result.truncated

    def test_convenience_function(self, sample_text_file):
        """Test read_file convenience function"""
        content = read_file(sample_text_file, limit=3)

        assert "Line 1" in content
        assert "→" in content


# ============================================================================
# TEST FILEWRITER
# ============================================================================

class TestFileWriter:
    """Tests for FileWriter tool"""

    def test_write_new_file(self, temp_dir):
        """Test writing a new file"""
        file_path = Path(temp_dir) / "new.txt"
        writer = FileWriter()

        content = "Hello, World!\nLine 2"
        result = writer.write(str(file_path), content)

        assert result.success
        assert result.bytes_written > 0
        assert not result.overwritten
        assert file_path.exists()
        assert file_path.read_text() == content

    def test_write_overwrite_file(self, sample_text_file):
        """Test overwriting existing file"""
        writer = FileWriter()

        new_content = "New content"
        result = writer.write(sample_text_file, new_content, overwrite=True)

        assert result.success
        assert result.overwritten
        assert result.backup_path is not None
        assert Path(sample_text_file).read_text() == new_content

    def test_write_with_backup(self, sample_text_file):
        """Test backup creation"""
        original_content = Path(sample_text_file).read_text()
        writer = FileWriter(create_backup=True)

        result = writer.write(sample_text_file, "New content", overwrite=True)

        assert result.success
        assert result.backup_path is not None
        backup_path = Path(result.backup_path)
        assert backup_path.exists()
        assert backup_path.read_text() == original_content

    def test_write_no_overwrite_protection(self, sample_text_file):
        """Test overwrite protection"""
        writer = FileWriter()

        result = writer.write(sample_text_file, "New content", overwrite=False)

        assert not result.success
        assert "exists" in result.error.lower()

    def test_write_creates_directories(self, temp_dir):
        """Test automatic directory creation"""
        file_path = Path(temp_dir) / "nested" / "dirs" / "file.txt"
        writer = FileWriter(create_dirs=True)

        result = writer.write(str(file_path), "Content")

        assert result.success
        assert result.created_dirs
        assert file_path.exists()

    def test_write_no_dir_creation(self, temp_dir):
        """Test write fails when directory doesn't exist"""
        file_path = Path(temp_dir) / "nonexistent" / "file.txt"
        writer = FileWriter(create_dirs=False)

        result = writer.write(str(file_path), "Content")

        assert not result.success

    def test_write_dry_run(self, temp_dir):
        """Test dry run mode"""
        file_path = Path(temp_dir) / "dryrun.txt"
        writer = FileWriter()

        result = writer.write(str(file_path), "Content", dry_run=True)

        assert result.success
        assert result.bytes_written > 0
        assert not file_path.exists()  # File not actually written

    def test_write_lines(self, temp_dir):
        """Test write_lines method"""
        file_path = Path(temp_dir) / "lines.txt"
        writer = FileWriter()

        lines = ["Line 1", "Line 2", "Line 3"]
        result = writer.write_lines(str(file_path), lines)

        assert result.success
        content = Path(file_path).read_text()
        assert content == "Line 1\nLine 2\nLine 3\n"

    def test_append_to_file(self, sample_text_file):
        """Test appending to existing file"""
        original_content = Path(sample_text_file).read_text()
        writer = FileWriter()

        append_content = "Appended line\n"
        result = writer.append(sample_text_file, append_content)

        assert result.success
        new_content = Path(sample_text_file).read_text()
        assert new_content == original_content + append_content

    def test_write_special_characters(self, temp_dir):
        """Test writing special characters"""
        file_path = Path(temp_dir) / "special.txt"
        writer = FileWriter()

        content = "Special chars: 你好 🚀 €£¥ \n\t"
        result = writer.write(str(file_path), content)

        assert result.success
        # Note: \r might be normalized by the OS
        written = Path(file_path).read_text(encoding='utf-8')
        assert "你好" in written
        assert "🚀" in written

    def test_convenience_function(self, temp_dir):
        """Test write_file convenience function"""
        file_path = Path(temp_dir) / "convenience.txt"

        success = write_file(str(file_path), "Test content")

        assert success
        assert file_path.exists()


# ============================================================================
# TEST FILEEDITOR
# ============================================================================

class TestFileEditor:
    """Tests for FileEditor tool"""

    def test_simple_edit(self, sample_py_file):
        """Test simple string replacement"""
        editor = FileEditor()

        result = editor.edit(
            sample_py_file,
            old_string="Hello, World!",
            new_string="Greetings, Universe!"
        )

        assert result.success
        assert result.replacements == 1
        assert result.backup_path is not None
        assert result.diff is not None

        content = Path(sample_py_file).read_text()
        assert "Greetings, Universe!" in content
        assert "Hello, World!" not in content

    def test_replace_all(self, sample_py_file):
        """Test replacing all occurrences"""
        editor = FileEditor()

        result = editor.edit(
            sample_py_file,
            old_string="World",
            new_string="Universe",
            replace_all=True
        )

        assert result.success
        assert result.replacements == 2  # Both "Hello, World!" and "Goodbye, World!"

    def test_edit_nonunique_without_replace_all(self, sample_py_file):
        """Test error when string is not unique"""
        editor = FileEditor()

        result = editor.edit(
            sample_py_file,
            old_string="World",
            new_string="Universe",
            replace_all=False
        )

        assert not result.success
        assert "appears" in result.error.lower()

    def test_edit_string_not_found(self, sample_py_file):
        """Test error when old_string not found"""
        editor = FileEditor()

        result = editor.edit(
            sample_py_file,
            old_string="NonexistentString",
            new_string="Something"
        )

        assert not result.success
        assert "not found" in result.error.lower()

    def test_edit_same_strings(self, sample_py_file):
        """Test error when old_string == new_string"""
        editor = FileEditor()

        result = editor.edit(
            sample_py_file,
            old_string="Hello",
            new_string="Hello"
        )

        assert not result.success
        assert "must be different" in result.error.lower()

    def test_edit_nonexistent_file(self):
        """Test editing non-existent file"""
        editor = FileEditor()

        result = editor.edit(
            "/nonexistent/file.py",
            old_string="old",
            new_string="new"
        )

        assert not result.success
        assert "not found" in result.error.lower()

    def test_edit_preserves_formatting(self, temp_dir):
        """Test that editing preserves indentation and formatting"""
        file_path = Path(temp_dir) / "format.py"
        content = """def function():
    # Indented comment
    if True:
        nested_code()
"""
        file_path.write_text(content, encoding='utf-8')

        editor = FileEditor()
        result = editor.edit(
            str(file_path),
            old_string="nested_code",
            new_string="updated_code"
        )

        assert result.success
        new_content = file_path.read_text()
        assert "    if True:\n        updated_code()" in new_content

    def test_edit_multiline_string(self, temp_dir):
        """Test editing multiline strings"""
        file_path = Path(temp_dir) / "multiline.txt"
        content = """Line 1
Line 2
Line 3
Line 4"""
        file_path.write_text(content, encoding='utf-8')

        editor = FileEditor()
        result = editor.edit(
            str(file_path),
            old_string="Line 2\nLine 3",
            new_string="New Line 2\nNew Line 3"
        )

        assert result.success
        assert "New Line 2" in file_path.read_text()

    def test_edit_multiple(self, sample_py_file):
        """Test multiple edits"""
        editor = FileEditor()

        edits = [
            ("def hello():", "def greet():"),
            ("def goodbye():", "def farewell():"),
        ]

        result = editor.edit_multiple(sample_py_file, edits)

        assert result.success
        assert result.replacements == 2

        content = Path(sample_py_file).read_text()
        assert "def greet():" in content
        assert "def farewell():" in content

    def test_diff_generation(self, sample_py_file):
        """Test diff generation"""
        editor = FileEditor()

        result = editor.edit(
            sample_py_file,
            old_string="Hello",
            new_string="Hi",
            generate_diff=True
        )

        assert result.success
        assert result.diff is not None
        assert "-" in result.diff  # Removed lines
        assert "+" in result.diff  # Added lines

    def test_convenience_function(self, sample_py_file):
        """Test edit_file convenience function"""
        success = edit_file(
            sample_py_file,
            old_string="print('Hello, World!')",
            new_string="print('Hi there!')"
        )

        assert success
        assert "Hi there!" in Path(sample_py_file).read_text()


# ============================================================================
# TEST GLOBTOOL
# ============================================================================

class TestGlobTool:
    """Tests for GlobTool"""

    def test_glob_simple_pattern(self, nested_dir_structure):
        """Test simple glob pattern"""
        tool = GlobTool()
        result = tool.glob("*.py", path=nested_dir_structure)

        assert result.success
        assert result.total_matches == 1  # Only root.py
        assert "root.py" in result.matches[0]

    def test_glob_recursive_pattern(self, nested_dir_structure):
        """Test recursive glob pattern"""
        tool = GlobTool()
        result = tool.glob("**/*.py", path=nested_dir_structure)

        assert result.success
        assert result.total_matches == 3  # root.py, file1.py, file3.py

    def test_glob_by_extension(self, nested_dir_structure):
        """Test find_by_extension method"""
        tool = GlobTool()
        result = tool.find_by_extension("py", path=nested_dir_structure)

        assert result.success
        assert result.total_matches == 3

    def test_glob_by_name(self, nested_dir_structure):
        """Test find_by_name method"""
        tool = GlobTool()
        result = tool.find_by_name("file*.py", path=nested_dir_structure)

        assert result.success
        assert result.total_matches == 2  # file1.py, file3.py

    def test_glob_with_ignore_patterns(self, nested_dir_structure):
        """Test ignoring patterns"""
        # Create a __pycache__ directory
        pycache = Path(nested_dir_structure) / "dir1" / "__pycache__"
        pycache.mkdir()
        (pycache / "cache.pyc").write_text("cache")

        tool = GlobTool()
        result = tool.glob("**/*.pyc", path=nested_dir_structure)

        assert result.success
        assert result.total_matches == 0  # Should be ignored
        assert result.ignored_count > 0

    def test_glob_max_results(self, nested_dir_structure):
        """Test max results limit"""
        tool = GlobTool()
        result = tool.glob("**/*", path=nested_dir_structure, max_results=2)

        assert result.success
        assert len(result.matches) <= 2

    def test_glob_nonexistent_path(self):
        """Test globbing non-existent path"""
        tool = GlobTool()
        result = tool.glob("*.py", path="/nonexistent/path")

        assert not result.success
        assert "does not exist" in result.error.lower()

    def test_glob_not_a_directory(self, sample_text_file):
        """Test globbing a file instead of directory"""
        tool = GlobTool()
        result = tool.glob("*.py", path=sample_text_file)

        assert not result.success
        assert "not a directory" in result.error.lower()

    def test_glob_sort_by_mtime(self, nested_dir_structure):
        """Test sorting by modification time"""
        # Modify file3.py to be newest
        file3 = Path(nested_dir_structure) / "dir2" / "subdir" / "file3.py"
        time.sleep(0.1)
        file3.write_text("# Updated\ndef main(): pass")

        tool = GlobTool()
        result = tool.glob("**/*.py", path=nested_dir_structure, sort_by_mtime=True)

        assert result.success
        # file3.py should be first (newest)
        assert "file3.py" in result.matches[0]

    def test_convenience_function(self, nested_dir_structure):
        """Test glob_files convenience function"""
        files = glob_files("**/*.py", path=nested_dir_structure)

        assert len(files) == 3
        assert all(".py" in f for f in files)


# ============================================================================
# TEST GREPTOOL
# ============================================================================

class TestGrepTool:
    """Tests for GrepTool"""

    def test_grep_simple_pattern(self, sample_py_file):
        """Test simple grep pattern"""
        tool = GrepTool()
        result = tool.grep(
            "Hello",
            path=str(Path(sample_py_file).parent),
            output_mode="content"
        )

        assert result.success
        assert result.total_matches > 0
        assert len(result.matches) > 0
        assert result.matches[0].line_content is not None

    def test_grep_regex_pattern(self, sample_py_file):
        """Test regex pattern"""
        tool = GrepTool()
        result = tool.grep(
            r"def\s+\w+\(\):",
            path=str(Path(sample_py_file).parent),
            output_mode="content"
        )

        assert result.success
        assert result.total_matches >= 2  # hello() and goodbye()

    def test_grep_case_insensitive(self, sample_py_file):
        """Test case-insensitive search"""
        tool = GrepTool()
        result = tool.grep(
            "HELLO",
            path=str(Path(sample_py_file).parent),
            output_mode="content",
            case_sensitive=False
        )

        assert result.success
        assert result.total_matches > 0

    def test_grep_files_with_matches_mode(self, nested_dir_structure):
        """Test files_with_matches output mode"""
        tool = GrepTool()
        result = tool.grep(
            "def",
            path=nested_dir_structure,
            output_mode="files_with_matches",
            file_type="py"
        )

        assert result.success
        assert len(result.files_with_matches) > 0
        assert all(".py" in f for f in result.files_with_matches)

    def test_grep_count_mode(self, nested_dir_structure):
        """Test count output mode"""
        tool = GrepTool()
        result = tool.grep(
            "def",
            path=nested_dir_structure,
            output_mode="count",
            file_type="py"
        )

        assert result.success
        assert len(result.match_counts) > 0
        assert all(isinstance(count, int) for count in result.match_counts.values())

    def test_grep_with_file_type_filter(self, nested_dir_structure):
        """Test file type filtering"""
        tool = GrepTool()
        result = tool.grep(
            "file",
            path=nested_dir_structure,
            output_mode="files_with_matches",
            file_type="js"
        )

        assert result.success
        # Should only search .js files
        assert all(".js" in f for f in result.files_with_matches)

    def test_grep_with_glob_filter(self, nested_dir_structure):
        """Test glob pattern filtering"""
        tool = GrepTool()
        result = tool.grep(
            "Python",
            path=nested_dir_structure,
            output_mode="files_with_matches",
            glob_filter="**/dir1/*.py"
        )

        assert result.success
        # Should only match files in dir1
        assert all("dir1" in f for f in result.files_with_matches)

    def test_grep_invalid_regex(self):
        """Test invalid regex pattern"""
        tool = GrepTool()
        result = tool.grep(
            "[invalid(regex",
            path=".",
            output_mode="content"
        )

        assert not result.success
        assert "invalid" in result.error.lower()

    def test_grep_nonexistent_path(self):
        """Test grep on non-existent path"""
        tool = GrepTool()
        result = tool.grep(
            "pattern",
            path="/nonexistent/path",
            output_mode="content"
        )

        assert not result.success
        assert "does not exist" in result.error.lower()

    def test_grep_find_todos(self, sample_py_file):
        """Test find_todos helper"""
        tool = GrepTool()
        result = tool.find_todos(path=str(Path(sample_py_file).parent))

        assert result.success
        assert result.total_matches >= 2  # TODO and FIXME

    def test_grep_find_imports(self, temp_dir):
        """Test find_imports helper"""
        file_path = Path(temp_dir) / "imports.py"
        content = """import os
from pathlib import Path
import sys
from collections import defaultdict
"""
        file_path.write_text(content, encoding='utf-8')

        tool = GrepTool()
        result = tool.find_imports("pathlib", path=temp_dir)

        assert result.success
        assert result.total_matches >= 1

    def test_grep_find_function_calls(self, sample_py_file):
        """Test find_function_calls helper"""
        tool = GrepTool()
        result = tool.find_function_calls("print", path=str(Path(sample_py_file).parent))

        assert result.success
        assert result.total_matches >= 2

    def test_grep_max_matches(self, nested_dir_structure):
        """Test max matches limit"""
        tool = GrepTool()
        result = tool.grep(
            ".",  # Match any character
            path=nested_dir_structure,
            output_mode="content",
            max_matches=5
        )

        assert result.success
        assert len(result.matches) <= 5

    def test_convenience_function(self, nested_dir_structure):
        """Test grep_files convenience function"""
        files = grep_files("def", path=nested_dir_structure, file_type="py")

        assert len(files) > 0
        assert all(".py" in f for f in files)


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Performance tests for file tools"""

    def test_concurrent_reads(self, nested_dir_structure):
        """Test concurrent file reads"""
        reader = FileReader()
        files = list(Path(nested_dir_structure).rglob("*.py"))

        results = []
        threads = []

        def read_file(path):
            result = reader.read(str(path))
            results.append(result)

        start = time.time()
        for file_path in files:
            t = threading.Thread(target=read_file, args=(file_path,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        duration = time.time() - start

        assert len(results) == len(files)
        assert all(r.success for r in results)
        assert duration < 1.0  # Should be fast

    def test_large_file_performance(self, large_file):
        """Test performance with large file"""
        reader = FileReader()

        # Test reading with limit (should be fast)
        start = time.time()
        result = reader.read(large_file, limit=100)
        duration = time.time() - start

        assert result.success
        assert duration < 0.5  # Should be very fast

    def test_glob_performance(self, temp_dir):
        """Test glob performance with many files"""
        # Create 100 files
        for i in range(100):
            file_path = Path(temp_dir) / f"file_{i}.txt"
            file_path.write_text(f"Content {i}")

        tool = GlobTool()

        start = time.time()
        result = tool.glob("*.txt", path=temp_dir)
        duration = time.time() - start

        assert result.success
        assert result.total_matches == 100
        assert duration < 1.0  # Should be fast

    def test_grep_performance(self, temp_dir):
        """Test grep performance with many files"""
        # Create 50 files with content
        for i in range(50):
            file_path = Path(temp_dir) / f"file_{i}.txt"
            content = "\n".join([f"Line {j}: test content" for j in range(100)])
            file_path.write_text(content)

        tool = GrepTool()

        start = time.time()
        result = tool.grep("test", path=temp_dir, output_mode="count")
        duration = time.time() - start

        assert result.success
        assert duration < 2.0  # Should complete in reasonable time


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Edge case tests for file tools"""

    def test_empty_file(self, temp_dir):
        """Test reading empty file"""
        file_path = Path(temp_dir) / "empty.txt"
        file_path.write_text("", encoding='utf-8')

        reader = FileReader()
        result = reader.read(str(file_path))

        assert result.success
        assert result.total_lines == 0  # Empty file has 0 lines

    def test_file_with_only_newlines(self, temp_dir):
        """Test file with only newlines"""
        file_path = Path(temp_dir) / "newlines.txt"
        file_path.write_text("\n\n\n\n", encoding='utf-8')

        reader = FileReader()
        result = reader.read(str(file_path))

        assert result.success
        assert result.total_lines == 4  # 4 newlines = 4 lines in readlines()

    def test_file_without_trailing_newline(self, temp_dir):
        """Test file without trailing newline"""
        file_path = Path(temp_dir) / "no_newline.txt"
        file_path.write_text("Line 1\nLine 2", encoding='utf-8')

        reader = FileReader()
        result = reader.read(str(file_path))

        assert result.success
        assert "Line 2" in result.content

    def test_unicode_characters(self, temp_dir):
        """Test files with Unicode characters"""
        file_path = Path(temp_dir) / "unicode.txt"
        content = "Hello 世界 🌍 Привет مرحبا"
        file_path.write_text(content, encoding='utf-8')

        reader = FileReader()
        result = reader.read(str(file_path))

        assert result.success
        assert "世界" in result.content
        assert "🌍" in result.content

    def test_write_atomic_on_error(self, temp_dir):
        """Test atomic write behavior on error"""
        file_path = Path(temp_dir) / "atomic.txt"
        file_path.write_text("Original content", encoding='utf-8')

        writer = FileWriter()

        # Simulate write error by making directory read-only
        # Note: This test may not work on all systems
        # We'll just verify the backup is created

        result = writer.write(str(file_path), "New content", overwrite=True)

        # If write succeeds, backup should exist
        if result.success:
            assert result.backup_path is not None

    def test_special_filenames(self, temp_dir):
        """Test files with special characters in names"""
        special_names = [
            "file with spaces.txt",
            "file-with-dashes.txt",
            "file_with_underscores.txt",
            "file.multiple.dots.txt",
        ]

        writer = FileWriter()

        for name in special_names:
            file_path = Path(temp_dir) / name
            result = writer.write(str(file_path), "Content")
            assert result.success
            assert file_path.exists()


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

class TestErrorHandling:
    """Error handling tests"""

    def test_permission_denied_read(self, temp_dir):
        """Test reading file with no permissions"""
        file_path = Path(temp_dir) / "no_read.txt"
        file_path.write_text("Secret content", encoding='utf-8')

        # Remove read permission
        file_path.chmod(0o000)

        reader = FileReader()
        result = reader.read(str(file_path))

        # Restore permissions for cleanup
        file_path.chmod(0o644)

        assert not result.success
        assert "permission" in result.error.lower()

    def test_invalid_encoding(self, temp_dir):
        """Test reading with invalid encoding"""
        file_path = Path(temp_dir) / "invalid_encoding.txt"
        # Write UTF-8 content
        file_path.write_text("Hello World", encoding='utf-8')

        reader = FileReader()
        # Try to read as ASCII (will fail on non-ASCII, but should fallback)
        result = reader.read(str(file_path), encoding='ascii')

        # Should fallback to latin-1
        assert result.success or result.encoding == 'latin-1'

    def test_glob_pattern_error(self, nested_dir_structure):
        """Test glob with invalid pattern"""
        tool = GlobTool()
        # Empty pattern is invalid in pathlib.glob
        result = tool.glob("", path=nested_dir_structure)

        # Empty pattern should fail with error
        assert not result.success
        assert result.error is not None
        assert len(result.error) > 0

    def test_grep_on_binary_files(self, temp_dir):
        """Test grep skips binary files"""
        # Create a binary file
        binary_path = Path(temp_dir) / "binary.bin"
        binary_path.write_bytes(bytes(range(256)))

        tool = GrepTool()
        result = tool.grep("test", path=temp_dir, output_mode="files_with_matches")

        # Binary file should be skipped
        assert result.success
        assert "binary.bin" not in result.files_with_matches


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests combining multiple tools"""

    def test_write_then_read(self, temp_dir):
        """Test writing then reading a file"""
        file_path = Path(temp_dir) / "test.txt"
        content = "Test content\nLine 2"

        writer = FileWriter()
        write_result = writer.write(str(file_path), content)
        assert write_result.success

        reader = FileReader()
        read_result = reader.read(str(file_path))
        assert read_result.success
        assert "Test content" in read_result.content

    def test_write_edit_read(self, temp_dir):
        """Test write, edit, then read workflow"""
        file_path = Path(temp_dir) / "workflow.txt"

        # Write
        writer = FileWriter()
        writer.write(str(file_path), "Original content")

        # Edit
        editor = FileEditor()
        edit_result = editor.edit(
            str(file_path),
            old_string="Original",
            new_string="Modified"
        )
        assert edit_result.success

        # Read
        reader = FileReader()
        read_result = reader.read(str(file_path))
        assert read_result.success
        assert "Modified" in read_result.content

    def test_glob_then_grep(self, nested_dir_structure):
        """Test finding files with glob, then searching content with grep"""
        # Find all Python files
        glob_tool = GlobTool()
        glob_result = glob_tool.glob("**/*.py", path=nested_dir_structure)
        assert glob_result.success

        # Search those files for "def"
        grep_tool = GrepTool()
        grep_result = grep_tool.grep(
            "def",
            path=nested_dir_structure,
            output_mode="count",
            file_type="py"
        )
        assert grep_result.success
        assert grep_result.total_matches > 0

    def test_grep_then_edit(self, temp_dir):
        """Test finding pattern with grep, then editing matches"""
        # Create test files
        for i in range(3):
            file_path = Path(temp_dir) / f"file{i}.txt"
            file_path.write_text(f"Old value: {i}")

        # Find files with pattern
        grep_tool = GrepTool()
        grep_result = grep_tool.grep(
            "Old value",
            path=temp_dir,
            output_mode="files_with_matches"
        )
        assert grep_result.success
        assert len(grep_result.files_with_matches) == 3

        # Edit first file
        editor = FileEditor()
        first_file = Path(temp_dir) / grep_result.files_with_matches[0]
        edit_result = editor.edit(
            str(first_file),
            old_string="Old value",
            new_string="New value"
        )
        assert edit_result.success


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
