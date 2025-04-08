package com.ecommerce_ap1.ecommerce.controllers;

import com.ecommerce_ap1.ecommerce.models.Endereco;
import com.ecommerce_ap1.ecommerce.services.EnderecoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/enderecos")
public class EnderecoController {

    @Autowired
    private EnderecoService enderecoService;

    // Cadastrar um novo endereço
    @PostMapping
    public ResponseEntity<Endereco> salvar(@RequestBody Endereco endereco) {
        Endereco enderecoSalvo = enderecoService.salvar(endereco);
        return ResponseEntity.ok(enderecoSalvo);
    }

    // Listar todos os endereços de um usuário
    @GetMapping("/usuario/{usuarioId}")
    public ResponseEntity<List<Endereco>> listarPorUsuario(@PathVariable Integer usuarioId) {
        List<Endereco> enderecos = enderecoService.listarPorUsuario(usuarioId);
        return ResponseEntity.ok(enderecos);
    }

    // Buscar um endereço por ID
    @GetMapping("/{id}")
    public ResponseEntity<Endereco> buscarPorId(@PathVariable Integer id) {
        Endereco endereco = enderecoService.buscarPorId(id);
        return ResponseEntity.ok(endereco);
    }

    // Atualizar um endereço
    @PutMapping("/{id}")
    public ResponseEntity<Endereco> atualizarEndereco(@PathVariable Integer id, @RequestBody Endereco novoEndereco) {
        Endereco enderecoAtualizado = enderecoService.atualizarEndereco(id, novoEndereco);
        return ResponseEntity.ok(enderecoAtualizado);
    }
}
