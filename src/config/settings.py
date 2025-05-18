# Agent used for Api-Calls
agent_name = "Weather_App_Fiedler"

# Caching Strategy
cache_name = ".cache"
expiration_cache = 3600
retries_cache = 5
backoff_factor_cache = 0.2

# Default UI Values
default_country = "Germany"
default_city = "Saarbrücken"
default_postal_code = "66111"

# Parameters used for open-meteo, modifying those will most likely break the code. I will not fix any errors occurring because of this!
daily_params = ["temperature_2m_max", "temperature_2m_min", "weather_code", "apparent_temperature_max",
                "apparent_temperature_min", "apparent_temperature_mean", "temperature_2m_mean", "rain_sum",
                "showers_sum", "snowfall_sum", "wind_speed_10m_max", "wind_direction_10m_dominant", "visibility_max",
                "visibility_min", "visibility_mean", "wind_speed_10m_mean", "wind_speed_10m_min", "wind_gusts_10m_min",
                "wind_gusts_10m_max", "wind_gusts_10m_mean", "relative_humidity_2m_min", "relative_humidity_2m_max",
                "relative_humidity_2m_mean", "cloud_cover_mean", "cloud_cover_max", "cloud_cover_min"]
# Parameters used for open-meteo, modifying those will most likely break the code. I will not fix any errors occurring because of this!
hourly_params = ["temperature_2m", "weather_code", "apparent_temperature", "relative_humidity_2m", "snowfall",
                 "showers", "rain", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "cloud_cover",
                 "visibility", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"]

# Shortcodes used by Streamlit for the Weather
weather_emojis = {
    0: ":sunny:",
    1: ":sun_behind_cloud:",
    2: ":partly_sunny:",
    3: ":cloud:",
    45: ":fog:",
    48: ":fog:",
    51: ":cloud_with_drizzle:",
    53: ":cloud_with_drizzle:",
    55: ":cloud_with_drizzle:",
    56: ":cloud_with_snow:",
    57: ":cloud_with_snow:",
    61: ":sun_behind_rain_cloud:",
    63: ":cloud_with_rain:",
    65: ":cloud_with_rain:",
    66: ":cloud_with_snow:",
    67: ":cloud_with_snow:",
    71: ":snowflake:",
    73: ":snowflake:",
    75: ":snowflake:",
    77: ":cloud_with_snow:",
    80: ":sun_behind_rain_cloud:",
    81: ":cloud_with_rain:",
    82: ":cloud_with_rain:",
    85: ":cloud_with_snow:",
    86: ":cloud_with_snow:",
    95: ":cloud_with_lightning_and_rain:",
    96: ":cloud_with_lightning_and_rain:",
    99: ":cloud_with_lightning_and_rain:",
}
# Shortcodes used by Streamlit for the Wind
wind_shortcodes = {
    "N": ":arrow_up:",  # 348.75°–11.25°
    "NNE": ":arrow_upper_right:",  # 11.25°–33.75°
    "NE": ":arrow_upper_right:",  # 33.75°–56.25°
    "ENE": ":arrow_upper_right:",  # 56.25°–78.75°
    "E": ":arrow_right:",  # 78.75°–101.25°
    "ESE": ":arrow_lower_right:",  # 101.25°–123.75°
    "SE": ":arrow_lower_right:",  # 123.75°–146.25°
    "SSE": ":arrow_lower_right:",  # 146.25°–168.75°
    "S": ":arrow_down:",  # 168.75°–191.25°
    "SSW": ":arrow_lower_left:",  # 191.25°–213.75°
    "SW": ":arrow_lower_left:",  # 213.75°–236.25°
    "WSW": ":arrow_lower_left:",  # 236.25°–258.75°
    "W": ":arrow_left:",  # 258.75°–281.25°
    "WNW": ":arrow_upper_left:",  # 281.25°–303.75°
    "NW": ":arrow_upper_left:",  # 303.75°–326.25°
    "NNW": ":arrow_upper_left:",  # 326.25°–348.75°
}
