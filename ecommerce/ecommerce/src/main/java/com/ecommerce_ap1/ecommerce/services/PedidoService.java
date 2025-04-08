package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;
import com.ecommerce_ap1.ecommerce.models.Pedido;
import com.ecommerce_ap1.ecommerce.models.ProdutoJPA;
import com.ecommerce_ap1.ecommerce.models.Usuario;
import com.ecommerce_ap1.ecommerce.repositories.PedidoRepository;
import com.ecommerce_ap1.ecommerce.repositories.ProdutoJPARepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

@Service
public class PedidoService {

    @Autowired
    private PedidoRepository pedidoRepository;


    @Autowired
    private ProdutoJPARepository produtoJPARepository;

    public Pedido realizarPedido(Pedido pedido) {


        // Carrega os produtos do pedido
        List<ProdutoJPA> produtos = new ArrayList<>();
        double total = 0.0;

        for (ProdutoJPA p : pedido.getProdutos()) {
            ProdutoJPA produto = produtoJPARepository.findById(p.getId())
                    .orElseThrow(() -> new RuntimeException("Produto com ID " + p.getId() + " não encontrado"));
            produtos.add(produto);
            total += produto.getPreco();
        }



        // Preenche dados do pedido
        pedido.setProdutos(produtos);
        pedido.setValorTotal(total);
        pedido.setDataHora(LocalDateTime.now());

        Pedido salvo = pedidoRepository.save(pedido);

        return salvo;
    }

    public List<Pedido> listarPedidos() {
        return pedidoRepository.findAll();
    }

}