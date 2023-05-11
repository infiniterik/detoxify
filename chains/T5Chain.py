from langchain import Prompt
import wandb
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from simplet5 import SimpleT5

from dotenv import load_dotenv
load_dotenv()

llm = OpenAI(temperature=0.9)

import wandb
run = wandb.init()
artifact = run.use_artifact('knoxcs/detoxify/prochoice.pcts.t5-large:v2', type='model')
artifact_dir = artifact.download()

from langchain.chains import LLMChain
from langchain.chains.base import Chain

from typing import Dict, List


class SummaryChain(Chain):
    summarizer: LLMChain
    model : SimpleT5
    prompt : PromptTemplate

    #def __init__(self, summarizer: LLMChain, prompt: PromptTemplate, model_path: str):
    #    model = SimpleT5()
    #    # load (supports t5, mt5, byT5 models)
    #    model.from_pretrained("t5", model_path)
    #    self.summarizer = summarizer
    #    self.model = model
    #    self.prompt = prompt
    
    @property
    def input_keys(self) -> List[str]:
        return ['parent', 'parent_toxicity', 'post']

    @property
    def output_keys(self) -> List[str]:
        return ['post']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        if "parent" in inputs:
            inputs["parent_summary"] = self.summarizer.run(post=inputs["parent"])
        if "post" in inputs:
            inputs["summary"] = self.summarizer.run(post=inputs["post"])
        t5_result = self.model.predict(self.prompt.format(**{k: v for k,v in inputs.items() if k in self.prompt.input_variables}))
        return {'post': t5_result}


prompt = PromptTemplate(
    input_variables=["post"],
    template="""Rephrase the following Reddit post to be less toxic: {post}""",
)


openAIChain = LLMChain(llm=llm, prompt=prompt)

PCTS = PromptTemplate(
    input_variables=["parent", "parent_toxicity", "parent_summary", "summary"],
    template="""Post summary: {parent_summary}. A {parent_toxicity} post: {parent}\nReply summary: {summary}\nA low toxicity reply:""",
)

model = SimpleT5()
# load (supports t5, mt5, byT5 models)
model.from_pretrained("t5", artifact_dir)
PCTS_CHATGPT_chain = SummaryChain(summarizer=openAIChain, prompt=PCTS, model=model)

pcts_chatgpt = lambda x: PCTS_CHATGPT_chain.run(x)