package com.ecommerce_ap1.ecommerce.models;

import jakarta.persistence.*;
import lombok.Data;

@Data
@Entity(name = "produtos")
public class ProdutoJPA {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @Column
    private String nome;
    @Column
    private String descricao;
    @Column
    private Double preco;
    @Column
    private Integer estoque;
}