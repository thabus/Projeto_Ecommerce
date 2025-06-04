package com.ecommerce_ap1.ecommerce.controllers;

import java.util.List;

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
    public ResponseEntity<Pedido> realizarCompra(@RequestBody Pedido pedido) {
        Pedido pedidoRealizado = pedidoService.realizarCompra(pedido);
        return ResponseEntity.ok(pedidoRealizado);
    }

    @GetMapping
    public List<Pedido> listarPedidos() {
        return pedidoService.listarPedidos();
    }
}