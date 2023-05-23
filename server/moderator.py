import openai

openai.api_key = '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'

def moderate(text):
    
    response = openai.Moderation.create(
        input=text
    )
    output = response["results"][0]
    is_flagged = output['flagged']

    return is_flagged