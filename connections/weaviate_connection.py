from copy import deepcopy
from datetime import timedelta
from typing import Optional, Union, Any

from streamlit import cache_data
from streamlit.connections import ExperimentalBaseConnection
from streamlit.connections.util import extract_from_dict
from streamlit.errors import StreamlitAPIException
from tenacity import retry, wait_fixed
from weaviate import Client
import logging

logger = logging.getLogger("weaviate_connection")

WEAVIATE_CONNECTION_PARAMS = {
    "url",
    "authorization",
    "api_key"
}

class WeaviateConnection(ExperimentalBaseConnection):

    def _connect(self, **kwargs) -> Client:
        import weaviate

        kwargs = deepcopy(kwargs)
        connection_params = extract_from_dict(WEAVIATE_CONNECTION_PARAMS, kwargs)
        if not len(connection_params):
            raise StreamlitAPIException(
                "Missing Weaviate connection configuration. "
                "Did you forget to set this in `secrets.toml` or as kwargs to `st.experimental_connection`?"
            )
        auth_params = {}
        if connection_params.get("api_key"):
            auth_params["auth_client_secret"] = weaviate.AuthApiKey(api_key=connection_params.get("api_key"))
        elif connection_params.get("authorization"):
            auth_params["additional_headers"] = {
                "Authorization": connection_params.get("authorization")
            }
        return weaviate.Client(
            url=connection_params.get("url"),
            **auth_params
        )

    def query(self, index_class: str,
              _query_attributes: str,
              ttl: Optional[Union[float, int, timedelta]] = None,
              k: int = 10,
              **kwargs):

        @retry(
            after=lambda _: self.reset(),
            reraise=True,
            wait=wait_fixed(1),
        )
        @cache_data(
            show_spinner="Running weaviate query....",
            ttl=ttl
        )
        def _query(
            index_class: str,
            _query_attributes: Optional[Any],
            k: int,
            **kwargs
        ):
            logger.info("Querying.......")
            query_obj = self._instance.query.get(index_class, _query_attributes)
            if kwargs.get("where_filter"):
                query_obj = query_obj.with_where(kwargs.get("where_filter"))
            if kwargs.get("additional"):
                query_obj = query_obj.with_additional(kwargs.get("additional"))
            try:
                result = query_obj.with_limit(k).do()
            except Exception as e:
                logger.error("Caught exception while querying weaviate: {}".format(str(e)))
                result = None
            return result.get("data").get("Get").get(index_class) if result else None
        return _query(index_class, _query_attributes, k, **kwargs)
