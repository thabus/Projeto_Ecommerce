import requests

class ProductAPI:
    def consultar_produtos(self, nomeProduto):
        try:
            response = requests.get(
                "http://localhost:8080/produtos/search",
                params={"productName": nomeProduto},
                timeout=5
            )
            if response.ok:
                return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão: {e}")
        return []