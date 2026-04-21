# pyteamtv

Python SDK for the TeamTV platform.

## Quick start

```bash
pip install pyteamtv pyiceberg[s3fs] polars
```

Set `TEAMTV_API_TOKEN` in your environment or `.env` file.

## Working with observation data (Polars)

Use `get_catalog()` to access observation data as a Polars DataFrame.
This returns pre-materialised data — fast and filterable.

```python
from pyteamtv import get_team
import polars as pl

team = get_team("My Team")
catalog = team.get_catalog()
df = catalog.load_table("observations").scan().to_polars()

# Filter to shots
shots = df.filter(pl.col("code") == "SHOT")

# Group by player
shots.group_by("full_name").len().sort("len", descending=True)

# Filter to a specific match
match = df.filter(pl.col("sporting_event_name") == "Team A - Team B")

# Distinguish own vs shared data
own = df.filter(pl.col("source_resource_group_id") == team.resource_group_id)
shared = df.filter(pl.col("source_resource_group_id") != team.resource_group_id)
```

### Use with DuckDB

```python
table = catalog.load_table("observations")
con = table.scan().to_duckdb("observations")
con.sql("SELECT code, COUNT(*) FROM observations GROUP BY code").show()
```

### Available columns

| Column | Description |
|---|---|
| `sporting_event_id` | Match UUID |
| `sporting_event_name` | Match name (e.g. "Team A - Team B") |
| `sporting_event_scheduled_at` | Scheduled time (UTC) |
| `observation_id` | Observation UUID |
| `code` | Observation type (e.g. SHOT, POSSESSION, CUSTOM) |
| `description` | Free-text description |
| `start_time`, `end_time` | Timing (seconds) |
| `clock_id` | Clock identifier |
| `team_id`, `team_name`, `team_ground` | Team context |
| `person_id`, `first_name`, `last_name`, `full_name`, `number` | Primary person |
| `attributes` | Raw observation attributes (JSON string) |
| `persons` | Additional persons by role (JSON string) |
| `source_resource_group_id`, `source_resource_group_name` | Data provenance |
| `enrichment`, `enrichment_version` | Computed fields (JSON string) |

## Examples

See [`pyteamtv/examples/analyze_observations.py`](pyteamtv/examples/analyze_observations.py) for a complete working script.
