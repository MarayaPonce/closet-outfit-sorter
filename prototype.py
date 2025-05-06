
import streamlit as st
import requests
from datetime import datetime, timedelta
from typing import List, Dict

# --- CONFIG ---
API_KEY = '2a7866daf05f37f889e8d6f275122659'
UNITS = 'metric'
STYLE_OPTIONS = ["sporty", "formal / elegant", "day-to-day", "day event", "night event"]

# Initialize wardrobe in session state
if "wardrobe_data" not in st.session_state:
    st.session_state.wardrobe_data = [
        {"name": "Black Blazer", "type": "jacket", "tags": ["formal / elegant", "cold"], "color": "black", "brand": "Zara"},
        {"name": "White Shirt", "type": "top", "tags": ["formal / elegant"], "color": "white", "brand": "H&M"},
        {"name": "Jeans", "type": "bottom", "tags": ["day-to-day"], "color": "blue", "brand": ""},
        {"name": "Raincoat", "type": "jacket", "tags": ["day-to-day", "rain"], "color": "blue", "brand": "Decathlon"},
        {"name": "Sweater", "type": "top", "tags": ["day-to-day", "cold"], "color": "gray", "brand": ""},
    ]

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
    tags = st.multiselect("Select style tags", STYLE_OPTIONS)
    brand = st.text_input("Brand (optional)", value="")

    if st.button("Save Item"):
        item = {
            "name": name,
            "type": type_,
            "color": color,
            "tags": tags,
            "brand": brand.strip()
        }
        st.session_state.wardrobe_data.append(item)
        st.success(f"Item saved: {name}")

elif page == "View Wardrobe":
    st.header("👚 All Saved Items")
    if not st.session_state.wardrobe_data:
        st.info("No clothing items saved yet.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(st.session_state.wardrobe_data):
            with cols[idx % 3]:
                st.markdown(f"**👕 {item['name']}**")
                st.markdown(f"- Type: `{item['type']}`")
                st.markdown(f"- Color: `{item['color']}`")
                st.markdown(f"- Tags: `{', '.join(item['tags'])}`")
                if item['brand']:
                    st.markdown(f"- Brand: `{item['brand']}`")
                if st.button("🗑️ Delete", key=f"delete_{idx}"):
                    st.session_state.wardrobe_data.pop(idx)
                    st.rerun()
                st.markdown("---")

elif page == "Suggest Outfit":
    st.header("🎯 Smart Outfit Recommender")
    event = st.selectbox("What kind of event are you dressing for?", STYLE_OPTIONS)
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

