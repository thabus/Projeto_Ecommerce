package com.ecommerce_ap1.ecommerce.repositories.cosmos;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import com.ecommerce_ap1.ecommerce.models.Produto;
import org.springframework.stereotype.Repository;

@Repository
public interface ProdutoRepository extends CosmosRepository<Produto, String> {

    void deleteByIdAndCategoria(String id, String categoria);

}