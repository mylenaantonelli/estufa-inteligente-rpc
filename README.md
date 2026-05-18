# Estufa Inteligente - Controle Distribuído (RPC)

Este projeto implementa um sistema de controle para uma estufa automatizada (fazenda vertical) utilizando **RPC (Remote Procedure Call)**. O objetivo é permitir que um computador cliente acione remotamente os atuadores de diferentes setores da estufa através da rede.

## Estrutura do Projeto

O sistema é dividido em 4 componentes principais:

* `servidor_hidroponico.py`: Nó responsável pelo controle de irrigação e monitoramento do nível de água.
* `servidor_iluminacao.py`: Nó responsável pelo ajuste da intensidade e do espectro da luz UV.
* `servidor_climatizador.py`: Nó responsável por definir a temperatura e controlar os exaustores.
* `cliente.py`: Painel de controle interativo que se conecta aos 3 servidores para enviar comandos e gerar o relatório diário de status.

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Comunicação:** Biblioteca nativa `xmlrpc`

## Como Executar

**Passo 1:** Abra o terminal e inicie os três servidores (eles ficarão aguardando conexões):
   ```bash
   python3 servidor_hidroponico.py
   python3 servidor_iluminacao.py
   python3 servidor_climatizador.py
```

**Passo 2:** Em um novo terminal, inicie a estação de controle:
```bash
   python3 cliente.py
```

> **Aviso:** Se for rodar em computadores diferentes na mesma rede local, lembre-se de alterar as variáveis de IP (onde está `localhost`) no arquivo `cliente.py` para o IP real de cada máquina servidora.
