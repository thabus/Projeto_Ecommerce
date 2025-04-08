package com.ecommerce_ap1.ecommerce.repositories;

import com.ecommerce_ap1.ecommerce.models.CartaoCredito;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CartaoCreditoRepository extends JpaRepository<CartaoCredito, Integer> {
    List<CartaoCredito> findByUsuarioId(Integer usuarioId);
}