from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_httpauth import HTTPTokenAuth
import json

import chains.openaiChain as openaiChain

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
@api.doc(body=rephrase, security='apikey')
class T5Endpoint(Resource):
    @auth.login_required
    def post(self):
        text = request.json["post"]
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ])
        return result["choices"][0].message.content

if __name__ == '__main__':
    app.run()
