package com.ecommerce_ap1.ecommerce.controllers;

import java.util.List;

import com.ecommerce_ap1.ecommerce.request.RealizarCompraRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.ecommerce_ap1.ecommerce.services.PedidoService;
import com.ecommerce_ap1.ecommerce.models.Pedido;

@RestController
@RequestMapping("/pedidos")
public class PedidoController {

    @Autowired
    private PedidoService pedidoService;

    @PostMapping("/comprar")
    public ResponseEntity<?> realizarCompra(@RequestBody RealizarCompraRequest request) {
        try {
            Pedido pedidoRealizado = pedidoService.realizarCompra(request);
            return ResponseEntity.ok(pedidoRealizado);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (RuntimeException e) {
            return ResponseEntity.internalServerError().body("Erro interno do servidor: " + e.getMessage());
        }
    }

    @GetMapping
    public List<Pedido> listarPedidos() {
        return pedidoService.listarPedidos();
    }
}
