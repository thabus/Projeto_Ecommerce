package com.ecommerce_ap1.ecommerce.controllers;

import com.ecommerce_ap1.ecommerce.models.Pedido;
import com.ecommerce_ap1.ecommerce.services.PedidoService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/relatorio-vendas")
public class RelatorioController {

    @Autowired
    private PedidoService pedidoService;

    @GetMapping
    public ResponseEntity<String> gerarRelatorio() {
        // Simulação de geração de relatório (seria com Power BI no final do pipeline)
        int totalPedidos = pedidoService.listarPedidos().size();
        double totalVendas = pedidoService.listarPedidos().stream()
                .mapToDouble(Pedido::getValorTotal)
                .sum();

        String relatorio = "Relatório de Vendas\n\nTotal de pedidos: " + totalPedidos +
                "\nValor total vendido: R$ " + totalVendas;

        return ResponseEntity.ok(relatorio);
    }
}
