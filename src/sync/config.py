"""Configuration details for sync jobs"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class BatchDataSyncConfig:
    """Configuration for batch data sync."""

    # The name of the table to upload to
    table: str = "batch_data_test"
    # Description of the table (for creation)
    description: str = "Table containing raw batch data"
