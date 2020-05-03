from flask import Flask, request, Response, jsonify
from transformers import BartForConditionalGeneration, BartConfig, BartTokenizer
import logging
import gunicorn
from newspaper import Article

app = Flask(__name__)

if __name__ != "__main__":
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

def init():
    ### Initialising the Model and Tokenizer as globals
    global model, tokenizer
    model = BartForConditionalGeneration.from_pretrained('bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('bart-large-cnn')


def summarize_url(url_):
        ### Summarize URL
        article_ = Article(url_)
        article_.download()
        article_.parse()
        text_ = article_.text
        summary_ = summarize_bart(text_)

        return summary_

def summarize_text(text_):
        ### Summarize text
        ### Clean text
        summary_ = summarize_bart(text_)

        return summary_

def summarize_bart(text):
        ###Using transformers to Summarize
        inputs = tokenizer.batch_encode_plus([text], max_length=1024, return_tensors='pt')
        summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=500, early_stopping=True)
        summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]

        return summary

## API to expose
@app.route("/greet")
def greet():
    return jsonify("Hello there!! I am working")

@app.route("/summarize", methods=['POST'])
def summarize():
        req = request.get_json()
        if req['url']:
            summary = summarize_url(req['url'])
        elif req['text']:
            summary = summarize_text(req['text'])

        return jsonify(summary)


### Main
if __name__ == "__main__":
    app.logger.info('Loading the mode...')
    init()
    app.logger.info('Model and Tokenizer Loaded')
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)

