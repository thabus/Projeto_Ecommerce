package com.ecommerce_ap1.ecommerce.repositories;

import com.ecommerce_ap1.ecommerce.models.ProdutoJPA;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProdutoJPARepository extends JpaRepository<ProdutoJPA, Integer> {
}