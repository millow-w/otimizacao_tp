# ----------------------------
# CONJUNTOS
# ----------------------------

set H;                     # casas (1..nt)
set Hbar;                  # H unido com escola (inclui 0)
set A within {Hbar, Hbar}; # arcos (i,j)
set I;                     # idades

# ----------------------------
# PARÂMETROS
# ----------------------------

param dij{A};              # qualidade do arco
param cij{A};              # distância do arco
param qki{H,I} >= 0;       # nº crianças idade k no nó i
param pk{I} >= 0;          # nível de atenção por idade
param rho >= 0;            # capacidade monitor
param Si{H} >= 0;          # distância direta escola-i
param Delta{H} >= 0;       # limite máximo caminhada
param alpha >= 0;          
param M >= 0;

# ----------------------------
# VARIÁVEIS
# ----------------------------

var z{i in H} integer >= 0;               # monitores que começam em i
var y{(i,j) in A} binary;                 # arco utilizado
var theta >= 0;                           # maior distância
var w{(i,j) in A, k in I} integer >= 0;   # fluxo crianças
var x{(i,j) in A} integer >= 0;           # fluxo monitores
var pi{i in H} >= 0;                      # distância até escola

# ----------------------------
# FUNÇÃO OBJETIVO (f1)
# ----------------------------

minimize f1:
    sum{i in H} z[i]
  + alpha * sum{(i,j) in A} dij[i,j] * y[i,j];

# (3) conservação fluxo crianças
subject to fluxo_criancas{i in H, k in I}:
    - sum{(j,i) in A} w[j,i,k]
    + sum{(i,j) in A} w[i,j,k]
    = qki[i,k];

# (4) conservação fluxo monitores
subject to fluxo_monitores{i in H}:
    - sum{(j,i) in A} x[j,i]
    + sum{(i,j) in A} x[i,j]
    = z[i];

# (5) capacidade monitor
subject to capacidade{(i,j) in A}:
    sum{k in I} pk[k] * w[i,j,k] <= rho * x[i,j];

# (6) ativação por fluxo criança
subject to ativacao1{(i,j) in A}:
    y[i,j] - sum{k in I} w[i,j,k] <= 0;

# (7) ativação por monitor
subject to ativacao2{(i,j) in A}:
    y[i,j] - x[i,j] <= 0;

# (8) big-M
subject to bigM{(i,j) in A}:
    x[i,j] - M * y[i,j] <= 0;

# (9) estrutura de árvore
subject to visita{i in H}:
    sum{(i,j) in A} y[i,j] = 1;

# (10) limite distância
subject to limite_dist{i in H}:
    pi[i] <= Delta[i];

# (11) definição theta
subject to define_theta{i in H}:
    pi[i] <= theta;

# (12) cálculo distância acumulada
subject to distancia{(i,j) in A: i != 0}:
    pi[j] - pi[i]
    + (Delta[j] - Si[i] + cij[i,j]) * y[i,j]
    + (Delta[j] - Si[i] - cij[j,i]) * y[j,i]
    <= Delta[j] - Si[i];

# (13) início de rota
subject to inicio_rota{i in H}:
    sum{(j,i) in A} y[j,i] + z[i] >= 1;

# (14) folha
subject to folha{(j,i) in A}:
    z[i] - M * (1 - y[j,i]) <= 0;

end;