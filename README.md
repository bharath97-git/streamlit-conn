# Streamlit 🔗 Weaviate experimental connection

This is a simple streamlit application which makes uses of it's experimental connection feature to connect to <a href="https://weaviate.io/" target="_blank">weaviate</a>
 vector store.

With the rapidly evolving LLMs, it is extremely essential for having playgrounds to quickly build, test and evaluate LLMs. Streamlit makes the job of data and ML engineers simple.


# Setup

## Pre-requisites

- Python (>= 3.9)
- A python virtual environment
- Poetry - If you don't have Poetry installed, you can find the installation instructions [here](https://python-poetry.org/docs/#installation).

## Installation

To install Streamlit and Weaviate, activate the virtual environment and run the following command:
```
poetry install
```

## Configurations
- In the base directory of the project, create a folder: **.streamlit** and create a file **secrets.toml** file.
- Copy the secrets.example.toml file to secrets.toml file and add the below configurations:
  1. url: Weaviate connection url
  2. api_key: Weaviate auth api key
  3. authorization: Bearer token for authorizing weaviate cluster(Provide either api key or authorization bearer token)
  4. class: Class name in weaviate cluster to retrieve data from

## Run..
Open the terminal, activate the poetry environment and run the application using the following command:
```
streamlit run main.py
```

# Contact
