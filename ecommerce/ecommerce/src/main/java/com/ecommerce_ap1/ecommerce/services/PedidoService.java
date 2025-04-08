package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;
import com.ecommerce_ap1.ecommerce.models.Pedido;
import com.ecommerce_ap1.ecommerce.models.Produto;
import com.ecommerce_ap1.ecommerce.models.Usuario;
import com.ecommerce_ap1.ecommerce.repositories.CartaoCreditoRepository;
import com.ecommerce_ap1.ecommerce.repositories.PedidoRepository;
import com.ecommerce_ap1.ecommerce.repositories.ProdutoRepository;
import com.ecommerce_ap1.ecommerce.repositories.UsuarioRepository;

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
    private UsuarioRepository usuarioRepository;

    @Autowired
    private ProdutoRepository produtoRepository;

    @Autowired
    private CartaoCreditoRepository cartaoRepository;

    public Pedido realizarPedido(Pedido pedido) {
        Integer usuarioId = pedido.getUsuario().getId();
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado"));

        // Carrega os produtos do pedido
        List<Produto> produtos = new ArrayList<>();
        double total = 0.0;

        for (Produto p : pedido.getProdutos()) {
            Produto produto = produtoRepository.findById(p.getId())
                    .orElseThrow(() -> new RuntimeException("Produto com ID " + p.getId() + " não encontrado"));
            produtos.add(produto);
            total += produto.getPreco();
        }

        // Verifica saldo nos cartões
        CartaoCredito cartaoUsado = null;
        for (CartaoCredito c : usuario.getCartoes()) {
            if (c.getSaldoDisponivel() >= total) {
                c.setSaldoDisponivel(c.getSaldoDisponivel() - total);
                cartaoRepository.save(c);
                cartaoUsado = c;
                break;
            }
        }

        if (cartaoUsado == null) {
            throw new RuntimeException("Saldo insuficiente em todos os cartões do usuário.");
        }

        // Preenche dados do pedido
        pedido.setUsuario(usuario);
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
