import pandas as pd
import random

NUM_INSTANCIAS = 10
ARQUIVO_PLANILHA = "distancia entre pontos.xlsx"
escola = 0
idades = [6,7,8,9,10]

# ===============================
# CARREGAR MATRIZ DE DISTÂNCIAS
# ===============================
df = pd.read_excel(ARQUIVO_PLANILHA, index_col=0)

# Corrigir índices
df.index = [0 if x == "ESCOLA" else int(x) for x in df.index]
df.columns = [0 if x == "ESCOLA" else int(x) for x in df.columns]

for instancia in range(1, NUM_INSTANCIAS + 1):

    # ===============================
    # 1. SELECIONAR 25 CASAS
    # ===============================
    todas_casas = list(range(1,31))
    casas = random.sample(todas_casas, 25)
    casas.sort()

    nos = casas + [escola]
    df_final = df.loc[nos, nos]

    # ===============================
    # 2. CALCULAR S_i
    # ===============================
    S = df_final.loc[casas, escola]

    # ===============================
    # 3. CALCULAR DELTA_i
    # ===============================
    S_ordenado = S.sort_values()

    def fator_delta(rank, total):
        if rank < total/3:
            return 2.0
        elif rank < 2*total/3:
            return 1.7
        else:
            return 1.4

    Delta = {}
    for i, (casa, s_val) in enumerate(S_ordenado.items()):
        Delta[casa] = round(s_val * fator_delta(i, len(casas)), 2)

    # ===============================
    # 4. GERAR q_{ik}
    # ===============================
    q = {}
    for casa in casas:
        for idade in idades:
            q[(casa, idade)] = random.randint(0,3)

    # ===============================
    # 5. GERAR d_{ij}
    # ===============================
    d = {}
    for i in nos:
        for j in nos:
            if i != j:
                d[(i,j)] = round(random.uniform(0.01,0.3),4)

    # ===============================
    # 6. DEFINIR p_k
    # ===============================
    p = {
        6: 2.0,
        7: 1.5,
        8: 1.5,
        9: 1.0,
        10: 1.0
    }

    rho = 5.0

    # ===============================
    # EXPORTAR .dat
    # ===============================
    nome_arquivo = f"instancia_{instancia}.dat"

    with open(nome_arquivo,"w") as f:

        # Conjunto H
        f.write("set H := ")
        f.write(" ".join(str(i) for i in casas))
        f.write(";\n\n")

        # Conjunto I
        f.write("set I := 6 7 8 9 10;\n\n")

        # Conjunto A
        f.write("set A :=\n")
        for i in nos:
            for j in nos:
                if i != j:
                    f.write(f"({i},{j}) ")
        f.write(";\n\n")

        # Param S (incluindo escola)
        f.write("param S :=\n")
        f.write(f"0 0.00\n")                    # ← NÓ 0
        for i in casas:
            f.write(f"{i} {S[i]:.2f}\n")
        f.write(";\n\n")

        # Param Delta (incluindo escola)
        f.write("param Delta :=\n")
        f.write(f"0 0.00\n")                    # ← NÓ 0
        for i in casas:
            f.write(f"{i} {Delta[i]}\n")
        f.write(";\n\n")

        # Param p
        f.write("param p :=\n")
        for k in idades:
            f.write(f"{k} {p[k]}\n")
        f.write(";\n\n")

        # Param q
        f.write("param q :=\n")
        for (i,k), val in q.items():
            f.write(f"{i} {k} {val}\n")
        f.write(";\n\n")

        # Param d
        f.write("param d :=\n")
        for (i,j), val in d.items():
            f.write(f"{i} {j} {val}\n")
        f.write(";\n\n")

        # Param c (distância real)
        f.write("param c :=\n")
        for i in nos:
            for j in nos:
                if i != j:
                    f.write(f"{i} {j} {df_final.loc[i,j]:.2f}\n")
        f.write(";\n\n")

        f.write(f"param rho := {rho};\n")
        f.write("end;\n")

    print(f"Instância {instancia} gerada!")

print("\nTodas as instâncias foram geradas com sucesso!")