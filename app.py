from flask import Flask, render_template, request
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
import ast

app = Flask(__name__)

with open("conversions/id2label.txt", "r") as data:
    id2label = ast.literal_eval(data.read())

with open("conversions/label2id.txt", "r") as data:
    label2id = ast.literal_eval(data.read())

deberta_v3_large = 'models/itsclassifier'
tokenizer = AutoTokenizer.from_pretrained(deberta_v3_large)
model = AutoModelForSequenceClassification.from_pretrained(deberta_v3_large,id2label=id2label, label2id=label2id, ignore_mismatched_sizes=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    def topprediction(text):
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
        predicted_class_id = logits.argmax().item()
        return model.config.id2label[str(predicted_class_id)]
    
    email = request.form.get('content')
    prediction = topprediction(email)
    return render_template("index.html", prediction=prediction, email=email)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)