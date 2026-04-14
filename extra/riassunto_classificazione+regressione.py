# Leggi CSV

import pandas as pd
df = pd.read_csv("hurdle_weather.csv")


# Stampiamo informazioni sul dataset

df.info()
df.isna().sum()
df['target_column'].hist()


# Dividiamo 'X' e 'y'

target_column = "RainfallTomorrow"

y = df[target_column]
X = df.drop(columns=[target_column])
X = X.drop(columns=['User_ID'])

# Conversione di colonne da stringhe (object) a numeri, se necessario

# matrice di correlazione (chiedi a gemini/chatgpt)

import matplotlib.pyplot as plt
import numpy as np

# 2. Calcolo della matrice di correlazione
corr = X.corr()

# 3. Creazione del grafico con Matplotlib
fig, ax = plt.subplots(figsize=(8, 6))

# Visualizza la matrice come immagine
im = ax.imshow(corr, cmap='RdBu_r', vmin=-1, vmax=1)

# Aggiunge la barra laterale (legenda colori)
plt.colorbar(im)

# Imposta le etichette per gli assi
ax.set_xticks(np.arange(len(corr.columns)))
ax.set_yticks(np.arange(len(corr.columns)))
ax.set_xticklabels(corr.columns)
ax.set_yticklabels(corr.columns)

# Ruota le etichette dell'asse X per leggibilità
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

# Opzionale: Aggiunge i valori numerici all'interno delle celle
for i in range(len(corr.columns)):
    for j in range(len(corr.columns)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", 
                ha="center", va="center", color="black")

ax.set_title("Matrice di Correlazione (Matplotlib)")
plt.tight_layout()
plt.show()


# Grid search per regressore (su tutto il dataset)

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [5, 10, None],
    'min_samples_leaf': [1, 2, 4],
}

grid_search = GridSearchCV(RandomForestRegressor(), param_grid=param_grid, n_jobs=-1)
grid_search.fit(X_train, y_train)

print("Best params:", grid_search.best_params_)
print("Best score:", grid_search.best_score_)


# Fare training del regressore sui parametri trovati

reg1 = RandomForestRegressor(max_depth = None, n_estimators = 200, n_jobs= -1)
reg1.fit(X_train, y_train)
y_pred1 = reg1.predict(X_test)

# Calcola risultato
print(reg1.score(X_test, y_test))
print(mean_absolute_error(y_pred1, y_test))


# Adattiamo i dati per il classificatore + regressore (su dati parziali)


# Dati per allenare il classificatore
X_train_clf = X_train
y_train_clf = (y_train > 0) # es. [True, False, False, ...]

# Dati per allenare il regressore
X_train_reg = X_train[y_train_clf]
y_train_reg = y_train[y_train_clf]


# Facciamo grid search + training del classificatore

# Perform Grid Search to find best parameters for the Classifier
search_clf = RandomForestClassifier()

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, None],
}

grid_search = GridSearchCV(search_clf, param_grid, cv=5, n_jobs = -1)
grid_search.fit(X_train_clf, y_train_clf)

print("Risultati medi per tutte le combinazioni:", grid_search.cv_results_["mean_test_score"])
print("Migliori parametri trovati:", grid_search.best_params_)
print("Punteggio migliore:", grid_search.best_score_)

# Train the Classifier with best parameters found
clf = RandomForestClassifier(max_depth = None, n_estimators = 200, n_jobs = -1)
reg = RandomForestRegressor(max_depth = None, n_estimators = 200, n_jobs= -1)
clf.fit(X_train_clf, y_train_clf)
reg.fit(X_train_reg, y_train_reg)


# Facciamo grid search + training del regressore

search_reg = RandomForestRegressor()

param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [10, None],
}

grid_search = GridSearchCV(search_reg, param_grid, cv=5, n_jobs = -1)
grid_search.fit(X_train_reg, y_train_reg)

print("Risultati medi per tutte le combinazioni:", grid_search.cv_results_["mean_test_score"])
print("Migliori parametri trovati:", grid_search.best_params_)
print("Punteggio migliore:", grid_search.best_score_)


# Calcoliamo le stime (y_pred) per il classificatore e regressore
# e le combiniamo

# Predict if it will rain, then predict the rain amount only for predicted rainy days
y_pred_clf = clf.predict(X_test)
y_pred_reg = reg.predict(X_test)
y_pred2 = np.where(y_pred_clf == 0, 0, y_pred_reg)


# Stampiamo lo score 'mean absolute error' delle stime combinate
print(mean_absolute_error(y_pred2, y_test))