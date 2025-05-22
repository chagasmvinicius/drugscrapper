import requests
import json

def consultar_panvel(termo_busca, cep):
    # Configuração da requisição
    url = f"https://www.panvel.com/api/v2/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'sessionid': '98170b38-0976-47a9-a950-9fa6e50dc500',
        'user-id': '8601417',
        'client-ip': '1'
    }
    
    payload = {
        "term": termo_busca,
        "itemsPerPage": 24,
        "currentPage": 1,
        "assortment": "mais relevantes",
        "filters": [
            {
                "name": "locatorCep",
                "values": [cep]
            }
        ],
        "searchOffers": False,
        "searchType": "term"
    }

    try:
        # Fazendo a requisição POST
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            timeout=10
        )
        
        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()
        
        # Processando a resposta
        dados = response.json()

        # Acessando a propriedade items
        if 'items' not in dados:
            raise ValueError("Resposta não contém a propriedade 'items'")
        
        items = dados['items']
        results = []
        
        for item in items[:24]:
            results.append({
                'id': item['panvelCode'],
                'short_description': item['brandName'].strip(),
                'price': float(item['discount']['dealPrice'] if item['discount']['dealPrice'] else item['originalPrice']) or 0.0,
                'price_str': f"R$ {item['discount']['dealPrice'] if item['discount']['dealPrice'] else item['originalPrice']}",
                'description': item['name'],
                'link': item['link'],
                'quantity': item['presentationTitle'].strip() or 'N/A',
                'drugstore': 'PANVEL'
            })
            
        return results
                
    except requests.exceptions.RequestException as e:
        return 'ERROR'
