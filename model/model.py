import pandas as pd #for creating Dataframes
import numpy as np
import matplotlib.pyplot as plt #for plotting graphs
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split #For implementing models
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score #For judging the model

data = pd.read_csv('model/dataset.csv')
# print(data.head(18))
data.columns = data.columns.str.strip()
# data["Category"] = data["Category"].str.strip()

category_mapping = {
    ' canned goods' : 1,
    ' medicines' : 2,
    ' cosmetics' : 3,
    ' beverages' : 4,
    ' grocery' : 5,

}

# print(data['Category'])
data['Class'] = data['cat'].map(category_mapping)

print(data['Class'])
x = data[['dfe','mrp','Class']]

y = pd.Series(data['clear'])

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(x_train,y_train)

# # Calculate evaluation metrics
# mae = mean_absolute_error(y_test, y_pred)
# mse = mean_squared_error(y_test, y_pred)
# r2 = r2_score(y_test, y_pred)
def findClearance( dfe, mrp, cl):
    if cl>5:
        return "Invalid Category"
    
    test = [[dfe, mrp, cl]]
    test_df = pd.DataFrame(test, columns=['dfe', 'mrp', 'Class'])

    y_pred = rf_regressor.predict(test_df)

    return int(y_pred)

print(findClearance(5,210,5))



# # Print the evaluation metrics
# print(f"Mean Absolute Error (MAE): {mae:.4f}")
# print(f"Mean Squared Error (MSE): {mse:.4f}")
# print(f"R-squared (R2) Score: {r2:.4f}")