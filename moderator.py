import openai

openai.api_key = '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'

def moderate(text):
    
    response = openai.Moderation.create(
        input=text
    )
    output = response["results"][0]
    is_flagged = output['flagged']

    return is_flagged