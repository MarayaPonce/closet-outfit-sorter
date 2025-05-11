import streamlit as st
import requests
from datetime import datetime, timedelta
from typing import List, Dict
from wardrobe import Wardrobe  # your class from wardrobe.py

# --- CONFIG ---
API_KEY = st.secrets ["api"]["API_KEY"]
UNITS = 'metric'
STYLE_OPTIONS = ["sporty", "formal / elegant", "day-to-day", "day event", "night event"]

# --- Initialize Wardrobe ---
if "wardrobe" not in st.session_state:
    st.session_state.wardrobe = Wardrobe("closet.csv")

if "wardrobe_data" not in st.session_state:
    st.session_state.wardrobe_data = st.session_state.wardrobe.get_items()

# --- Weather + Outfit Suggestion Functions ---
def get_tomorrow_weather_tags(city: str, api_key: str) -> List[str]:
    if not api_key:
        raise ValueError("API key must be provided for weather lookup.")
    
    assert not city.isnumeric(), "City name cannot be purely numeric."

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
        try:
            if not name:
                raise ValueError("Clothing name cannot be empty.")
            if not type_:
                raise ValueError("Clothing type cannot be empty")
            assert not name.isnumeric(), "Clothing name cannot be numeric."
            assert len(name) <= 50
            assert len(type_) <= 30
            assert len(brand) <= 50

            item = {
                "name": name,
                "type": type_,
                "color": color,
                "tags": tags,
                "brand": brand.strip()
            }

            st.session_state.wardrobe.add_item(item)
            st.session_state.wardrobe_data = st.session_state.wardrobe.get_items()
            st.success(f"Item saved: {name}")
        except (AssertionError, ValueError) as e:
            st.error(str(e))

elif page == "View Wardrobe":
    st.header("👚 All Saved Items")
    wardrobe = st.session_state.wardrobe_data

    if not wardrobe:
        st.info("No clothing items saved yet.")
    else:
        with st.expander("🔍 Filter items"):
            colors = sorted(set(item["color"] for item in wardrobe if item["color"]))
            types = sorted(set(item["type"] for item in wardrobe if item["type"]))
            brands = sorted(set(item["brand"] for item in wardrobe if item["brand"]))
            all_tags = sorted(set(tag for item in wardrobe for tag in item["tags"]))

            selected_colors = st.multiselect("Filter by Color", colors, key="color_filter")
            selected_types = st.multiselect("Filter by Type", types, key="type_filter")
            selected_brands = st.multiselect("Filter by Brand", brands, key="brand_filter")
            selected_tags = st.multiselect("Filter by Style Tags", all_tags, key="tag_filter")

            if st.button("Reset Filters"):
                st.session_state.color_filter = []
                st.session_state.type_filter = []
                st.session_state.brand_filter = []
                st.session_state.tag_filter = []

            filtered_wardrobe = [
                item for item in wardrobe
                if (not selected_colors or item["color"] in selected_colors)
                and (not selected_types or item["type"] in selected_types)
                and (not selected_brands or item["brand"] in selected_brands)
                and (not selected_tags or any(tag in item["tags"] for tag in selected_tags))
            ]

        cols = st.columns(3)
        if not filtered_wardrobe:
            st.warning("No items match the selected filters.")
        for idx, item in enumerate(filtered_wardrobe):
            with cols[idx % 3]:
                st.markdown(f"**👕 {item['name']}**")
                st.markdown(f"- Type: `{item['type']}`")
                st.markdown(f"- Color: `{item['color']}`")
                st.markdown(f"- Tags: `{', '.join(item['tags'])}`")
                if item['brand']:
                    st.markdown(f"- Brand: `{item['brand']}`")
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
            st.subheader("Recommended Outfit:")
            for item in outfit:
                st.markdown(f"**👕 {item['name']}** - `{item['type']}`, `{item['color']}`")
        else:
            st.warning("No suitable outfit found.")


