package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.Pedido;
import com.ecommerce_ap1.ecommerce.models.Produto;
import com.ecommerce_ap1.ecommerce.models.Usuario; // Importa a classe Usuario
import com.ecommerce_ap1.ecommerce.request.RealizarCompraRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import java.util.stream.Collectors;

@Service
public class PedidoService {

    private List<Pedido> pedidos = new ArrayList<>();

    @Autowired
    private ProdutoService produtoService;

    @Autowired
    private CartaoCreditoService cartaoCreditoService;

    @Autowired
    private UsuarioService usuarioService;

    public Pedido criarPedido(RealizarCompraRequest request) {
        List<String> produtosNomes = new ArrayList<>();
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
            produtosNomes.add(produto.getNome());
            valorTotal += produto.getPreco();
        }

        Pedido novoPedido = new Pedido();
        novoPedido.setId(UUID.randomUUID().toString());
        novoPedido.setUsuarioId(request.getUsuarioId());

        Integer usuarioIdInt;
        try {
            usuarioIdInt = Integer.parseInt(request.getUsuarioId());
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("ID de usuário inválido na requisição. Deve ser um número inteiro.", e);
        }

        Usuario usuario = usuarioService.buscarUsuarioPorId(usuarioIdInt)
                                .orElseThrow(() -> new IllegalArgumentException("Usuário com ID " + request.getUsuarioId() + " não encontrado."));
        novoPedido.setUsuarioNome(usuario.getNome());

        novoPedido.setProdutosIds(request.getProdutosIds());
        novoPedido.setProdutos(produtosNomes);
        novoPedido.setValorTotal(valorTotal);
        novoPedido.setDataPedido(new Date());
        novoPedido.setStatus("pendente");

        pedidos.add(novoPedido);
        return novoPedido;
    }

    public Pedido processarPagamentoPedido(String pedidoId, String cartaoIdString) {
        Pedido pedido = buscarPedidoPorId(pedidoId)
            .orElseThrow(() -> new IllegalArgumentException("Pedido com ID " + pedidoId + " não encontrado."));

        if (!"pendente".equalsIgnoreCase(pedido.getStatus())) {
            throw new IllegalArgumentException("Pedido já foi pago ou está em outro status: " + pedido.getStatus());
        }

        Integer idCartao;
        try {
            idCartao = Integer.parseInt(cartaoIdString);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("ID do cartão inválido. Deve ser um número inteiro.", e);
        }

        List<Produto> produtosDoPedido = new ArrayList<>();
        for (String prodId : pedido.getProdutosIds()) {
            Produto produto = produtoService.buscarProdutoPorId(prodId)
                .orElseThrow(() -> new IllegalArgumentException("Produto com ID " + prodId + " não encontrado no sistema."));
            produtosDoPedido.add(produto);
        }

        try {
            String descricaoTransacao = "Pagamento do pedido: " + pedido.getId();
            cartaoCreditoService.realizarCompra(idCartao, pedido.getValorTotal(), descricaoTransacao);
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("Falha no pagamento: " + e.getMessage());
        }

        for (Produto produto : produtosDoPedido) {
            produtoService.decrementarEstoque(produto.getId(), 1);
        }

        pedido.setStatus("pago");
        return pedido;
    }

    public List<Pedido> listarTodosOsPedidos() {
        return new ArrayList<>(pedidos);
    }

    public Optional<Pedido> buscarPedidoPorId(String id) {
        return pedidos.stream()
            .filter(p -> p.getId().equals(id))
            .findFirst();
    }

    public List<Pedido> buscarPedidosPorNomeProduto(String nomeProduto) {
        List<Pedido> pedidosEncontrados = new ArrayList<>();
        String nomeProdutoLower = nomeProduto.toLowerCase();

        for (Pedido pedido : this.pedidos) {
            if (pedido.getProdutos() != null) {
                for (String nomeProdNoPedido : pedido.getProdutos()) {
                    if (nomeProdNoPedido.toLowerCase().contains(nomeProdutoLower)) {
                        pedidosEncontrados.add(pedido);
                        break;
                    }
                }
            }
        }
        return pedidosEncontrados;
    }

    public List<Pedido> listarPedidos(String usuarioId, String status) {
        List<Pedido> listaFiltrada = new ArrayList<>(pedidos);

        if (usuarioId != null && !usuarioId.trim().isEmpty()) {
            listaFiltrada = listaFiltrada.stream()
                                         .filter(pedido -> pedido.getUsuarioId() != null && pedido.getUsuarioId().equals(usuarioId))
                                         .collect(Collectors.toList());
        }

        if (status != null && !status.trim().isEmpty()) {
            final String lowerCaseStatus = status.toLowerCase();
            listaFiltrada = listaFiltrada.stream()
                                         .filter(pedido -> pedido.getStatus() != null && pedido.getStatus().toLowerCase().equals(lowerCaseStatus))
                                         .collect(Collectors.toList());
        }

        return listaFiltrada;
    }
}