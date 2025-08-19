import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your Excel sheet
df = pd.read_excel(r"E:\MAC\Term_2\Advanced Database Topics\Project\Py\Data\Final data_1.xlsx", sheet_name="Retail Trade")

# Clean data: drop rows with missing sales or Max Temperature
df_clean = df.dropna(subset=["Value", "Max_Temperature"])

# Define temperature bins and labels
bins = [-100, -10, 0, 10, 20, 100]
labels = ['< -10°C', '-10 to 0°C', '0 to 10°C', '10 to 20°C', '> 20°C']

# Create a new column for temperature range
df_clean["Temp_Range"] = pd.cut(df_clean["Max_Temperature"], bins=bins, labels=labels)

# Group by temperature range and calculate average sales
grouped_sales = df_clean.groupby("Temp_Range")["Value"].mean().reset_index()

# Plot average sales per temperature range
plt.figure(figsize=(10, 6))
sns.barplot(data=grouped_sales, x="Temp_Range", y="Value", palette="coolwarm")
plt.title("Average Sales Value by Max Temperature Range")
plt.xlabel("Max Temperature Range")
plt.ylabel("Average Sales Value (Dollars)")
plt.grid(True)
plt.tight_layout()
plt.show()
