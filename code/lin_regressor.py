import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Step 1: Load Excel file
file_path = r'E:\MAC\Term_2\Advanced Database Topics\Project\Py\Data\Final data_1.xlsx'
df = pd.read_excel(file_path)

# Step 2: Basic cleaning
df['Max_Temperature'] = pd.to_numeric(df['Max_Temperature'], errors='coerce')
df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
df.dropna(subset=['Value'], inplace=True)
df.head()
# Fill missing temperatures using monthly average per province
for temp_col in ['Max_Temperature', 'Min_Temperature', 'Avg_Temperature']:
    df[temp_col] = pd.to_numeric(df[temp_col], errors='coerce')
    df[temp_col] = df.groupby(['Province', 'Year', 'Month'])[temp_col].transform(lambda x: x.fillna(x.mean()))
    df[temp_col] = df[temp_col].fillna(df[temp_col].mean())  # Final fallback


df.drop(columns=['Measurement_Count','Min_Temperature', 'Avg_Temperature', 'UOM'])
# Step 3: Analyze per province and category
results = []

grouped = df.groupby(['Province', 'Category'])
for (province, category), group in grouped:
    if len(group) < 5:
        continue  # Skip small groups

    X = group[['Max_Temperature']]  # Change to multiple cols for multivariate
    y = group['Value']

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    results.append({
        'Province': province,
        'Category': category,
        'R2_Score': r2,
        'Coef': model.coef_[0],
        'Intercept': model.intercept_
    })

    # Plot
    plt.scatter(X, y, label='Actual')
    plt.plot(X, y_pred, color='red', label='Predicted')
    plt.title(f'{province} - {category}')
    plt.xlabel('Max Temperature')
    plt.ylabel('Retail Value')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Step 4: Summary of results
summary_df = pd.DataFrame(results)
summary_df.sort_values(by='R2_Score', ascending=False, inplace=True)
print(summary_df[summary_df['R2_Score']>0.3])



# this shows that Food 