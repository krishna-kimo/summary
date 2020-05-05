from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import List
from transformers import BartForConditionalGeneration, BartConfig, BartTokenizer
import logging
from newspaper import Article
from config import MODEL_NAME, TOKENIZER

## Initialising the FastAPI app
app = FastAPI()

## Definition of the request body structure
class Item(BaseModel):
    url: str
    text: str = None

class SummaryResponse(BaseModel):
    summary: List[str] = []

## Initialising the model and tokemizer as globals
global model, tokenizer 
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = BartTokenizer.from_pretrained(TOKENIZER)

## Util functions

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

@app.get("/greet")
async def greet():
    return {"message": "Hi there!!!! I am working"}

@app.post("/summarize", response_model=SummaryResponse)
async def summarize(item: Item):
    url_ = item.url
    text_ = item.text

    summary_ = summarize_url(url_) 
    return SummaryResponse(
            summary = summary_
            )


