package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;
import com.ecommerce_ap1.ecommerce.repositories.CartaoCreditoRepository;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;


@Service
public class CartaoCreditoService {

    @Autowired
    private CartaoCreditoRepository cartaoRepository;

    public void realizarCompra(Integer idCartao, double valorCompra) {
        CartaoCredito cartao = cartaoRepository.findById(idCartao)
            .orElseThrow(() -> new IllegalArgumentException("Cartão não encontrado"));

        if (cartao.getSaldoDisponivel() < valorCompra) {
            throw new IllegalArgumentException("Saldo insuficiente para a compra.");
        }

        cartao.setSaldoDisponivel(cartao.getSaldoDisponivel() - valorCompra);
        cartaoRepository.save(cartao);
    }

    public java.util.Optional<CartaoCredito> buscarCartaoPorId(Integer id) {
        return cartaoRepository.findById(id);
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
