from xmlrpc.server import SimpleXMLRPCServer
import datetime

ESPECTROS_VALIDOS = {
    "vermelho"  : "Estimula floração e frutificação",
    "azul"      : "Favorece crescimento vegetativo",
    "branco"    : "Espectro completo para uso geral",
    "uv"        : "Ativa defesas naturais das plantas",
    "infravermelho": "Estimula alongamento dos caules",
}

estado = {
    "intensidade"      : 70,       
    "espectro_atual"   : "branco",
    "ligado"           : True,
    "ultima_alteracao" : None,
    "historico"        : [],
}

def ajustar_intensidade(valor):
    try:
        valor = int(valor)
    except (ValueError, TypeError):
        return "[ILUMINAÇÃO] Valor inválido. Use um número inteiro de 0 a 100."

    if not (0 <= valor <= 100):
        return "[ILUMINAÇÃO] Intensidade deve estar entre 0 e 100."

    estado["intensidade"]      = valor
    estado["ligado"]           = valor > 0
    estado["ultima_alteracao"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    estado["historico"].append(f"Intensidade → {valor}% em {estado['ultima_alteracao']}")

    if valor == 0:
        msg = "Painel desligado (intensidade = 0%)"
    elif valor < 30:
        msg = f"Intensidade baixa: {valor}%"
    elif valor < 70:
        msg = f"Intensidade moderada: {valor}%"
    else:
        msg = f"Intensidade alta: {valor}%"

    return f"[ILUMINAÇÃO] {msg}"


def mudar_espectro(cor):
    cor = cor.strip().lower()

    if cor not in ESPECTROS_VALIDOS:
        opcoes = ", ".join(ESPECTROS_VALIDOS.keys())
        return f"[ILUMINAÇÃO] Espectro '{cor}' inválido. Opções: {opcoes}"

    estado["espectro_atual"]   = cor
    estado["ultima_alteracao"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    estado["historico"].append(f"Espectro → {cor} em {estado['ultima_alteracao']}")

    efeito = ESPECTROS_VALIDOS[cor]
    return (f"[ILUMINAÇÃO] Espectro alterado para '{cor.upper()}'. "
            f"Efeito: {efeito}")


def gerar_relatorio():
    return {
        "setor"            : "Painel de Iluminação UV",
        "intensidade"      : f"{estado['intensidade']}%",
        "espectro"         : estado["espectro_atual"].upper(),
        "status"           : "Ligado" if estado["ligado"] else "Desligado",
        "ultima_alteracao" : estado["ultima_alteracao"] or "Nenhuma até agora",
        "total_ajustes"    : str(len(estado["historico"])),
    }


servidor = SimpleXMLRPCServer(("localhost", 9002))
servidor.register_function(ajustar_intensidade)
servidor.register_function(mudar_espectro)
servidor.register_function(gerar_relatorio)
servidor.register_introspection_functions()

print("=" * 55)
print("  Painel de Iluminação UV - Servidor RPC iniciado")
print("  Endereço: localhost | Porta: 9002")
print("  Aguardando conexões do cliente controlador")
print("=" * 55)

servidor.serve_forever()