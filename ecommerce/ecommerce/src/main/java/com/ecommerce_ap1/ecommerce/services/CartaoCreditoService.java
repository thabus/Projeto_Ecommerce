package com.ecommerce_ap1.ecommerce.services;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;
import com.ecommerce_ap1.ecommerce.repositories.CartaoCreditoRepository;

@Service
public class CartaoCreditoService {

    @Autowired
    private CartaoCreditoRepository cartaoRepository;

    public CartaoCredito salvar(CartaoCredito cartao) {
        return cartaoRepository.save(cartao);
    }


    public CartaoCredito buscarPorId(Integer id) {
        return cartaoRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Cartão não encontrado"));
    }

    public CartaoCredito atualizarSaldo(Integer cartaoId, double novoSaldo) {
        CartaoCredito cartao = buscarPorId(cartaoId);
        cartao.setSaldoDisponivel(novoSaldo);
        return cartaoRepository.save(cartao);
    }

    public List<CartaoCredito> listarPorUsuario(Integer usuarioId) {
        return cartaoRepository.findByUsuarioId(usuarioId);
    }
}
