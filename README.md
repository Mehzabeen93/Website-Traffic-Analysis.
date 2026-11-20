# Website Traffic Analysis Dashboard

## Project Overview
This project analyzes website traffic data to understand visitor behaviour, traffic sources, device usage, conversion rates, and website page performance.

An interactive dashboard was developed using Python, Pandas, Plotly, and Streamlit to present important website performance metrics and insights.

## Project Objectives
- Analyze website traffic and visitor activity.
- Identify the most effective traffic sources.
- Compare website usage across devices.
- Calculate bounce rates and conversion rates.
- Analyze monthly traffic and conversion trends.
- Evaluate the performance of individual website pages.

## Tools and Technologies
- **Python:** Data analysis and programming.
- **Pandas:** Data cleaning and manipulation.
- **NumPy:** Numerical operations.
- **Matplotlib and Seaborn:** Exploratory data analysis.
- **Plotly:** Interactive visualizations.
- **Streamlit:** Interactive dashboard development.

## Dataset Description
The project uses a website traffic dataset containing 2,000 sessions.

Important columns include:
- Session_ID
- User_ID
- Date
- Traffic_Source
- Device
- Page_Visited
- Session_Duration
- Pages_Per_Session
- Bounce
- Conversion

## Dashboard Features
- Total Sessions and Total Users
- Bounce Rate and Conversion Rate
- Website Traffic by Source
- Website Traffic by Device
- Conversion Rate by Traffic Source
- Conversion Rate by Device
- Monthly Website Traffic Trend
- Monthly Conversion Trend
- Website Page Performance
- Interactive filters for traffic source, device, and month

## Key Findings
- Organic search generated the highest number of sessions.
- Direct traffic had the highest conversion rate among traffic sources.
- Mobile devices generated the largest share of website sessions.
- Desktop users had a higher conversion rate than mobile users.
- Website page performance varied across pages in terms of traffic, conversions, and bounce rates.

## Project Structure

```text
Website-Traffic-Analysis/
│
├── Website_Traffic_Analysis.ipynb
├── Website_Traffic_Dashboard.ipynb
├── Website_Traffic_Analysis_Dataset.csv
├── app.py
├── README.md
└── requirements.txt
```

## How to Run the Project

1. Clone or download this repository.
2. Install the required libraries:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:

```bash
streamlit run app.py
```

4. Open the local URL displayed in your terminal to view the dashboard.

## Skills Demonstrated
Python, Data Analysis, Data Cleaning, Exploratory Data Analysis (EDA), Pandas, NumPy, Data Visualization, Plotly, Streamlit, and Dashboard Development.

