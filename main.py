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

    if selected_city != "Toutes": 
        filtered_df = filtered_df[filtered_df["city_name"] == selected_city]

    if len(selected_dates) == 2:
        start_date = pd.Timestamp(selected_dates[0])
        end_date = pd.Timestamp(selected_dates[1])

        filtered_df = filtered_df[(filtered_df["forecast_date"] >= start_date) & (filtered_df["forecast_date"] <= end_date)]

    if selected_risk != "Tous":
        filtered_df = filtered_df[filtered_df["risk_category"] == selected_risk]

    if filtered_df.empty:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
        return

    number_of_cities = filtered_df["city_name"].nunique()
    max_temperature = filtered_df["temperature_max"].max()
    max_precipitation = filtered_df["precipitation"].max()
    number_of_risk_periods = filtered_df[filtered_df["weather_risk_score"] >= 50].shape[0]
    highest_risk_city = (filtered_df.loc[filtered_df["weather_risk_score"].idxmax(), "city_name"])

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Nombre de villes", number_of_cities)
    col2.metric("Température maximale", f"{max_temperature:.1f} °C")
    col3.metric("Précipitations maximales", f"{max_precipitation:.1f} mm")
    col4.metric("Périodes à risque", number_of_risk_periods)
    col5.metric("Ville au risque le plus élevé", highest_risk_city)

    st.subheader("Évolution du risque")

    risk_chart = filtered_df[["forecast_date", "weather_risk_score"]].set_index("forecast_date")

app()