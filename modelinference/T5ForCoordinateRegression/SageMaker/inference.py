import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import json

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

def model_fn(model_dir):
    print(f"CUDA available: {torch.cuda.is_available()}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    print(f"Model is being loaded on device: {device}")
    model = T5ForCoordinateRegression(model_dir).cuda()
    tokenizer = T5Tokenizer.from_pretrained(model_dir)
    model.eval()
    return model, tokenizer

def input_fn(request_body, request_content_type):
    if request_content_type == 'application/json':
        input_data = json.loads(request_body)
        return input_data
    else:
        raise ValueError("Content type not supported!")

def predict_fn(input_data, model_and_tokenizer):
    model, tokenizer = model_and_tokenizer
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    abstract = input_data['abstract']
    text = input_data['text']
    max_length = input_data.get('max_length', 512)

    input_text = f"predict coordinates: {abstract} [SEP] predict coordinate of this text: {text}"
    inputs = tokenizer(input_text, max_length=max_length, padding="max_length", truncation=True, return_tensors="pt").to(device)
    
    print(f"Inputs are on device: {inputs['input_ids'].device}")

    with torch.no_grad():
        outputs = model(input_ids=inputs['input_ids'], attention_mask=inputs['attention_mask'])

    predicted_coords = outputs.squeeze().cpu().numpy()
    x_pred, y_pred = predicted_coords[0], predicted_coords[1]

    def denormalize_coordinates(x_norm, y_norm, x_min, x_max, y_min, y_max):
        x_denorm = x_norm * (x_max - x_min) + x_min
        y_denorm = y_norm * (y_max - y_min) + y_min
        return x_denorm, y_denorm
    
    x_min, x_max = -58, 3452
    y_min, y_max = -179, 4697   

    x_denorm, y_denorm = denormalize_coordinates(x_pred, y_pred, x_min, x_max, y_min, y_max)

    return {
        'x_pred': x_pred,
        'y_pred': y_pred,
        'x_denorm': x_denorm,
        'y_denorm': y_denorm
    }

def output_fn(prediction, response_content_type):
    if response_content_type == 'application/json':
        return json.dumps(prediction)
    else:
        raise ValueError("Content type not supported!")
