import re
import matplotlib.pyplot as plt

monitores = {}

with open("resultado.txt") as f:
    for line in f:
        if "z[" in line:
            parts = line.split()
            
            # formato esperado:
            # [No., z[2], *, 2, 0]
            if len(parts) >= 4:
                nome = parts[1]
                valor = int(parts[3])   # <-- coluna Activity
                
                if valor > 0:
                    match = re.search(r'z\[(\d+)\]', nome)
                    if match:
                        node = int(match.group(1))
                        monitores[node] = valor

print("Monitores encontrados:", monitores)

# Plot simples
if monitores:
    plt.figure()
    x = list(monitores.keys())
    y = list(monitores.values())
    plt.bar(x, y)
    plt.xlabel("Nó")
    plt.ylabel("Quantidade de Monitores")
    plt.title("Distribuição mínima de monitores")
    plt.show()
else:
    print("Nenhum monitor encontrado.")