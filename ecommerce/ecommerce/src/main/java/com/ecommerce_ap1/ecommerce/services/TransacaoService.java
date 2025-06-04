package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.Transacao;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class TransacaoService {

    // Simulação de banco de dados em memória
    private List<Transacao> transacoes = new ArrayList<>();

    public List<Transacao> obterExtrato(String cartaoId) {
        // Filtra as transações pelo id do cartão
        List<Transacao> extrato = new ArrayList<>();
        for (Transacao t : transacoes) {
            if (t.getCartaoId().equals(cartaoId)) {
                extrato.add(t);
            }
        }
        return extrato;
    }

    public void registrarTransacao(Transacao transacao) {
        transacoes.add(transacao);
    }
}