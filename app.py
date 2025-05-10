import json
from flask import Flask, request, Response
import os
from scraper import *

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    drug = request.args.get('medicamento')
    cep = request.args.get('cep')

    # Chamadas para o scraper
    results_drogaraia = search_drugs(drug, cep, 'https://www.drogaraia.com.br/')
    results_drogasil = search_drugs(drug, cep, 'https://www.drogasil.com.br/')
    results = results_drogaraia + results_drogasil

    # Remover duplicatas por (id, link)
    checked = set()
    unics = []
    for item in results:
        index = (item.get('id'), item.get('link'))
        if index not in checked:
            checked.add(index)
            unics.append(item)

    # Ordenar pelos preços
    unics = sorted(unics, key=lambda x: float(x.get('price', 0)))

    results_obj = {
        'count': len(unics),
        'drugs': unics
    }

    json_string = json.dumps(results_obj, ensure_ascii=False)
    return Response(json_string, content_type="application/json")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))