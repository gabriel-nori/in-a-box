# Example: process-modeler

Input: "Hoje o pedido chega por WhatsApp, o dono anota num caderno, o padeiro produz e o entregador leva."

## Process Modeler: Pedido de assinatura
**Hoje o caderno é o ponto de falha; no to-be o pedido nasce numa planilha única.**

### Scope and actors
Gatilho: cliente envia pedido. Fins: pedido entregue, ou pedido recusado. Atores: Cliente, Dono, Padeiro, Entregador.

### As-is (Mermaid)
```mermaid
flowchart LR
  subgraph Cliente
    A([Envia pedido no WhatsApp])
  end
  subgraph Dono
    B[Anota no caderno]
    C{Tem capacidade?}
    D[Avisa que não há vaga]
  end
  subgraph Padeiro
    E[Produz o pedido]
  end
  subgraph Entregador
    F[Entrega na portaria]
  end
  A --> B --> C
  C -- sim --> E --> F --> G([Pedido entregue])
  C -- não --> D --> H([Pedido recusado])
```

### To-be (Mermaid)
```mermaid
flowchart LR
  subgraph Cliente
    A([Envia pedido no WhatsApp])
  end
  subgraph Dono
    B[Registra na planilha]
    C{Tem capacidade?}
    D[Avisa que não há vaga]
  end
  subgraph Padeiro
    E[Produz pelo mapa do dia]
  end
  subgraph Entregador
    F[Entrega e confirma na planilha]
  end
  A --> B --> C
  C -- sim --> E --> F --> G([Pedido entregue])
  C -- não --> D --> H([Pedido recusado])
```

### Delta
- Caderno vira planilha compartilhada: o padeiro lê o mapa do dia sem perguntar ao dono.
- Entrega passa a ser confirmada: remove o "entregou?" por mensagem.
- Não desenhado: mensagens entre pools e eventos de borda (limite do Mermaid, não do processo).
