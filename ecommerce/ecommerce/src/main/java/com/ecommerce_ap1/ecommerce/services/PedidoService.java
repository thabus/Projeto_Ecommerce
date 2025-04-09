package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;
import com.ecommerce_ap1.ecommerce.models.Pedido;
import com.ecommerce_ap1.ecommerce.models.Produto;
import com.ecommerce_ap1.ecommerce.models.Usuario;
import com.ecommerce_ap1.ecommerce.repositories.CartaoCreditoRepository;
import com.ecommerce_ap1.ecommerce.repositories.PedidoRepository;
import com.ecommerce_ap1.ecommerce.repositories.UsuarioRepository;
import com.ecommerce_ap1.ecommerce.repositories.cosmos.ProdutoRepository;

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
    private CartaoCreditoRepository cartaoRepository;

    @Autowired
    private ProdutoRepository produtoRepository;

    public Pedido realizarPedido(Pedido pedido) {
        Integer usuarioId = pedido.getUsuario().getId();
        Usuario usuario = usuarioRepository.findById(usuarioId)
                .orElseThrow(() -> new RuntimeException("Usuário não encontrado"));

        // Lista de IDs dos produtos enviados
        List<String> produtoIds = pedido.getProdutoIds();
        List<Produto> produtos = new ArrayList<>();
        double total = 0.0;

        for (String id : produtoIds) {
            Produto produto = produtoRepository.findById(id)
                    .orElseThrow(() -> new RuntimeException("Produto com ID " + id + " não encontrado"));
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
        pedido.setProdutoIds(produtoIds);
        pedido.setValorTotal(total);
        pedido.setDataHora(LocalDateTime.now());
        pedido.setCartao(cartaoUsado);

        Pedido salvo = pedidoRepository.save(pedido);

        return salvo;
    }

    public List<Pedido> listarPedidos() {
        return pedidoRepository.findAll();
    }
}
