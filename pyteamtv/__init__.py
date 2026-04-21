"""
pyteamtv — Python SDK for the TeamTV platform.

Quick start::

    from pyteamtv import get_team

    team = get_team("My Team")

Working with observation data
-----------------------------

Use ``get_catalog()`` to query observation data. This returns
pre-materialised data via Apache Iceberg — fast, filterable, and ready
for analysis with Polars, DuckDB, or Pandas.

::

    catalog = team.get_catalog()
    df = catalog.load_table("observations").scan().to_polars()

    # Filter, aggregate, join — standard Polars/Pandas/DuckDB workflows
    shots = df.filter(pl.col("code") == "SHOT")

The catalog is auto-discovered from the platform's service registry.
Requires ``pyiceberg`` (``pip install pyiceberg[s3fs]``).

Available tables:

- **observations** — one row per observation across all sporting events
  the team has access to (own + shared). Columns include
  ``sporting_event_id``, ``sporting_event_name``, ``code``,
  ``team_id``, ``team_name``, ``person_id``, ``first_name``,
  ``last_name``, ``start_time``, ``end_time``, ``attributes`` (JSON),
  ``source_resource_group_id``, and more.
"""

import os
from typing import Optional

try:
    __PYTEAMTV_SETUP__
except NameError:
    __PYTEAMTV_SETUP__ = False

if not __PYTEAMTV_SETUP__:
    from .api import TeamTVApp, TeamTVUser

    def get_team(name: Optional[str] = None, resource_group_id: Optional[str] = None):
        """
        Get a TeamResourceGroup by name or resource_group_id.

        Requires the ``TEAMTV_API_TOKEN`` environment variable to be set.

        For data analysis, use ``team.get_catalog()`` to access
        observation data efficiently::

            team = get_team("My Team")
            catalog = team.get_catalog()
            df = catalog.load_table("observations").scan().to_polars()
        """
        if "TEAMTV_API_TOKEN" in os.environ:
            app = TeamTVUser(os.environ["TEAMTV_API_TOKEN"])
            return app.get_team(name=name, resource_group_id=resource_group_id)
        else:
            raise Exception("'TEAMTV_API_TOKEN' environment variable is not set.")


__version__ = "0.40.0"
