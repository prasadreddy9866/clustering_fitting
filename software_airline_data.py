# -*- coding: utf-8 -*-
"""software airline data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1og5hCMDek9o9uvJsODjP-luZkQs0agkP
"""

# Import libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

# Upload the dataset
file_path = 'Airline Quality Ratings.csv'

# Read the CSV file
airline_data = pd.read_csv(file_path)

# Show the data variables
print(airline_data.head(10))

# Define the dimension of the dataset
print(f"Shape of the dataset: {airline_data.shape}")

# Determine a summary of the dataset
print("\nDataset Info:")
airline_data.info()

# Check for null values in the dataset
null_values = airline_data.isnull().sum()

# Check the number of null values
print("Null values in each column:")
print(null_values)

# Fill null values in the 'Arrival Delay' column with the mean
mean_arrival_delay = airline_data['Arrival Delay'].mean()
airline_data['Arrival Delay'].fillna(mean_arrival_delay, inplace=True)

# Identify missing rows
print("Null values after filling:")
print(airline_data['Arrival Delay'].isnull().sum())

# Illustrate a bar plot
plt.figure(figsize=(10, 6))
sns.barplot(x='Gender', y='Ease of Online Booking', hue='Customer Type', data=airline_data, palette='viridis')

# Add labels and title
plt.title('Ease of Online Booking by Gender and Customer Type', fontsize=16)
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Ease of Online Booking', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=0)

# Show the plot
plt.tight_layout()
plt.show()

# Make a scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Flight Distance', y='Arrival Delay', hue='Satisfaction', data=airline_data, palette='coolwarm', s=100, edgecolor='black')

# Add labels and title
plt.title('Flight Distance vs Arrival Delay by Satisfaction', fontsize=16)
plt.xlabel('Flight Distance (miles)', fontsize=12)
plt.ylabel('Arrival Delay (minutes)', fontsize=12)

# Add a legend with custom positioning
plt.legend(title='Satisfaction', loc='upper right', fontsize=10)

# Display grid for better readability
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()

# Select only numeric columns for correlation
numeric_data = airline_data.select_dtypes(include=['float64', 'int64'])

# Compute the correlation matrix
corr_matrix = numeric_data.corr()

# Design a heatmap
plt.figure(figsize=(15, 9))
sns.heatmap(corr_matrix, annot=True, cmap='turbo', fmt='.1f', linewidths=1, cbar_kws={'shrink': 0.8}, square=True)

# Add labels and title
plt.title('Correlation Heatmap of Numeric Variables', fontsize=16)
plt.xlabel('Variables', fontsize=12)
plt.ylabel('Variables', fontsize=12)

# Display the plot
plt.tight_layout()
plt.show()

# Design a box plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Type of Travel', y='Seat Comfort', hue='Class', data=airline_data, palette='Set2')

# Add labels and title
plt.title('Seat Comfort by Type of Travel and Class', fontsize=16)
plt.xlabel('Type of Travel', fontsize=12)
plt.ylabel('Seat Comfort', fontsize=12)

# Rotate x-axis labels for better readability
plt.xticks(rotation=0)

# Add a legend with custom positioning
plt.legend(title='Class', loc='lower left', fontsize=10)

# Display grid for better readability
plt.grid(True)

# Show the plot
plt.tight_layout()
plt.show()

# Deploy the LabelEncoder
label_encoder = LabelEncoder()

# Convert all object columns into numbers
for column in airline_data.select_dtypes(include=['object']).columns:
    airline_data[column] = label_encoder.fit_transform(airline_data[column])

# Show the encoded dataframe
print(airline_data)

# Select dependant and independant features
X = airline_data.drop(columns=['Satisfaction', 'ID'])  # Drop 'ID' and 'Satisfaction' from features
y = airline_data['Satisfaction']  # Target is the 'Satisfaction' column

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Fit and train the Logistic Regression model
log_model = LogisticRegression()
log_model.fit(X_train, y_train)

# Make predictions on the test set
log_pred = log_model.predict(X_test)

# Evaluate the model
log_accuracy = accuracy_score(y_test, log_pred)
log_class_report = classification_report(y_test, log_pred)

# Print the evaluation results
print(f"Accuracy: {log_accuracy:.2f}")
print("\nClassification Report:")
print(log_class_report)

# Develop the confusion matrix
conf_matrix = confusion_matrix(y_test, log_pred)

# Plot the confusion matrix
plt.figure(figsize=(6, 4))
sns.heatmap(conf_matrix, annot=True, fmt='f', cmap='inferno', cbar=False, xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)

# Add labels and title
plt.title('Confusion Matrix', fontsize=16)
plt.xlabel('Predicted', fontsize=12)
plt.ylabel('Actual', fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()

# Fit and train the Random Forest Regressor model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Make predictions on the test set
rf_pred = rf_model.predict(X_test)

# Measure Mean Squared Error (MSE) and R² score
rf_mse = mean_squared_error(y_test, rf_pred)
rf_r2 = r2_score(y_test, rf_pred)

# Print the evaluation results
print(f"Mean Squared Error (MSE): {rf_mse:.2f}")
print(f"R² Score: {rf_r2:.2f}")

# K-means clustering
satisfaction_data = airline_data[['Satisfaction']]

# Elbow method to determine optimal number of clusters
inertia = []
for k in range(1, 11):  # Trying cluster sizes from 1 to 10
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(satisfaction_data)
    inertia.append(kmeans.inertia_)

# Plotting the elbow plot
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertia, marker='o', color='b')
plt.title('Elbow Method for Optimal K', fontsize=16)
plt.xlabel('Number of Clusters (K)', fontsize=12)
plt.ylabel('Inertia (Sum of squared distances)', fontsize=12)
plt.xticks(range(1, 11))
plt.grid(True)
plt.tight_layout()
plt.show()

# Perform K-means clustering with 5 clusters
kmeans = KMeans(n_clusters=5, random_state=42)
airline_data['Cluster'] = kmeans.fit_predict(satisfaction_data)

# Display the first few rows with assigned clusters
print(airline_data.head())


