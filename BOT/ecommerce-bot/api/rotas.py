import requests

class ProductAPI:
    def verificar_produtos(self, nome_produto: str):
        try:
            response = requests.get(
                "https://ibmec-cloud-ecommerce-edaefwhmebadf4ey.canadacentral-01.azurewebsites.net/produtos/search",
                params={"nome": nome_produto},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão ao buscar produto '{nome_produto}': {e}")
            return []


class PedidoAPI:
    def verificar_pedidos_por_produto(self, nome_produto: str):
        try:
            response = requests.get(
                "https://ibmec-cloud-ecommerce-edaefwhmebadf4ey.canadacentral-01.azurewebsites.net/pedidos/search",
                params={"nome": nome_produto},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão ao buscar pedido por nome de produto: {e}")
            return []

    def criar_pedido(self, usuario_id: str, produtos_ids: list[str]):
        try:
            payload = {
                "usuarioId": usuario_id,
                "produtosIds": produtos_ids
            }
            response = requests.post(
                "https://ibmec-cloud-ecommerce-edaefwhmebadf4ey.canadacentral-01.azurewebsites.net/pedidos/criar",
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao criar pedido para usuário {usuario_id}: {e}")
            return None

    def processar_pagamento_pedido(self, pedido_id: str, cartao_id: int):
        try:
            payload = {
                "cartaoId": cartao_id
            }
            response = requests.post(
                f"https://ibmec-cloud-ecommerce-edaefwhmebadf4ey.canadacentral-01.azurewebsites.net/pedidos/processarPagamento/{pedido_id}",
                json=payload,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao processar pagamento do pedido {pedido_id}: {e}")
            return None

    def listar_pedidos_por_usuario_e_status(self, usuario_id: str, status: str = None):
        try:
            params = {"usuarioId": usuario_id}
            if status:
                params["status"] = status
            response = requests.get(
                "https://ibmec-cloud-ecommerce-edaefwhmebadf4ey.canadacentral-01.azurewebsites.net/pedidos",
                params=params,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao listar pedidos por usuário {usuario_id} e status: {e}")
            return []

    def buscar_pedido_por_id(self, pedido_id: str):
        try:
            response = requests.get(
                f"https://ibmec-cloud-ecommerce-edaefwhmebadf4ey.canadacentral-01.azurewebsites.net/pedidos/{pedido_id}",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar pedido por ID: {e}")
            return None


class UsuarioAPI:
    def buscar_usuario_por_id(self, usuario_id: str):
        try:
            response = requests.get(
                f"https://ibmec-cloud-ecommerce-edaefwhmebadf4ey.canadacentral-01.azurewebsites.net/usuarios/{usuario_id}",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar usuário por ID '{usuario_id}': {e}")
            return None

class PedidoPagoAPI:
    def verificar_lista_compras(self, usuario_id: str):
        try:
            params = {
                "status": "pago",
                "usuarioId": usuario_id
            }

            response = requests.get(
                "https://ibmec-cloud-ecommerce-edaefwhmebadf4ey.canadacentral-01.azurewebsites.net/pedidos",
                params=params,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão ou ao buscar pedidos pagos: {e}")
            return []
