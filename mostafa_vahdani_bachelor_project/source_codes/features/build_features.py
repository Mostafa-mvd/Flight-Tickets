# Python scripts or Jupyter notebooks that contain code to generate, transform, or manipulate features from raw data. These scripts might involve tasks like encoding categorical variables, scaling numeric features, feature selection,creating interaction terms, etc.

import pandas as pd
from sklearn.decomposition import PCA


processed_dataset_path = "/home/magnus9102/Mostafa/Py/Github/data-science/mostafa_vahdani_bachelor_project/data/processed/flight_tickets_dataset.csv"

df = pd.read_csv(processed_dataset_path)

X = df.drop(['ticket_price_T'], axis=1)
y = df['ticket_price_T']

pca = PCA(n_components=2)
pca.fit(X)
print(pca.explained_variance_ratio_)  # [pca1_variance, pca2_variance]
