package com.ecommerce_ap1.ecommerce.repositories.cosmos;

import com.azure.spring.data.cosmos.repository.CosmosRepository;
import com.ecommerce_ap1.ecommerce.models.Produto;

import java.util.List;

import org.springframework.stereotype.Repository;

@Repository
public interface ProdutoRepository extends CosmosRepository<Produto, String> {

    void deleteByIdAndCategoria(String id, String categoria);

    List<Produto> findByNomeContainingIgnoreCase(String nome);

}