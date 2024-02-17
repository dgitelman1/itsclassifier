from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
import ast
import os
import logging

app = Flask(__name__)
port = int(os.environ.get('FLASK_PORT', 8080))
cors = CORS(app, origins=["http://localhost:3000"])
print("App running on port ", port)
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)


with open("conversions/id2label.txt", "r") as data:
    id2label = ast.literal_eval(data.read())

with open("conversions/label2id.txt", "r") as data:
    label2id = ast.literal_eval(data.read())

deberta_v3_large = 'models/itsclassifier'
tokenizer = AutoTokenizer.from_pretrained(deberta_v3_large)
model = AutoModelForSequenceClassification.from_pretrained(deberta_v3_large,id2label=id2label, label2id=label2id, ignore_mismatched_sizes=True)

@app.route('/ping')
def ping():
    app.logger.info('Flask app received ping')
    #return jsonify({'status': 'OK'})
    return "Pong!"

@app.route("/predict", methods=["POST"])
def predict():
    def topprediction(text):
        try:
            app.logger.info('topprediction: Trying topprediction')
            inputs = tokenizer(text, return_tensors="pt")
            app.logger.info('topprediction: Successfully tokenized inputs')
            with torch.no_grad():
                logits = model(**inputs).logits
            app.logger.info('topprediction: Successfully created logits')
            predicted_class_id = logits.argmax().item()
            app.logger.info('topprediction: Returning model prediction')
            return model.config.id2label[str(predicted_class_id)]
        except Exception as e:
            app.logger.error(f"topprediction: An error occurred in topprediction: {e}")
            return None
    
    app.logger.info('Flask app received a predict request')
    app.logger.info(f'Request data: {request.json}')

    ticket = request.json['ticket']
    app.logger.info(f'Creating prediction for {ticket}...')
    prediction = topprediction(ticket)
    app.logger.info(f'Returning prediction: {prediction}')
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)