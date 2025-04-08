package com.ecommerce_ap1.ecommerce.repositories;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.ecommerce_ap1.ecommerce.models.Endereco;

public interface EnderecoRepository extends JpaRepository<Endereco, Integer> {
    List<Endereco> findByUsuarioId(Integer usuarioId);
}
