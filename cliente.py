import xmlrpc.client
import datetime


class Relatorio:

    def __init__(self, proxy_hidro, proxy_luz, proxy_clima):
        self.proxy_hidro = proxy_hidro
        self.proxy_luz   = proxy_luz
        self.proxy_clima = proxy_clima

    def _linha(self, char="─", largura=55):
        return char * largura

    def _bloco_setor(self, dados: dict) -> str:
        setor = dados.pop("setor", "Setor desconhecido")
        linhas = [f"{setor}"]
        for chave, valor in dados.items():
            chave_fmt = chave.replace("_", " ").capitalize()
            linhas.append(f"     • {chave_fmt:<22}: {valor}")
        return "\n".join(linhas)

    def gerar(self) -> str:
        agora  = datetime.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        linhas = []

        linhas.append(self._linha("═"))
        linhas.append("RELATÓRIO GERAL DA ESTUFA INTELIGENTE")
        linhas.append(f"Gerado em: {agora}")
        linhas.append(self._linha("═"))

        setores = [
            ("Hidropônico",    self.proxy_hidro),
            ("Iluminação UV",  self.proxy_luz),
            ("Climatizador",   self.proxy_clima),
        ]

        for nome, proxy in setores:
            linhas.append(self._linha())
            try:
                dados = proxy.gerar_relatorio()   
                linhas.append(self._bloco_setor(dados))
            except Exception as e:
                linhas.append(f"{nome}: erro ao consultar servidor ({e})")

        linhas.append(self._linha("═"))
        linhas.append("Fim do relatório.")
        linhas.append(self._linha("═"))

        return "\n".join(linhas)


def cabecalho():
    print("\n" + "═" * 55)
    print("ESTAÇÃO DE CONTROLE — ESTUFA INTELIGENTE")
    print("═" * 55)

def menu_principal():
    print("\n─────────────────────────────────────")
    print("  Escolha o setor ou ação:                    ")
    print("  [1] Setor Hidropônico                       ")
    print("  [2] Iluminação UV                           ")
    print("  [3] Climatizador                            ")
    print("  [4] Relatório Geral                         ")
    print("  [0] Sair                                    ")
    print("───────────────────────────────────────")

def menu_hidroponico(proxy):
    print("\n  [HIDROPÔNICO] O que deseja fazer?")
    print("  [1] Ativar irrigação")
    print("  [2] Checar nível de água")
    print("  [0] Voltar")
    op = input("  Opção: ").strip()

    if op == "1":
        try:
            tempo = int(input("  Tempo de irrigação (segundos): ").strip())
            resultado = proxy.ativar_irrigacao(tempo)
            print(f"\n  {resultado}")
        except ValueError:
            print("Digite um número inteiro.")
        except Exception as e:
            print(f"Erro de comunicação: {e}")

    elif op == "2":
        try:
            resultado = proxy.checar_nivel_agua()
            print(f"\n  {resultado}")
        except Exception as e:
            print(f"Erro de comunicação: {e}")


def menu_iluminacao(proxy):
    print("\n  [ILUMINAÇÃO UV] O que deseja fazer?")
    print("  [1] Ajustar intensidade (0–100%)")
    print("  [2] Mudar espectro de luz")
    print("  [0] Voltar")
    op = input("  Opção: ").strip()

    if op == "1":
        try:
            valor = int(input("  Intensidade (0 a 100): ").strip())
            resultado = proxy.ajustar_intensidade(valor)
            print(f"\n  {resultado}")
        except ValueError:
            print("Digite um número inteiro.")
        except Exception as e:
            print(f"Erro de comunicação: {e}")

    elif op == "2":
        print("Espectros disponíveis: vermelho | azul | branco | uv | infravermelho")
        try:
            cor = input("Espectro desejado: ").strip()
            resultado = proxy.mudar_espectro(cor)
            print(f"\n  {resultado}")
        except Exception as e:
            print(f"Erro de comunicação: {e}")


def menu_climatizador(proxy):
    print("\n  [CLIMATIZADOR] O que deseja fazer?")
    print("  [1] Definir temperatura-alvo")
    print("  [2] Abrir exaustores")
    print("  [3] Fechar exaustores")
    print("  [0] Voltar")
    op = input("  Opção: ").strip()

    if op == "1":
        try:
            graus = float(input("  Temperatura desejada (°C): ").strip())
            resultado = proxy.definir_temperatura(graus)
            print(f"\n  {resultado}")
        except ValueError:
            print("Digite um número:")
        except Exception as e:
            print(f"Erro de comunicação: {e}")

    elif op == "2":
        try:
            resultado = proxy.abrir_exaustores()
            print(f"\n  {resultado}")
        except Exception as e:
            print(f"Erro de comunicação: {e}")

    elif op == "3":
        try:
            resultado = proxy.fechar_exaustores()
            print(f"\n  {resultado}")
        except Exception as e:
            print(f"Erro de comunicação: {e}")


def conectar(porta, nome):
    url = f"http://localhost:{porta}"
    try:
        proxy = xmlrpc.client.ServerProxy(url)
        proxy.system.listMethods()
        print(f"{nome} conectado (porta {porta})")
        return proxy
    except Exception:
        print(f"{nome} Indisponível (porta {porta}) — inicie o servidor antes!")
        return None


def main():
    cabecalho()
    print("\n  Conectando aos setores da estufa")
    print("─" * 55)

    proxy_hidro = conectar(9001, "Setor Hidropônico")
    proxy_luz   = conectar(9002, "Painel Iluminação UV")
    proxy_clima = conectar(9003, "Climatizador")

    relatorio = Relatorio(proxy_hidro, proxy_luz, proxy_clima)

    print("─" * 55)

    while True:
        menu_principal()
        opcao = input("  Opção: ").strip()

        if opcao == "1":
            if proxy_hidro:
                menu_hidroponico(proxy_hidro)
            else:
                print("Servidor hidropônico indisponível")

        elif opcao == "2":
            if proxy_luz:
                menu_iluminacao(proxy_luz)
            else:
                print("Servidor de iluminação indisponível")

        elif opcao == "3":
            if proxy_clima:
                menu_climatizador(proxy_clima)
            else:
                print("Servidor climatizador indisponível")

        elif opcao == "4":
            print("\n  Gerando relatório geral")
            print(relatorio.gerar())

        elif opcao == "0":
            print("\n Encerrando estação de controle\n")
            break

        else:
            print("Opção inválida - Tente novamente")


if __name__ == "__main__":
    main()