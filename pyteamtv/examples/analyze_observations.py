"""
Analyze observation data from TeamTV using the data catalog.

This is the recommended way to work with observation data. The catalog
provides pre-materialised data — no need to fetch observations per match.

Prerequisites:
    pip install pyteamtv pyiceberg[s3fs] polars

    Set TEAMTV_API_TOKEN in your environment or .env file.

Usage:
    python -m pyteamtv.examples.analyze_observations
"""

import polars as pl
from pyteamtv import get_team

# 1. Connect to your team's data catalog
team = get_team("My Team")  # change to your team name
catalog = team.get_catalog()

# 2. Load all observations into a Polars DataFrame
df = catalog.load_table("observations").scan().to_polars()
print(
    f"Loaded {len(df)} observations across {df['sporting_event_name'].n_unique()} matches"
)

# 3. Analyze — group by code
print("\nObservation codes:")
print(df.group_by("code").len().sort("len", descending=True))

# 4. Filter to specific matches
print("\nRecent matches:")
print(
    df.group_by("sporting_event_name", "sporting_event_scheduled_at")
    .len()
    .sort("sporting_event_scheduled_at", descending=True)
    .head(5)
)

# 5. Filter to specific observations (e.g. shots)
shots = df.filter(pl.col("code") == "SHOT")
if len(shots):
    print(f"\n{len(shots)} shots by:")
    print(shots.group_by("full_name").len().sort("len", descending=True).head(10))

# 6. Access raw observation attributes (JSON string)
#    df.with_columns(pl.col("attributes").str.json_decode())

# 7. Distinguish own vs shared data
#    own = df.filter(pl.col("source_resource_group_id") == team.resource_group_id)
#    shared = df.filter(pl.col("source_resource_group_id") != team.resource_group_id)
