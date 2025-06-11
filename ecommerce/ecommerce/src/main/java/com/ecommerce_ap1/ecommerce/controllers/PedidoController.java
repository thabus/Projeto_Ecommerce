package com.ecommerce_ap1.ecommerce.controllers;

import java.util.List;
import java.util.Map;

import com.ecommerce_ap1.ecommerce.request.RealizarCompraRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.ecommerce_ap1.ecommerce.services.PedidoService;
import com.ecommerce_ap1.ecommerce.models.Pedido;

@RestController
@RequestMapping("/pedidos")
public class PedidoController {

    @Autowired
    private PedidoService pedidoService;

    @PostMapping("/criar")
    public ResponseEntity<?> criarPedido(@RequestBody RealizarCompraRequest request) {
        try {
            Pedido novoPedido = pedidoService.criarPedido(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(novoPedido);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (RuntimeException e) {
            return ResponseEntity.internalServerError().body("Erro interno do servidor: " + e.getMessage());
        }
    }

    @PostMapping("/processarPagamento/{pedidoId}")
    public ResponseEntity<?> processarPagamentoPedido(@PathVariable String pedidoId, @RequestBody RealizarCompraRequest request) {
        try {
            if (request.getCartaoId() == null || request.getCartaoId() <= 0) {
                return ResponseEntity.badRequest().body("ID do cartão não fornecido ou inválido para processar o pagamento.");
            }

            Pedido pedidoPago = pedidoService.processarPagamentoPedido(pedidoId, String.valueOf(request.getCartaoId()));
            return ResponseEntity.ok(pedidoPago);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (RuntimeException e) {
            return ResponseEntity.internalServerError().body("Erro interno do servidor: " + e.getMessage());
        }
    }

    @GetMapping
    public ResponseEntity<?> listarPedidos(
        @RequestParam(required = false) String usuarioId,
        @RequestParam(required = false) String status
    ) {
        try {
            List<Pedido> pedidosRetorno = pedidoService.listarPedidos(usuarioId, status);

            if (pedidosRetorno.isEmpty()) {
                return ResponseEntity.ok(Map.of("message", "Nenhum pedido encontrado com os filtros fornecidos."));
            }
            return ResponseEntity.ok(pedidosRetorno);
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                                 .body(Map.of("message", "Ocorreu um erro interno ao listar os pedidos: " + e.getMessage()));
        }
    }

    @GetMapping("/search")
    public ResponseEntity<List<Pedido>> buscarPedidosPorNomeProduto(@RequestParam String nome) {
        List<Pedido> pedidos = pedidoService.buscarPedidosPorNomeProduto(nome);
        if (pedidos.isEmpty()) {
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.ok(pedidos);
    }
}