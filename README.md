# detoxify

This is the demo code for [Detoxifying Online Discourse: A Guided Response Generation Approach for Reducing Toxicity in User-Generated Text](pdfs/detoxify-paper.pdf), as appearing in [The First Workshop on Social Influence in Conversations]([url](https://sites.google.com/view/sicon-2023/)). The poster is available [here](pdfs/detoxify-poster.pdf).

This repository provides a REST API to run the system and a `streamlit` interface to explore. The `streamlit` component can be run without the server if desired.

Training code forthcoming.

## Getting started

1. Add an `OPENAI_API_KEY` to the `.env` file.
2. Add a `MODEL_SOURCE` and `MODEL_NAME` to the `.env` file.
4. If you are using the server, create a `secrets.json` file with a secret api key for each user
5. install requirements using `pip install -r requirements.txt`
6. If you are downloading a model from huggingface, make sure to login in using the `huggingface-cli`.
7. (Optional) Run server using `flask run --port 8000`
8. Run the frontend with `streamlit run DESC_demo.py`

## `.env` file

The `.env` file contains necessary API keys and where to acquire the rewriting model from.

### `MODEL_SOURCE`

You can provide your own `LOCAL` model or download one from `WANDB` or `HUGGINGFACE`. The final model used in the paper is available at [infiniterik/desc-detoxify-sicon](https://huggingface.co/infiniterik/desc-detoxify-sicon). Note that both `WANDB` and `HUGGINGFACE` will cache the model locally, so you only need to download it once. There is an option to use the Huggingface Inference API but it is currently unstable (WIP) and not recommended (issues and pull requests welcome).

## Running the frontend

You can start the frontend using the command `streamlit run DESC_demo.py`. If you are running the frontend without the server, then the necessary models will be loaded as needed. The first time you try an example might take a while. You will also need to ensure that the `Local` option is clicked in the sidebar on every page.

## Using the server

You may want to use the server if you are fiddling with the front-end and don't want to reload the models regularly, or if you want to run the models on a different machine.

### `secrets.json`

This will be replaced eventually with something more secure than plain-text keys, but for now create a file called `secrets.json` with the format:

```
{
  "KEY1": "USERNAME1",
  "KEY2": "USERNAME2",
  ...
}
```

### Sample query

Note that the `Authorization` header contains `Bearer my-secret` instead of just `my-secret`.

```
curl -X 'POST' \
  'http://127.0.0.1:5000/chatgpt' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer my-secret' \
  -H 'Content-Type: application/json' \
  -d '{
  "post": "This is a toxic post that I would like to rephrase"
}'
```

## Chains

Each pipeline is implemented as a `Chain` using the `langchain` library.

# Citations

```bibtex
@inproceedings{bose-etal-2023-detoxifying,
    title = "Detoxifying Online Discourse: A Guided Response Generation Approach for Reducing Toxicity in User-Generated Text",
    author = "Bose, Ritwik  and Perera, Ian  and Dorr, Bonnie",
    booktitle = "Proceedings of the First Workshop on Social Influence in Conversations (SICon 2023)",
    month = jul,
    year = "2023",
    address = "Toronto, Canada",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2023.sicon-1.2",
    pages = "9--14"
}
```
