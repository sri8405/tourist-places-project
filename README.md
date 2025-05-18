# Tourist Place Recommender

A modern web application for recommending tourist places and planning itineraries in Indian cities.

## Features

- City-based tourist place recommendations
- Interactive itinerary planning
- Real-time analytics and statistics
- Modern dark-themed UI with animations
- Responsive design for all devices

## Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd tourist-recommender
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

## Deployment

### Deploying to Streamlit Cloud

1. Create a GitHub repository and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <repository-url>
git push -u origin main
```

2. Go to [Streamlit Cloud](https://streamlit.io/cloud)

3. Sign in with your GitHub account

4. Click "New app"

5. Select your repository, branch, and main file (app.py)

6. Click "Deploy"

### Deploying to Heroku

1. Create a `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

2. Create a `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

3. Install the Heroku CLI and login:
```bash
heroku login
```

4. Create a new Heroku app:
```bash
heroku create your-app-name
```

5. Deploy to Heroku:
```bash
git push heroku main
```

### Deploying to AWS

1. Create an EC2 instance

2. Install required packages:
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv nginx
```

3. Clone your repository and set up the environment:
```bash
git clone <repository-url>
cd tourist-recommender
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Set up Nginx as a reverse proxy:
```bash
sudo nano /etc/nginx/sites-available/streamlit
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

5. Enable the site and restart Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/streamlit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. Run the application:
```bash
streamlit run app.py
```

## Environment Variables

Create a `.env` file with the following variables:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Data Structure

The application uses a CSV file (`data/top_indian_places.csv`) containing information about tourist places in major Indian cities, including:
- Place name
- Category
- Monthly visitors
- Location coordinates
- Type
- Best time to visit
- Historical rainfall data
- Temperature trends

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Plotly
- Scikit-learn

## Usage

1. Select a city from the available options
2. View recommended tourist places
3. Generate custom itineraries based on number of days
4. Explore analytics and statistics
5. Check weather information and best times to visit

## Contributing

Feel free to submit issues and enhancement requests! 