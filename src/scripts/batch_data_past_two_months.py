"""
Script to recompute batch rewards for the current and previous month.
"""

import argparse
import os
from web3 import Web3
from dotenv import load_dotenv
import asyncio


from src.models.tables import SyncTable
from src.fetch.orderbook import OrderbookFetcher
from src.logger import set_log
from src.utils import node_suffix
from src.sync.batch_data import sync_batch_data


log = set_log(__name__)

if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser("Script Arguments")
    parser.add_argument(  # pylint: disable=duplicate-code
        "--sync-table",
        type=SyncTable,
        required=True,
        choices=list(SyncTable),
    )
    args, _ = parser.parse_known_args()

    orderbook = OrderbookFetcher()
    network = node_suffix(os.environ.get("NETWORK", "mainnet"))
    log.info(f"Network is set to: {network}")
    web3 = Web3(Web3.HTTPProvider(os.environ.get("NODE_URL" + "_" + network)))

    if args.sync_table == SyncTable.BATCH_DATA:
        asyncio.run(sync_batch_data(web3, orderbook, network, recompute_previous_month=True))
    else:
        log.error(f"unsupported sync_table '{args.sync_table}'")