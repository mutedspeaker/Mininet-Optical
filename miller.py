import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Load the data from the CSV file
data = pd.read_csv('data.csv')
data['ch'] = data['ch'].astype('category')

# Visualize the data with a scatter plot
fig, ax = plt.subplots()
ax.scatter(data['ch'], data['gOSNR'], label='gOSNR')
ax.scatter(data['ch'], data['OSNR'], label='OSNR')
ax.set_xlabel('Channel number')
ax.set_ylabel('Signal-to-noise ratio')
ax.legend()
plt.show()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data[['ch']], data[['gOSNR', 'OSNR']], test_size=0.2)

# Use a polynomial regression model to improve accuracy
poly = PolynomialFeatures(degree=3)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)
model = LinearRegression()
model.fit(X_train_poly, y_train)

# Evaluate the model on the testing set
y_pred = model.predict(X_test_poly)
mse = mean_squared_error(y_test, y_pred)
y_test_range = (y_test.max().values - y_test.min().values).flatten()[0]
accuracy = (1 - mse/y_test_range)

# Print the accuracy metrics
print(f'Mean Squared Error: {mse:.4f}')
print(f'Accuracy: {accuracy:.2f}%')

# Visualize the accuracy of the model with a graph
# train_sizes = [0.1, 0.3, 0.5, 0.7, 0.9]
train_sizes = [0.1, 0.3, 0.6]
train_errors = []
test_errors = []
for size in train_sizes:
    X_train_size, X_test_size, y_train_size, y_test_size = train_test_split(data[['ch']], data[['gOSNR', 'OSNR']], train_size=size)
    X_train_poly_size = poly.fit_transform(X_train_size)
    X_test_poly_size = poly.transform(X_test_size)
    model_size = LinearRegression()
    model_size.fit(X_train_poly_size, y_train_size)
    train_errors.append(mean_squared_error(y_train_size, model_size.predict(X_train_poly_size)))
    test_errors.append(mean_squared_error(y_test_size, model_size.predict(X_test_poly_size)))
fig, ax = plt.subplots()
ax.plot(train_sizes, train_errors, label='Training error')
ax.plot(train_sizes, test_errors, label='Testing error')
ax.set_xlabel('Training set size')
ax.set_ylabel('Mean squared error')
ax.legend()
plt.show()

# Use the model to make predictions for new channel numbers
new_channels = pd.DataFrame({'ch': range(1, 91)})
new_channels['ch'] = new_channels['ch'].astype('category')
new_channels_poly = poly.transform(new_channels[['ch']])
new_predictions = model.predict(new_channels_poly)
fig, ax = plt.subplots()
ax.plot(new_channels['ch'], new_predictions[:, 0], label='gOSNR')
ax.plot(new_channels['ch'], new_predictions[:, 1], label='OSNR')
ax.set_xlabel('Channel number')
ax.set_ylabel('Signal-to-noise ratio')
ax.legend()
plt.show()

# Create a combined predicted vs actual values plot for gOSNR and OSNR
fig, ax = plt.subplots()
ax.scatter(y_test['gOSNR'], y_pred[:, 0], label='Predicted gOSNR', color='blue')
ax.scatter(y_test['OSNR'], y_pred[:, 1], label='Predicted OSNR', color='orange')
ax.plot([y_test['gOSNR'].min(), y_test['gOSNR'].max()], [y_test['gOSNR'].min(), y_test['gOSNR'].max()], 'k--', label='Actual')
ax.set_xlabel('Actual')
ax.set_ylabel('Predicted')
ax.legend()
plt.show()


