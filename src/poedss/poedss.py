import asyncio
import json
import logging
from time import sleep

import click
import requests
from dateutil.parser import parse

from poedss import streamManager as sm

from . import __version__

logger = logging.getLogger(__name__)


class Poedss:
    def __init__(self, speed):

        logger.info("poedss init")

        # Get patient files
        manager = sm.StreamManager()

        dataframe = None

        try:
            logger.info("Getting Dataframe")
            dataframe = manager.getDataframe()
            dataframe = dataframe.fillna("")
            row_iter = dataframe.itertuples(index=False)
            next_row_iter = dataframe.itertuples(index=False)
            next(next_row_iter)
            for row, next_row in zip(row_iter, next_row_iter):
                # print(row.datetime)
                d1 = row.datetime
                d2 = next_row.datetime
                delta = d2 - d1
                sleep(abs(delta.total_seconds()) / speed)
                output = row._asdict()
                del output[sm.ColumnNames.DATETIME.value]
                logger.info(f"SENDING {d1} {output}")
                r = requests.post(
                    url="http://siddhi.local:8281/eventStream",
                    json=output,
                    headers={"Content-Type": "application/json"},
                )
                print(r)

        except KeyboardInterrupt:
            pass


@click.command()
@click.argument("speed", default=1000)
@click.version_option(version=__version__)
def main(speed):
    """A Project Oriented and Event-Driven Software Systems Project."""
    logger.info("Starting application")
    Poedss(speed)
