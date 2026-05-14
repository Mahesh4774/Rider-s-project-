import streamlit as st
from streamlit_folium import st_folium
from rider import analyze_route
from mapping import draw_map

st.set_page_config(page_title="Mischief", layout="wide")
st.title("Mischief")
st.caption("Find the fun route, not just the fast one")

col1, col2 = st.columns(2)
with col1:
    start = st.text_input("Start location", placeholder="e.g. Thrissur")
with col2:
    end = st.text_input("Destination", placeholder="e.g. Munnar")

if st.button("Analyze route"):
    with st.spinner("Analyzing route..."):
        result = analyze_route(start, end)

    st.session_state.result = result

if "result" in st.session_state:
    result = st.session_state.result

    st.subheader("Route analysis")
    st.metric("Total distance", f"{result['total_km']:.2f} km")
    st.metric("Twisty sections found", len(result["twisty_groups"]))


    m = draw_map(result["route"], result["twisty_groups"], result["rhythm_points"])
    st_folium(m, width=1200, height=600)