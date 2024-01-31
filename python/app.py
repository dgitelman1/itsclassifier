from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
import ast
import os

app = Flask(__name__)
port = int(os.environ.get('FLASK_PORT', 4000))
cors = CORS(app, origins=["http://localhost:3000"])
print("App running on port ", port)


with open("conversions/id2label.txt", "r") as data:
    id2label = ast.literal_eval(data.read())

with open("conversions/label2id.txt", "r") as data:
    label2id = ast.literal_eval(data.read())

deberta_v3_large = 'models/itsclassifier'
tokenizer = AutoTokenizer.from_pretrained(deberta_v3_large)
model = AutoModelForSequenceClassification.from_pretrained(deberta_v3_large,id2label=id2label, label2id=label2id, ignore_mismatched_sizes=True)

@app.route('/ping')
def ping():
    print("Returning ping...")
    return jsonify({'status': 'OK'})

@app.route("/predict", methods=["POST"])
def predict():
    def topprediction(text):
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
        predicted_class_id = logits.argmax().item()
        return model.config.id2label[str(predicted_class_id)]
    
    ticket = request.json['ticket']
    prediction = topprediction(ticket)
    print("Returning prediction...")
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)