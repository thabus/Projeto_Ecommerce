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

    @ElementCollection
    @CollectionTable(name = "pedido_produto_ids", joinColumns = @JoinColumn(name = "pedido_id"))
    @Column(name = "produto_id")
    private List<String> produtoIds; // Armazena apenas os IDs dos produtos

    @Column
    private Double valorTotal;

    @Column
    private LocalDateTime dataHora;

    @ManyToOne
    @JoinColumn(name = "cartao_id")
    private CartaoCredito cartao;
}
