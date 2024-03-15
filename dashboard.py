# dashboard.py
# Import Libraries
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import json
from streamlit import cache_data
from PIL import Image
import plotly.graph_objects as go

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Overview'

# State name mapping dictionary
state_name_map = {
    'andaman-&-nicobar-islands': 'Andaman & Nicobar Island',
    'andhra-pradesh': 'Andhra Pradesh',
    'arunachal-pradesh': 'Arunanchal Pradesh',
    'assam': 'Assam',
    'bihar': 'Bihar',
    'chandigarh': 'Chandigarh',
    'chhattisgarh': 'Chhattisgarh',
    'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadara & Nagar Havelli',
    'delhi': 'NCT of Delhi',
    'goa': 'Goa',
    'gujarat': 'Gujarat',
    'haryana': 'Haryana',
    'himachal-pradesh': 'Himachal Pradesh',
    'jammu-&-kashmir': 'Jammu & Kashmir',
    'jharkhand': 'Jharkhand',
    'karnataka': 'Karnataka',
    'kerala': 'Kerala',
    'lakshadweep': 'Lakshadweep',
    'madhya-pradesh': 'Madhya Pradesh',
    'maharashtra': 'Maharashtra',
    'manipur': 'Manipur',
    'meghalaya': 'Meghalaya',
    'mizoram': 'Mizoram',
    'nagaland': 'Nagaland',
    'odisha': 'Odisha',
    'puducherry': 'Puducherry',
    'punjab': 'Punjab',
    'rajasthan': 'Rajasthan',
    'sikkim': 'Sikkim',
    'tamil-nadu': 'Tamil Nadu',
    'telangana': 'Telangana',
    'tripura': 'Tripura',
    'uttar-pradesh': 'Uttar Pradesh',
    'uttarakhand': 'Uttarakhand',
    'west-bengal': 'West Bengal'
}

@cache_data
def fetch_data(query):
    db_config = {
        'host': 'localhost',
        'user': "root",
        'password': "root",
        'database': 'phonepe_data'
    }
    engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")
    data = pd.read_sql(query, engine)
    engine.dispose()
    return data

def get_distinct_states():
    query = "SELECT DISTINCT State FROM aggregated_transaction ORDER BY State"
    return fetch_data(query)['State'].tolist()

def get_distinct_years():
    query = "SELECT DISTINCT Year FROM aggregated_transaction ORDER BY Year"
    return fetch_data(query)['Year'].tolist()


def show_transaction_data(data):
    if not data.empty:
        fig = px.bar(data, x='TransactionType', y='TransactionCount', title='Transaction Count by Type',color_discrete_sequence=['cyan'])
        st.plotly_chart(fig)
    else:
        st.write("No data available.")


def get_yearly_transaction_values():
    query = """
        SELECT Year, SUM(TransactionAmount) AS TotalValue
        FROM aggregated_transaction
        GROUP BY Year
        ORDER BY Year;
    """
    return fetch_data(query)


def create_yearly_transaction_values_chart(df):
    fig = go.Figure(data=[
        go.Bar(name='Total Transaction Value', x=df['Year'], y=df['TotalValue'],marker_color='cyan')
    ])
    fig.update_layout(title_text='Yearly Total Transaction Value')
    return fig

def fetch_filtered_data(state, year, quarter, transaction_type):
    query_conditions = []
    if state != 'All':
        query_conditions.append(f"State = '{state}'")
    if year != 'All':
        query_conditions.append(f"Year = {year}")
    if quarter != "All":
        query_conditions.append(f"Quarter = {quarter}")
    if transaction_type != 'All':
        query_conditions.append(f"TransactionType = '{transaction_type}'")

    query = "SELECT * FROM aggregated_transaction"
    if query_conditions:
        query += " WHERE " + " AND ".join(query_conditions)
    return fetch_data(query)

# Fetch data to show user growth overtime in Overview page
def show_user_growth_over_time():
    st.subheader("User Growth Over Time")

    # SQL query to fetch user growth data
    query = """
    SELECT Year, Quarter, SUM(RegisteredUsers) AS TotalUsers
    FROM aggregated_user
    GROUP BY Year, Quarter
    ORDER BY Year, Quarter;
    """
    user_growth_data = fetch_data(query)

    # Combining Year and Quarter for the x-axis
    user_growth_data['Period'] = user_growth_data['Year'].astype(str) + ' Q' + user_growth_data['Quarter'].astype(str)

    # Check if data is available and create chart
    if not user_growth_data.empty:
        fig = px.line(user_growth_data, x='Period', y='TotalUsers',
                      title='User Growth Over Time', markers=True)
                # Change line and marker colors
        fig.update_traces(line_color='cyan', marker_color='cyan')
        st.plotly_chart(fig)
    else:
        st.write("No user growth data available.")


def top_states_by_transaction_amount():
    query = """
    SELECT State, SUM(TransactionAmount) AS TotalAmount
    FROM aggregated_transaction
    GROUP BY State
    ORDER BY TotalAmount DESC
    LIMIT 10;
    """
    data = fetch_data(query)

    if not data.empty:

        fig = px.bar(data, x='State', y='TotalAmount',
                     title='Top 10 States by Transaction Amount',
                     labels={'TotalAmount': 'Total Transaction Amount'},
                     color='TotalAmount',
                     color_continuous_scale='tealgrn')
        st.plotly_chart(fig)
    else:
        st.write("No data available.")


def least_states_by_transaction_amount():
    query = """
    SELECT State, SUM(TransactionAmount) AS TotalAmount
    FROM aggregated_transaction
    GROUP BY State
    ORDER BY TotalAmount ASC
    LIMIT 10;
    """
    data = fetch_data(query)

    if not data.empty:
        fig = px.bar(data, x='State', y='TotalAmount',
                     title='Least 10 States by Transaction Amount',
                     labels={'TotalAmount': 'Total Transaction Amount'},
                     color='TotalAmount',
                     color_continuous_scale='tealgrn')
        st.plotly_chart(fig)
    else:
        st.write("No data available.")

def top_states_by_users():
    query = """
    SELECT State, SUM(RegisteredUsers) AS TotalUsers
    FROM aggregated_user
    GROUP BY State
    ORDER BY TotalUsers DESC
    LIMIT 10;
    """
    data = fetch_data(query)

    if not data.empty:
        fig = px.bar(data, x='State', y='TotalUsers',
                     title='Top 10 States by Users',
                     labels={'TotalUsers': 'Total Number of Users'},
                     color='TotalUsers',
                     color_continuous_scale='tealgrn')
        st.plotly_chart(fig)
    else:
        st.write("No data available.")

def least_states_by_users():
    query = """
    SELECT State, SUM(RegisteredUsers) AS TotalUsers
    FROM aggregated_user
    GROUP BY State
    ORDER BY TotalUsers ASC
    LIMIT 10;
    """
    data = fetch_data(query)

    if not data.empty:
        fig = px.bar(data, x='State', y='TotalUsers',
                     title='Least 10 States by Users',
                     labels={'TotalUsers': 'Total Number of Users'},
                     color='TotalUsers',
                     color_continuous_scale='tealgrn')
        st.plotly_chart(fig)
    else:
        st.write("No data available.")

def top_states_by_transaction_volume():
    query = """
    SELECT State, SUM(TransactionCount) AS TotalVolume
    FROM aggregated_transaction
    GROUP BY State
    ORDER BY TotalVolume DESC
    LIMIT 10;
    """
    data = fetch_data(query)

    if not data.empty:
        fig = px.bar(data, x='State', y='TotalVolume',
                     title='Top 10 States by Transaction Volume',
                     labels={'TotalVolume': 'Total Transaction Volume'},
                     color='TotalVolume',
                     color_continuous_scale='tealgrn')
        st.plotly_chart(fig)
    else:
        st.write("No data available.")


def least_states_by_transaction_volume():
    query = """
    SELECT State, SUM(TransactionCount) AS TotalVolume
    FROM aggregated_transaction
    GROUP BY State
    ORDER BY TotalVolume ASC
    LIMIT 10;
    """
    data = fetch_data(query)

    if not data.empty:
        fig = px.bar(data, x='State', y='TotalVolume',
                     title='Least 10 States by Transaction Volume',
                     labels={'TotalVolume': 'Total Transaction Volume'},
                     color='TotalVolume',
                     color_continuous_scale='tealgrn')
        st.plotly_chart(fig)
    else:
        st.write("No data available.")


question_functions = {
    "Top 10 States based on Transaction Amount": top_states_by_transaction_amount,
    "Bottom 10 States based on Transaction Amount": least_states_by_transaction_amount,
    "Top 10 States based on Total Users": top_states_by_users,
    "Bottom 10 States based on Total Users": least_states_by_users,
    "Top 10 States based on Transaction Volume": top_states_by_transaction_volume,
    "Bottom 10 States based on Transaction Volume": least_states_by_transaction_volume
}

# Column layout for logos
col1, col2, col3 = st.columns([1,6,1])

# Load and display Guvi logo
with col1:
    image = Image.open("C:\\Users\\lpugh\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\guvi_w.png")

    new_size = (100, 100) 
    resized_image = image.resize(new_size)
    st.image(resized_image)

# Load and display Phonepe logo
with col3:
    image = Image.open("C:\\Users\\lpugh\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\PhonePe.png")

    new_size = (80, 80)
    resized_image = image.resize(new_size)
    st.image(resized_image)

def show_overview():
    st.subheader("Overview of PhonePe Transactions")

    # PhonePe Summary
    st.markdown("""
    ### About PhonePe
    PhonePe is a leading digital payment platform in India, offering a range of financial services including mobile payments, banking, and online money transfers. Founded in 2015, it operates on the Unified Payments Interface (UPI) developed by the National Payments Corporation of India (NPCI). PhonePe is known for its user-friendly interface and widespread acceptance across merchants and businesses in India.

    This dashboard provides insights derived from transaction data available in the PhonePe Pulse repository. Here, you can explore transaction trends, geographical insights, and other key metrics.
    """)

    # Display Total Transactions and transaction amounts with plotly visualisation
    # Fetch data
    yearly_transaction_values = get_yearly_transaction_values()

    # Create visualizations
    transaction_values_chart = create_yearly_transaction_values_chart(yearly_transaction_values)

    # Display charts
    st.plotly_chart(transaction_values_chart)

    # Display User Growth Over Time
    show_user_growth_over_time()


def show_transaction_analysis():
    st.subheader("Detailed Transaction Analysis")

    selected_state = st.selectbox('Select State', options=['All'] + get_distinct_states())
    selected_year = st.select_slider("Select Year", options=['All'] + get_distinct_years())
    selected_quarter = st.selectbox('Select Quarter', options=['All', 1, 2, 3, 4])
    selected_type = st.selectbox('Select Transaction Type',options=['All', 'Recharge & bill payments', 'Peer-to-peer payments','Merchant payments', 'Financial Services', 'Others'])

    # Fetch filtered data
    data = fetch_filtered_data(selected_state, selected_year, selected_quarter, selected_type)

    # Calculate summary statistics
    total_transactions = data['TransactionCount'].sum() if not data.empty else 0
    average_amount = data['TransactionAmount'].mean() if not data.empty else 0
    total_amount = data['TransactionAmount'].sum() if not data.empty else 0

    # Display summary statistics
    st.metric("Total Transactions", total_transactions)
    st.metric("Average Transaction Amount", f"₹{average_amount:.2f}")
    st.metric("Total Transaction Amount", f"₹{total_amount:.2f}")

    # Display transaction data
    show_transaction_data(data)


def show_geographical_insights():
    st.subheader("Geographical Insights")

    # Year selection
    selected_year = st.selectbox("Select Year", options=['All'] + get_distinct_years())

    # Display a loading message while fetching and processing data
    with st.spinner('Loading data...'):
        # Query for choropleth data based on year
        geo_query = "SELECT State, SUM(TransactionAmount) AS TotalAmount FROM aggregated_transaction "
        if selected_year != 'All':
            geo_query += f"WHERE Year = {selected_year} "
        geo_query += "GROUP BY State"
        geo_data = fetch_data(geo_query)

        # Apply the mapping to align state names
        geo_data['State'] = geo_data['State'].map(state_name_map)

        if not geo_data.empty:
            # Create choropleth map
            choropleth_fig = create_choropleth(geo_data, india_geojson, 'State', 'TotalAmount')
            st.plotly_chart(choropleth_fig)
        else:
            st.write("No geographical data available.")


def load_geojson(geojson_path):
    with open(geojson_path, 'r') as file:
        return json.load(file)


india_geojson = load_geojson('states_india.geojson')

def create_choropleth(dataframe, geojson, location_column, color_column):
    fig = px.choropleth(dataframe,
                        geojson=geojson,
                        locations=location_column,
                        featureidkey="properties.st_nm",
                        color=color_column,
                        hover_data=[location_column, color_column],
                        color_continuous_scale="Viridis")
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=700, width=900)
    return fig
def show_top_data_insights():
    st.subheader("Top Data Insights")
    question = st.selectbox("Select a Data Insight to View", list(question_functions.keys()))

    if question in question_functions:
        question_functions[question]()



def create_nav_button(label, key):
    # Custom styling for the selected button
    if st.session_state['current_page'] == key:
        # Button style for the active/selected page
        button_style = """
        <style>
            .btn-primary {
                border-color: rgb(255, 75, 75);
                background-color: rgb(255, 75, 75);
            }
            .btn-primary:hover {
                background-color: rgb(255, 100, 100);
                border-color: rgb(255, 100, 100);
            }
        </style> """
    else:
        # Default button style
        button_style = ""

    st.markdown(button_style, unsafe_allow_html=True)
    if st.button(label):
        st.session_state['current_page'] = key

def main():
    st.markdown("<h1 style='text-align: center;'>PhonePe Pulse Data Dashboard</h1>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    <div class="centered-text">
    The PhonePe Pulse Data Dashboard project is a sophisticated visualization tool designed to provide deep insights into the transaction data of PhonePe, one of India's leading digital payment platforms.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("____________________________________________________________________________________________________________________________________________________________________________")

    # Navigation
    pages = {
        "Overview": show_overview,
        "Transaction Analysis": show_transaction_analysis,
        "Geographical Insights": show_geographical_insights,
        "Top Data Insights": show_top_data_insights
    }

    # Initialize current_page in session state
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Overview'

    # Create navigation buttons
    cols = st.columns(4)
    for i, (key, _) in enumerate(pages.items()):
        with cols[i]:
            create_nav_button(key, key)

    # Display the current page content
    pages[st.session_state['current_page']]()

if __name__ == "__main__":
    main()