package com.ecommerce_ap1.ecommerce.controllers;

import java.util.List;

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
            // --- INÍCIO DA CORREÇÃO ---
            // Verifica se o ID do cartão é nulo (para Integer) ou se tem um valor inválido (ex: 0)
            // Se getCartaoId() retorna Integer, você não pode chamar .isEmpty()
            if (request.getCartaoId() == null || request.getCartaoId() <= 0) { // Assume que IDs de cartão válidos são > 0
                return ResponseEntity.badRequest().body("ID do cartão não fornecido ou inválido para processar o pagamento.");
            }
            // --- FIM DA CORREÇÃO ---

            // Passamos o ID do cartão para o service como String, pois o service faz a conversão para Integer
            Pedido pedidoPago = pedidoService.processarPagamentoPedido(pedidoId, String.valueOf(request.getCartaoId()));
            return ResponseEntity.ok(pedidoPago);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (RuntimeException e) {
            return ResponseEntity.internalServerError().body("Erro interno do servidor: " + e.getMessage());
        }
    }

    @GetMapping
    public ResponseEntity<List<Pedido>> listarPedidos(@RequestParam(required = false) String status) {
        List<Pedido> pedidosRetorno;
        if (status != null && !status.trim().isEmpty()) {
            // Se um status for fornecido, filtra os pedidos
            pedidosRetorno = pedidoService.listarPedidos(status);
        } else {
            // Caso contrário, retorna todos os pedidos (método listarPedidos original)
            pedidosRetorno = pedidoService.listarPedidos(null); // Chamando o método com null para obter todos
        }

        if (pedidosRetorno.isEmpty()) {
            return ResponseEntity.noContent().build(); // Retorna 204 No Content se nada for encontrado
        }
        return ResponseEntity.ok(pedidosRetorno); // Retorna 200 OK com a lista de pedidos
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