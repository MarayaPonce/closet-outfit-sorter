
import streamlit as st

# List to hold saved clothing items (in session state for persistence)
if "wardrobe_data" not in st.session_state:
    st.session_state.wardrobe_data = []

# Title
st.title("👗 Your Digital Wardrobe")

# Sidebar navigation
page = st.sidebar.radio("Menu", ["Add Clothing Item", "View Wardrobe"])

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

