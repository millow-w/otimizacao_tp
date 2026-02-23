# --- CONJUNTOS ---
set H; # Conjunto de casas
set H_bar := H union {0}; # Casas + Escola (nó 0)
set A within (H_bar cross H_bar); # Arestas/Caminhos
set I; # Idades das crianças

# --- PARÂMETROS ---
param d{A};         # Qualidade do caminho
param q{H, I};      # Qtd de crianças de idade k na casa i
param p{I};         # Nível de atenção por idade
param rho;          # Capacidade do monitor (ex: 5.0)
param S{H};         # Distância direta casa-escola
param Delta{H};     # Distância máxima permitida
param c{A};         # Distância entre i e j
param alpha := 0; # Peso da segurança (critério desempate)
param M := sum{i in H, k in I} q[i,k];    # Valor total de crianças

# --- VARIÁVEIS ---
var z{H} integer, >= 0;          # Monitores que começam em i
var y{A} binary;                 # Arco (i,j) é usado?
var theta >= 0;                  # Caminho mais longo (para objetivo 2)
var w{A, I} integer, >= 0;       # Crianças de idade k no arco (i,j)
var x{A} integer, >= 0;          # Monitores no arco (i,j)
var pi{H_bar} >= 0;              # Distância acumulada até a escola

# --- FUNÇÃO OBJETIVO (Exemplo: Minimizar Monitores) ---
minimize obj1: sum{i in H} z[i] + alpha * sum{(i,j) in A} d[i,j] * y[i,j];

# --- RESTRIÇÕES ---

# (3) Continuidade das crianças
s.t. R3{i in H, k in I}:
    -sum{(j,i) in A} w[j,i,k] + sum{(i,j) in A} w[i,j,k] = q[i,k];

# (4) Continuidade dos monitores
s.t. R4{i in H}:
    -sum{(j,i) in A} x[j,i] + sum{(i,j) in A} x[i,j] = z[i];

# (5) Capacidade de supervisão
s.t. R5{(i,j) in A}:
    sum{k in I} p[k] * w[i,j,k] - rho * x[i,j] <= 0;

# (6, 7, 8) Ativação de arcos e segurança
s.t. R6{(i,j) in A}: y[i,j] - sum{k in I} w[i,j,k] <= 0;
s.t. R7{(i,j) in A}: y[i,j] - x[i,j] <= 0;
s.t. R8{(i,j) in A}: x[i,j] - M * y[i,j] <= 0;

# (9) Todos os nós visitados
s.t. R9{i in H}: sum{(i,j) in A} y[i,j] = 1;

# (10, 11) Distâncias e maior trajeto
  s.t. R10{i in H}: pi[i] <= Delta[i];
  s.t. R11{i in H}: pi[i] <= theta;

# (12) Cálculo da distância (MTZ adaptado)
# s.t. R12{(i,j) in A: i != 0}:
   # pi[j] - pi[i] + (Delta[j] - S[i] + c[i,j]) * y[i,j] 
   # + (Delta[j] - S[i] - c[j,i]) * y[j,i] <= Delta[j] - S[i];

# (13) Garantia de visita ou início de monitor
s.t. R13{i in H}:
    sum{(j,i) in A} y[j,i] + z[i] >= 1;

# (14) Impede monitor novo se a casa já for visitada
s.t. R14{i in H, (j,i) in A}: 
    z[i] <= M * (1 - y[j,i]);

# Distãncia da escola
s.t. Escola: pi[0] = 0;

solve;

display sum{i in H} z[i], theta;
end;