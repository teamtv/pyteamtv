from typing import Optional

import marimo as mo

from .app import _get_current_app, App


@mo.cache
def _get_cache():
    return {}


def get_current_app(
    app_id: Optional[str] = None,
    use_cache: bool = False,
    raise_on_missing_token: bool = True,
) -> App:
    return _get_current_app(
        app_id=app_id,
        session=_get_cache(),
        token=mo.query_params().get("token"),
        use_cache=use_cache,
        raise_on_missing_token=raise_on_missing_token,
    )
