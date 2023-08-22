import pandas as pd

from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split


final_dataset_path = "/home/magnus9102/Mostafa/Py/Github/data-science/mostafa_vahdani_bachelor_project/data/interim/final_flight_tickets_dataset.csv"

df = pd.read_csv(final_dataset_path)

y = df['ticket_price_T']
X = df.drop('ticket_price_T', axis=1)

s = StandardScaler()
X = s.fit_transform(X)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

