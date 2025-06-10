package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.Transacao;
import com.ecommerce_ap1.ecommerce.repositories.TransacaoRepository; 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;
import java.util.UUID;

@Service
public class TransacaoService {

    @Autowired
    private TransacaoRepository transacaoRepository;

    public List<Transacao> obterExtrato(String cartaoId) {
        return transacaoRepository.findByCartaoId(cartaoId);
    }

    public void registrarTransacao(Transacao transacao) {
        if (transacao.getId() == null || transacao.getId().isEmpty()) {
            transacao.setId(UUID.randomUUID().toString());
        }
        if (transacao.getDataTransacao() == null) {
            transacao.setDataTransacao(new Date());
        }
        transacaoRepository.save(transacao);
    }
}
