from src.extraction  import *
from src.transformation.cleaning import *
from src.transformation.validating import *
from src.transformation.features import *
from src.loading import *
from src.analytics.analytics import *
from src.database import *
import streamlit as st



def app():
    st.title("Weather & Risk Dashboard")
    st.write("Analyse des prévisions météorologiques et des niveaux de risque.")

    connection = connect_database(HOST, PORT, DATABASE, USER, PASSWORD)

    try:
        df = load_data(connection)
    finally:
        connection.close()

    df["forecast_date"] = pd.to_datetime(df["forecast_date"])

    st.sidebar.header("Filtres")

    cities = ["Toutes"] + sorted(df["city_name"].unique().tolist())

    selected_city = st.sidebar.selectbox("Ville", cities)

    min_date = df["forecast_date"].min().date()
    max_date = df["forecast_date"].max().date()

    selected_dates = st.sidebar.date_input(
        "Période",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    risk_levels = ["Tous", "low", "moderate", "high", "very_high"]

    selected_risk = st.sidebar.selectbox("Niveau de risque", risk_levels)

    filtered_df = df.copy()

app()