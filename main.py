import streamlit as st
import logging
from connections.weaviate_connection import WeaviateConnection
from PIL import Image

img = Image.open("./assets/favicon.ico")
st.set_page_config(
    page_title="Weaviate Connection",
    page_icon=img,
    layout="wide",
)

st.title("Experimental Weaviate connection")

logger = logging.getLogger("streamlit")
kwargs = st.secrets.get("connections").get("weaviate")

conn = st.experimental_connection("weaviate", type=WeaviateConnection, **kwargs)
logger.info("Successfully established connection to weaviate.....")
where_filter = {}
class_name = kwargs.get("class", "WikiData")
st.text_input("Enter class name:", value=class_name)
k = st.number_input("Number of rows:", value=10)
if st.button("Get data"):
    data = conn.query(class_name, _query_attributes=["text", "source_url", "title"], where_filter=where_filter, k=k)
    st.table(data)
