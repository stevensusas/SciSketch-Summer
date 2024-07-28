from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Document(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/api/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    document = db.session.get(Document, document_id)
    if document is None:
        return jsonify({"name": "Untitled Document", "content": ""})
    return jsonify({"name": document.name, "content": json.loads(document.content)})

@app.route('/api/documents/<document_id>', methods=['POST'])
def save_document(document_id):
    data = request.json
    name = data.get('name')
    content = data.get('content')
    content_str = json.dumps(content)  # Convert content to JSON string
    document = db.session.get(Document, document_id)
    if document is None:
        document = Document(id=document_id, name=name, content=content_str)
    else:
        document.name = name
        document.content = content_str
    db.session.add(document)
    db.session.commit()
    return jsonify({"status": "success"}), 200

@app.route('/api/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        document = Document.query.get(document_id)
        if document is None:
            return jsonify({"error": "Document not found"}), 404

        db.session.delete(document)
        db.session.commit()
        return jsonify({"message": "Document deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

@app.route('/api/documents', methods=['GET'])
def get_all_documents():
    documents = Document.query.all()
    documents_data = [{"id": doc.id, "content": json.loads(doc.content), "name": doc.name} for doc in documents]
    return jsonify(documents_data)

if __name__ == '__main__':
    # app.run(host='localhost', port=5000, debug=True)
    app.run(debug=True)
