import pandas as pd
import plotly.express as px
import streamlit as st

import config.settings
from config.logging_config import debug_log, setup_logging
from domain.facade.weather_facade import WeatherFacade
from domain.models.location import Location


class WebappUI:

    """
    Initialization of basic parameters and UI
    """

    def __init__(self):
        setup_logging()
        self.facade = WeatherFacade(api_name="open-meteo")
        st.set_page_config(layout="wide")  # this has to be the first st in the entire document?
        self._initialize_session()

    @debug_log
    def _initialize_session(self) -> None:
        st.session_state.setdefault("df", None)
        st.session_state.setdefault("location", None)
        st.session_state.setdefault("current_page", "summary")
        st.session_state.setdefault("time_interval", "Days")
        st.session_state.setdefault("last_fetch_params", None)

    @debug_log
    def render_ui(self) -> None:
        st.header("Weather App by J. Fiedler / Sorry4MyCode", divider="rainbow")
        self._sidebar()
        self._page_controls()
        self._current_page()

    @debug_log
    def _sidebar(self) -> None:
        with st.sidebar:
            st.subheader("Location Details")

            default_country = config.settings.default_country
            country = st.text_input("Country (*)", value=default_country).strip()

            default_postal_code = config.settings.default_postal_code
            postal_code = st.text_input("Postal Code", value=default_postal_code).strip()

            default_city = config.settings.default_city
            city = st.text_input("City", value=default_city).strip()

            st.divider()
            st.subheader("Forecast Details")

            time_interval = st.selectbox("Time Interval", ["Days", "Hours"], key="time_interval")

            duration = st.slider("Time span (Days)", min_value=-7, max_value=7, step=1, value=(-7, 7))

            st.divider()

            if st.button("Go", type="primary"):
                if self._validate_input(country=country, postal_code=postal_code, city=city):
                    if st.session_state.location is None:
                        location = self._get_location(country=country, postal_code=postal_code, city=city)
                        st.session_state.location = location  # Update session state with the new location
                    else:
                        location = st.session_state.location
                    self._fetch_weather(
                        location=location,
                        time_interval=time_interval,
                        duration=duration
                    )

            if st.session_state.df is not None:
                df = st.session_state.df
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="data.csv",
                    mime="text/csv",
                    icon=":material/download:",
                )

            self._refresh_data_automatically(duration=duration)

    @debug_log
    def _page_controls(self):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Summary View :bar_chart:", use_container_width=True):
                st.session_state.current_page = "summary"
        with col2:
            if st.button("Detailed Analysis :chart_with_upwards_trend:", use_container_width=True):
                st.session_state.current_page = "details"

    @debug_log
    def _current_page(self) -> None:
        if st.session_state.df is not None and st.session_state.location:
            if st.session_state.current_page == "summary":
                self._display_summary()
            else:
                self._display_details()
        else:
            st.info("Click 'Go' in the sidebar to fetch weather data")

    @debug_log
    def _refresh_data_automatically(self, duration) -> None:
        """
        this entire section is just to automatically refetch the data when time_interval or duration
        change, otherwise it throws harmless but annoying errors
        """
        if st.session_state.location is not None and st.session_state.df is not None:
            current_time_interval = st.session_state.time_interval
            current_duration = duration
            last_params = st.session_state.last_fetch_params

            if last_params:
                last_time_interval = last_params.get("time_interval")
                last_duration = last_params.get("duration")
                last_location = last_params.get("location")

                if (
                        current_time_interval != last_time_interval
                        or current_duration != last_duration
                        or st.session_state.location != last_location
                ):
                    self._fetch_weather(
                        location=st.session_state.location,
                        time_interval=current_time_interval.lower(),
                        duration=current_duration,
                    )

    """
    Input processing and fetch logic
    """

    @debug_log
    def _validate_input(self, country, postal_code, city) -> bool:
        if not country:
            st.error("Please enter a country.")
            return False
        if not postal_code and not city:
            st.error("Please enter at least a postal code or city.")
            return False
        return True

    @debug_log
    def _get_location(self, country, postal_code, city):
        return Location(country=country, postal_code=postal_code, city=city)

    @debug_log
    def _fetch_weather(self, location, time_interval, duration) -> None:
        try:
            df = self.facade.get_weather(
                location=location,
                time_interval=time_interval.lower(),
                duration=duration
            )
            df = df.reset_index()
            st.session_state.df = df

            st.session_state.last_fetch_params = {
                "time_interval": time_interval,
                "duration": duration,
                "location": location,
            }
        except Exception as e:
            st.error(f"Error fetching weather data: {str(e)}")

    @debug_log
    def _display_summary(self):
        st.subheader(f"Weather Summary {st.session_state.time_interval}")

        if st.session_state.time_interval == "Days":
            self._display_daily_summary()
        else:
            self._display_hourly_summary()

    @debug_log
    def _display_daily_summary(self):
        df = st.session_state.df
        # st.dataframe(df, use_container_width=True)

        with st.expander("Today's Weather :rainbow:", expanded=True):
            current_value = self._get_current(df=df)
            cols = st.columns(3)
            with cols[0]:
                st.metric("Temperature :thermometer:",
                          f"{current_value['temperature_2m_min']:.1f} - {current_value['temperature_2m_max']:.1f}°C")
                st.metric("Feels like :sweat_smile:",
                          f"{current_value['apparent_temperature_min']:.1f} - {current_value['apparent_temperature_max']:.1f}°C")
                st.metric("Humidity :sweat_drops:",
                          f"{current_value['relative_humidity_min']:.1f} - {current_value['relative_humidity_max']:.1f}%")
            with cols[1]:
                emoji = config.settings.weather_emojis.get(current_value['weather_code'], "❓")
                st.metric(f"Weather Code {emoji}", current_value['weather_code'])
                st.metric("Cloud Cover :cloud:",
                          f"{current_value['cloud_cover_min']:.1f} - {current_value['cloud_cover_max']:.1f} %")
                st.metric("Visibility :eyes:",
                          f"{current_value['visibility_min']:.1f} - {current_value['visibility_max']:.1f} m")
            with cols[2]:
                st.metric("Wind :wind_blowing_face:",
                          f"{current_value['wind_speed_10m_min']:.1f} - {current_value['wind_speed_10m_max']:.1f} km/h")
                wind_abbreviation = self._get_wind_direction(current_value['wind_direction_10m_dominant'])
                emoji = config.settings.wind_shortcodes.get(wind_abbreviation, ":question:")
                st.metric(f"Wind direction: {emoji}", f"{wind_abbreviation}")
                st.metric("Wind gusts :tornado:",
                          f"{current_value['wind_gust_10m_min']:.1f} - {current_value['wind_gust_10m_max']:.1f} km/h")

        with st.expander(label="Temperature :thermometer:", expanded=True):
            cols = st.columns(3)
            with cols[0]:
                st.metric("Lowest Temperature :snowflake:", f"{df['temperature_2m_min'].min():.1f}°C")
            with cols[1]:
                st.metric("Average Temperature :dart:", f"{df['temperature_2m_mean'].mean():.1f}°C")
            with cols[2]:
                st.metric("Max Temperature :fire:", f"{df['temperature_2m_max'].max():.1f}°C")

        with st.expander(label="Wind :wind_blowing_face:", expanded=True):
            cols = st.columns(3)
            with cols[0]:
                st.metric("Slowest Wind Speed", f"{df['wind_speed_10m_min'].min():.1f} km/h")
                st.metric("Slowest Wind Gusts", f"{df['wind_gust_10m_min'].min():.1f} km/h")
            with cols[1]:
                st.metric("Average Wind Speed", f"{df['wind_speed_10m_mean'].mean():.1f} km/h")
                st.metric("Average Wind Gusts", f"{df['wind_gust_10m_mean'].mean():.1f} km/h")
            with cols[2]:
                st.metric("Fastest Wind Speed", f"{df['wind_speed_10m_max'].max():.1f} km/h")
                st.metric("Fastest Wind Gusts", f"{df['wind_gust_10m_max'].max():.1f} km/h")

    @debug_log
    def _display_hourly_summary(self):
        df = st.session_state.df
        # st.dataframe(df, use_container_width=True)

        with st.expander("Current Weather :rainbow:", expanded=True):
            current_value = self._get_current(df=df)
            cols = st.columns(3)
            with cols[0]:
                st.metric("Temperature :thermometer:", f"{current_value['temperature_2m']:.1f}°C")
                st.metric("Feels like :sweat_smile:", f"{current_value['apparent_temperature_2m']:.1f}°C")
                st.metric("Humidity :sweat_drops:", f"{current_value['relative_humidity_2m']:.1f}%")
            with cols[1]:
                emoji = config.settings.weather_emojis.get(current_value['weather_code'], ":question:")
                st.metric(f"Weather Code {emoji}", current_value['weather_code'])
                st.metric("Cloud Cover :cloud:", f"{current_value['cloud_cover']:.1f}%")
                st.metric("Visibility :eyes:", f"{current_value['visibility']:.1f} m")
            with cols[2]:
                st.metric("Wind :wind_blowing_face:", f"{current_value['wind_speed_10m']:.1f} km/h")
                wind_abbreviation = self._get_wind_direction(current_value['wind_direction_10m_dominant'])
                emoji = config.settings.wind_shortcodes.get(wind_abbreviation, ":question:")
                st.metric(f"Wind direction: {emoji}", f"{wind_abbreviation}")
                st.metric("Wind gusts :tornado:", f"{current_value['wind_gust_10m']:.1f} km/h")

        with st.expander(label="Temperature :thermometer:", expanded=True):
            cols = st.columns(3)
            with cols[0]:
                st.metric("Lowest Temperature :snowflake:", f"{df['temperature_2m'].min():.1f}°C")
            with cols[1]:
                st.metric("Average Temperature :dart:", f"{df['temperature_2m'].mean():.1f}°C")
            with cols[2]:
                st.metric("Max Temperature :fire:", f"{df['temperature_2m'].max():.1f}°C")

        with st.expander(label="Wind :wind_blowing_face:", expanded=True):
            cols = st.columns(3)
            with cols[0]:
                st.metric("Slowest Wind Speed", f"{df['wind_speed_10m'].min():.1f} km/h")
                st.metric("Slowest Wind Gusts", f"{df['wind_gust_10m'].min():.1f} km/h")
            with cols[1]:
                st.metric("Average Wind Speed", f"{df['wind_speed_10m'].mean():.1f} km/h")
                st.metric("Average Wind Gusts", f"{df['wind_gust_10m'].mean():.1f} km/h")
            with cols[2]:
                st.metric("Fastest Wind Speed", f"{df['wind_speed_10m'].max():.1f} km/h")
                st.metric("Fastest Wind Gusts", f"{df['wind_gust_10m'].max():.1f} km/h")

    @debug_log
    def _display_details(self):
        st.subheader("Detailed Analysis")
        if st.session_state.time_interval == "Days":
            self._display_daily_details()
        else:
            self._display_hourly_details()

    @debug_log
    def _display_daily_details(self):
        df = st.session_state.df
        # st.dataframe(df, use_container_width=True)

        # Tabs with loop-based plotting
        tabs = st.tabs(["Temperature", "Precipitation", "Wind", "Visibility & Clouds", "Wind Gusts"])
        plots = [
            {"tab": 0, "title": "Temperature Over Time",
             "cols": ['temperature_2m_min', 'temperature_2m_max', 'temperature_2m_mean'],
             "y_label": "Temperature (°C)"},
            {"tab": 0, "title": "Apparent Temperature Over Time",
             "cols": ['apparent_temperature_min', 'apparent_temperature_max', 'apparent_temperature_mean'],
             "y_label": "Apparent Temp (°C)"},
            {"tab": 1, "title": "Precipitation Types", "cols": ['rain_sum', 'snowfall_sum', 'showers_sum'],
             "y_label": "Amount (mm)", "kind": "bar"},
            {"tab": 2, "title": "Wind Speed Over Time",
             "cols": ['wind_speed_10m_min', 'wind_speed_10m_max', 'wind_speed_10m_mean'], "y_label": "Speed (km/h)"},
            {"tab": 3, "title": "Visibility Over Time", "cols": ['visibility_min', 'visibility_max', 'visibility_mean'],
             "y_label": "Visibility (m)"},
            {"tab": 3, "title": "Cloud Cover Over Time",
             "cols": ['cloud_cover_min', 'cloud_cover_max', 'cloud_cover_mean'], "y_label": "Cloud (%)"},
            {"tab": 4, "title": "Wind Gusts Over Time",
             "cols": ['wind_gust_10m_min', 'wind_gust_10m_max', 'wind_gust_10m_mean'], "y_label": "Gust Speed (km/h)"},
        ]

        self._plot_data(df, tabs, plots)

    @debug_log
    def _display_hourly_details(self):
        df = st.session_state.df
        # st.dataframe(df, use_container_width=True)

        tabs = st.tabs(["Temperature", "Precipitation", "Wind", "Visibility & Clouds", "Wind Gusts"])
        plots = [
            {"tab": 0, "title": "Temperature vs Apparent Temperature",
             "cols": ['temperature_2m', 'apparent_temperature_2m'],
             "y_label": "Temperature (°C)"},
            {"tab": 1, "title": "Precipitation Over Time",
             "cols": ['rain', 'shower', 'snowfall'],
             "y_label": "Amount mm", "kind": "bar"},
            {"tab": 2, "title": "Wind Over Time",
             "cols": ['wind_speed_10m'],
             "y_label": "Wind Speed (km/h)"},
            {"tab": 3, "title": "Visibility Over Time",
             "cols": ['visibility'],
             "y_label": "Visibility (m)"},
            {"tab": 3, "title": "Cloud Cover Over Time",
             "cols": ['cloud_cover_high', 'cloud_cover_mid', 'cloud_cover_low'],
             "y_label": "Cloud (%)"},
            {"tab": 4, "title": "Wind Gusts Over Time",
             "cols": ['wind_gust_10m'],
             "y_label": "Gust Speed (km/h)"}
        ]

        self._plot_data(df, tabs, plots)

    @debug_log
    def _get_current(self, df):
        # Work on a copy and ensure timestamps are parsed
        df = df.copy()
        df["timestamp"] = pd.to_datetime(df["timestamp"])  # Result looks the same, modern Python uses types
        timestamps = df["timestamp"]

        # Keep timezone if present
        now = pd.Timestamp.now(tz=timestamps.dt.tz)

        # Daily
        if timestamps.dt.hour.nunique() == 1:
            today = now.normalize()
            is_today = timestamps.dt.normalize() == today
            if is_today.any():
                # If today is found, use today
                return df.loc[is_today].iloc[0]
            else:
                # Fallback, just take the last available day if you can not find today
                past = df[timestamps <= now]
                if not past.empty:
                    return past.iloc[-1]
                '''
                Before the front-end crashes just return the first row of the dataset.
                This should never be executed as long as the backend is not faulty
                '''
                return df.iloc[0]
        else:  # Hourly
            df["time_diff"] = (timestamps - now).abs()
            best_idx = df["time_diff"].idxmin()
            return df.loc[best_idx]

    @debug_log
    def _get_wind_direction(self, degree):
        directions = [
            "N", "NNE", "NE", "ENE",
            "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW",
            "W", "WNW", "NW", "NNW"
        ]
        normalized_degree = degree % 360
        index = int((normalized_degree + 11.25) / 22.5) % 16
        return directions[index]

    @debug_log
    def _plot_data(self, df, tabs, plots):
        for spec in plots:
            with tabs[spec['tab']]:
                with st.expander(label=spec['title'], expanded=True):
                    st.header(spec['title'])
                    kind = spec.get('kind', 'line')
                    fig = (
                        px.bar(df, x='timestamp', y=spec['cols'], title=spec['title'],
                               labels={'value': spec['y_label']})
                        if kind == 'bar'
                        else px.line(df, x='timestamp', y=spec['cols'], title=spec['title'],
                                     labels={'value': spec['y_label']})
                    )
                    fig.update_layout(
                        hovermode='x unified',
                        legend_title=None,
                        margin=dict(t=40, r=20, l=20, b=20)
                    )
                    fig.update_xaxes(rangeslider_visible=True)
                    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    app = WebappUI()
    app.render_ui()
