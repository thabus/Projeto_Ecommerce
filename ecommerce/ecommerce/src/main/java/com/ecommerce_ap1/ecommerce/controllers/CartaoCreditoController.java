package com.ecommerce_ap1.ecommerce.controllers;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;
import com.ecommerce_ap1.ecommerce.services.CartaoCreditoService;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/cartoes")
public class CartaoCreditoController {

    @Autowired
    private CartaoCreditoService cartaoService;

    @GetMapping
    public List<CartaoCredito> listarTodos() {
        return cartaoService.listarTodos();
    }


    @PutMapping("/{id}/saldo")
    public CartaoCredito atualizarSaldo(
        @PathVariable Integer id,
        @RequestParam double novoSaldo
    ) {
        return cartaoService.atualizarSaldo(id, novoSaldo);
    }

    @GetMapping("/{id}")
    public ResponseEntity<CartaoCredito> buscarCartaoPorId(@PathVariable Integer id) {
        return cartaoService.buscarCartaoPorId(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
}


    @PostMapping("/{id}/compra")
    public ResponseEntity<String> realizarCompra(
        @PathVariable Integer id,
        @RequestParam double valor
    ) {
        try {
            cartaoService.realizarCompra(id, valor);
            return ResponseEntity.ok("Compra realizada com sucesso!");
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }

}
