from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chat_models import ChatOpenAI as OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from simplet5 import SimpleT5
from chains.T5Chain import model

from dotenv import load_dotenv
load_dotenv()

llm = OpenAI(temperature=0.9)

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
        return ['result', 'prompt']

    def _call(self, inputs: Dict[str, str]) -> Dict[str, str]:
        if "parent" in inputs:
            inputs["parent_summary"] = self.summarizer.run(post=inputs["parent"])
        if "post" in inputs:
            inputs["summary"] = self.summarizer.run(post=inputs["post"])
        t5_prompt = self.prompt.format(**{k: v for k,v in inputs.items() if k in self.prompt.input_variables})
        t5_result = self.model.predict(t5_prompt)
        return {'result': t5_result, 'prompt': t5_prompt}

system_message = SystemMessagePromptTemplate.from_template("You are a helpful assistant that rewrites reddit posts using less toxic language. When you receive a post, return a less toxic version of the post maintaining the original voice of the author.")
human_message = HumanMessagePromptTemplate.from_template("{post}")

prompt = ChatPromptTemplate.from_messages([system_message, human_message])

openAIChain = LLMChain(llm=llm, prompt=prompt)

PCTS = PromptTemplate(
    input_variables=["parent", "parent_toxicity", "parent_summary", "summary"],
    template="""Post summary: {parent_summary}. A {parent_toxicity} post: {parent}\nReply summary: {summary}\nA low toxicity reply:""",
)

PCTS_CHATGPT_chain = SummaryChain(summarizer=openAIChain, prompt=PCTS, model=model)

pcts_chatgpt = lambda x: {k: v for k, v in PCTS_CHATGPT_chain(x).items() if k in ["result", "prompt"]}