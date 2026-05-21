# 🌿 Estufa Inteligente — Controle Distribuído via RPC

Este projeto implementa um sistema de controle para uma **estufa automatizada (fazenda vertical)** utilizando **RPC (Remote Procedure Call)** com a biblioteca nativa `xmlrpc` do Python. O objetivo é permitir que um computador cliente acione remotamente os atuadores de diferentes setores da estufa através da rede.

---

## 📁 Estrutura do Projeto

```
estufa-inteligente-rpc/
├── servidor_hidroponico.py    # Servidor do setor hidropônico  (porta 9001)
├── servidor_iluminacao.py     # Servidor do painel de iluminação UV (porta 9002)
├── servidor_climatizador.py   # Servidor do climatizador (porta 9003)
└── cliente.py                 # Painel de controle interativo (cliente RPC)
```

| Arquivo | Responsabilidade |
|---|---|
| `servidor_hidroponico.py` | Controle de irrigação e monitoramento do nível de água |
| `servidor_iluminacao.py` | Ajuste de intensidade e espectro de luz UV |
| `servidor_climatizador.py` | Definição de temperatura-alvo e controle dos exaustores |
| `cliente.py` | Painel de controle que se conecta aos 3 servidores via RPC |

---

## ⚙️ Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Comunicação:** Biblioteca nativa `xmlrpc` (sem dependências externas)

---

## 🚀 Como Executar

### ✅ Configuração Padrão — Tudo na mesma máquina (localhost)

O projeto já está **pronto para rodar localmente**. Não é necessária nenhuma alteração no código.

**Passo 1:** Abra **3 terminais separados** e inicie cada servidor:

```bash
# Terminal 1
python servidor_hidroponico.py

# Terminal 2
python servidor_iluminacao.py

# Terminal 3
python servidor_climatizador.py
```

> No Linux/macOS, use `python3` no lugar de `python`.

**Passo 2:** Abra um **4º terminal** e inicie o painel de controle:

```bash
python cliente.py
```

Os servidores ficam aguardando conexões nas portas **9001**, **9002** e **9003** respectivamente. O cliente se conecta automaticamente a todos eles via `localhost`.

---

## 🌐 Executar em Máquinas Diferentes (Rede Local)

Para distribuir os servidores em computadores diferentes na mesma rede, são necessárias **duas alterações**: uma em cada servidor e outra no cliente.

### 1️⃣ Alterar o endereço de escuta em cada servidor

Por padrão, os servidores escutam somente em `"localhost"`, o que os torna inacessíveis por outras máquinas. Para aceitar conexões externas, substitua `"localhost"` por `"0.0.0.0"` (escuta em todas as interfaces de rede) em cada arquivo de servidor.

**`servidor_hidroponico.py`** — linha final de configuração:
```python
# Antes (somente localhost):
servidor = SimpleXMLRPCServer(("localhost", 9001))

# Depois (aceita conexões de qualquer IP da rede):
servidor = SimpleXMLRPCServer(("0.0.0.0", 9001))
```

**`servidor_iluminacao.py`**:
```python
# Antes:
servidor = SimpleXMLRPCServer(("localhost", 9002))

# Depois:
servidor = SimpleXMLRPCServer(("0.0.0.0", 9002))
```

**`servidor_climatizador.py`**:
```python
# Antes:
servidor = SimpleXMLRPCServer(("localhost", 9003))

# Depois:
servidor = SimpleXMLRPCServer(("0.0.0.0", 9003))
```

---

### 2️⃣ Alterar os IPs no cliente

No arquivo `cliente.py`, a função `conectar()` usa `localhost` como endereço fixo. Substitua pelo **IP real** de cada máquina servidora na rede local.

**`cliente.py`** — função `main()` (por volta das linhas 170–172):
```python
# Antes (todos na mesma máquina):
proxy_hidro = conectar(9001, "Setor Hidropônico")
proxy_luz   = conectar(9002, "Painel Iluminação UV")
proxy_clima = conectar(9003, "Climatizador")
```

A função `conectar()` monta a URL como `http://localhost:<porta>`. Altere-a para aceitar um IP como parâmetro, ou substitua diretamente as URLs:

```python
# Depois (servidores em máquinas diferentes):
proxy_hidro = xmlrpc.client.ServerProxy("http://192.168.1.10:9001")  # IP da máquina do servidor hidropônico
proxy_luz   = xmlrpc.client.ServerProxy("http://192.168.1.11:9002")  # IP da máquina do servidor de iluminação
proxy_clima = xmlrpc.client.ServerProxy("http://192.168.1.12:9003")  # IP da máquina do servidor climatizador
```

> **Como descobrir o IP de cada máquina:**
> - **Windows:** Execute `ipconfig` no terminal e procure por "Endereço IPv4"
> - **Linux/macOS:** Execute `ip addr` ou `ifconfig`

---

### 3️⃣ Liberar as portas no firewall (se necessário)

Se as conexões não forem estabelecidas, pode ser necessário liberar as portas **9001**, **9002** e **9003** no firewall de cada máquina servidora.

**Windows (PowerShell como Administrador):**
```powershell
New-NetFirewallRule -DisplayName "Estufa RPC 9001" -Direction Inbound -Protocol TCP -LocalPort 9001 -Action Allow
New-NetFirewallRule -DisplayName "Estufa RPC 9002" -Direction Inbound -Protocol TCP -LocalPort 9002 -Action Allow
New-NetFirewallRule -DisplayName "Estufa RPC 9003" -Direction Inbound -Protocol TCP -LocalPort 9003 -Action Allow
```

**Linux (ufw):**
```bash
sudo ufw allow 9001/tcp
sudo ufw allow 9002/tcp
sudo ufw allow 9003/tcp
```

---

## 📋 Resumo das Portas

| Servidor | Porta | Funções RPC disponíveis |
|---|---|---|
| Hidropônico | 9001 | `ativar_irrigacao(tempo)`, `checar_nivel_agua()`, `gerar_relatorio()` |
| Iluminação UV | 9002 | `ajustar_intensidade(valor)`, `mudar_espectro(cor)`, `gerar_relatorio()` |
| Climatizador | 9003 | `definir_temperatura(graus)`, `abrir_exaustores()`, `fechar_exaustores()`, `gerar_relatorio()` |

---

## 📝 Observações

- Os estados dos servidores são mantidos **em memória** durante a execução. Ao reiniciar um servidor, os valores voltam ao padrão inicial.
- O cliente continua funcionando mesmo que um dos servidores esteja indisponível — ele exibe uma mensagem de erro e desabilita apenas o setor afetado.
- A opção **[4] Relatório Geral** no cliente consulta os três servidores simultaneamente e exibe um resumo completo do estado da estufa.
