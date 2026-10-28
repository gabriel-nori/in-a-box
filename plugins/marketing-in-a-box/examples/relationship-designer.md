# Example: relationship-designer

Input: "Fluxo de relacionamento da assinatura de pães, para consumidores e para condomínios."

## Relationship Designer: Assinatura de pães
**Dois fluxos com bases diferentes; ambos com saída em uma mensagem.**

### B2C: assinante (pessoa física)
- **Base legal:** consentimento (LGPD art. 7 I), colhido no formulário de assinatura, com finalidade específica: avisos de entrega e ofertas da padaria. Aviso e oferta são caixas separadas.
- **Fluxo:** assinatura → mensagem de boas-vindas (pede confirmação) → aviso de entrega diário → oferta quinzenal (só quem marcou) → pesquisa após 30 dias.
- **Opt-out:** responder PARAR a qualquer mensagem; efeito imediato; a entrega continua se o plano estiver ativo.
- **Registro:** data, texto aceito e finalidade, por assinante.

### B2B: síndico e administradora
- **Base legal:** legítimo interesse (art. 7 IX, art. 10) para contato sobre o serviço no condomínio, apenas dados necessários (nome, cargo, e-mail corporativo). Contato é pessoa; o direito de oposição vale.
- **Fluxo:** primeiro contato com apresentação → follow-up em 7 dias → encerramento se não houver resposta (sem terceira tentativa).
- **Opt-out:** link de descadastro e frase "não quero receber"; honrado em até 10 dias úteis (CAN-SPAM como referência, caso haja contato nos EUA); remetente identificado com endereço.
- **Registro:** origem do contato e motivo da escolha de legítimo interesse.

### Saída
Contato que pede saída vai para lista de supressão; não recebe novas mensagens.

### Não coberto
Revisão jurídica: validar antes do lançamento (lawyer-in-a-box).
