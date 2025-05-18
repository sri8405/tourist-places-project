import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import seaborn as sns
from geopy.distance import geodesic
import base64
import os

# Set page config
st.set_page_config(
    page_title="Tourist Place Recommender",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS and JS
def load_css():
    with open("static/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Add Font Awesome
    st.markdown("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """, unsafe_allow_html=True)

def load_js():
    with open("static/script.js") as f:
        st.markdown(f"<script>{f.read()}</script>", unsafe_allow_html=True)

load_css()
load_js()

# Helper functions
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def create_metric_card(title, value, delta=None):
    return f"""
    <div class="metric-card fade-in">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        {f'<div class="metric-delta">{delta}</div>' if delta else ''}
    </div>
    """

def create_place_card(place):
    # Get image for the place
    image_path = f"assets/{place['place_name'].lower().replace(' ', '_')}.jpg"
    if not os.path.exists(image_path):
        image_path = "assets/default_place.jpg"
    
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    
    return f"""
    <div class="place-card fade-in">
        <div class="place-image" style="background-image: url('data:image/jpeg;base64,{image_data}')"></div>
        <div class="place-content">
            <h3>{place['place_name']}</h3>
            <div class="place-details">
                <p><strong>Category:</strong> {place['category']}</p>
                <p><strong>Type:</strong> {place['type']}</p>
                <p><strong>Monthly Visitors:</strong> {place['monthly_visitors']:,}</p>
                <p><strong>Best Time:</strong> {place['best_time_to_visit']}</p>
            </div>
        </div>
    </div>
    """

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('data/top_indian_places.csv')

df = load_data()

# Helper functions
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

def generate_optimal_route(places, num_days):
    # Simple optimization: group places by category and visitor count
    places = places.sort_values(['category', 'monthly_visitors'], ascending=[True, False])
    return np.array_split(places, num_days)

def predict_visitors(historical_data, months_ahead=6):
    X = np.array(range(len(historical_data))).reshape(-1, 1)
    y = historical_data
    model = LinearRegression()
    model.fit(X, y)
    future_X = np.array(range(len(historical_data), len(historical_data) + months_ahead)).reshape(-1, 1)
    return model.predict(future_X)

# Sidebar with enhanced styling
with st.sidebar:
    st.title("🗺️ Navigation")
    st.markdown("---")
    page = st.radio(
        "Go to",
        ["Home", "Place Recommender", "Itinerary Planner", "Analytics", "City Comparison", "About"],
        label_visibility="collapsed"
    )

# Home Page
if page == "Home":
    st.title("Welcome to Tourist Place Recommender")
    
    # Hero section with background image
    st.markdown("""
        <div class="hero-section fade-in">
            <h2>Explore India's Finest Destinations</h2>
            <p>Plan your perfect trip with our comprehensive travel guide</p>
            <div class="hero-buttons">
                <a href="#cities" class="hero-button">Explore Cities</a>
                <a href="#features" class="hero-button secondary">Learn More</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("""
        <div id="features" class="features-section animate-on-scroll">
            <h2>Why Choose Us?</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <i class="fas fa-map-marked-alt"></i>
                    <h3>Smart Recommendations</h3>
                    <p>Get personalized recommendations based on your preferences</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-route"></i>
                    <h3>Optimal Itineraries</h3>
                    <p>Plan your perfect trip with our intelligent itinerary generator</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-chart-line"></i>
                    <h3>Real-time Analytics</h3>
                    <p>Make informed decisions with our comprehensive analytics</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display available cities with enhanced metrics
    st.markdown('<div id="cities">', unsafe_allow_html=True)
    st.subheader("Available Cities")
    cities = df['city'].unique()
    cols = st.columns(4)
    for idx, city in enumerate(cities):
        with cols[idx % 4]:
            city_data = df[df['city'] == city]
            total_visitors = city_data['monthly_visitors'].sum()
            st.markdown(
                create_metric_card(
                    city,
                    f"{total_visitors:,}",
                    f"{len(city_data)} places"
                ),
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Place Recommender
elif page == "Place Recommender":
    st.title("Tourist Place Recommender")
    
    # Enhanced city selection
    selected_city = st.selectbox(
        "Select a City",
        df['city'].unique(),
        format_func=lambda x: f"🏙️ {x}"
    )
    
    # Filter places for selected city
    city_places = df[df['city'] == selected_city]
    
    # Advanced filters
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.multiselect(
            "Filter by Category",
            options=city_places['category'].unique(),
            default=city_places['category'].unique()
        )
    with col2:
        selected_type = st.multiselect(
            "Filter by Type",
            options=city_places['type'].unique(),
            default=city_places['type'].unique()
        )
    
    # Apply filters
    filtered_places = city_places[
        (city_places['category'].isin(selected_category)) &
        (city_places['type'].isin(selected_type))
    ]
    
    # Display top places with enhanced cards
    st.subheader(f"Top Places in {selected_city}")
    
    # Create columns for place cards
    cols = st.columns(3)
    for idx, place in filtered_places.iterrows():
        with cols[idx % 3]:
            st.markdown(create_place_card(place), unsafe_allow_html=True)

# Itinerary Planner
elif page == "Itinerary Planner":
    st.title("Itinerary Planner")
    
    # Enhanced city selection
    selected_city = st.selectbox(
        "Select a City",
        df['city'].unique(),
        format_func=lambda x: f"🏙️ {x}"
    )
    
    # Number of days with enhanced UI
    num_days = st.number_input(
        "Number of Days",
        min_value=1,
        max_value=7,
        value=3,
        help="Choose how many days you want to spend in the city"
    )
    
    if st.button("Generate Itinerary", help="Click to generate your personalized itinerary"):
        city_places = df[df['city'] == selected_city]
        
        # Generate optimal route
        daily_places = generate_optimal_route(city_places, num_days)
        
        st.subheader(f"{num_days}-Day Itinerary for {selected_city}")
        
        for day, places in enumerate(daily_places):
            st.markdown(f"""
                <div class="itinerary-day fade-in">
                    <h3>Day {day + 1}</h3>
            """, unsafe_allow_html=True)
            
            for _, place in places.iterrows():
                st.markdown(f"""
                    <div class="place-card">
                        <h4>{place['place_name']}</h4>
                        <div class="place-details">
                            <p><strong>Category:</strong> {place['category']}</p>
                            <p><strong>Type:</strong> {place['type']}</p>
                            <p><strong>Best Time to Visit:</strong> {place['best_time_to_visit']}</p>
                            <p><strong>Expected Visitors:</strong> {place['monthly_visitors']:,}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# Analytics
elif page == "Analytics":
    st.title("Analytics Dashboard")
    
    # Enhanced city selection
    selected_city = st.selectbox(
        "Select a City",
        df['city'].unique(),
        format_func=lambda x: f"🏙️ {x}"
    )
    
    city_data = df[df['city'] == selected_city]
    
    # Create tabs with enhanced styling
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Visitor Statistics",
        "🌡️ Weather Analysis",
        "📈 Category Distribution",
        "🗺️ Place Clustering"
    ])
    
    with tab1:
        st.subheader("Visitor Statistics")
        
        # Total visitors with enhanced metric card
        total_visitors = city_data['monthly_visitors'].sum()
        st.markdown(
            create_metric_card(
                "Total Monthly Visitors",
                f"{total_visitors:,}",
                "Across all places"
            ),
            unsafe_allow_html=True
        )
        
        # Visitor prediction with enhanced visualization
        st.subheader("Visitor Prediction")
        historical_data = city_data['monthly_visitors'].values
        future_visitors = predict_visitors(historical_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            y=historical_data,
            name="Historical",
            line=dict(color="#4CAF50")
        ))
        fig.add_trace(go.Scatter(
            y=future_visitors,
            name="Predicted",
            line=dict(color="#FFA500", dash="dash")
        ))
        fig.update_layout(
            title="Visitor Trend and Prediction",
            xaxis_title="Months",
            yaxis_title="Visitors",
            template="plotly_dark",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top 5 busiest places with enhanced visualization
        st.subheader("Top 5 Busiest Places")
        top_places = city_data.nlargest(5, 'monthly_visitors')
        fig = px.bar(
            top_places,
            x='place_name',
            y='monthly_visitors',
            title="Top 5 Busiest Places",
            labels={'place_name': 'Place', 'monthly_visitors': 'Monthly Visitors'},
            template="plotly_dark",
            color='monthly_visitors',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Weather Analysis")
        
        # Temperature trend with enhanced gauge
        temp_range = city_data['temperature_trend'].iloc[0].split('-')
        min_temp, max_temp = map(int, temp_range)
        
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=(min_temp + max_temp) / 2,
            title={'text': "Average Temperature (°C)"},
            gauge={
                'axis': {'range': [min_temp, max_temp]},
                'bar': {'color': "#4CAF50"},
                'steps': [
                    {'range': [min_temp, (min_temp + max_temp)/2], 'color': "lightgray"},
                    {'range': [(min_temp + max_temp)/2, max_temp], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': (min_temp + max_temp) / 2
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
        
        # Rainfall and best time with enhanced cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                create_metric_card(
                    "Historical Rainfall",
                    f"{city_data['historical_rainfall'].iloc[0]} mm"
                ),
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                create_metric_card(
                    "Best Time to Visit",
                    city_data['best_time_to_visit'].iloc[0]
                ),
                unsafe_allow_html=True
            )
    
    with tab3:
        st.subheader("Category Distribution")
        
        # Category distribution with enhanced pie chart
        category_counts = city_data['category'].value_counts()
        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title="Category Distribution",
            template="plotly_dark",
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
        # Type distribution with enhanced bar chart
        type_counts = city_data['type'].value_counts()
        fig = px.bar(
            x=type_counts.index,
            y=type_counts.values,
            title="Type Distribution",
            labels={'x': 'Type', 'y': 'Count'},
            template="plotly_dark",
            color=type_counts.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Place Clustering")
        
        # Enhanced scatter plot
        fig = px.scatter(
            city_data,
            x='longitude',
            y='latitude',
            color='category',
            size='monthly_visitors',
            hover_data=['place_name', 'type', 'monthly_visitors'],
            title="Place Distribution Map",
            template="plotly_dark"
        )
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        st.plotly_chart(fig, use_container_width=True)

# City Comparison
elif page == "City Comparison":
    st.title("City Comparison")
    
    # Enhanced city selection
    selected_cities = st.multiselect(
        "Select Cities to Compare",
        options=df['city'].unique(),
        default=df['city'].unique()[:2],
        format_func=lambda x: f"🏙️ {x}"
    )
    
    if len(selected_cities) >= 2:
        # Compare total visitors with enhanced visualization
        st.subheader("Total Visitors Comparison")
        city_visitors = df[df['city'].isin(selected_cities)].groupby('city')['monthly_visitors'].sum()
        fig = px.bar(
            x=city_visitors.index,
            y=city_visitors.values,
            title="Total Monthly Visitors by City",
            labels={'x': 'City', 'y': 'Monthly Visitors'},
            template="plotly_dark",
            color=city_visitors.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Compare category distribution with enhanced visualization
        st.subheader("Category Distribution Comparison")
        category_data = df[df['city'].isin(selected_cities)].groupby(['city', 'category'])['monthly_visitors'].sum().reset_index()
        fig = px.bar(
            category_data,
            x='city',
            y='monthly_visitors',
            color='category',
            title="Category Distribution by City",
            labels={'x': 'City', 'y': 'Monthly Visitors'},
            template="plotly_dark",
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Compare weather conditions with enhanced cards
        st.subheader("Weather Conditions Comparison")
        weather_data = df[df['city'].isin(selected_cities)].groupby('city').agg({
            'historical_rainfall': 'first',
            'temperature_trend': 'first'
        }).reset_index()
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("Historical Rainfall (mm)")
            fig = px.bar(
                weather_data,
                x='city',
                y='historical_rainfall',
                template="plotly_dark",
                color='historical_rainfall',
                color_continuous_scale='Viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("Temperature Range (°C)")
            for _, row in weather_data.iterrows():
                st.markdown(
                    create_metric_card(
                        row['city'],
                        row['temperature_trend']
                    ),
                    unsafe_allow_html=True
                )

# About Page
elif page == "About":
    st.title("About Tourist Place Recommender")
    
    # Mission Section
    st.markdown("### Our Mission")
    st.markdown("To help travelers discover and explore the rich cultural heritage and beautiful destinations across India, making trip planning easier and more enjoyable.")
    
    # Developers Section
    st.markdown("### Meet the Developers")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class="developer-card">
                <h3>Sriram</h3>
                <p>Full Stack Developer</p>
                <p>Specialized in Python, Data Science, and Web Development</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="developer-card">
                <h3>Sahil Yadav</h3>
                <p>Data Scientist</p>
                <p>Expert in Machine Learning and Data Analytics</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("### Features")
    features = [
        "Smart place recommendations based on user preferences",
        "Interactive itinerary planning",
        "Real-time analytics and statistics",
        "Weather information and best time to visit",
        "City-wise comparison tools"
    ]
    for feature in features:
        st.markdown(f"- {feature}")
    
    # Technologies Section
    st.markdown("### Technologies Used")
    tech_stack = ["Python", "Streamlit", "Pandas", "NumPy", "Plotly", "Scikit-learn", "Matplotlib"]
    tech_cols = st.columns(4)
    for idx, tech in enumerate(tech_stack):
        with tech_cols[idx % 4]:
            st.markdown(f"""
                <div class="tech-item">
                    {tech}
                </div>
            """, unsafe_allow_html=True)
    
    # Contact Section
    st.markdown("### Contact")
    st.markdown("For any queries or suggestions, please reach out to us at:")
    st.markdown("Email: contact@touristrecommender.com")

if __name__ == "__main__":
    pass 