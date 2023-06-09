from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_httpauth import HTTPTokenAuth
import json

import chains.openaiChain as openaiChain
import chains.T5Chain as T5Chain
import chains.T5ChainChatGPT as T5ChainChatGPT
import chains.stancedriven as stancedriven

from langchain.prompts import PromptTemplate


from dotenv import load_dotenv
load_dotenv()


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

app = Flask(__name__)
api = Api(app, authorizations=authorizations, security='apikey')
auth = HTTPTokenAuth()

with open("secrets.json") as secrets:
    tokens = json.load(secrets)

@auth.verify_token
def verify_token(token):
    if token in tokens:
        print(tokens[token])
        return tokens[token]
    else:
        print("Invalid token - " + token)

rephrase = api.model("Rephrase", {
    "post": fields.String(description="The post to be rephrased", required=True)
})

rephraseT5WithParent = api.model("RephraseT5WithParent", {
    "post": fields.String(description="The post to be rephrased", required=True),
    "parent": fields.String(description="The parent post", required=False),
    "parent_toxicity": fields.String(description="The toxicity of the parent post (high or low)", required=False),
    "model": fields.String(description="The model to use", required=True)
})

stanceDrivenDemo = api.model("StanceDrivenDemo", {
    "stances": fields.String("The stances to use", required=True)
})

@api.route('/chatgpt', endpoint='chatgpt')
@api.doc(body=rephrase, security='apikey')
class ChatGPT(Resource):
    @auth.login_required
    def post(self):
        text = request.json["post"]
        return openaiChain.runOpenAIChain(text)

@api.route('/t5', endpoint='t5')
@api.doc(body=rephraseT5WithParent, security='apikey')
class T5Endpoint(Resource):
    @auth.login_required
    def post(self):
        model = request.json["model"]
        rq = {k: v for k, v in request.json.items() if k != "model"}
        if model == "chatgpt":
            return T5ChainChatGPT.pcts_chatgpt(rq)
        return T5Chain.pcts_gpt(rq)

@api.route('/stanceDriven', endpoint='stancedriven')
@api.doc(body=stanceDrivenDemo, security='apikey')
class StanceDrivenEndpoint(Resource):
    @auth.login_required
    def post(self):
        rq = {k: v for k, v in request.json.items() if k != "model"}
        return stancedriven.stance_detection(rq)

if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")
