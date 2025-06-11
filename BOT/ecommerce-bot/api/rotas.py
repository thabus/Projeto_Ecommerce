# api/rotas.py
import requests

class ProductAPI:
    def verificar_produtos(self, nomeProduto):
        try:
            response = requests.get(
                "http://localhost:80/produtos/search",
                params={"nome": nomeProduto},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão ao buscar produto: {e}")
            return []


class PedidoAPI:
    def verificar_pedidos_por_produto(self, nomeProduto):
        try:
            response = requests.get(
                "http://localhost:80/pedidos/search",
                params={"nome": nomeProduto},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão ao buscar pedido por nome de produto: {e}")
            return []

    def criar_pedido(self, cliente_id: str, produto_ids: list[str]):
        try:
            payload = {
                "clienteId": cliente_id,
                "produtosIds": produto_ids
            }
            response = requests.post(
                "http://localhost:80/pedidos/criar",
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar pedido: {e}")
            return None

    def processar_pagamento_pedido(self, pedido_id: str, cartao_id: int):
        """Processa o pagamento de um pedido pendente."""
        try:
            payload = {
                "cartaoId": cartao_id
            }
            response = requests.post(
                f"http://localhost:80/pedidos/processarPagamento/{pedido_id}",
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao processar pagamento do pedido {pedido_id}: {e}")
            return None


class PedidoPagoAPI:
    def verificar_lista_compras(self):
        try:
            response = requests.get(
                "http://localhost:80/pedidos",
                params={"status": "pago"},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão ou ao buscar pedidos pagos: {e}")
            return []