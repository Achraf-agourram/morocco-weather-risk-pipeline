
from src.database import *
import streamlit as st
import pydeck as pdk
import os
from dotenv import load_dotenv

load_dotenv()

def add_risk_color(df):
    def get_color(score):
        if score >= 80:
            return [230, 50, 50]

        if score >= 60:
            return [240, 130, 40]

        if score >= 40:
            return [240, 190, 50]

        if score >= 20:
            return [60, 180, 120]

        return [150, 210, 220]

    df["risk_color"] = df["weather_risk_score"].apply(get_color)

    return df

def app():
    st.title("Weather & Risk Dashboard")
    st.write("Analyse des prévisions météorologiques et des niveaux de risque.")

    try:
        connection = connect_database(os.getenv("DB_HOST"), os.getenv("DB_PORT"), os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"))
        df = load_data(connection)
        connection.close()
    except psycopg2.OperationalError as e:
        st.error("La connexion à la base de données a échoué, réessayer plus tard.")
        return

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


    filtered_df = add_risk_color(filtered_df)

    col_map, col_legend = st.columns([4, 1])

    with col_map:
        st.subheader("Carte des risques météorologiques")

        filtered_df = add_risk_color(filtered_df)

        map_layer = pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            get_position="[longitude, latitude]",
            get_fill_color="risk_color",
            get_radius=7000,
            pickable=True
        )

        map_view = pdk.ViewState(latitude=31.8, longitude=-7.1, zoom=5.2)

        map_deck = pdk.Deck(
            layers=[map_layer],
            initial_view_state=map_view,
            tooltip={
                "html": """
                    <b>{city_name}</b><br/>
                    Date: {forecast_date}<br/>
                    Risk: {weather_risk_score}/100<br/>
                    Catégorie: {risk_category}<br/>
                    Température: {temperature_max} °C<br/>
                    Précipitations: {precipitation} mm
                """
            }
        )

        st.pydeck_chart(map_deck, width="stretch")

    with col_legend:
        st.markdown("### Légende")
        st.markdown("""
        🔴 très élevé  80 - 100

        🟠 élevé  60 - 79

        🟡 moyen  40 - 59

        🟢 faible  20 - 39

        🔵 très faible  0 - 19
        """)
    

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
    st.line_chart(risk_chart)

    st.subheader("Températures")
    temperature_chart = filtered_df[["forecast_date", "temperature_max", "temperature_min"]].set_index("forecast_date")
    st.line_chart(temperature_chart)

    st.subheader("Précipitations")
    precipitation_chart = filtered_df[["forecast_date", "precipitation"]].set_index("forecast_date")
    st.bar_chart(precipitation_chart)


app()