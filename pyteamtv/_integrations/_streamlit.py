from typing import Optional

import streamlit as st

from .app import _get_current_app, App


def get_current_app(
    app_id: Optional[str] = None,
    use_cache: bool = False,
    raise_on_missing_token: bool = True,
) -> App:
    query_params = st.experimental_get_query_params()

    return _get_current_app(
        app_id=app_id,
        session=st.session_state,
        token=query_params.get("token", [None])[0],
        use_cache=use_cache,
        raise_on_missing_token=raise_on_missing_token,
    )
