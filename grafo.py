import re
import math
import networkx as nx
import matplotlib.pyplot as plt

# =========================
# 1) LER ARQUIVO .out
# =========================
with open("solucao_2_f1.out", "r", encoding="utf-8") as f:
    texto = f.read()

# =========================
# 2) EXTRAIR ARCOS (y[i,j]=1) E VALORES (z[i])
# =========================
arcos = []
valores_z = {}

# Padrão para y[i,j] = 1
# Captura o valor na coluna de "Activity" (o primeiro número após o *)
for match in re.finditer(r"y\[(\d+),(\d+)\]\s+\*\s+(\d+)", texto):
    if int(match.group(3)) == 1:
        arcos.append((int(match.group(1)), int(match.group(2))))

# Padrão para z[i]
# Captura o índice i e o valor da variável z
for match in re.finditer(r"z\[(\d+)\]\s+\*\s+(\d+)", texto):
    idx_i = int(match.group(1))
    valor_z = int(match.group(2))
    valores_z[idx_i] = valor_z

# =========================
# 3) DEFINIR GRAFO E LAYOUT
# =========================
H = sorted(set(i for i, j in arcos) | set(j for i, j in arcos if j != 0))
escola = 0
Hbar = H + [escola]

G = nx.DiGraph()
G.add_nodes_from(Hbar)
G.add_edges_from(arcos)

# Layout Radial
pos = {0: (0, 0)}
N = len(H)
raio = 8 # Aumentado para dar espaço aos labels
for k, casa in enumerate(H):
    ang = 2 * math.pi * k / N
    pos[casa] = (raio * math.cos(ang), raio * math.sin(ang))

# =========================
# 4) DESENHAR
# =========================
plt.figure(figsize=(10, 10))

# Desenha arestas e nós
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, alpha=0.6)
nx.draw_networkx_nodes(G, pos, nodelist=[0], node_color='royalblue', node_size=1200)
nx.draw_networkx_nodes(G, pos, nodelist=H, node_color='orange', node_size=900)

# Label DENTRO do nó (o índice i)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', 
                        font_color='black')

# Label ACIMA do nó (o valor de z[i])
for i in H:
    if i in valores_z:
        x, y = pos[i]
        plt.text(x, y + 0.8, s=str(valores_z[i]), 
                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'),
                 horizontalalignment='center', fontsize=11, fontweight='bold', color='red')

plt.title("Solução Ótima com Valores de z[i]")
plt.axis("off")
plt.show()