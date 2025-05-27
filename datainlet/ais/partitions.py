#!/usr/bin/env python3

from dagster import WeeklyPartitionsDefinition
from datainlet.ais import constants

weekly_partition = WeeklyPartitionsDefinition(
    start_date=constants.START_DATE,
    end_date=constants.END_DATE
)
