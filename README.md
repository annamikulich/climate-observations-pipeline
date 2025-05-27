# Hawaii Climate Data Analysis

This project analyzes historical weather data collected from stations across Hawaii. It uses SQLAlchemy ORM to extract climate data from a SQLite database, then applies exploratory data analysis and visualization to understand precipitation patterns and temperature distributions.

## 📌 Project Overview

- **Database**: SQLite (`hawaii.sqlite`)
- **Tables**: `measurement`, `station`
- **ORM**: SQLAlchemy (automap)
- **Visualization**: Matplotlib
- **Analysis goals**:
  - Precipitation trends over the last 12 months
  - Identify the most active weather station
  - Analyze temperature observations from the most active station

## 🚀 How to Run

1. Clone this repository  
2. Install dependencies  
   ```bash
   pip install -r requirements.txt

   📊 Sample Output

Precipitation Timeline:
Temperature Histogram (most active station):
⚙️ Tech Stack

Python 3.x
SQLite
SQLAlchemy
Pandas
Matplotlib
Jupyter Notebook
