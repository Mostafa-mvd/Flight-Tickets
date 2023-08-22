import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


clean_dataset_path = "/home/magnus9102/Mostafa/Py/Github/data-science/mostafa_vahdani_bachelor_project/data/interim/build_features_flight_tickets_dataset.csv"

df = pd.read_csv(clean_dataset_path)

plt.figure(figsize=(5, 5))

# 1
# Count of flights with different months.
# There are around 7000 flights scheduled in the month of 6 so at this time can be the peak month.
# sns.countplot(x='month', data=df)

# 2
# plt.scatter(df['company_name'], df['ticket_price_T'])
#‌ plt.xticks(rotation=90)

# 3
# Count of flights with different Airlines
# sns.countplot(x='company_name', data=df)
# plt.xticks(rotation=90)

# 4
# sns.countplot(x='dep_flight_time', data=df)

# 5
# sns.boxplot(df['ticket_price_T'])

# 6
# Avg price in each month
df.groupby('month')['ticket_price_T'].mean().plot(kind='bar', rot=90)

plt.show()
