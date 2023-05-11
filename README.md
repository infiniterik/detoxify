# Getting started

1. Add an `OPENAI_API_KEY`, `PROMPTLAYER_API_KEY`, and `WANDB_API_KEY` to the `.env` file.
2. create a `secrets.json` file with a secret api key for each user
3. install requirements using `pip install -r requirements.txt`
4. run the server using `python app.py`


## `secrets.json`

This will be replaced eventually with something more secure than plain-text keys, but for now create a file called `secrets.json` with the format:

```
{
  "KEY1": "USERNAME1",
  "KEY2": "USERNAME2",
  ...
}
```

## Sample query

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