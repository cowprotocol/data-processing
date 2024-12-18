"""Main Entry point for app_hash sync"""
import argparse
import asyncio
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from web3 import Web3

from src.fetch.orderbook import OrderbookFetcher
from src.logger import set_log
from src.models.tables import SyncTable
from src.sync.config import (
    BatchDataSyncConfig,
)
from src.sync.batch_data import sync_batch_data
from src.utils import node_suffix

log = set_log(__name__)


@dataclass
class ScriptArgs:
    """Runtime arguments' parser/initializer"""

    sync_table: SyncTable

    def __init__(self) -> None:
        parser = argparse.ArgumentParser("Dune Community Sources Sync")
        parser.add_argument(
            "--sync-table",
            type=SyncTable,
            required=True,
            choices=list(SyncTable),
        )
        arguments, _ = parser.parse_known_args()
        self.sync_table: SyncTable = arguments.sync_table

def main() -> None:
    """
    Main function
    """
    load_dotenv()
    args = ScriptArgs()
    orderbook = OrderbookFetcher()
    network = os.environ.get("NETWORK", "mainnet")
    log.info(f"Network is set to: {network}")
    web3 = Web3(
        Web3.HTTPProvider(os.environ.get("NODE_URL" + "_" + node_suffix(network)))
    )
 
    # if args.sync_table == SyncTable.BATCH_DATA:
    #     table = os.environ["BATCH_DATA_TARGET_TABLE"]
    #     assert table, "BATCH DATA sync needs a BATCH_DATA_TARGET_TABLE env"
    #     asyncio.run(
    #         sync_batch_data(
    #             web3,
    #             orderbook,
    #             config=BatchDataSyncConfig(table),
    #         )
    #     )
    # else:
    #     log.error(f"unsupported sync_table '{args.sync_table}'")


if __name__ == "__main__":
    main()
