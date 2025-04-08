package com.ecommerce_ap1.ecommerce.models;

import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDateTime;
import java.util.List;

@Data
@Entity(name = "pedidos")
public class Pedido {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;

    @ManyToMany
    @JoinTable(
        name = "pedido_produto",
        joinColumns = @JoinColumn(name = "pedido_id"),
        inverseJoinColumns = @JoinColumn(name = "produto_id")
    )
    @Column
    private List<ProdutoJPA> produtos;

    @Column
    private Double valorTotal;

    @Column
    private LocalDateTime dataHora;

    @ManyToOne
    @JoinColumn(name = "cartao_id")
    private CartaoCredito cartao;
}