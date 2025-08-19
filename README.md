# Localized-Retail-Demand-Forecasting-Using-Climate-in-Canada
# Localized Retail Demand Forecasting Using Climate and Consumer Trends

##  Project Overview

This project develops a data-driven forecasting system to predict retail sales across Canadian provinces by integrating localized factors such as climate data and  holiday schedules trends. Traditional models often overlook regional variations, which is particularly critical in a country like Canada with its diverse climate. This solution leverages time-series analysis and machine learning to provide accurate, province- and category-specific forecasts, enabling retailers to optimize inventory, staffing, and promotions.

##  Key Features

*   **Multi-Factor Integration:** Combines historical sales data with temperature, holidays, and news-driven consumer trends.
*   **Province-Level Granularity:** Delivers forecasts tailored to the unique economic and climatic conditions of each Canadian province and territory.
*   **Retail Category Analysis:** Examines five major retail sectors (e.g., Clothing, Groceries) with varying sensitivities to external factors.
*   **Advanced Modeling:** Utilizes Facebook's Prophet model for its robust handling of seasonality and support for external regressors like temperature.
*   **Comprehensive Analysis:** Includes regression analysis, holiday impact assessment (via t-tests), and thematic modeling of news events using LDA.

##  Technology Stack

*   **Programming Language:** Python
*   **Database:** MongoDB Atlas (for storing and managing heterogeneous datasets)
*   **Forecasting Model:** Facebook Prophet
*   **Data Processing & Analysis:** Pandas, NumPy, Scikit-learn, Statsmodels
*   **Visualization:** Matplotlib, Seaborn

