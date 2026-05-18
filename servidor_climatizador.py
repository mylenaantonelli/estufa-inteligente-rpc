from xmlrpc.server import SimpleXMLRPCServer
import datetime

estado = {
    "temperatura_atual"  : 22.0,   
    "temperatura_alvo"   : 22.0,
    "exaustores_abertos" : False,
    "ultima_alteracao"   : None,
    "modo"               : "estável",  
    "total_ajustes"      : 0,
}

def definir_temperatura(graus):
    try:
        graus = float(graus)
    except (ValueError, TypeError):
        return "[CLIMATIZADOR] Valor inválido. Informe a temperatura em graus Celsius."

    if not (10.0 <= graus <= 40.0):
        return ("[CLIMATIZADOR] Temperatura fora da faixa segura (10°C a 40°C). "
                "Operação cancelada para proteger as plantas.")

    anterior = estado["temperatura_alvo"]
    estado["temperatura_alvo"]  = graus
    estado["ultima_alteracao"]  = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    estado["total_ajustes"]    += 1

    if graus > anterior:
        estado["modo"] = "aquecendo"
        seta = "↑"
    elif graus < anterior:
        estado["modo"] = "resfriando"
        seta = "↓"
    else:
        estado["modo"] = "estável"
        seta = "→"


    if 18.0 <= graus <= 28.0:
        mensagem = "Dentro da faixa ideal"
    elif graus < 18.0:
        mensagem = "Temperatura baixa"
    else:
        mensagem = "Temperatura alta"

    return (f"[CLIMATIZADOR] {seta} Temperatura-alvo definida: {graus:.1f}°C "
            f"(anterior: {anterior:.1f}°C) | {mensagem}")


def abrir_exaustores():
    if estado["exaustores_abertos"]:
        return "[CLIMATIZADOR] Exaustores já estão abertos - Nenhuma ação necessária."

    estado["exaustores_abertos"] = True
    estado["ultima_alteracao"]   = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    estado["modo"]               = "ventilando"
    estado["total_ajustes"]     += 1

    return ("[CLIMATIZADOR] Exaustores Abertos "
            "Ventilação forçada ativada")


def fechar_exaustores():
    if not estado["exaustores_abertos"]:
        return "[CLIMATIZADOR] Exaustores já estão fechados"

    estado["exaustores_abertos"] = False
    estado["ultima_alteracao"]   = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    estado["modo"]               = "estável"

    return "[CLIMATIZADOR] Exaustores Fechados - Ventilação desativada"


def gerar_relatorio():
    return {
        "setor"               : "Climatizador",
        "temperatura_alvo"    : f"{estado['temperatura_alvo']:.1f}°C",
        "temperatura_atual"   : f"{estado['temperatura_atual']:.1f}°C",
        "modo"                : estado["modo"].upper(),
        "exaustores"          : "Abertos" if estado["exaustores_abertos"] else "Fechados",
        "ultima_alteracao"    : estado["ultima_alteracao"] or "Nenhuma até agora",
        "total_ajustes"       : str(estado["total_ajustes"]),
    }


servidor = SimpleXMLRPCServer(("localhost", 9003))
servidor.register_function(definir_temperatura)
servidor.register_function(abrir_exaustores)
servidor.register_function(fechar_exaustores)
servidor.register_function(gerar_relatorio)
servidor.register_introspection_functions()

print("=" * 55)
print("  Climatizador - Servidor RPC iniciado")
print("  Endereço: localhost | Porta: 9003")
print("  Aguardando conexões do cliente controlador")
print("=" * 55)

servidor.serve_forever()