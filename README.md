# Getting started

1. Add an `OPENAI_API_KEY` to your to your environment.
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
