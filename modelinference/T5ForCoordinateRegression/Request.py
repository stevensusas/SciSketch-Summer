from flask import Flask, request, jsonify
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

app = Flask(__name__)

class T5ForCoordinateRegression(torch.nn.Module):
    def __init__(self, model_path):
        super().__init__()
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        self.regression_head = torch.nn.Linear(self.model.config.d_model, 2)

    def forward(self, input_ids, attention_mask):
        outputs = self.model.encoder(input_ids=input_ids, attention_mask=attention_mask)
        last_hidden_state = outputs.last_hidden_state
        regression_output = self.regression_head(last_hidden_state[:, -1])
        return regression_output

# Load the fine-tuned model and tokenizer
model_path = "/Users/stevensu/Desktop/T5ForCoordinateRegression/regression-model-flan-t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForCoordinateRegression(model_path)
model.eval()

def predict_coordinates(abstract, text, max_length=512):
    input_text = f"predict coordinates: {abstract} [SEP] predict coordinate of this text: {text}"
    inputs = tokenizer(input_text, max_length=max_length, padding="max_length", truncation=True, return_tensors="pt")

    with torch.no_grad():
        outputs = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])

    predicted_coords = outputs.squeeze().numpy()
    return predicted_coords[0], predicted_coords[1]  # x, y

def denormalize_coordinates(x_norm, y_norm, x_min, x_max, y_min, y_max):
    x_denorm = x_norm * (x_max - x_min) + x_min
    y_denorm = y_norm * (y_max - y_min) + y_min
    return x_denorm, y_denorm

# Coordinate ranges
x_min, x_max = -58, 3452
y_min, y_max = -179, 4697

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    abstract = data.get('abstract')
    text = data.get('text')
    
    if not abstract or not text:
        return jsonify({'error': 'Abstract and text are required'}), 400

    try:
        x_pred, y_pred = predict_coordinates(abstract, text)
        x_denorm, y_denorm = denormalize_coordinates(x_pred, y_pred, x_min, x_max, y_min, y_max)
        response = {
            'normalized_coordinates': {
                'x': float(x_pred),
                'y': float(y_pred)
            },
            'denormalized_coordinates': {
                'x': float(x_denorm),
                'y': float(y_denorm)
            }
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
