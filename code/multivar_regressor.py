from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error

# Select relevant columns
df_model = df_clean[["Value", "Max_Temperature", "Month", "Province", "Category"]].dropna()

# Features and target
X = df_model[["Max_Temperature", "Month", "Province", "Category"]]
y = df_model["Value"]

# Define categorical transformer
categorical_features = ["Province", "Category"]
categorical_transformer = OneHotEncoder(drop="first")

# Preprocessing and model pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", categorical_transformer, categorical_features)
    ],
    remainder='passthrough'  # leave numeric features as-is
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", LinearRegression())
])

# Fit the model
pipeline.fit(X, y)

from sklearn.metrics import mean_squared_error
import numpy as np

# Compute R² and RMSE
r2 = r2_score(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)

print(f"R² Score: {r2:.4f}")
print(f"Root Mean Squared Error (RMSE): ${rmse:,.2f}")
