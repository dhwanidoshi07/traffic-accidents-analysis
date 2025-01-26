# import required libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title='TRAFFIC ACCIDENTS EXPLORATORY DATA ANALYSIS', layout="wide")

# Load data
final_data = pd.read_csv("traffic_accidents.csv")

# Introduction Section
row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.title('Traffic Accident Insights: An Exploratory Data Analysis')

row3_spacer1, row3_1, row3_spacer2 = st.columns((.1, 3.2, .1))
with row3_1:
    st.markdown("This interactive web application provides an in-depth analysis of traffic accidents using a comprehensive dataset sourced from Kaggle. The dataset includes various columns such as weather conditions, traffic way types, lighting conditions, crash types, and more, enabling users to explore key factors influencing road safety.")
    st.markdown("Through engaging visualizations like line charts and bar graphs, users can analyze trends over time and assess the distribution of accidents across different metrics. Additionally, a correlation heatmap highlights relationships between numerical variables, facilitating exploratory data analysis (EDA) for informed decision-making regarding traffic safety improvements.")
    see_data = st.expander('You can click here to see the raw data first 👉')
    with see_data:
        st.dataframe(data=final_data.reset_index(drop=True))

# Metrics Selection Section
st.header("Select Metrics to Analyze Accidents")

# Create three columns for dropdowns
col1, col2, col3 = st.columns(3)

# Unique values for dropdowns
weather_conditions = final_data['weather_condition'].unique()
traffic_way_types = final_data['trafficway_type'].unique()
road_surface_conditions = final_data['roadway_surface_cond'].unique()

# Dropdown menus for user selection
with col1:
    selected_weather = st.selectbox("Weather Conditions", options=weather_conditions)

with col2:
    selected_traffic_way = st.selectbox("Traffic Way Type", options=traffic_way_types)

with col3:
    selected_road_surface = st.selectbox("Roadway Surface Condition", options=road_surface_conditions)

# Calculate number of accidents based on selected metrics
filtered_data = final_data[
    (final_data['weather_condition'] == selected_weather) &
    (final_data['trafficway_type'] == selected_traffic_way) &
    (final_data['roadway_surface_cond'] == selected_road_surface)
]

number_of_accidents = filtered_data.shape[0]

# Prepare the final statement with formatting
final_statement = (
    f"No of accidents in **{selected_weather.lower()}** weather conditions in "
    f"**{selected_traffic_way.lower()}** traffic on "
    f"**{selected_road_surface.lower()}** roads are: "
    f"<span style='color:red; font-size:20px;'><strong>{number_of_accidents}</strong></span>"
)

# Display the result with larger font size and HTML formatting
st.markdown(final_statement, unsafe_allow_html=True)

# New Section for Line Chart Selection
st.header("Analyze Accident Trends")

# Create two columns for metric selection and chart display
metric_col, chart_col = st.columns(2)

# Centering the dropdown menu in the left column with reduced width
with metric_col:
    # Use a markdown container to center the dropdown
    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    
    # Dropdown menu for selecting metrics with new labels (unique key)
    selected_metric_trend = st.selectbox("Select Metric", options=["Hour", "Day", "Month"], key="metric_select_trend")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Prepare data for line chart based on user selection
if selected_metric_trend == "Hour":
    # Count accidents by hour and ensure all hours from 0 to 24 are represented
    line_chart_data = final_data['crash_hour'].value_counts().reindex(range(25), fill_value=0)
    title = "Accident Trends by Hour"
elif selected_metric_trend == "Day":
    # Count accidents by day of the week (assuming days are coded from 0-6)
    line_chart_data = final_data['crash_day_of_week'].value_counts().reindex(range(7), fill_value=0)
    title = "Accident Trends by Day of the Week"
else:  # Month
    # Count accidents by month and map values to month names
    line_chart_data = final_data['crash_month'].value_counts().reindex(range(1, 13), fill_value=0)
    title = "Accident Trends by Month"

# Display the line chart in the right column
with chart_col:
    st.subheader(title)
    
    # Create a line chart using seaborn or matplotlib
    plt.figure(figsize=(10, 5))
    
    if selected_metric_trend == "Hour":
        sns.lineplot(data=line_chart_data, marker='o')
        plt.xticks(range(25))  # Show all hours from 0 to 24 on x-axis
        plt.xlabel('Hour of Day')
        
    elif selected_metric_trend == "Day":
        sns.lineplot(data=line_chart_data, marker='o')
        plt.xticks(range(7), ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])  # Day names on x-axis
        plt.xlabel('Day of the Week')
        
    else:  # Month
        month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        sns.lineplot(data=line_chart_data, marker='o')
        plt.xticks(range(1, 13), month_names)  # Month names on x-axis
        plt.xlabel('Month')

    plt.ylabel('Number of Accidents')
    
    # Show the plot in Streamlit
    plt.title(title)
    st.pyplot(plt)

# New Section for Bar Chart Selection
st.header("Analyze Accident Metrics")

# Create two columns for metric selection and chart display for bar chart
metric_col_bar, chart_col_bar = st.columns(2)

with metric_col_bar:
    # Centering the dropdown menu in the left column with reduced width for bar chart metrics
    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    
    # Dropdown menu for selecting metrics with new labels (excluding certain metrics)
    selected_metric_bar = st.selectbox(
        "Select Metric",
        options=[
            "Weather conditions",
            "Lighting condition",
            "Crash type",
            "Intersection?",
            "Damage"
        ],
        key="metric_select_bar"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Prepare data for bar chart based on user selection
metric_mapping_bar = {
    "Weather conditions": "weather_condition",
    "Lighting condition": "lighting_condition",
    "Crash type": "crash_type",
    "Intersection?": "intersection_related_i",
    "Damage": "damage"
}

selected_column_bar = metric_mapping_bar[selected_metric_bar]

# Count occurrences of each category in the selected column for bar chart
bar_chart_data = final_data[selected_column_bar].value_counts()

# Display the bar chart in the right column for bar chart metrics
with chart_col_bar:
    st.subheader(f"{selected_metric_bar} Distribution")
    
    # Create a bar chart using seaborn or matplotlib with pastel colors
    plt.figure(figsize=(10, 5))
    
    sns.barplot(x=bar_chart_data.index, y=bar_chart_data.values)
    
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.xlabel(selected_metric_bar)
    plt.ylabel('Number of Accidents')
    
    # Show the plot in Streamlit
    plt.title(f'Distribution of {selected_metric_bar}')
    st.pyplot(plt)

# New Section for Correlation Heatmap
st.header("Correlation Heatmap")

# Select only numerical columns from the DataFrame
numerical_data = final_data.select_dtypes(include=['float64', 'int64'])

# Calculate correlation matrix for numerical columns only
correlation_matrix = numerical_data.corr()

# Create a heatmap using seaborn
plt.figure(figsize=(10, 6))  # Adjusted figure size

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap='coolwarm',
    square=True,
    cbar_kws={"shrink": .8},
    annot_kws={"size": 8}  # Smaller font size for annotations
)

plt.title('Correlation Heatmap of Numerical Features')
st.pyplot(plt)
