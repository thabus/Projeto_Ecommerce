package com.ecommerce_ap1.ecommerce.services;

import com.ecommerce_ap1.ecommerce.models.Pedido;
import com.ecommerce_ap1.ecommerce.models.Produto;
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

    /**
     * Cria um novo pedido com status "pendente".
     *
     * @param request Dados para a criação do pedido, incluindo IDs dos produtos e ID do cliente.
     * @return O pedido recém-criado com status "pendente".
     * @throws IllegalArgumentException se nenhum produto for selecionado ou se um produto não for encontrado/estiver fora de estoque.
     */
    public Pedido criarPedido(RealizarCompraRequest request) {
        List<Produto> produtosValidados = new ArrayList<>();
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
            produtosValidados.add(produto); // Adiciona o produto validado
            valorTotal += produto.getPreco();
        }

        Pedido novoPedido = new Pedido();
        novoPedido.setId(UUID.randomUUID().toString());
        novoPedido.setClienteId(request.getClienteId());
        novoPedido.setProdutosIds(request.getProdutosIds()); // Armazena apenas os IDs
        novoPedido.setValorTotal(valorTotal);
        novoPedido.setDataPedido(new Date());
        novoPedido.setStatus("pendente"); // Status inicial do pedido

        pedidos.add(novoPedido);
        return novoPedido;
    }

    /**
     * Processa o pagamento de um pedido existente.
     *
     * @param pedidoId O ID do pedido a ser processado.
     * @param cartaoId O ID do cartão de crédito a ser usado para o pagamento.
     * @return O pedido com o status atualizado para "pago".
     * @throws IllegalArgumentException se o pedido não for encontrado, já estiver pago, ou se houver um erro no pagamento.
     */
    public Pedido processarPagamentoPedido(String pedidoId, String cartaoIdString) {
        Pedido pedido = buscarPedidoPorId(pedidoId)
            .orElseThrow(() -> new IllegalArgumentException("Pedido com ID " + pedidoId + " não encontrado."));

        if (!"pendente".equalsIgnoreCase(pedido.getStatus())) {
            throw new IllegalArgumentException("Pedido já foi pago ou está em outro status: " + pedido.getStatus());
        }

        // --- INÍCIO DA CORREÇÃO ---
        Integer idCartao;
        try {
            idCartao = Integer.parseInt(cartaoIdString); // Converte String para Integer
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("ID do cartão inválido. Deve ser um número inteiro.", e);
        }
        // --- FIM DA CORREÇÃO ---

        List<Produto> produtosDoPedido = new ArrayList<>();
        for (String prodId : pedido.getProdutosIds()) { // Renomeado para evitar conflito com 'produtoId' do loop externo se existir
            Produto produto = produtoService.buscarProdutoPorId(prodId)
                .orElseThrow(() -> new IllegalArgumentException("Produto com ID " + prodId + " não encontrado no sistema."));
            produtosDoPedido.add(produto);
        }

        try {
            String descricaoTransacao = "Pagamento do pedido: " + pedido.getId();
            // Passa o idCartao que agora é um Integer
            cartaoCreditoService.realizarCompra(idCartao, pedido.getValorTotal(), descricaoTransacao);
        } catch (IllegalArgumentException e) {
            throw new IllegalArgumentException("Falha no pagamento: " + e.getMessage());
        }

        // Decrementar estoque apenas após o sucesso do pagamento
        for (Produto produto : produtosDoPedido) {
            produtoService.decrementarEstoque(produto.getId(), 1); // Decrementa 1 unidade para cada produto no pedido
        }

        pedido.setStatus("pago"); // Atualiza o status do pedido
        return pedido;
    }

    public List<Pedido> listarPedidos() {
        return new ArrayList<>(pedidos); // Retorna uma cópia para evitar modificações externas
    }

    /**
     * Busca um pedido pelo seu ID.
     * @param id O ID do pedido.
     * @return Um Optional contendo o pedido se encontrado, ou um Optional vazio.
     */
    public Optional<Pedido> buscarPedidoPorId(String id) {
        return pedidos.stream()
            .filter(p -> p.getId().equals(id))
            .findFirst();
    }

    /**
     * Busca pedidos que contêm um produto com o nome especificado.
     * @param nomeProduto O nome do produto a ser pesquisado.
     * @return Uma lista de pedidos que contêm o produto.
     */
    public List<Pedido> buscarPedidosPorNomeProduto(String nomeProduto) {
        List<Pedido> pedidosEncontrados = new ArrayList<>();
        String nomeProdutoLower = nomeProduto.toLowerCase();

        for (Pedido pedido : this.pedidos) {
            for (String produtoId : pedido.getProdutosIds()) {
                Optional<Produto> produtoOpt = produtoService.buscarProdutoPorId(produtoId);
                if (produtoOpt.isPresent()) {
                    Produto produto = produtoOpt.get();
                    // Usar contains para busca parcial e ignorar caixa
                    if (produto.getNome().toLowerCase().contains(nomeProdutoLower)) {
                        pedidosEncontrados.add(pedido);
                        break;
                    }
                }
            }
        }
        return pedidosEncontrados;
    }

    // filtra por status
    public List<Pedido> listarPedidos(String status) {
        if (status == null || status.trim().isEmpty()) {
            return new ArrayList<>(pedidos); // Retorna todos os pedidos se o status for nulo ou vazio
        }
        final String lowerCaseStatus = status.toLowerCase(); // Converte para minúsculas uma vez
        return pedidos.stream()
                      .filter(pedido -> pedido.getStatus() != null && pedido.getStatus().toLowerCase().equals(lowerCaseStatus))
                      .collect(Collectors.toList());
    }
}