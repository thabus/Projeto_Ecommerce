package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.Produto;
import com.ecommerce_ap1.ecommerce.repositories.cosmos.ProdutoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional; // Importar Optional para findById

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

    public Optional<Produto> buscarProdutoPorId(String id) {
        return produtoRepository.findById(id);
    }

    public Produto decrementarEstoque(String id, int quantidade) {
        Produto produto = produtoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Produto não encontrado para decrementar estoque: " + id));

        if (produto.getEstoque() < quantidade) {
            throw new IllegalArgumentException("Estoque insuficiente para o produto: " + produto.getNome());
        }

        produto.setEstoque(produto.getEstoque() - quantidade);
        return produtoRepository.save(produto);
    }

    public Produto atualizarProduto(String id, Produto produtoAtualizado) {
        Produto produto = produtoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Produto não encontrado para atualização"));

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
            .orElseThrow(() -> new RuntimeException("Produto não encontrado para remoção: " + id));

        produtoRepository.delete(produto);
    }

    public List<Produto> buscarPorNome(String nome) {
        return produtoRepository.findByNomeContainingIgnoreCase(nome);
    }

    public List<Produto> findByNomeContains(String nome) {
        return produtoRepository.findByNomeContains(nome);
    }
}
