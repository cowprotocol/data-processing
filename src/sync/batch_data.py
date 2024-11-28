"""Main Entry point for batch data sync"""
import os
from dotenv import load_dotenv
from dune_client.client import DuneClient
from web3 import Web3
from src.fetch.orderbook import OrderbookFetcher, OrderbookEnv
from src.logger import set_log
from src.sync.config import BatchDataSyncConfig
from src.sync.common import compute_block_and_month_range
from src.models.block_range import BlockRange


log = set_log(__name__)


async def sync_batch_data(
    node: Web3,
    orderbook: OrderbookFetcher,
    config: BatchDataSyncConfig,
) -> None:
    """Batch data Sync Logic"""
    load_dotenv()
    network = os.environ["NETWORK"]

    block_range_list, months_list, is_even = compute_block_and_month_range(node)
    for i, _ in enumerate(block_range_list):
        start_block = block_range_list[i][0]
        end_block = block_range_list[i][1]
        if is_even[i]:
            table_name = "raw_batch_data_latest_even_month_" + str(network)
        else:
            table_name = "raw_batch_data_latest_odd_month_" + str(network)
        block_range = BlockRange(block_from=start_block, block_to=end_block)
        log.info(
            f"About to process block range ({start_block}, {end_block}) for month {months_list[i]}"
        )
        batch_data = orderbook.get_batch_data(block_range)
        log.info("SQL query successfully executed. About to update analytics table.")
        batch_data.to_sql(
            table_name,
            orderbook._pg_engine(OrderbookEnv.ANALYTICS),
            if_exists="replace",
        )
        log.info(
            f"batch data sync run completed successfully for month {months_list[i]}"
        )
