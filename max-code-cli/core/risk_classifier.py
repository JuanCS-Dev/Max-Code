"""
Risk Classifier - Assess risk of file operations

Classifies operations by risk level to determine if user confirmation is needed.

Biblical Foundation:
"O prudente prevê o perigo e toma precauções; o simples segue adiante e sofre as consequências" (Provérbios 27:12)
Wisdom through risk assessment.

Features:
- 5 risk levels (SAFE → CRITICAL)
- Critical file pattern detection
- Batch operation assessment
- Reversibility tracking
- Detailed reasoning

Soli Deo Gloria
"""

from enum import Enum
from typing import Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path


class RiskLevel(Enum):
    """Risk levels for operations"""
    SAFE = "safe"          # Read-only, no side effects
    LOW = "low"            # Create new files, append
    MEDIUM = "medium"      # Edit existing files
    HIGH = "high"          # Delete, overwrite critical files
    CRITICAL = "critical"  # System operations, batch deletes
    
    def __lt__(self, other):
        """Compare risk levels"""
        if not isinstance(other, RiskLevel):
            return NotImplemented
        order = list(RiskLevel)
        return order.index(self) < order.index(other)
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other


@dataclass
class RiskAssessment:
    """Result of risk assessment"""
    level: RiskLevel
    reason: str
    affected_files: List[str]
    reversible: bool
    backup_available: bool = False
    
    @property
    def requires_confirmation(self) -> bool:
        """Check if confirmation is required"""
        return self.level >= RiskLevel.MEDIUM


class RiskClassifier:
    """
    Classifies operations by risk level
    
    Examples:
        >>> classifier = RiskClassifier()
        >>> risk = classifier.assess_file_operation("write", "/path/file.py", exists=True)
        >>> if risk.requires_confirmation:
        ...     # Ask confirmation
    """
    
    # Critical file patterns (high risk to modify/delete)
    CRITICAL_PATTERNS = [
        ".git/",
        ".github/workflows/",
        "node_modules/",
        "__pycache__/",
        ".env",
        ".env.prod",
        ".env.production",
        "secrets",
        "secret",
        "config.prod",
        "config.production",
        "database",
        "db.sqlite",
        ".credentials",
        "private_key",
        "id_rsa",
    ]
    
    # Protected file extensions
    PROTECTED_EXTENSIONS = [
        ".key",
        ".pem",
        ".crt",
        ".p12",
        ".pfx",
    ]
    
    # System directories (critical to modify)
    SYSTEM_DIRS = [
        "/etc/",
        "/usr/",
        "/bin/",
        "/sbin/",
        "/boot/",
        "/sys/",
        "/proc/",
    ]
    
    def __init__(self):
        """Initialize risk classifier"""
        pass
    
    def assess_file_operation(
        self,
        operation: str,  # "read", "write", "delete", "edit"
        filepath: str,
        file_exists: bool = False,
        content_size: int = 0,
        is_batch: bool = False
    ) -> RiskAssessment:
        """
        Assess risk of file operation
        
        Args:
            operation: Type of operation
            filepath: Target file path
            file_exists: Whether file exists
            content_size: Size of content in bytes
            is_batch: Whether part of batch operation
        
        Returns:
            RiskAssessment
        """
        path = Path(filepath)
        
        # Read operations are always safe
        if operation == "read":
            return RiskAssessment(
                level=RiskLevel.SAFE,
                reason="Read-only operation (no changes to filesystem)",
                affected_files=[filepath],
                reversible=True,
                backup_available=False
            )
        
        # Check if file/path is critical
        is_critical = self._is_critical_file(filepath)
        is_system_path = self._is_system_path(filepath)
        
        # System paths are always critical
        if is_system_path:
            return RiskAssessment(
                level=RiskLevel.CRITICAL,
                reason=f"System path modification: {filepath}",
                affected_files=[filepath],
                reversible=False,
                backup_available=False
            )
        
        # Delete operations
        if operation == "delete":
            if is_critical:
                return RiskAssessment(
                    level=RiskLevel.CRITICAL,
                    reason=f"Deleting critical file: {self._get_critical_reason(filepath)}",
                    affected_files=[filepath],
                    reversible=False,
                    backup_available=False
                )
            
            if is_batch:
                return RiskAssessment(
                    level=RiskLevel.HIGH,
                    reason="Batch deletion (irreversible)",
                    affected_files=[filepath],
                    reversible=False,
                    backup_available=False
                )
            
            return RiskAssessment(
                level=RiskLevel.HIGH,
                reason="File deletion is irreversible",
                affected_files=[filepath],
                reversible=False,
                backup_available=False
            )
        
        # Write/Edit operations
        if operation in ["write", "edit"]:
            if not file_exists:
                # Creating new file (low risk)
                return RiskAssessment(
                    level=RiskLevel.LOW,
                    reason="Creating new file",
                    affected_files=[filepath],
                    reversible=True,
                    backup_available=False
                )
            
            # Modifying existing file
            if is_critical:
                return RiskAssessment(
                    level=RiskLevel.HIGH,
                    reason=f"Modifying critical file: {self._get_critical_reason(filepath)}",
                    affected_files=[filepath],
                    reversible=True,  # If using git or backups
                    backup_available=True
                )
            
            # Large file changes (>50KB)
            if content_size > 50000:
                return RiskAssessment(
                    level=RiskLevel.MEDIUM,
                    reason=f"Large file modification ({content_size:,} bytes)",
                    affected_files=[filepath],
                    reversible=True,
                    backup_available=True
                )
            
            # Standard file modification
            return RiskAssessment(
                level=RiskLevel.MEDIUM,
                reason="Modifying existing file",
                affected_files=[filepath],
                reversible=True,
                backup_available=True
            )
        
        # Unknown operation (cautious approach)
        return RiskAssessment(
            level=RiskLevel.MEDIUM,
            reason=f"Unknown operation: {operation}",
            affected_files=[filepath],
            reversible=False,
            backup_available=False
        )
    
    def assess_batch_operation(
        self,
        operations: List[Tuple[str, str]]  # [(operation, filepath), ...]
    ) -> RiskAssessment:
        """
        Assess risk of multiple operations
        
        Args:
            operations: List of (operation, filepath) tuples
        
        Returns:
            RiskAssessment for the entire batch
        """
        if len(operations) > 20:
            return RiskAssessment(
                level=RiskLevel.CRITICAL,
                reason=f"Large batch operation ({len(operations)} files) - review carefully",
                affected_files=[op[1] for op in operations],
                reversible=False,
                backup_available=False
            )
        
        if len(operations) > 10:
            return RiskAssessment(
                level=RiskLevel.HIGH,
                reason=f"Batch operation on {len(operations)} files",
                affected_files=[op[1] for op in operations],
                reversible=False,
                backup_available=False
            )
        
        # Assess individual risks
        risks = [
            self.assess_file_operation(op, fp, is_batch=True)
            for op, fp in operations
        ]
        
        # Take highest risk level
        max_risk = max(risks, key=lambda r: r.level)
        
        # Check if any are critical
        critical_files = [
            r.affected_files[0] for r in risks
            if r.level == RiskLevel.CRITICAL
        ]
        
        if critical_files:
            return RiskAssessment(
                level=RiskLevel.CRITICAL,
                reason=f"Batch includes {len(critical_files)} critical file(s)",
                affected_files=[op[1] for op in operations],
                reversible=False,
                backup_available=False
            )
        
        return RiskAssessment(
            level=max_risk.level,
            reason=f"Batch: {max_risk.reason} ({len(operations)} files)",
            affected_files=[op[1] for op in operations],
            reversible=all(r.reversible for r in risks),
            backup_available=any(r.backup_available for r in risks)
        )
    
    def _is_critical_file(self, filepath: str) -> bool:
        """Check if file matches critical patterns"""
        filepath_lower = filepath.lower()
        
        # Check patterns
        for pattern in self.CRITICAL_PATTERNS:
            if pattern in filepath_lower:
                return True
        
        # Check extensions
        for ext in self.PROTECTED_EXTENSIONS:
            if filepath_lower.endswith(ext):
                return True
        
        return False
    
    def _is_system_path(self, filepath: str) -> bool:
        """Check if path is in system directory"""
        for sys_dir in self.SYSTEM_DIRS:
            if filepath.startswith(sys_dir):
                return True
        return False
    
    def _get_critical_reason(self, filepath: str) -> str:
        """Get reason why file is critical"""
        filepath_lower = filepath.lower()
        
        if ".env" in filepath_lower:
            return "environment configuration"
        if ".git/" in filepath_lower:
            return "git repository metadata"
        if "secret" in filepath_lower or "password" in filepath_lower:
            return "contains secrets/credentials"
        if "database" in filepath_lower or "db." in filepath_lower:
            return "database file"
        if any(ext in filepath_lower for ext in self.PROTECTED_EXTENSIONS):
            return "cryptographic key/certificate"
        if "node_modules/" in filepath_lower or "__pycache__/" in filepath_lower:
            return "generated/dependency directory"
        
        return "critical system file"


# Convenience function
def assess_operation(
    operation: str,
    filepath: str,
    file_exists: bool = False,
    **kwargs
) -> RiskAssessment:
    """
    Convenience function to assess operation risk
    
    Args:
        operation: Operation type
        filepath: File path
        file_exists: Whether file exists
        **kwargs: Additional arguments
    
    Returns:
        RiskAssessment
    """
    classifier = RiskClassifier()
    return classifier.assess_file_operation(
        operation,
        filepath,
        file_exists,
        **kwargs
    )


# Export
__all__ = [
    'RiskLevel',
    'RiskAssessment',
    'RiskClassifier',
    'assess_operation',
]
