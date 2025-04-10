package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.Produto;
import com.ecommerce_ap1.ecommerce.repositories.cosmos.ProdutoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class ProdutoService {

    @Autowired
    private ProdutoRepository produtoRepository;

    public Produto criarProduto(Produto produto) {
        return produtoRepository.save(produto);
    }

    public List<Produto> listarProdutos() {
        List<Produto> produtos = new ArrayList<>();
        produtoRepository.findAll().forEach(produtos::add);
        return produtos;
    }

    public Produto atualizarProduto(String id, Produto produtoAtualizado) {
        Produto produto = produtoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Produto não encontrado"));

        if (produtoAtualizado.getNome() != null) {
            produto.setNome(produtoAtualizado.getNome());
        }
        if (produtoAtualizado.getDescricao() != null) {
            produto.setDescricao(produtoAtualizado.getDescricao());
        }
        if (produtoAtualizado.getPreco() != null) {
            produto.setPreco(produtoAtualizado.getPreco());
        }
        if (produtoAtualizado.getEstoque() != null) {
            produto.setEstoque(produtoAtualizado.getEstoque());
        }
        if (produtoAtualizado.getCategoria() != null) {
            produto.setCategoria(produtoAtualizado.getCategoria());
        }

        return produtoRepository.save(produto);
    }


    public void removerProduto(String id, String categoria) {
        Produto produto = produtoRepository.findById(id)
            .orElseThrow(() -> new RuntimeException("Produto não encontrado"));

        if (!produto.getCategoria().equals(categoria)) {
            throw new RuntimeException("Categoria não corresponde à do produto.");
        }

        // Este método é seguro e funciona porque a partition key já está no objeto
        produtoRepository.delete(produto);
    }


}
