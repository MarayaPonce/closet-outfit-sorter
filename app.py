import streamlit as st
import requests
from datetime import datetime, timedelta
from typing import List, Dict

# --- CONFIG ---
API_KEY = '2a7866daf05f37f889e8d6f275122659'
UNITS = 'metric'

# Initialize wardrobe in session state
if "wardrobe_data" not in st.session_state:
    st.session_state.wardrobe_data = []

# --- Weather + Outfit Suggestion Functions ---
def get_tomorrow_weather_tags(city: str, api_key: str) -> List[str]:
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={UNITS}"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Weather API error: " + response.json().get("message", "Unknown error"))
        return []

    data = response.json()
    tomorrow = (datetime.utcnow() + timedelta(days=1)).date()
    temps = []
    tags = set()

    for item in data["list"]:
        forecast_time = datetime.fromtimestamp(item["dt"])
        if forecast_time.date() == tomorrow:
            temp = item["main"]["temp"]
            condition = item["weather"][0]["main"].lower()
            temps.append(temp)
            if "rain" in condition:
                tags.add("rain")
            if "snow" in condition:
                tags.add("cold")

    if temps:
        avg_temp = sum(temps) / len(temps)
        if avg_temp < 10:
            tags.add("cold")
        elif avg_temp > 25:
            tags.add("hot")
        else:
            tags.add("mild")

    return list(tags)

def suggest_outfit(event_tag: str, weather_tags: List[str], closet: List[Dict]) -> List[Dict]:
    outfit = []
    used_types = set()
    for item in closet:
        if event_tag in item["tags"] or any(tag in item["tags"] for tag in weather_tags):
            if item["type"] not in used_types:
                outfit.append(item)
                used_types.add(item["type"])
    return outfit

# --- Streamlit UI ---
st.title("👗 Your Digital Wardrobe")

page = st.sidebar.radio("Menu", ["Add Clothing Item", "View Wardrobe", "Suggest Outfit"])

if page == "Add Clothing Item":
    st.header("Add a New Clothing Item")
    name = st.text_input("Name")
    type_ = st.text_input("Type (top, bottom, etc.)")
    color = st.text_input("Color")
    tags_input = st.text_input("Tags (comma-separated)")
    custom_tag = st.text_input("Custom Tag")

    if st.button("Save Item"):
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        item = {
            "name": name,
            "type": type_,
            "color": color,
            "tags": tags,
            "custom_tag": custom_tag
        }
        st.session_state.wardrobe_data.append(item)
        st.success(f"Item saved: {name}")

elif page == "View Wardrobe":
    st.header("👚 All Saved Items")
    if not st.session_state.wardrobe_data:
        st.info("No clothing items saved yet.")
    else:
        for i, item in enumerate(st.session_state.wardrobe_data, 1):
            st.markdown(f"### Item {i}")
            st.write(f"**Name:** {item['name']}")
            st.write(f"**Type:** {item['type']}")
            st.write(f"**Color:** {item['color']}")
            st.write(f"**Tags:** {', '.join(item['tags'])}")
            st.write(f"**Custom Tag:** {item['custom_tag']}")
            st.markdown("---")

elif page == "Suggest Outfit":
    st.header("🎯 Smart Outfit Recommender")
    event = st.selectbox("What kind of event are you dressing for?", ["formal", "casual", "sporty"])
    city = st.text_input("Enter your city for weather forecast:", "Madrid")

    if st.button("Suggest Based on Tomorrow's Weather"):
        weather_tags = get_tomorrow_weather_tags(city, API_KEY)
        st.markdown(f"**Weather tags for tomorrow in {city}:** `{', '.join(weather_tags)}`")

        outfit = suggest_outfit(event, weather_tags, st.session_state.wardrobe_data)

        if outfit:
            st.success("Here's your suggested outfit:")
            for item in outfit:
                st.write(f"👕 **{item['name']}** — Type: {item['type']}, Tags: {', '.join(item['tags'])}")
        else:
            st.warning("No suitable outfit found in your wardrobe.")

