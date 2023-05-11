from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_httpauth import HTTPTokenAuth
import json

import chains.openaiChain as openaiChain
import chains.T5Chain as T5Chain

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
        return T5Chain.pcts_chatgpt(rq)

if __name__ == '__main__':
    app.run()
