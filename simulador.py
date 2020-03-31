
## Efeito do transporte

## Simulação epidemologica usando o modelo SIR espacialmente explicito para analisar o efeito
## do deslocamento sobre o espalhamento da doença.

# Esta simulação é uma adaptação do modelo proposto em  ## https://lexparsimon.github.io/coronavirus/

## Os dados para esta simulaçao foram retirados da pesquisa de origem e destino feita pelo Metro de SP em 2017
## para acessar os dados completos acessar http://www.metro.sp.gov.br/pesquisa-od/

import numpy as np
import pandas as pd


# Iniciar o vetor com a população de cada uma das  517 zonas analizadas
censo = pd.read_excel('data/Pesquisa-Origem-Destino-2017-Banco-Dados/OD 2017/Tabelas Gerais/Dados Gerais OD2017.xlsx',
                  sheet_name= "Tabela 2", skiprows = 8, nrows = 517, dtype= "int", header=None)

censo_np= np.array(censo)


N_k = censo_np[:,12]
 # numero de localizacáo



# Para facilitar vou deleter pop =0

idx= np.where(N_k==0)
N_k=np.delete(N_k,idx)

locs_len = len(N_k)

#importar origem destino
OD_raw = pd.read_excel('data/Pesquisa-Origem-Destino-2017-Banco-Dados/OD 2017/Tabelas Gerais/Tab24_OD2017.xlsx',
                   sheet_name="Tabela 24", skiprows=8, nrows=517, dtype="int", header=None)
OD= np.array(OD_raw)[:,range(1,518)]


# deletar as zonas 0

OD=np.delete(OD, idx, axis=0)
OD=np.delete(OD, idx, axis=1)


SIR = np.zeros(shape=(locs_len, 3))  # Montar array com 3 colunas para  grupos S  I R
SIR[:, 0] = N_k  # Iniciar o gruopo S  com as populacoes
np.random.seed(seed=100)

n, p = 1, .01  #  Sorteio de lugares para comecar as infecçoes
first_infections= np.random.binomial(n, p, locs_len)

SIR[:, 0] = SIR[:, 0] - (first_infections*10)
SIR[:, 1] = SIR[:, 1] + (first_infections*10)  # move infections to the I group

# row normalize the SIR matrix for keeping track of group proportions
row_sums = SIR.sum(axis=1)
SIR_n = SIR / row_sums[:, np.newaxis]

# initialize parameters
beta = 1.6
gamma = 0.04
public_trans = 1# alpha
R0 = beta / gamma
beta_vec = np.random.gamma(1.6, 2, locs_len)
gamma_vec = np.full(locs_len, gamma)
public_trans_vec = np.full(locs_len, public_trans)

# make copy of the SIR matrices
SIR_sim = SIR.copy()
SIR_nsim = SIR_n.copy()

# run model
print(SIR_sim.sum(axis=0).sum() == N_k.sum())
from tqdm import tqdm

infected_pop_norm = []
susceptible_pop_norm = []
recovered_pop_norm = []
for time_step in tqdm(range(100)):
    infected_mat = np.array([SIR_nsim[:, 1], ] * locs_len).transpose()
    OD_infected = np.round(OD * infected_mat)
    inflow_infected = OD_infected.sum(axis=0)
    inflow_infected = np.round(inflow_infected * public_trans_vec)
    print('total infected inflow: ', inflow_infected.sum())
    new_infect = beta_vec * SIR_sim[:, 0] * inflow_infected / (N_k + OD.sum(axis=0))
    new_recovered = gamma_vec * SIR_sim[:, 1]
    new_infect = np.where(new_infect > SIR_sim[:, 0], SIR_sim[:, 0], new_infect)
    SIR_sim[:, 0] = SIR_sim[:, 0] - new_infect
    SIR_sim[:, 1] = SIR_sim[:, 1] + new_infect - new_recovered
    SIR_sim[:, 2] = SIR_sim[:, 2] + new_recovered
    SIR_sim = np.where(SIR_sim < 0, 0, SIR_sim)

    # recompute the normalized SIR matrix
    row_sums = SIR_sim.sum(axis=1)
    SIR_nsim = SIR_sim / row_sums[:, np.newaxis]
    S = SIR_sim[:, 0].sum() / N_k.sum()
    I = SIR_sim[:, 1].sum() / N_k.sum()
    R = SIR_sim[:, 2].sum() / N_k.sum()
    print(S, I, R, (S + I + R) * N_k.sum(), N_k.sum())
    print('\n')
    infected_pop_norm.append(I)
    susceptible_pop_norm.append(S)
    recovered_pop_norm.append(R)

results=np.column_stack((susceptible_pop_norm,infected_pop_norm, recovered_pop_norm))

np.savetxt("results/alpha1.csv", results, delimiter=",")