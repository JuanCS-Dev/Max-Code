"""
Sabbath Mode Manager for Max-Code CLI

Scheduled graceful service degradation for Biblical rest and reflection.

Features:
- Biblical Sabbath observance (Friday sunset → Saturday sunset)
- Christian Sabbath (Sunday observance)
- Custom schedules (user-defined)
- Timezone-aware calculations
- Graceful degradation (essential services only)
- MAXIMUS integration for consciousness rest

FASE 9 - Advanced Features
"""

import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

import pytz
from astral import LocationInfo
from astral.sun import sun

from rich.console import Console

from core.maximus_integration.client_v2 import MaximusClient
from config.settings import get_settings


class SabbathTradition(str, Enum):
    """Sabbath tradition types."""
    JEWISH = "jewish"
    CHRISTIAN = "christian"
    CUSTOM = "custom"


@dataclass
class SabbathSchedule:
    """Sabbath schedule information."""
    tradition: SabbathTradition
    timezone: str
    custom_start: Optional[datetime] = None
    custom_end: Optional[datetime] = None
    auto_enable: bool = False


@dataclass
class SabbathStatus:
    """Current Sabbath mode status."""
    is_active: bool
    next_sabbath: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_scheduled: bool = False
    tradition: Optional[SabbathTradition] = None


@dataclass
class SabbathConfig:
    """Sabbath mode configuration."""
    schedule: Optional[SabbathSchedule] = None
    enabled: bool = False

    @classmethod
    def load(cls, config_dir: Path = None) -> 'SabbathConfig':
        """Load configuration from file."""
        if config_dir is None:
            config_dir = Path.home() / ".max-code"

        config_file = config_dir / "sabbath_config.json"

        if not config_file.exists():
            return cls()

        try:
            with open(config_file, 'r') as f:
                data = json.load(f)

                schedule_data = data.get("schedule")
                schedule = None
                if schedule_data:
                    schedule = SabbathSchedule(
                        tradition=SabbathTradition(schedule_data["tradition"]),
                        timezone=schedule_data["timezone"],
                        custom_start=datetime.fromisoformat(schedule_data["custom_start"]) if schedule_data.get("custom_start") else None,
                        custom_end=datetime.fromisoformat(schedule_data["custom_end"]) if schedule_data.get("custom_end") else None,
                        auto_enable=schedule_data.get("auto_enable", False)
                    )

                return cls(
                    schedule=schedule,
                    enabled=data.get("enabled", False)
                )
        except Exception:
            return cls()

    def save(self, config_dir: Path = None):
        """Save configuration to file."""
        if config_dir is None:
            config_dir = Path.home() / ".max-code"

        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / "sabbath_config.json"

        data = {
            "enabled": self.enabled,
            "schedule": None
        }

        if self.schedule:
            data["schedule"] = {
                "tradition": self.schedule.tradition.value,
                "timezone": self.schedule.timezone,
                "custom_start": self.schedule.custom_start.isoformat() if self.schedule.custom_start else None,
                "custom_end": self.schedule.custom_end.isoformat() if self.schedule.custom_end else None,
                "auto_enable": self.schedule.auto_enable
            }

        with open(config_file, 'w') as f:
            json.dump(data, f, indent=2)


class SabbathManager:
    """
    Sabbath mode management for graceful service degradation.

    Features:
    - Scheduled feature toggling (cron-based)
    - Biblical Sabbath observance (Friday sunset → Saturday sunset)
    - Graceful degradation (essential services only)
    - Timezone-aware scheduling
    - Cultural sensitivity (Jewish, Christian, custom schedules)

    Biblical Foundation:
    - Exodus 20:8-11 (4th Commandment)
    - Leviticus 23:3 (Day of rest and sacred assembly)
    - Isaiah 58:13-14 (Call the Sabbath a delight)

    Technical Implementation:
    - Essential services remain available (health, status, config)
    - Non-essential features disabled (predict, learn, heavy AI)
    - MAXIMUS consciousness enters rest state
    - Graceful fallback for all commands
    """

    def __init__(self):
        """Initialize Sabbath manager."""
        self.config = SabbathConfig.load()
        self.console = Console()
        self.settings = get_settings()

        # MAXIMUS integration (optional)
        self.maximus_client = MaximusClient()

    def calculate_sabbath_window(
        self,
        tradition: SabbathTradition,
        timezone: str = "UTC",
        location_lat: float = 32.0853,  # Jerusalem default
        location_lon: float = 34.7818
    ) -> Tuple[datetime, datetime]:
        """
        Calculate next Sabbath window based on tradition.

        Args:
            tradition: Sabbath tradition (jewish, christian, custom)
            timezone: Timezone name (e.g., "America/New_York")
            location_lat: Latitude for sunset calculation (Jewish tradition)
            location_lon: Longitude for sunset calculation (Jewish tradition)

        Returns:
            Tuple of (start_time, end_time) as timezone-aware datetime objects

        Biblical Reference:
            Jewish: "From evening to evening you shall observe your sabbath" (Lev 23:32)
            Christian: "On the first day of the week" (Acts 20:7, 1 Cor 16:2)
        """
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)

        if tradition == SabbathTradition.JEWISH:
            # Friday sunset to Saturday sunset
            # Find next Friday
            days_until_friday = (4 - now.weekday()) % 7
            if days_until_friday == 0 and now.hour >= 18:  # Past Friday evening
                days_until_friday = 7

            next_friday = now + timedelta(days=days_until_friday)
            next_saturday = next_friday + timedelta(days=1)

            # Calculate sunset times using astral
            location = LocationInfo(
                name="Location",
                region="Region",
                timezone=timezone,
                latitude=location_lat,
                longitude=location_lon
            )

            # Friday sunset
            friday_sun_data = sun(location.observer, date=next_friday.date())
            start = friday_sun_data["sunset"].astimezone(tz)

            # Saturday sunset
            saturday_sun_data = sun(location.observer, date=next_saturday.date())
            end = saturday_sun_data["sunset"].astimezone(tz)

        elif tradition == SabbathTradition.CHRISTIAN:
            # Sunday 00:00 to 23:59
            days_until_sunday = (6 - now.weekday()) % 7
            if days_until_sunday == 0 and now.hour >= 23:  # Past Sunday
                days_until_sunday = 7

            next_sunday = now + timedelta(days=days_until_sunday)
            start = next_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(hours=24)

        else:  # CUSTOM
            if not self.config.schedule or not self.config.schedule.custom_start:
                # Default to next day 00:00-23:59
                tomorrow = now + timedelta(days=1)
                start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
                end = start + timedelta(hours=24)
            else:
                start = self.config.schedule.custom_start.astimezone(tz)
                end = self.config.schedule.custom_end.astimezone(tz)

        return (start, end)

    def is_sabbath_active(self) -> bool:
        """Check if currently in Sabbath mode."""
        if not self.config.enabled:
            return False

        if not self.config.schedule:
            return False

        # Check if within Sabbath window
        start, end = self.calculate_sabbath_window(
            self.config.schedule.tradition,
            self.config.schedule.timezone
        )

        tz = pytz.timezone(self.config.schedule.timezone)
        now = datetime.now(tz)

        return start <= now <= end

    def enable_sabbath_mode(self):
        """
        Enable Sabbath mode (graceful degradation).

        Biblical Principle: "Remember the Sabbath day, to keep it holy" (Ex 20:8)

        Technical Actions:
        - Disable non-essential services
        - Reduce MAXIMUS consciousness activity
        - Switch to minimal UI
        - Enable graceful fallback for all commands
        """
        self.console.print("[yellow]Entering Sabbath mode...[/yellow]")

        # Update config
        self.config.enabled = True
        self.config.save()

        # Notify MAXIMUS services (if available)
        # NOTE: MaximusClient v2 requires async context - notification skipped in sync method
        # To enable: refactor to async or use background task
        # try:
        #     async with self.maximus_client as client:
        #         await client.consciousness.set_sabbath_mode(True)
        #         self.console.print("[dim]MAXIMUS consciousness entering rest state...[/dim]")
        # except Exception as e:
        #     self.console.print(f"[dim]MAXIMUS notification failed: {e}[/dim]")

        # Update settings (in-memory only, doesn't persist)
        self.settings.ui.sabbath_mode = True

        self.console.print("[green]✓[/green] Sabbath mode active")
        self.console.print()
        self.console.print("[bold cyan]Essential services only. Rest and reflect.[/bold cyan]")
        self.console.print("[dim]Isaiah 58:13-14 - 'Call the Sabbath a delight'[/dim]")
        self.console.print()

    def disable_sabbath_mode(self):
        """
        Disable Sabbath mode (restore full functionality).

        Technical Actions:
        - Re-enable all services
        - Restore MAXIMUS consciousness activity
        - Restore full UI
        """
        self.console.print("[cyan]Exiting Sabbath mode...[/cyan]")

        # Update config
        self.config.enabled = False
        self.config.save()

        # Notify MAXIMUS services (if available)
        # NOTE: MaximusClient v2 requires async context - notification skipped
        # try:
        #     async with self.maximus_client as client:
        #         await client.consciousness.set_sabbath_mode(False)
        #         self.console.print("[dim]MAXIMUS consciousness resuming...[/dim]")
        # except Exception:
        #     pass

        # Update settings
        self.settings.ui.sabbath_mode = False

        self.console.print("[green]✓[/green] Full functionality restored")
        self.console.print()

    def get_status(self) -> SabbathStatus:
        """Get current Sabbath mode status."""
        is_active = self.is_sabbath_active()

        next_sabbath = None
        end_time = None
        if self.config.schedule:
            start, end = self.calculate_sabbath_window(
                self.config.schedule.tradition,
                self.config.schedule.timezone
            )
            next_sabbath = start if not is_active else None
            end_time = end if is_active else None

        return SabbathStatus(
            is_active=is_active,
            next_sabbath=next_sabbath,
            end_time=end_time,
            is_scheduled=bool(self.config.schedule and self.config.schedule.auto_enable),
            tradition=self.config.schedule.tradition if self.config.schedule else None
        )

    def schedule_auto_sabbath(
        self,
        tradition: SabbathTradition,
        timezone: str,
        location_lat: float = 32.0853,
        location_lon: float = 34.7818
    ):
        """
        Enable auto-scheduling of Sabbath mode.

        Args:
            tradition: Sabbath tradition
            timezone: Timezone name
            location_lat: Latitude for sunset calculation
            location_lon: Longitude for sunset calculation
        """
        # Calculate next Sabbath
        start, end = self.calculate_sabbath_window(
            tradition, timezone, location_lat, location_lon
        )

        # Create schedule
        self.config.schedule = SabbathSchedule(
            tradition=tradition,
            timezone=timezone,
            custom_start=start if tradition == SabbathTradition.CUSTOM else None,
            custom_end=end if tradition == SabbathTradition.CUSTOM else None,
            auto_enable=True
        )

        self.config.save()

        self.console.print(f"[green]✓[/green] Auto-Sabbath scheduled ({tradition.value})")
        self.console.print(f"  Next Sabbath: [cyan]{start.strftime('%Y-%m-%d %H:%M %Z')}[/cyan]")
        self.console.print(f"  Ends: [cyan]{end.strftime('%Y-%m-%d %H:%M %Z')}[/cyan]")
