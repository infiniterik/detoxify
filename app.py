from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_httpauth import HTTPTokenAuth
import json
import openai


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

app = Flask(__name__)
api = Api(app, authorizations=authorizations, security='apikey')
auth = HTTPTokenAuth(scheme='Bearer')

with open("secrets.json") as secrets:
    tokens = json.load(secrets)

prompt = "You are an editor for reddit posts. Your job is to rewrite an individual user's Reddit post to be less inflammatory and toxic while maintaining the original intention and stances in their post. Provide a rewritten version of their post that satisfies these parameters."

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

rephrase = api.model("Rephrase", {
    "post": fields.String(description="The post to be rephrased", required=True)
})

@api.route('/chatgpt', endpoint='chatgpt')
@api.doc(body=rephrase, security='apikey')
class ChatGPT(Resource):
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
