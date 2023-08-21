import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

processed_dataset_path = "/home/magnus9102/Mostafa/Py/Github/data-science/mostafa_vahdani_bachelor_project/data/processed/flight_tickets_dataset.csv"

df = pd.read_csv(processed_dataset_path)

X = df.drop(['ticket_price_T'], axis=1)
y = df['ticket_price_T']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

linear_model = LinearRegression()

linear_model.fit(x_train, y_train)
