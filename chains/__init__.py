from dotenv import load_dotenv
from langchain.llms import OpenAI
from simplet5 import SimpleT5
import os

load_dotenv()


def wandb_dl(model_name='knoxcs/detoxify/prochoice.pcts.t5-large:v2'):
    import wandb
    run = wandb.init()
    artifact = run.use_artifact(model_name, type='model')
    artifact_dir = artifact.download()
    return artifact_dir

def huggingface_dl(model_name='infiniterik/desc-detoxify-prochoice'):
    from huggingface_hub import snapshot_download
    return snapshot_download(repo_id=model_name)

def huggingface_inference(model_name='infiniterik/desc-detoxify-prochoice'):
    from huggingface_hub import InferenceClient
    client = InferenceClient()
    return lambda text: client.text_generation(text, model=model_name)

def load_model(artifact_dir):
    model = SimpleT5()
    model.from_pretrained("t5", artifact_dir)
    return model.predict

if os.getenv("MODEL_SOURCE") == "WANDB":
    artifact_dir = wandb_dl(os.getenv("MODEL_NAME"))
    model = load_model(artifact_dir)
elif os.getenv("MODEL_SOURCE") == "HUGGINGFACE":
    artifact_dir = huggingface_dl(os.getenv("MODEL_NAME"))
    model = load_model(artifact_dir)
elif os.getenv("MODEL_SOURCE") == "LOCAL":
    artifact_dir = os.getenv("MODEL_NAME")
    model = load_model(artifact_dir)
elif os.getenv("MODEL_SOURCE") == "INFERENCE":
    model = huggingface_inference(os.getenv("MODEL_NAME"))
else:
    raise Exception("Invalid model source")


llm = OpenAI(temperature=0.9)