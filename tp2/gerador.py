import pandas as pd
import random

def geradorDeInstancias():
    matriz = pd.read_excel("distancia entre pontos.xlsx")
    if 'Unnamed: 0' in matriz.columns:
        matriz = matriz.drop(columns=['Unnamed: 0'])

    casasEscolhidas = random.sample(range(1,31), 25)

    # CONJUNTOS
    H = casasEscolhidas
    escola = 0 # escola tá em i = 30 ou j = "ESCOLA"
    Hbar = H + [escola]
    A = A = [(i, j) for i in H for j in Hbar if i != j]
    idades = list(range(6, 11))

    # PARÂMETROS
    alpha = 0
    rho = 5 # quantidade de crianças que o monitor consegue supervisionar
    q = {}
    total_criancas = 0
    for casa in casasEscolhidas:
        q[casa] = {}
        for idade in idades:
            valor = random.randint(0,3)
            q[casa][idade] = valor
            total_criancas += valor
    M = total_criancas
    pk = {6: 2.0, 7: 1.5, 8: 1.5, 9: 1.0, 10: 1.0}
    Si = {}
    linha_escola = matriz.iloc[30]
    for casa in casasEscolhidas:
        Si[casa] = int(linha_escola[casa])
    Deltai = {}
    casas_ordenadas = sorted(Si.items(), key=lambda item: item[1])
    for idx, (casa, distancia) in enumerate(casas_ordenadas):
        if idx < 8:
            delta = 2.0
        elif idx < 17:
            delta = 1.7
        else:
            delta = 1.4
        Deltai[casa] = round(delta * distancia, 2)
    c = {}
    for (i, j) in A:
        coluna_busca = "ESCOLA" if j == escola else j
        linha_busca = 30 if i == escola else i - 1
        c[i,j] = int(matriz.at[linha_busca, coluna_busca])
    d = {}
    for (i, j) in A:
        d[i,j] = round(random.uniform(0.01, 0.3), 2)
    print("Delta: ", Deltai)
    salvar_arquivo_dat("problema_1.dat", H, Hbar, A, idades, c, d, q, pk, rho, Si, Deltai, alpha, M)
    print("Arquivo problema.dat gerado com sucesso!")

def salvar_arquivo_dat(nome_arquivo, H, Hbar, A, idades, cij, dij, qki, pk, rho, Si, Delta, alpha, M):
    with open(nome_arquivo, 'w') as f:
        f.write("data;\n\n") # Início da seção de dados para o GLPK

        # --- CONJUNTOS ---
        f.write(f"set H := {' '.join(map(str, sorted(H)))};\n\n")
        f.write(f"set Hbar := {' '.join(map(str, sorted(Hbar)))};\n\n")
        f.write(f"set I := {' '.join(map(str, sorted(idades)))};\n\n")
        
        f.write("set A := \n")
        for i, j in A:
            f.write(f"  ({i},{j})\n") # GLPK prefere (i,j) para conjuntos de pares
        f.write(";\n\n")

        # --- PARÂMETROS ESCALARES ---
        f.write(f"param rho := {rho};\n")
        f.write(f"param alpha := {alpha};\n")
        f.write(f"param M := {M};\n\n")

        # --- PARÂMETROS VETORIAIS ---
        f.write("param pk := \n")
        for k in sorted(pk.keys()):
            f.write(f"  [{k}] {pk[k]}\n")
        f.write(";\n\n")

        f.write("param Si := \n")
        for i in sorted(H):
            f.write(f"  [{i}] {Si[i]}\n")
        f.write(";\n\n")

        f.write("param Delta := \n")
        for i in sorted(H):
            f.write(f"  [{i}] {round(Delta[i], 2)}\n")
        f.write(";\n\n")

        # --- PARÂMETROS MATRICIAIS (cij e dij) ---
        f.write("param cij := \n")
        for (i, j) in A:
            f.write(f"  [{i},{j}] {cij[i,j]}\n")
        f.write(";\n\n")

        f.write("param dij := \n")
        for (i, j) in A:
            f.write(f"  [{i},{j}] {round(dij[i,j], 2)}\n")
        f.write(";\n\n")

        # --- PARÂMETRO qki {H, I} ---
        f.write("param qki := \n")
        for casa in sorted(H):
            for idade in sorted(idades):
                f.write(f"  [{casa},{idade}] {qki[casa][idade]}\n")
        f.write(";\n\n")
        
        f.write("end;\n") # OBRIGATÓRIO para o GLPK

if __name__ == "__main__":
    geradorDeInstancias()

