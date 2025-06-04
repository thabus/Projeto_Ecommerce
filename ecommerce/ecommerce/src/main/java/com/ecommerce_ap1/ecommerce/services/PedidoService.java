package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.Pedido;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class PedidoService {

    // Simulação de banco de dados em memória
    private List<Pedido> pedidos = new ArrayList<>();

    public Pedido realizarCompra(Pedido pedido) {
        // Lógica para processar a compra (ex: validar estoque, calcular valor, etc.)
        pedidos.add(pedido);
        return pedido;
    }

    public List<Pedido> listarPedidos() {
        return pedidos;
    }
}