import openai

openai.api_key = 'api_key'

def moderate(text):
    response = openai.Moderation.create(
        input=text
    )
    output = response["results"][0]
    return output['flagged']
