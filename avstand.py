import streamlit as st
import json

@st.cache_data
def import_data(filename):
    with open(filename) as file:
        content = file.read()
    output = json.loads(content)
    return output

def fetch_data():
    st.session_state.geodata = import_data("tatorter_distance.json")
    st.session_state.valid_geo = list(st.session_state.geodata.keys())

def show_initial_information():
    st.logo("af-logotyp-rgb-540px.jpg")
    st.title("Avstånd mellan orter")
    initial_text = "Fågelvägen"
    st.markdown(f"<p style='font-size:12px;'>{initial_text}</p>", unsafe_allow_html=True)

def initiate_session_state():
    if "valid_geo" not in st.session_state:
        st.session_state.valid_geo = []

def create_string(skills, start):
    if start:
        strings = [f"<strong>{start}</strong><br />"]
    else:
        strings = []
    for s in skills:
        strings.append(s)
    string = "<br />".join(strings)
    skill_string = f"<p style='font-size:16px;'>{string}</p>"
    return skill_string

def create_maxlist(data, max):
    output = []
    for place, distance in data.items():
        if distance >= max[0] and distance <= max[1]:
            output.append(f"{place} - {distance} km")
    return output

def choose_geo():
    show_initial_information()
    max_distance = st.slider("Minimalt och maximalt avstånd", 0, 100, (20, 30))
    valid_geos = sorted(st.session_state.valid_geo)
    selected_geo = st.selectbox(
        "Välj en ort",
        (valid_geos), placeholder = "", index = None)
    if selected_geo:
        other_geo = st.session_state.geodata.get(selected_geo)
        maxlist = create_maxlist(other_geo, max_distance)
        geo_string = create_string(maxlist, "Orter inom ditt valda avstånd:")
        st.markdown(geo_string, unsafe_allow_html = True)

def main ():
    initiate_session_state()
    fetch_data()
    choose_geo()

if __name__ == '__main__':
    main ()