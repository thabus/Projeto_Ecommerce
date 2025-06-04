package com.ecommerce_ap1.ecommerce.repositories;

import com.ecommerce_ap1.ecommerce.models.Transacao;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface TransacaoRepository extends JpaRepository<Transacao, String> {
    List<Transacao> findByCartaoId(String cartaoId);
}