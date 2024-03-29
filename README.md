# PhonePe Pulse Data Dashboard

## Overview

The PhonePe Pulse Data Dashboard is an advanced, interactive visualization platform designed to analyze and display transaction data from PhonePe, one of the leading digital payment systems in India. This dashboard leverages the power of Python, MySQL, and Streamlit to present a user-friendly interface that delivers deep insights into transaction patterns, user growth metrics, and geographical payment trends across India.

Developed with the goal of enhancing data-driven decision-making, this tool is invaluable for business analysts, marketing teams, and decision-makers seeking to understand the dynamics of digital payments in the expansive Indian market.

## Features

- **Interactive Visualizations:** Users can interact with various filters and controls to view data based on specific parameters such as transaction type, geographical location, time period, and more.
- **Geographical Insights:** Utilizes choropleth maps to depict transaction volumes and values across different states and regions, offering a visual representation of market penetration and user activity.
- **User Growth Tracking:** Displays trends in user growth over time, aiding in the identification of key growth periods and patterns.
- **Performance Optimization:** Incorporates Streamlit's `@st.experimental_memo` for efficient data fetching and caching, ensuring quick load times and a responsive user experience.
- **Customizable Graphs:** Offers options to adjust graph colors and styles, making data presentation clearer and more visually appealing.

## Technical Architecture

### Data Processing

- **Script:** `data_extraction.py`
- **Function:** Processes raw JSON transaction data, converting it into structured CSV formats. These datasets are then loaded into a MySQL database for secure and scalable storage.

### Visualization Dashboard

- **Technology:** Streamlit
- **Script:** `dashboard.py`
- **Capabilities:** Powers the interactive dashboard, fetching data from the MySQL database and rendering dynamic charts and maps based on user input.

## Getting Started

### Prerequisites

- Python 3.x
- MySQL server
- Streamlit
- Pandas
- Plotly

### Installation

1. Clone the repository to your local machine:
    ```
    git clone https://github.com/your-repo/phonepe-pulse-dashboard.git
    ```
2. Navigate into the project directory and install the required Python packages:
    ```
    cd phonepe-pulse-dashboard
    pip install -r requirements.txt
    ```
3. Ensure your MySQL server is running and has a database ready for the project.

4. Run the `data_extraction.py` script to process and load the data into your MySQL database:
    ```
    python data_extraction.py
    ```

### Launching the Dashboard

Execute the following command to start the Streamlit dashboard:
   ```
    streamlit run dashboard.py
   ```
Navigate to the displayed URL in your web browser to interact with the PhonePe Pulse Data Dashboard.

