<img width="2940" height="1822" alt="image" src="https://github.com/user-attachments/assets/906d8327-cc84-4470-8998-3bd2dcb70f07" /># Dublin Bikes Web Application

A full-stack web application for real-time Dublin Bikes station monitoring, built as part of the COMP30830 Software Engineering module at University College Dublin.

---

## Features

- **Interactive Map** — View all Dublin Bikes stations on a Google Maps interface
- **Real-time Availability** — Live bike and stand counts for every station
- **Weather Widget** — Current Dublin weather conditions displayed alongside station data
- **Availability History** — Chart showing the last 48 data points for any selected station
- **ML Prediction** — Gradient Boosting model predicting future bike availability
- **User Authentication** — Register, log in, and log out with secure password hashing

---

## Screenshots

> **Map View**
>
> *<img width="2940" height="1822" alt="image" src="https://github.com/user-attachments/assets/2984cc44-3801-4664-8a5e-f105fdc20d11" />
*

> **Station Detail Panel**
>
> *<img width="674" height="1294" alt="image" src="https://github.com/user-attachments/assets/08e392ac-1632-4ead-aef8-84946ed0b267" />
*

> **Availability History Chart**
>
> *<img width="672" height="1302" alt="image" src="https://github.com/user-attachments/assets/52b8d80d-ffde-4e94-90b9-4cbc891810b7" />
*

> **Login / Register Page**
>
> *<img width="2906" height="1490" alt="image" src="https://github.com/user-attachments/assets/b27dd278-d1b7-40fb-aa09-91283529302e" />
<img width="2910" height="1444" alt="image" src="https://github.com/user-attachments/assets/e3a91346-d197-4ed0-b675-e0335fabbd74" />

*

---

## Tech Stack

| Layer     | Technology                                  |
|-----------|---------------------------------------------|
| Backend   | Python 3, Flask, SQLAlchemy                 |
| Database  | MySQL 8.0                                   |
| Auth      | Flask-Login, Werkzeug                       |
| Frontend  | Vanilla JS (ES Modules), Google Maps API    |
| ML Model  | scikit-learn (GradientBoostingRegressor)    |
| Config    | python-dotenv                               |

---

## Project Structure

```
comp30830/
├── myapp/
│   ├── run.py              # App entry point
│   ├── config.py           # Dev / Test / Production configs
│   └── app/
│       ├── __init__.py     # App factory
│       ├── db.py           # SQLAlchemy engine (per-request caching)
│       ├── models.py       # User model (Flask-Login)
│       ├── api/            # REST API blueprint
│       │   └── routes.py
│       ├── auth/           # Login / Register / Logout blueprint
│       │   └── routes.py
│       ├── main/           # Main page blueprint
│       │   └── routes.py
│       ├── ml/             # Trained model files (.pkl)
│       ├── static/
│       │   ├── css/
│       │   └── js/         # ES module JS (map, chart, UI, API client)
│       └── templates/      # Jinja2 HTML templates
├── bikes_database.sql      # Database schema
├── ml_bike_prediction.ipynb # Model training notebook
├── data/                   # Raw scraped bike data
└── weather_data/           # Raw scraped weather data
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- MySQL 8.0+
- A Google Maps API key
- An OpenWeatherMap API key (for the data scraper)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/QAQcarry/comp30830-project.git
cd comp30830
```

**2. Install Python dependencies**

```bash
pip install flask flask-login sqlalchemy pymysql werkzeug python-dotenv scikit-learn pandas requests
```

**3. Set up the database**

```bash
mysql -u <your_user> -p < bikes_database.sql
```

**4. Configure environment variables**

Create a `.env` file in the `myapp/` directory (copy the template below):

```env
SECRET_KEY=your-secret-key-here

DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bikes

GOOGLE_MAPS_KEY=your_google_maps_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
```

> All keys are required. The app will fail to start without `SECRET_KEY`, `DB_*`, and `GOOGLE_MAPS_KEY`.

**5. Run the application**

```bash
cd myapp
python run.py
```

The app will be available at `http://127.0.0.1:5000`.

---

## API Endpoints

All endpoints require authentication. Log in via the `/auth/login` page first, then use the same session to call these endpoints.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/stations` | All station metadata |
| GET | `/api/available/all` | Latest availability for every station |
| GET | `/api/available/<id>` | Latest availability for a single station |
| GET | `/api/available/<id>/history` | Last 48 availability records for a station |
| GET | `/api/weather` | Most recent weather record |

---

## Machine Learning

The prediction model is a **Gradient Boosting Regressor** trained on historical availability data scraped at 5-minute intervals. The trained model (`bike_availability_model.pkl`) and feature list (`model_features.pkl`) are stored in `myapp/app/ml/`. See `ml_bike_prediction.ipynb` for the full training pipeline.

---

## Team

| Name | 
|------|
| *Mutian Xu* | 
| *Wenfei Song* | 
| *John Shannon* | 

---

## License

This project was developed for academic purposes as part of COMP30830 at University College Dublin.
