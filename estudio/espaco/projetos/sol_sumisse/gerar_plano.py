"""Gera o plano.json de "E se o Sol sumisse?" a partir dos tempos da fala (linhas.json).

Rode de novo sempre que a voz mudar (voz-guia ou voz final):
    python3 estudio/espaco/projetos/sol_sumisse/gerar_plano.py

Por que um gerador: a Terra anda na órbita por movimentos encadeados (pontos fixos do círculo),
o que deixa o ponto de saída e a reta tangente exatos. Os instantes desses pontos dependem
dos tempos de cada palavra, que mudam quando a voz final entra.
"""
import json, math, os, re

AQUI = os.path.dirname(os.path.abspath(__file__))
LIN = json.load(open(os.path.join(AQUI, "linhas.json")))
FALAS = {l["id"]: l for l in LIN["linhas"]}
TOTAL = LIN["total"]
CAUDA = 1.7


def sem_acento(s):
    import unicodedata
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def T(ref):
    """mesmo formato de tempo do estúdio: "A1", "A1.fim", "A1.2", "A1:palavra", "A1:palavra.fim", com +/- segundos"""
    m = re.match(r"^(.+?)([+-]\d+(?:\.\d+)?)?$", ref)
    base, off = m.group(1), float(m.group(2) or 0)
    fim = base.endswith(".fim")
    if fim:
        base = base[:-4]
    if ":" in base:
        fid, w = base.split(":")
        pals = [p for pc in FALAS[fid]["pedacos"] for p in pc["palavras"]]
        for p in pals:
            if sem_acento(re.sub(r"[^\w-]", "", p["t"])).startswith(sem_acento(w)):
                return (p["t1"] if fim else p["t0"]) + off
        raise KeyError(ref)
    if "." in base:
        fid, k = base.split(".")
        pc = FALAS[fid]["pedacos"][int(k) - 1]
        return (pc["t1"] if fim else pc["t0"]) + off
    return (FALAS[base]["t1"] if fim else FALAS[base]["t0"]) + off


# ---------------------------------------------------------------- geometria (escala de diagrama, fora de escala)
R = 10.0                 # raio da órbita da Terra
A0, AC = -112.0, -68.0   # ângulo da Terra no começo e na chegada da última luz (graus)


def P(a):
    r = math.radians(a)
    return [round(R * math.cos(r), 4), 0.0, round(R * math.sin(r), 4)]


def TAN(a):  # direção do movimento (ângulo crescente)
    r = math.radians(a)
    return [-math.sin(r), 0.0, math.cos(r)]


def soma(p, d, k):
    return [round(p[i] + d[i] * k, 4) for i in range(3)]


tS = T("A1:sumisse")          # o Sol some
tF0 = T("B1:sairia")          # versão de filme: a Terra dispara
tF1 = min(tF0 + 1.1, T("B1.fim") - 0.05)
tB2 = T("B1.fim") + 0.05       # rebobina na pausa antes do "Mas"
tR1 = T("B2") + 0.25
tC = T("C1:chega")            # a última luz e a gravidade chegam juntas
PAUSA = tR1 - tF0             # o tempo do "filme" não conta para a órbita nem para a luz
tCe = tC - PAUSA
OMEGA = (AC - A0) / tCe       # graus por segundo de vídeo
V = R * math.radians(OMEGA)   # a mesma velocidade na reta (não acelera ao sair)
tFIM = TOTAL + CAUDA + 2.0


def ang(t):
    te = t if t < tF0 else (tF0 if t < tR1 else t - PAUSA)
    return A0 + (AC - A0) * te / tCe


AF = ang(tF0)


def arco(t0, t1, passo=0.7):
    n = max(1, round((t1 - t0) / passo))
    out = []
    for k in range(1, n + 1):
        a, b = t0 + (t1 - t0) * (k - 1) / n, t0 + (t1 - t0) * k / n
        out.append({"de": round(a, 3), "ate": round(b, 3), "para": P(ang(b if b < tF0 or b >= tR1 else tF0)), "curva": "linear"})
    return out


movs = arco(0.0, tF0)
movs.append({"de": round(tF0, 3), "ate": round(tF1, 3), "para": soma(P(AF), TAN(AF), 9.0), "curva": "parte"})
movs.append({"de": round(tB2, 3), "ate": round(tR1, 3), "para": P(AF), "curva": "suave"})
movs += arco(tR1, tC)
movs.append({"de": round(tC, 3), "ate": round(tFIM, 3), "para": soma(P(AC), TAN(AC), V * (tFIM - tC)), "curva": "linear"})

L_SETA = 6.0
seta_de, seta_para = P(AC), soma(P(AC), TAN(AC), L_SETA)


def cam(enq, ocupa, az, el, mm=35):
    return {"enquadrar": enq, "ocupa": ocupa, "az": az, "el": el, "mm": mm, "so_altura": True}


def escuro(az, el):
    """luz por trás do planeta (o lado que a câmera vê fica no escuro): não dá para desligar a luz no estúdio"""
    a, e = math.radians(az), math.radians(el)
    return [round(-math.sin(a) * math.cos(e), 4), round(-math.sin(e), 4), round(-math.cos(a) * math.cos(e), 4)]


SOL = {"de": "sol"}


def terra_em(t):
    """posição da Terra no instante t (mesma agenda dos movimentos)"""
    if t < tF0:
        return P(ang(t))
    if t < tR1:
        return P(AF)
    if t < tC:
        return P(ang(t))
    return soma(P(AC), TAN(AC), V * (t - tC))


def eixo(t, extra=0.0):
    """az da câmera que deixa o lugar do Sol embaixo e a Terra em cima na tela"""
    x, _, z = terra_em(t)
    return round(math.degrees(math.atan2(-x, -z)) + extra, 2)


ORDEM = ["inicio", "A2", "B1", "B2", "B3", "C1", "C1:chega+0.05", "C2", "C3", "D1", "D2", "D3", "Q1"]
FIM_V = TOTAL + CAUDA


def tt(ref):
    return 0.0 if ref == "inicio" else T(ref)


# (de, novo, heroi, enquadrar, ocupa_de, ocupa_para, el_de, el_para, compo_y, giro extra em graus)
ROT = [
    ("inicio", "o Sol embaixo, a Terra e a Lua em cima, a luz entre os dois", "terra", ["sol", "terra"], 0.62, 0.64, 74, 72, 0.36, 0),
    ("A2", "o Sol sumiu: a última luz sobe do lugar vazio até a Terra", "terra", ["sol", "terra"], 0.64, 0.66, 72, 70, 0.36, 0),
    ("B1", "a versão de filme: a Terra dispara na hora", None, ["sol", "terra"], 0.66, 0.64, 70, 72, 0.38, 0),
    ("B2", "rebobina: a gravidade sai do lugar vazio junto com a luz", None, ["sol", "terra"], 0.64, 0.64, 72, 74, 0.38, 0),
    ("B3", "a Terra continua girando em volta do lugar vazio", None, ["vazio", "terra"], 0.64, 0.62, 74, 74, 0.38, 0),
    ("C1", "a última luz chegando na Terra", "terra", ["terra", "lua"], 0.5, 0.47, 70, 68, 0.33, 0),
    ("C1:chega+0.05", "o céu fica preto: a Terra apaga", "terra", ["terra", "lua"], 0.47, 0.48, 68, 66, 0.33, 4),
    ("C2", "a Lua, que ainda brilhava, apaga também", "lua", ["terra", "lua"], 0.48, 0.5, 66, 64, 0.33, 8),
    ("C3", "a Terra sai em linha reta, tangente à órbita", "terra", ["terra", "reta"], 0.68, 0.7, 70, 68, 0.36, 0),
    ("D1", "o gelo começa a cobrir a Terra", "terra", ["terra"], 0.4, 0.43, 62, 58, 0.36, 6),
    ("D2", "o gelo fica mais grosso: o mar congela por cima", "terra", ["terra"], 0.43, 0.46, 58, 54, 0.36, 14),
    ("D3", "por baixo do gelo, a água ainda líquida acende", "terra", ["terra"], 0.44, 0.42, 54, 50, 0.34, 22),
    ("Q1", "a Terra no escuro, longe do lugar vazio; a câmera continua recuando", "terra", ["terra", "vazio"], 0.42, 0.7, 52, 64, 0.36, 0),
]
planos = []
az_ant = None
for i, (de, novo, heroi, enq, oc0, oc1, el0, el1, cy, giro) in enumerate(ROT):
    t0 = tt(de)
    t1 = tt(ROT[i + 1][0]) if i + 1 < len(ROT) else FIM_V
    az1 = eixo((t0 + t1) / 2 if de != "B1" else tF0, giro)
    if de == "Q1":
        az1 = eixo(FIM_V)
    az0 = az_ant if az_ant is not None else eixo(t0)
    pl = {"de": de, "novo": novo, "longo": True, "compo": {"x": 0.46, "y": cy}, "luz": SOL,
          "camera": {"de": cam(enq, oc0, az0, el0), "para": cam(enq, oc1, az1, el1), "curva": "meio" if de == "Q1" else "suave"}}
    if i > 0:
        pl["continuo"] = True
    if heroi:
        pl["heroi"] = heroi
    planos.append(pl)
    az_ant = az1

objetos = {
    "sol": {"corpo": "estrelaG", "pos": [0, 0, 0], "raio": 2.0, "halo": 2.6, "sai": "direto",
            "mostrar": [["inicio", "A1:sumisse"]], "fundo": True},
    "terra": {"corpo": "terra", "pos": P(A0), "raio": 1.3, "movimentos": movs},
    "lua": {"corpo": "lua", "raio": 0.36, "orbita": {"em": "terra", "raio": 2.4, "periodo": 16, "fase": 0.35}},
    "luar": {"tipo": "brilho", "em": "lua", "raio": 0.95, "cor": "#FFF1D2", "opacidade": 0.45,
             "mostrar": [["inicio", "C2:apaga"]], "fundo": True},
    "orbita": {"tipo": "orbita", "em": [0, 0, 0], "raio": R, "tracejada": True, "destaque": True, "opacidade": 0.6, "fundo": True},
    "vazio": {"tipo": "orbita", "em": [0, 0, 0], "raio": 2.0, "tracejada": True, "cor": "#9FB3E6", "opacidade": 0.85,
              "entra": "cresce", "mostrar": [["B3:nada-0.3", None]], "fundo": True},
    "reta": {"tipo": "seta", "pos": soma(seta_de, TAN(AC), L_SETA / 2), "raio": L_SETA / 2, "de": seta_de, "para": seta_para,
             "largura": 0.12, "cor": "#FFD166", "desenha": ["C3:linha", "C3:linha+0.9"], "mostrar": [["C3:linha-0.05", "D1"]]},
    "fundo": {"tipo": "oceano", "em": "terra", "raio": 1.39, "opacidade": 0.55, "entra": "cresce",
              "realce": [{"de": "D3.3", "ate": "D3.3+0.3", "para": 0.7}, {"de": "D3.fim", "ate": "D3.fim+0.6", "para": 0.35}],
              "mostrar": [["D3.3-0.05", None]]},
    "gelo": {"tipo": "casca", "em": "terra", "raio": 1.48, "cor": "#EAF6FF", "opacidade": 0.5, "entra": "cresce",
             "escala": [{"de": "D2:ano", "ate": "D2.fim", "para": 1.06}], "mostrar": [["D1:semana", None]]},
}

eventos = [
    {"tipo": "clarao", "em": "A1:sumisse", "alvo": "sol", "forca": 0.55, "dur": 0.6},
    {"tipo": "som", "em": "A1:sumisse", "nota": "grave"},
    {"tipo": "som", "em": "B1", "nota": "plim"},
    {"tipo": "rebobinar", "em": "B1.fim+0.05", "ate": "B2+0.25"},
    {"tipo": "som", "em": "C1:chega", "nota": "grave"},
    {"tipo": "som", "em": "D1", "nota": "plim"},
    {"tipo": "som", "em": "D3", "nota": "plim"},
    {"tipo": "som", "em": "Q1", "nota": "plim"},
]

plano = {
    "titulo": "E se o Sol sumisse?",
    "estilo": "vivo",
    "cauda": CAUDA,
    "luz": SOL,
    "extra": "extra.js",
    "frente": {  # lido pelo extra.js: a última luz e a onda da gravidade andam juntas
        "R": R, "chegada": P(AC),
        "t": {"some": "A1:sumisse", "voo": "B1:sairia", "volta": "B2+0.25", "grav": "B2+0.25", "chega": "C1:chega", "lua": "C2:apaga"},
    },
    "objetos": objetos,
    "planos": planos,
    "eventos": eventos,
}
json.dump(plano, open(os.path.join(AQUI, "plano.json"), "w"), ensure_ascii=False, indent=1)
print(f"plano.json: {len(movs)} movimentos da Terra, órbita de {A0:.0f}° a {AC:.0f}°, "
      f"{OMEGA:.2f}°/s, {V:.3f} u/s na reta; luz chega em {tC:.2f} s; vídeo {TOTAL + CAUDA:.1f} s")
