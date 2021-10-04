# ----- importando csv ------
df_pca_janeiro <- read.csv('../../app/home/data/treated_data/df_pca_janeiro.csv')

# ----- Transformando index -----
row.names(df_pca_janeiro) <- df_pca_janeiro$Municipio

# ----- manipulacao de quadrantes de cargas fatoriais -----
# rodando a pca com os valores positivos as cargas fatorias se mostraram com a mesma tendencia entre
# casos_novos e recuperados, e entre obitos e repasses, por conta da correlacao positiva.
# vamos manipular o sinal para que tenham pesos em direcoes opostas ao calcularmos o ranking
df_pca_janeiro$CasosNovos_pc <- df_pca_janeiro$CasosNovos_pc*-1
df_pca_janeiro$Obitos_pc <- df_pca_janeiro$Obitos_pc*-1
df_pca_janeiro$RepasseEstadual_pc <- df_pca_janeiro$RepasseEstadual_pc*-1

# ----- Matriz de correlacao -----
#gráfico com representação numérica, linha de tendência e distribuições
chart.Correlation(df_pca_janeiro[6:10], histogram = TRUE, pch = "+")

#salvando matriz
rho_dataframe <- cor(df_pca_janeiro[6:10]) #lembrar se selecionar apenas as colunas numericas

#heatmap - outra opção de visualização
rho_dataframe %>% 
  melt() %>% 
  ggplot() +
  geom_tile(aes(x = Var1, y = Var2, fill = value)) +
  geom_text(aes(x = Var1, y = Var2, label = round(x = value, digits = 3)),
            size = 4) +
  labs(x = NULL,
       y = NULL,
       fill = "Correlações") +
  scale_fill_gradient2(low = "dodgerblue4", 
                       mid = "white", 
                       high = "brown4",
                       midpoint = 0) +
  theme(panel.background = element_rect("white"),
        panel.grid = element_line("grey95"),
        panel.border = element_rect(NA),
        legend.position = "bottom",
        axis.text.x = element_text(angle = 0))

# ----- esfericidade de bartlet -----
cortest.bartlett(R = rho_dataframe)

# ----- rodando pca -----
dataframe_std <- df_pca_janeiro[6:10] %>% 
  scale() %>% 
  data.frame()

# Rodando a PCA
afpc_dataframe <- prcomp(dataframe_std)
summary(afpc_dataframe)


# ----- autovetores -----
#Visualizando os pesos que cada variável tem em cada componente principal 
#obtido pela PCA
ggplotly(
  data.frame(afpc_dataframe$rotation) %>%
    mutate(var = names(df_pca_janeiro[6:10])) %>%
    melt(id.vars = "var") %>%
    mutate(var = factor(var)) %>%
    ggplot(aes(x = var, y = value, fill = var)) +
    geom_bar(stat = "identity", color = "black") +
    facet_wrap(~variable) +
    labs(x = NULL, y = NULL, fill = "Legenda:") +
    scale_fill_viridis_d() +
    theme_bw() +
    theme(axis.text.x = element_text(angle = 90))
)

# ----- selecionando fatores -----
#resolvemos utilizar todos os fatores
#k <- sum((afpc_dataframe$sdev ^ 2) > 1)
k=5
# ----- cargas fatoriais e comunalidades -----
#Cargas Fatoriais
cargas_fatoriais <- afpc_dataframe$rotation[, 1:k] %*% diag(afpc_dataframe$sdev[1:k])

#Ralatorio com comunilidades
data.frame(cargas_fatoriais) %>%
  rename(cargaF1 = X1,
         cargaF2 = X2,
         cargaF3 = X3,
         cargaF4 = X4,
         cargaF5 = X5) %>%
  mutate(Comunalidades = rowSums(cargas_fatoriais ^ 2)) -> cf_comunalidades

#Plotagem Cargas Fatoriais - para visualizacao do estresse do gráfico (fazer apenas se 2 fatores foram escolhidos)
data.frame(cargas_fatoriais) %>%
  ggplot(aes(x = X1, y = X2)) +
  geom_point(color = "orange") +
  geom_hline(yintercept = 0, color = "darkorchid") +
  geom_vline(xintercept = 0, color = "darkorchid") +
  geom_text_repel(label = row.names(cargas_fatoriais)) +
  labs(x = "cargaF1",
       y = "cargaF2") +
  theme_bw()


# ----- socres fatoriais -----
# Scores Fatoriais - TODOS os scores, representados em linhas
scores_fatoriais <- t(afpc_dataframe$rotation)/afpc_dataframe$sdev 
colnames(scores_fatoriais) <- colnames(dataframe_std)

# Scores dos Fatores selecionados, representados em colunas
scores_fatoriais %>%
  t() %>%
  data.frame() %>%
  rename(PC1 = 1,
         PC2 = 2,
         PC3 = 3,
         PC4 = 4,
         PC5 = 5) %>%
  select(PC1, PC2, PC3, PC4, PC5)

# ----- ranking -----
#Assumindo-se apenas o F1 e F2 como indicadores, calculam-se os scores 
#fatorias
score_D1 <- abs(scores_fatoriais[1,])
score_D1

score_D2 <- abs(scores_fatoriais[2,])
score_D2

score_D3 <- abs(scores_fatoriais[3,])
score_D3

score_D4 <- abs(scores_fatoriais[4,])
score_D4

score_D5 <- abs(scores_fatoriais[5,])
score_D5

#Estabelecendo o ranking dos indicadores assumido
F1 <- t(apply(dataframe_std, 1, function(x) x * score_D1))
F2 <- t(apply(dataframe_std, 1, function(x) x * score_D2))
F3 <- t(apply(dataframe_std, 1, function(x) x * score_D3))
F4 <- t(apply(dataframe_std, 1, function(x) x * score_D4))
F5 <- t(apply(dataframe_std, 1, function(x) x * score_D5))

#Na construção de rankings no R, devemos efetuar a multiplicação por -1, 
#visto que os scores fatoriais das observações mais fortes são, por padrão, 
#apresentados acompanhados do sinal de menos.
F1 <- data.frame(F1) %>%
  mutate(fator1 = rowSums(.) * 1)

F2 <- data.frame(F2) %>%
  mutate(fator2 = rowSums(.) * 1)

F3 <- data.frame(F3) %>%
  mutate(fator3 = rowSums(.) * 1)

F4 <- data.frame(F4) %>%
  mutate(fator4 = rowSums(.) * 1)

F5 <- data.frame(F5) %>%
  mutate(fator5 = rowSums(.) * 1)

# ----- novas colunas de fatores adicionadas ao df -----
# Importando as colunas de fatores F1 e F2
df_pca_janeiro["Fator1"] <- F1$fator1
df_pca_janeiro["Fator2"] <- F2$fator2
df_pca_janeiro["Fator3"] <- F3$fator3
df_pca_janeiro["Fator4"] <- F4$fator4
df_pca_janeiro["Fator5"] <- F5$fator5

# ----- criando ranking -----
#Criando um ranking pela soma ponderada dos fatores por sua variância
#compartilhada:

#Calculando a variância compartilhada
var_compartilhada <- (afpc_dataframe$sdev ^ 2/sum(afpc_dataframe$sdev ^ 2))
var_compartilhada

df_pca_janeiro %>%
  mutate(pontuacao = Fator1 * var_compartilhada[1] +
           Fator2 * var_compartilhada[2] +
           Fator3 * var_compartilhada[3] +
           Fator4 * var_compartilhada[4] +
           Fator5 * var_compartilhada[5]) -> df_pca_janeiro

# Visualizando o ranking final
df_pca_janeiro <- df_pca_janeiro %>%
                  arrange(desc(pontuacao))

# ----- salvando em .csv -----
write.csv(df_pca_janeiro,'../../app/home/data/treated_data/ranking_janeiro_21.csv')
