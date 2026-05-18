from xmlrpc.server import SimpleXMLRPCServer
import datetime

estado = {
    "nivel_agua"       : 85.0,   
    "irrigacao_ativa"  : False,
    "tempo_irrigacao"  : 0,
    "ultima_irrigacao" : None,
    "total_irrigacoes" : 0,
}


def ativar_irrigacao(tempo):
    if tempo <= 0:
        return "[HIDROPÔNICO] Tempo inválido. Informe um valor positivo."

    estado["irrigacao_ativa"]   = True
    estado["tempo_irrigacao"]   = tempo
    estado["ultima_irrigacao"]  = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    estado["total_irrigacoes"] += 1
    consumo = tempo * 0.5
    estado["nivel_agua"] = max(0.0, estado["nivel_agua"] - consumo)

    return (f"[HIDROPÔNICO] Irrigação ativada por {tempo}s. "
            f"Consumo: {consumo:.1f}%. "
            f"Nível atual: {estado['nivel_agua']:.1f}%")


def checar_nivel_agua():
    nivel = estado["nivel_agua"]

    if nivel > 70:
        status = "Normal"
    elif nivel > 30:
        status = "Atenção - é preciso reabastecer"
    else:
        status = "Crítico - é preciso reabastecer urgentemente"

    return (f"[HIDROPÔNICO] Nível de água: {nivel:.1f}% | {status}")


def gerar_relatorio():
    nivel = estado["nivel_agua"]
    if nivel > 70:
        status_agua = "Normal"
    elif nivel > 30:
        status_agua = "Atenção"
    else:
        status_agua = "Crítico"

    return {
        "setor"             : "Setor Hidropônico",
        "nivel_agua"        : f"{nivel:.1f}%",
        "status_agua"       : status_agua,
        "irrigacao_ativa"   : "Sim" if estado["irrigacao_ativa"] else "Não",
        "ultima_irrigacao"  : estado["ultima_irrigacao"] or "Nenhuma até agora",
        "total_irrigacoes"  : str(estado["total_irrigacoes"]),
    }


servidor = SimpleXMLRPCServer(("localhost", 9001))
servidor.register_function(ativar_irrigacao)
servidor.register_function(checar_nivel_agua)
servidor.register_function(gerar_relatorio)
servidor.register_introspection_functions()  

print("=" * 55)
print("  Setor Hidropônico - Servidor RPC iniciado")
print("  Endereço: localhost | Porta: 9001")
print("  Aguardando conexões do cliente controlador")
print("=" * 55)

servidor.serve_forever()