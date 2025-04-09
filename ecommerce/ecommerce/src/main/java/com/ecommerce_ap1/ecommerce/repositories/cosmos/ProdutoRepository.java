package com.ecommerce_ap1.ecommerce.repositories.cosmos;

import com.ecommerce_ap1.ecommerce.models.Produto;
import com.azure.spring.data.cosmos.repository.CosmosRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProdutoRepository extends CosmosRepository<Produto, String> {

    void deleteByIdAndProdutoCategoria(String id, String produtoCategoria);

}