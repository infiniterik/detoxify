from langchain import Prompt
import wandb
#from langchain.chat_models import ChatOpenAI as OpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from chains.T5Chain import model

from simplet5 import SimpleT5

from dotenv import load_dotenv
load_dotenv()

llm = OpenAI(temperature=0.9)

from langchain.chains import LLMChain
from langchain.chains.base import Chain

from typing import Dict, List


class StanceChain(Chain):
    generation : LLMChain
    model : SimpleT5
    prompt : PromptTemplate
    
    @property
    def input_keys(self) -> List[str]:
        return ['stances']

    @property
    def output_keys(self) -> List[str]:
        return ['result', 'prompt']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        if "stances" in inputs:
            inputs["generation"] = self.generation.run(stances=inputs["stances"])
        t5_prompt = self.prompt.format(**{k: v for k,v in inputs.items() if k in self.prompt.input_variables})
        t5_result = self.model.predict(t5_prompt)
        return {'result': t5_result, 'prompt': t5_prompt}


summarizationPrompt = PromptTemplate(
    input_variables=["stances"],
    template="""Write a general comment that expresses the following stances: {stances}""",
)


openAIChain = LLMChain(llm=llm, prompt=summarizationPrompt)

stancedetectiontemplate = PromptTemplate(
    input_variables=["generation"],
    template="""Parent summary: What do you think?\n A low toxicity post: That is just my opinion. What do you think?\nReply summary: {generation}\nA low toxicity reply:""",
)

stance_detection_chain = StanceChain(generation=openAIChain, prompt=stancedetectiontemplate, model=model)

stance_detection = lambda x: {k: v for k, v in stance_detection_chain(x).items() if k in ["result", "prompt"]}