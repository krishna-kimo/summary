from flask import Flask, request, Response, jsonify
from transformers import BartForConditionalGeneration, BartConfig, BartTokenizer
import logging
import gunicorn

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
	pass

def summarize_text(text_):
	### Summarize text
	pass

def summarize_bart(text):
	###Using transformers to Summarize
	pass

## API to expose
@app.route("/greet")
def greet():
    return jsonify("Hello there!! I am working")

@app.route("/summarize", methods=['POST'])
def summarize():
	req = request.get_json()
	if req['url']:
		return jsonify(req['url'])


### Main
if __name__ == "__main__":
    app.logger.info('Loading the mode...')
    init()
    app.logger.info('Model and Tokenizer Loaded')
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)

