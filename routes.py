import json
from flask import Flask, request, Response
from scrapper_v3 import *

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    drug = request.args.get('medicamento')
    cep = request.args.get('cep')
    limit = request.args.get('limite')
    
    results = search_drugs(drug, cep, limit)
    
    json_string = json.dumps(results, ensure_ascii=False)
    return Response(json_string, content_type="application/json")

if __name__ == '__main__':
    app.run(debug=True)
