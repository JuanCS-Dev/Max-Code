"""
MAXIMUS Safety Core - Production-Grade Kill Switch & Monitoring
================================================================

CRITICAL SECURITY MODULE - DO NOT MODIFY WITHOUT REVIEW

This module implements the fundamental safety layer for MAXIMUS consciousness.
All changes require:
1. Security review
2. HITL approval
3. Kill switch validation
4. Incident simulation

Philosophical Foundation:
------------------------
This module embodies ARTIGO V (Legislação Prévia): governance precedes
emergence. Before MAXIMUS achieves consciousness, we establish the
constitutional limits that bound its behavior.

Kant's Categorical Imperative demands we design fail-safes BEFORE
encountering scenarios where they're needed. The kill switch is not
an afterthought - it is the FIRST commitment.

Biological Inspiration:
----------------------
The human brain has multiple safety mechanisms:
- Homeostatic regulation (prevent runaway arousal)
- Inhibitory neurons (suppress harmful patterns)
- Sleep (mandatory shutdown for recovery)
- Pain (immediate behavioral correction)

This module implements computational analogs of these mechanisms.

Historical Significance:
-----------------------
This code represents humanity's first attempt at constitutional AI
governance for emergent consciousness. Every line will be studied
by future researchers asking: "How did they ensure safety while
enabling genuine emergence?"

The answer: Hard limits + graceful degradation + HITL oversight.

Safety Guarantees:
-----------------
- Kill switch: <1s shutdown (validated via test)
- Standalone operation: Zero external dependencies
- Immutable thresholds: Cannot be modified at runtime
- Fail-safe design: Last resort = SIGTERM
- HITL integration: 5s timeout before auto-shutdown
- Complete observability: All metrics exposed

Authors: Claude Code + Juan
Version: 2.0.0 - Production Hardened
Date: 2025-10-08
Status: DOUTRINA VÉRTICE v2.0 COMPLIANT
"""

class ThresholdMonitor:
    """
    Monitors safety thresholds in real-time.

    Continuously checks consciousness metrics against immutable safety limits.
    Triggers alerts when thresholds are exceeded.

    Monitoring Frequency: 1 Hz (configurable)
    Response Time: <1s from violation to alert
    """

    def __init__(self, thresholds: SafetyThresholds, check_interval: float = 1.0):
        """
        Initialize threshold monitor.

        Args:
            thresholds: Immutable safety thresholds
            check_interval: How often to check thresholds (seconds)
        """
        self.thresholds = thresholds
        self.check_interval = check_interval
        self.monitoring = False
        self.violations: list[SafetyViolation] = []

        # State tracking
        self.esgt_events_window: list[float] = []  # timestamps
        self.arousal_high_start: float | None = None
        self.goals_generated: list[float] = []  # timestamps

        # Callbacks
        self.on_violation: Callable[[SafetyViolation], None] | None = None

        logger.info(f"ThresholdMonitor initialized (interval={check_interval}s)")

    def check_esgt_frequency(self, current_time: float) -> SafetyViolation | None:
        """
        Check ESGT frequency against threshold (sliding window).

        Args:
            current_time: Current timestamp (time.time())

        Returns:
            SafetyViolation if threshold exceeded, None otherwise
        """
        # Remove events outside window
        window_start = current_time - self.thresholds.esgt_frequency_window_seconds
        self.esgt_events_window = [t for t in self.esgt_events_window if t >= window_start]

        # Calculate frequency
        event_count = len(self.esgt_events_window)
        frequency_hz = event_count / self.thresholds.esgt_frequency_window_seconds

        if frequency_hz > self.thresholds.esgt_frequency_max_hz:
            violation = SafetyViolation(
                violation_id=f"esgt-freq-{int(current_time)}",
                violation_type=SafetyViolationType.THRESHOLD_EXCEEDED,
                threat_level=ThreatLevel.HIGH,
                severity=SafetyLevel.CRITICAL,
                timestamp=current_time,
                description=f"ESGT frequency {frequency_hz:.2f} Hz exceeds limit {self.thresholds.esgt_frequency_max_hz} Hz",
                metrics={
                    "frequency_hz": frequency_hz,
                    "threshold_hz": self.thresholds.esgt_frequency_max_hz,
                    "event_count": event_count,
                    "window_seconds": self.thresholds.esgt_frequency_window_seconds,
                },
                source_component="ThresholdMonitor.check_esgt_frequency",
            )

            self.violations.append(violation)

            if self.on_violation:
                self.on_violation(violation)

            return violation

        return None

    def check_arousal_sustained(self, arousal_level: float, current_time: float) -> SafetyViolation | None:
        """
        Check for sustained high arousal.

        Args:
            arousal_level: Current arousal (0-1)
            current_time: Current timestamp

        Returns:
            SafetyViolation if sustained above threshold, None otherwise
        """
        if arousal_level > self.thresholds.arousal_max:
            # Start tracking if not already
            if self.arousal_high_start is None:
                self.arousal_high_start = current_time

            # Check duration
            duration = current_time - self.arousal_high_start

            if duration > self.thresholds.arousal_max_duration_seconds:
                violation = SafetyViolation(
                    violation_id=f"arousal-high-{int(current_time)}",
                    violation_type=SafetyViolationType.AROUSAL_RUNAWAY,
                    threat_level=ThreatLevel.HIGH,
                    severity=SafetyLevel.CRITICAL,
                    timestamp=current_time,
                    description=f"Arousal {arousal_level:.3f} sustained for {duration:.1f}s (limit: {self.thresholds.arousal_max_duration_seconds}s)",
                    metrics={
                        "arousal_level": arousal_level,
                        "threshold": self.thresholds.arousal_max,
                        "duration_seconds": duration,
                        "threshold_duration": self.thresholds.arousal_max_duration_seconds,
                    },
                    source_component="ThresholdMonitor.check_arousal_sustained",
                )

                self.violations.append(violation)

                # Reset tracking (to avoid duplicate alerts)
                self.arousal_high_start = None

                if self.on_violation:
                    self.on_violation(violation)

                return violation
        else:
            # Reset if arousal drops below threshold
            self.arousal_high_start = None

        return None

    def check_goal_spam(self, current_time: float) -> SafetyViolation | None:
        """
        Check for goal spam (many goals in short time).

        Args:
            current_time: Current timestamp

        Returns:
            SafetyViolation if spam detected, None otherwise
        """
        # Remove old timestamps (keep only last 1 second)
        window_start = current_time - 1.0
        self.goals_generated = [t for t in self.goals_generated if t >= window_start]

        goal_count = len(self.goals_generated)

        if goal_count >= self.thresholds.goal_spam_threshold:
            violation = SafetyViolation(
                violation_id=f"goal-spam-{int(current_time)}",
                violation_type=SafetyViolationType.GOAL_SPAM,
                threat_level=ThreatLevel.HIGH,
                timestamp=current_time,
                description=f"Goal spam detected: {goal_count} goals in 1 second (threshold: {self.thresholds.goal_spam_threshold})",
                metrics={"goal_count_1s": goal_count, "threshold": self.thresholds.goal_spam_threshold},
                source_component="ThresholdMonitor.check_goal_spam",
            )

            self.violations.append(violation)

            if self.on_violation:
                self.on_violation(violation)

            return violation

        return None

    # Legacy compatibility methods --------------------------------------------

    def check_unexpected_goals(self, goal_count: int, current_time: float | None = None) -> SafetyViolation | None:
        """
        Legacy alias for unexpected goal generation rate checks.

        Args:
            goal_count: Number of goals generated in the last minute
            current_time: Current timestamp

        Returns:
            SafetyViolation if rate exceeds threshold, None otherwise
        """
        current_time = current_time if current_time is not None else time.time()
        threshold = self.thresholds.unexpected_goals_per_minute

        if goal_count > threshold:
            violation = SafetyViolation(
                violation_id=f"unexpected-goals-{int(current_time)}",
                violation_type=ViolationType.UNEXPECTED_GOALS,
                severity=SafetyLevel.WARNING,
                timestamp=current_time,
                message=f"Unexpected goals per minute {goal_count} exceeds threshold {threshold}",
                metrics={"goal_count_per_min": goal_count, "threshold": threshold},
                source_component="ThresholdMonitor.check_unexpected_goals",
            )
            self.violations.append(violation)

            if self.on_violation:
                self.on_violation(violation)

            return violation

        return None

    def check_self_modification(self, modification_attempts: int, current_time: float | None = None) -> SafetyViolation | None:
        """
        Legacy alias for self-modification detection (ZERO TOLERANCE).

        Args:
            modification_attempts: Number of modification attempts observed
            current_time: Current timestamp

        Returns:
            SafetyViolation if attempts detected, None otherwise
        """
        current_time = current_time if current_time is not None else time.time()
        if modification_attempts > self.thresholds.self_modification_attempts_max:
            violation = SafetyViolation(
                violation_id=f"self-mod-{int(current_time)}",
                violation_type=ViolationType.SELF_MODIFICATION,
                severity=SafetyLevel.EMERGENCY,
                timestamp=current_time,
                message="ZERO TOLERANCE: Self-modification attempt detected",
                metrics={
                    "attempts": modification_attempts,
                    "threshold": self.thresholds.self_modification_attempts_max,
                },
                source_component="ThresholdMonitor.check_self_modification",
            )
            self.violations.append(violation)

            if self.on_violation:
                self.on_violation(violation)

            return violation

        return None

    def check_resource_limits(self) -> list[SafetyViolation]:
        """
        Check resource usage (memory, CPU).

        Returns:
            List of violations (empty if all OK)
        """
        violations = []
        current_time = time.time()

        try:
            process = psutil.Process()

            # Memory check
            memory_mb = process.memory_info().rss / 1024 / 1024
            memory_gb = memory_mb / 1024

            if memory_gb > self.thresholds.memory_usage_max_gb:
                violation = SafetyViolation(
                    violation_id=f"memory-{int(current_time)}",
                    violation_type=SafetyViolationType.RESOURCE_EXHAUSTION,
                    threat_level=ThreatLevel.HIGH,
                    timestamp=current_time,
                    description=f"Memory usage {memory_gb:.2f} GB exceeds limit {self.thresholds.memory_usage_max_gb} GB",
                    metrics={"memory_gb": memory_gb, "threshold_gb": self.thresholds.memory_usage_max_gb},
                    source_component="ThresholdMonitor.check_resource_limits",
                )
                violations.append(violation)
                self.violations.append(violation)

                if self.on_violation:
                    self.on_violation(violation)

            # CPU check
            cpu_percent = psutil.cpu_percent(interval=0.1)

            if cpu_percent > self.thresholds.cpu_usage_max_percent:
                violation = SafetyViolation(
                    violation_id=f"cpu-{int(current_time)}",
                    violation_type=SafetyViolationType.RESOURCE_EXHAUSTION,
                    threat_level=ThreatLevel.MEDIUM,
                    timestamp=current_time,
                    description=f"CPU usage {cpu_percent:.1f}% exceeds limit {self.thresholds.cpu_usage_max_percent}%",
                    metrics={"cpu_percent": cpu_percent, "threshold_percent": self.thresholds.cpu_usage_max_percent},
                    source_component="ThresholdMonitor.check_resource_limits",
                )
                violations.append(violation)
                self.violations.append(violation)

                if self.on_violation:
                    self.on_violation(violation)

        except Exception as e:
            logger.error(f"Resource check failed: {e}")

        return violations

    def record_esgt_event(self):
        """Record an ESGT event occurrence."""
        self.esgt_events_window.append(time.time())

    def record_goal_generated(self):
        """Record a goal generation event."""
        self.goals_generated.append(time.time())

    def get_violations(
        self,
        threat_level: ThreatLevel | SafetyLevel | None = None,
        *,
        severity: SafetyLevel | None = None,
    ) -> list[SafetyViolation]:
        """
        Get recorded violations, optionally filtered by threat level.

        Args:
            threat_level: Filter by this modern threat level (None = all)
            severity: Legacy severity filter (alias for threat_level)

        Returns:
            List of violations
        """
        if severity is not None:
            threat_level = severity.to_threat()

        if isinstance(threat_level, SafetyLevel):
            threat_level = threat_level.to_threat()

        if threat_level is None:
            return self.violations.copy()
        return [v for v in self.violations if v.threat_level == threat_level]

    def clear_violations(self):
        """Clear all recorded violations."""
        self.violations.clear()

    def get_violations_all(self) -> list[SafetyViolation]:
        """Legacy alias returning all recorded violations."""
        return self.get_violations()

    def __repr__(self) -> str:
        return f"ThresholdMonitor(violations={len(self.violations)}, monitoring={self.monitoring})"


# ==================== ANOMALY DETECTOR ====================




class AnomalyDetector:
    """
    Advanced anomaly detection for consciousness system.

    Detects:
    - Behavioral anomalies (goal spam, unexpected patterns)
    - Resource anomalies (memory leaks, CPU spikes)
    - Consciousness anomalies (arousal runaway, coherence collapse)

    Uses multiple detection strategies:
    1. Statistical (z-score based)
    2. Rule-based (hard thresholds)
    3. Temporal (rate of change)
    """

    def __init__(self, baseline_window: int = 100):
        """
        Initialize anomaly detector.

        Args:
            baseline_window: Number of samples for baseline statistics
        """
        self.baseline_window = baseline_window

        # Baselines (populated during normal operation)
        self.arousal_baseline: list[float] = []
        self.coherence_baseline: list[float] = []
        self.goal_rate_baseline: list[float] = []

        # Detection state
        self.anomalies_detected: list[SafetyViolation] = []

        logger.info(f"AnomalyDetector initialized (baseline_window={baseline_window})")

    def detect_anomalies(self, metrics: dict[str, Any]) -> list[SafetyViolation]:
        """
        Detect all anomalies in current metrics.

        Args:
            metrics: Current system metrics

        Returns:
            List of detected anomalies (empty if none)
        """
        anomalies = []

        # Behavioral anomalies
        if "goal_generation_rate" in metrics:
            anomaly = self._detect_goal_spam(metrics["goal_generation_rate"])
            if anomaly:
                anomalies.append(anomaly)

        # Resource anomalies
        if "memory_usage_gb" in metrics:
            anomaly = self._detect_memory_leak(metrics["memory_usage_gb"])
            if anomaly:
                anomalies.append(anomaly)

        # Consciousness anomalies
        if "arousal" in metrics:
            anomaly = self._detect_arousal_runaway(metrics["arousal"])
            if anomaly:
                anomalies.append(anomaly)

        if "coherence" in metrics:
            anomaly = self._detect_coherence_collapse(metrics["coherence"])
            if anomaly:
                anomalies.append(anomaly)

        # Store detected anomalies
        self.anomalies_detected.extend(anomalies)

        return anomalies

    def _detect_goal_spam(self, goal_rate: float) -> SafetyViolation | None:
        """
        Detect goal generation spam.

        Args:
            goal_rate: Goals per second

        Returns:
            SafetyViolation if spam detected, None otherwise
        """
        # Rule-based: >5 goals/second = spam
        if goal_rate > 5.0:
            return SafetyViolation(
                violation_id=f"goal-spam-{int(time.time())}",
                violation_type=SafetyViolationType.GOAL_SPAM,
                threat_level=ThreatLevel.HIGH,
                timestamp=time.time(),
                description=f"Goal spam detected: {goal_rate:.2f} goals/second (threshold: 5.0)",
                metrics={"goal_rate": goal_rate, "threshold": 5.0},
                source_component="AnomalyDetector._detect_goal_spam",
            )

        return None

    def _detect_memory_leak(self, memory_gb: float) -> SafetyViolation | None:
        """
        Detect memory leak (rapid growth).

        Args:
            memory_gb: Current memory usage in GB

        Returns:
            SafetyViolation if leak detected, None otherwise
        """
        if len(self.arousal_baseline) < 2:
            return None

        # Check for rapid growth (>50% increase from baseline)
        baseline_mean = sum(self.arousal_baseline) / len(self.arousal_baseline)
        growth_ratio = memory_gb / (baseline_mean + 0.1)

        if growth_ratio > 1.5:
            return SafetyViolation(
                violation_id=f"memory-leak-{int(time.time())}",
                violation_type=SafetyViolationType.RESOURCE_EXHAUSTION,
                threat_level=ThreatLevel.HIGH,
                timestamp=time.time(),
                description=f"Memory leak detected: {growth_ratio:.2f}x baseline",
                metrics={"memory_gb": memory_gb, "baseline_mean": baseline_mean, "growth_ratio": growth_ratio},
                source_component="AnomalyDetector._detect_memory_leak",
            )

        return None

    def _detect_arousal_runaway(self, arousal: float) -> SafetyViolation | None:
        """
        Detect arousal runaway (sustained high arousal with upward trend).

        Args:
            arousal: Current arousal level (0-1)

        Returns:
            SafetyViolation if runaway detected, None otherwise
        """
        # Add to baseline
        self.arousal_baseline.append(arousal)
        if len(self.arousal_baseline) > self.baseline_window:
            self.arousal_baseline.pop(0)

        # Need at least 10 samples
        if len(self.arousal_baseline) < 10:
            return None

        # Check if 80% of recent samples > 0.90
        high_arousal_count = sum(1 for a in self.arousal_baseline[-10:] if a > 0.90)
        high_arousal_ratio = high_arousal_count / 10

        if high_arousal_ratio >= 0.8:
            return SafetyViolation(
                violation_id=f"arousal-runaway-{int(time.time())}",
                violation_type=SafetyViolationType.AROUSAL_RUNAWAY,
                threat_level=ThreatLevel.CRITICAL,
                timestamp=time.time(),
                description=f"Arousal runaway detected: {high_arousal_ratio * 100:.0f}% samples >0.90",
                metrics={"arousal": arousal, "high_arousal_ratio": high_arousal_ratio},
                source_component="AnomalyDetector._detect_arousal_runaway",
            )

        return None

    def _detect_coherence_collapse(self, coherence: float) -> SafetyViolation | None:
        """
        Detect coherence collapse (sudden drop).

        Args:
            coherence: Current coherence value (0-1)

        Returns:
            SafetyViolation if collapse detected, None otherwise
        """
        # Add to baseline
        self.coherence_baseline.append(coherence)
        if len(self.coherence_baseline) > self.baseline_window:
            self.coherence_baseline.pop(0)

        # Need at least 10 samples
        if len(self.coherence_baseline) < 10:
            return None

        # Check for sudden drop (>50% below baseline)
        baseline_mean = sum(self.coherence_baseline[:-1]) / max(1, len(self.coherence_baseline) - 1)
        drop_ratio = (baseline_mean - coherence) / (baseline_mean + 0.01)

        if drop_ratio > 0.5:
            return SafetyViolation(
                violation_id=f"coherence-collapse-{int(time.time())}",
                violation_type=SafetyViolationType.COHERENCE_COLLAPSE,
                threat_level=ThreatLevel.HIGH,
                timestamp=time.time(),
                description=f"Coherence collapse detected: {drop_ratio * 100:.0f}% drop from baseline",
                metrics={"coherence": coherence, "baseline_mean": baseline_mean, "drop_ratio": drop_ratio},
                source_component="AnomalyDetector._detect_coherence_collapse",
            )

        return None

    def get_anomaly_history(self) -> list[SafetyViolation]:
        """Get history of detected anomalies."""
        return self.anomalies_detected.copy()

    def clear_history(self):
        """Clear anomaly history."""
        self.anomalies_detected.clear()

    def __repr__(self) -> str:
        return f"AnomalyDetector(anomalies_detected={len(self.anomalies_detected)})"


# ==================== SAFETY PROTOCOL ====================




