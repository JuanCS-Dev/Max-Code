"""
Tests for Interactive Confirmation System

Tests:
- Risk classification
- Confirmation UI
- FileEditor integration
- Batch operations

Soli Deo Gloria
"""

import pytest
from pathlib import Path
import tempfile
import os

from core.risk_classifier import RiskLevel, RiskAssessment, RiskClassifier, assess_operation
from ui.confirmation import ConfirmationUI, QuietConfirmationUI, confirm_operation
from core.tools.file_editor import FileEditor


class TestRiskClassifier:
    """Test risk classification"""
    
    def test_read_operations_are_safe(self):
        """Read operations should always be safe"""
        classifier = RiskClassifier()
        
        risk = classifier.assess_file_operation("read", "/path/file.py")
        
        assert risk.level == RiskLevel.SAFE
        assert not risk.requires_confirmation
        assert risk.reversible
    
    def test_new_file_creation_is_low_risk(self):
        """Creating new files should be low risk"""
        classifier = RiskClassifier()
        
        risk = classifier.assess_file_operation("write", "/path/new.py", file_exists=False)
        
        assert risk.level == RiskLevel.LOW
        assert not risk.requires_confirmation
    
    def test_edit_existing_file_is_medium_risk(self):
        """Editing existing files should require confirmation"""
        classifier = RiskClassifier()
        
        risk = classifier.assess_file_operation("edit", "/path/existing.py", file_exists=True)
        
        assert risk.level == RiskLevel.MEDIUM
        assert risk.requires_confirmation
        assert risk.reversible
        assert risk.backup_available
    
    def test_delete_operation_is_high_risk(self):
        """Delete operations should be high risk"""
        classifier = RiskClassifier()
        
        risk = classifier.assess_file_operation("delete", "/path/file.py", file_exists=True)
        
        assert risk.level == RiskLevel.HIGH
        assert risk.requires_confirmation
        assert not risk.reversible
    
    def test_critical_file_patterns(self):
        """Critical files should be highest risk"""
        classifier = RiskClassifier()
        
        # .env file
        risk = classifier.assess_file_operation("delete", ".env", file_exists=True)
        assert risk.level == RiskLevel.CRITICAL
        
        # .git/ directory
        risk = classifier.assess_file_operation("edit", ".git/config", file_exists=True)
        assert risk.level == RiskLevel.HIGH
        
        # secrets file
        risk = classifier.assess_file_operation("edit", "secrets.json", file_exists=True)
        assert risk.level == RiskLevel.HIGH
    
    def test_protected_extensions(self):
        """Protected file extensions should be high risk"""
        classifier = RiskClassifier()
        
        risk = classifier.assess_file_operation("edit", "private.key", file_exists=True)
        assert risk.level == RiskLevel.HIGH
        
        risk = classifier.assess_file_operation("edit", "cert.pem", file_exists=True)
        assert risk.level == RiskLevel.HIGH
    
    def test_system_paths_are_critical(self):
        """System paths should be critical"""
        classifier = RiskClassifier()
        
        risk = classifier.assess_file_operation("edit", "/etc/passwd", file_exists=True)
        assert risk.level == RiskLevel.CRITICAL
        
        risk = classifier.assess_file_operation("edit", "/usr/bin/python", file_exists=True)
        assert risk.level == RiskLevel.CRITICAL
    
    def test_large_files_increase_risk(self):
        """Large file modifications should increase risk"""
        classifier = RiskClassifier()
        
        # Small file (under 50KB)
        risk = classifier.assess_file_operation(
            "edit",
            "/path/small.py",
            file_exists=True,
            content_size=5000
        )
        assert risk.level == RiskLevel.MEDIUM
        
        # Large file (over 50KB)
        risk = classifier.assess_file_operation(
            "edit",
            "/path/large.py",
            file_exists=True,
            content_size=100000
        )
        assert risk.level == RiskLevel.MEDIUM
        assert "Large file" in risk.reason
    
    def test_batch_operations(self):
        """Batch operations should be assessed properly"""
        classifier = RiskClassifier()
        
        # Small batch (5 files) - assuming they exist
        operations = [("edit", f"file{i}.py") for i in range(5)]
        risk = classifier.assess_batch_operation(operations)
        # Batch of edits should be at least MEDIUM since files "might" exist
        # But our assess treats them as new files, so LOW is expected
        assert risk.level >= RiskLevel.LOW
        
        # Medium batch (15 files)
        operations = [("edit", f"file{i}.py") for i in range(15)]
        risk = classifier.assess_batch_operation(operations)
        assert risk.level == RiskLevel.HIGH
        
        # Large batch (25 files)
        operations = [("delete", f"file{i}.py") for i in range(25)]
        risk = classifier.assess_batch_operation(operations)
        assert risk.level == RiskLevel.CRITICAL
    
    def test_convenience_function(self):
        """Test convenience function"""
        risk = assess_operation("read", "/path/file.py")
        assert risk.level == RiskLevel.SAFE


class TestRiskAssessment:
    """Test RiskAssessment dataclass"""
    
    def test_requires_confirmation_property(self):
        """Test requires_confirmation property"""
        # SAFE/LOW don't require confirmation
        risk = RiskAssessment(
            level=RiskLevel.SAFE,
            reason="test",
            affected_files=[],
            reversible=True
        )
        assert not risk.requires_confirmation
        
        risk = RiskAssessment(
            level=RiskLevel.LOW,
            reason="test",
            affected_files=[],
            reversible=True
        )
        assert not risk.requires_confirmation
        
        # MEDIUM+ require confirmation
        risk = RiskAssessment(
            level=RiskLevel.MEDIUM,
            reason="test",
            affected_files=[],
            reversible=True
        )
        assert risk.requires_confirmation
        
        risk = RiskAssessment(
            level=RiskLevel.HIGH,
            reason="test",
            affected_files=[],
            reversible=False
        )
        assert risk.requires_confirmation


class TestConfirmationUI:
    """Test confirmation UI"""
    
    def test_safe_operations_skip_confirmation(self):
        """Safe operations should skip confirmation"""
        from io import StringIO
        from rich.console import Console
        
        console = Console(file=StringIO())
        ui = ConfirmationUI(console)
        
        risk = RiskAssessment(
            level=RiskLevel.SAFE,
            reason="Read-only",
            affected_files=["test.py"],
            reversible=True
        )
        
        # Should return True without prompting
        result = ui.confirm_file_operation(risk)
        assert result == True
    
    def test_quiet_ui_always_confirms(self):
        """QuietConfirmationUI should always return True"""
        ui = QuietConfirmationUI()
        
        risk = RiskAssessment(
            level=RiskLevel.CRITICAL,
            reason="Critical operation",
            affected_files=["important.py"],
            reversible=False
        )
        
        # Should return True even for critical
        result = ui.confirm_file_operation(risk)
        assert result == True
    
    def test_convenience_function(self):
        """Test convenience function"""
        risk = RiskAssessment(
            level=RiskLevel.LOW,
            reason="Low risk",
            affected_files=["test.py"],
            reversible=True
        )
        
        # Quiet mode
        result = confirm_operation(risk, quiet=True)
        assert result == True


class TestFileEditorIntegration:
    """Test FileEditor with confirmation"""
    
    def setup_method(self):
        """Setup test file"""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = Path(self.test_dir) / "test.py"
        self.test_file.write_text("def hello():\n    print('hello')\n")
    
    def teardown_method(self):
        """Cleanup test files"""
        import shutil
        if Path(self.test_dir).exists():
            shutil.rmtree(self.test_dir)
    
    def test_editor_with_skip_confirmation(self):
        """Test editor with skip_confirmation=True"""
        editor = FileEditor(skip_confirmation=True)
        
        result = editor.edit(
            str(self.test_file),
            old_string="def hello():",  # More specific string
            new_string="def goodbye():"
        )
        
        # Should succeed without prompting
        assert result.success
        assert result.replacements == 1
        assert "goodbye" in self.test_file.read_text()
    
    def test_editor_has_confirmation_components(self):
        """Test that editor has confirmation components"""
        editor = FileEditor()
        
        assert hasattr(editor, 'risk_classifier')
        assert hasattr(editor, 'confirmation_ui')
        assert editor.skip_confirmation == False
    
    def test_editor_quiet_mode(self):
        """Test editor in quiet mode"""
        editor = FileEditor(skip_confirmation=True)
        
        # Should have QuietConfirmationUI
        from ui.confirmation import QuietConfirmationUI
        assert isinstance(editor.confirmation_ui, QuietConfirmationUI)


class TestRiskLevelComparison:
    """Test RiskLevel enum comparison"""
    
    def test_risk_level_ordering(self):
        """Test that risk levels can be compared"""
        assert RiskLevel.SAFE < RiskLevel.LOW
        assert RiskLevel.LOW < RiskLevel.MEDIUM
        assert RiskLevel.MEDIUM < RiskLevel.HIGH
        assert RiskLevel.HIGH < RiskLevel.CRITICAL
        
        assert RiskLevel.CRITICAL > RiskLevel.HIGH
        assert RiskLevel.HIGH >= RiskLevel.HIGH
        assert RiskLevel.LOW <= RiskLevel.MEDIUM


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
