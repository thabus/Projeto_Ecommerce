package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;
import com.ecommerce_ap1.ecommerce.models.Transacao;
import com.ecommerce_ap1.ecommerce.repositories.CartaoCreditoRepository;

import java.util.Date;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


@Service
public class CartaoCreditoService {

    @Autowired
    private CartaoCreditoRepository cartaoRepository;

    @Autowired
    private TransacaoService transacaoService;

    public void realizarCompra(Integer idCartao, double valorCompra, String descricaoTransacao) {
        CartaoCredito cartao = cartaoRepository.findById(idCartao)
            .orElseThrow(() -> new IllegalArgumentException("Cartão de crédito não encontrado."));

        if (cartao.getSaldoDisponivel() < valorCompra) {
            throw new IllegalArgumentException("Saldo insuficiente no cartão para a compra.");
        }

        cartao.setSaldoDisponivel(cartao.getSaldoDisponivel() - valorCompra);
        cartaoRepository.save(cartao);

        Transacao transacao = new Transacao();
        transacao.setCartaoId(String.valueOf(idCartao)); 
        transacao.setValor(valorCompra);
        transacao.setDataTransacao(new Date());
        transacao.setDescricao(descricaoTransacao);
        transacaoService.registrarTransacao(transacao);
    }

    public java.util.Optional<CartaoCredito> buscarCartaoPorId(Integer id) {
        return cartaoRepository.findById(id);
    }

    public List<Transacao> obterExtrato(Integer cartaoId) {
        return transacaoService.obterExtrato(cartaoId.toString());
    }

    public List<CartaoCredito> listarTodos() {
        return cartaoRepository.findAll();
    }

    public CartaoCredito atualizarSaldo(Integer idCartao, double novoSaldo) {
        CartaoCredito cartao = cartaoRepository.findById(idCartao)
            .orElseThrow(() -> new IllegalArgumentException("Cartão não encontrado"));

        cartao.setSaldoDisponivel(novoSaldo);
        return cartaoRepository.save(cartao);
    }
}
