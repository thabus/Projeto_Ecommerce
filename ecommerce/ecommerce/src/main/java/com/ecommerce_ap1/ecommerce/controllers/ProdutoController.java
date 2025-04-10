package com.ecommerce_ap1.ecommerce.controllers;

import com.ecommerce_ap1.ecommerce.models.Produto;
import com.ecommerce_ap1.ecommerce.services.ProdutoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/produtos")
public class ProdutoController {

    @Autowired
    private ProdutoService produtoService;

    // Criar novo produto
    @PostMapping
    public Produto criarProduto(@RequestBody Produto produto) {
        return produtoService.criarProduto(produto);
    }

    // Listar todos os produtos
    @GetMapping
    public List<Produto> listarProdutos() {
        return produtoService.listarProdutos();
    }

    // Atualizar produto (PATCH ou PUT parcial)
    @PutMapping("/{id}")
    public Produto atualizarProduto(
            @PathVariable String id,
            @RequestBody Produto produtoAtualizado
    ) {
        return produtoService.atualizarProduto(id, produtoAtualizado);
    }

    // Deletar produto (requer ID e categoria por ser PartitionKey)
    @DeleteMapping("/{id}/{categoria}")
    public ResponseEntity<String> deletar(
        @PathVariable String id,
        @PathVariable("categoria") String categoria) {
    produtoService.removerProduto(id, categoria);
    return ResponseEntity.ok("Produto com ID " + id + " e categoria '" + categoria + "' foi deletado com sucesso.");
}

}
