"""Interval parsing utilities."""

from __future__ import annotations

from dataclasses import dataclass


_UNIT_TO_SECONDS = {
    "microseconds": 1e-6,
    "milliseconds": 1e-3,
    "seconds": 1.0,
    "minutes": 60.0,
    "hours": 3600.0,
}


@dataclass(frozen=True)
class ClickInterval:
    """Validated click interval."""

    raw_value: float
    unit: str

    @property
    def seconds(self) -> float:
        return self.raw_value * _UNIT_TO_SECONDS[self.unit]


def parse_interval(value: float, unit: str) -> ClickInterval:
    """Parse an interval value and unit into a validated ClickInterval."""

    if unit not in _UNIT_TO_SECONDS:
        raise ValueError(
            f"Unsupported unit '{unit}'. Use one of: {', '.join(_UNIT_TO_SECONDS)}"
        )

    if value <= 0:
        raise ValueError("Interval must be greater than 0.")

    return ClickInterval(raw_value=float(value), unit=unit)
