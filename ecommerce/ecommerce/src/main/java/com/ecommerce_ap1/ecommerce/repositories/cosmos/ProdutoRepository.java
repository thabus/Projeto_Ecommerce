package com.ecommerce_ap1.ecommerce.repositories.cosmos;

import com.ecommerce_ap1.ecommerce.models.Produto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProdutoRepository extends JpaRepository<Produto, String> {
}