package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.Pedido;
import com.ecommerce_ap1.ecommerce.models.Produto;
import com.ecommerce_ap1.ecommerce.request.RealizarCompraRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.UUID;
@Service
public class PedidoService {

    private List<Pedido> pedidos = new ArrayList<>();

    @Autowired
    private ProdutoService produtoService;

    @Autowired
    private CartaoCreditoService cartaoCreditoService;


    public Pedido realizarCompra(RealizarCompraRequest request) {
        List<Produto> produtosComprados = new ArrayList<>();
        double valorTotal = 0.0;

        if (request.getProdutosIds() == null || request.getProdutosIds().isEmpty()) {
            throw new IllegalArgumentException("Nenhum produto selecionado para a compra.");
        }

        for (String produtoId : request.getProdutosIds()) {
            Produto produto = produtoService.buscarProdutoPorId(produtoId)
                .orElseThrow(() -> new IllegalArgumentException("Produto com ID " + produtoId + " não encontrado."));

            if (produto.getEstoque() < 1) {
                throw new IllegalArgumentException("Produto '" + produto.getNome() + "' está fora de estoque.");
            }

            produtosComprados.add(produto);
            valorTotal += produto.getPreco();
        }
        try {
            String descricaoTransacao = "Compra de produtos: " + String.join(", ", request.getProdutosIds());
            cartaoCreditoService.realizarCompra(request.getCartaoId(), valorTotal, descricaoTransacao);
        } catch (IllegalArgumentException e) {
            throw e;
        }

        for (Produto produto : produtosComprados) {
            produtoService.decrementarEstoque(produto.getId(), 1);
        }

        Pedido novoPedido = new Pedido();
        novoPedido.setId(UUID.randomUUID().toString());
        novoPedido.setClienteId(request.getClienteId());
        novoPedido.setProdutosIds(request.getProdutosIds());
        novoPedido.setValorTotal(valorTotal);
        novoPedido.setDataPedido(new Date());
        novoPedido.setStatus("Concluído");

        pedidos.add(novoPedido);
        return novoPedido;
    }

    public List<Pedido> listarPedidos() {
        return pedidos;
    }
}
