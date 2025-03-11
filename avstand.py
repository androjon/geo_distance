import streamlit as st
import json
import operator

@st.cache_data
def import_data(filename):
    with open(filename) as file:
        content = file.read()
    output = json.loads(content)
    return output

def fetch_data():
    st.session_state.distance = import_data("tatorter_distance.json")
    st.session_state.locations_id = import_data("ortnamn_id.json")
    st.session_state.id_locations = import_data("id_ortnamn.json")
    st.session_state.valid_locations = list(st.session_state.locations_id.keys())
    st.session_state.geodata = import_data("tatorter_distance.json")
    st.session_state_ad_data = import_data("yb_ort_annonser_nu_2024.json")
    st.session_state.occupationdata = import_data("valid_occupations_with_info_25.json")
    for key, value in st.session_state.occupationdata.items():
        st.session_state.valid_occupations[value["preferred_label"]] = key

def show_initial_information():
    st.logo("af-logotyp-rgb-540px.jpg")
    st.title("Avstånd mellan orter")
    initial_text = "Fågelvägen"
    st.markdown(f"<p style='font-size:12px;'>{initial_text}</p>", unsafe_allow_html=True)

def initiate_session_state():
    if "valid_occupations" not in st.session_state:
        st.session_state.valid_occupations = {}

def create_string(data, start):
    if start:
        strings = [f"<strong>{start}</strong><br />"]
    else:
        strings = []
    for i in data:
        strings.append(i)
    string = "<br />".join(strings)
    skill_string = f"<p style='font-size:16px;'>{string}</p>"
    return skill_string

def create_maxlist(data, max):
    output = []
    alla_nu = 0
    alla_historiskt= 0
    for i in data:
        if i["avstånd"] <= max:
            alla_nu += i["nu"]
            alla_historiskt += i["historiskt"]

            output.append(f"{i['ort']} ({i['nu']}, {i['historiskt']}) - {i['avstånd']} km")

    return output, alla_nu, alla_historiskt

def choose_geo():
    show_initial_information()

    valid_occupations = list(st.session_state.valid_occupations.keys())
    valid_occupations = sorted(valid_occupations)
    selected_occupation_name = st.selectbox(
        "Välj en yrkesbenämning",
        (valid_occupations), placeholder = "", index = None)
    if selected_occupation_name:
        id_selected_occupation = st.session_state.valid_occupations.get(selected_occupation_name)
        ads_occupation = st.session_state_ad_data.get(id_selected_occupation)

        valid_locations = sorted(st.session_state.valid_locations)
        selected_location = st.selectbox(
            "Välj en ort",
            (valid_locations), placeholder = "", index = None)

        if selected_location:
            id_selected_location = st.session_state.locations_id.get(selected_location) 
            other_locations = st.session_state.geodata.get(id_selected_location)

            locations_with_distance = []

            ads_selected = ads_occupation.get(id_selected_location)
            if not ads_selected:
                ads_selected = [0, 0]
            nu_grund = ads_selected[0]
            historiskt_grund = ads_selected[1]
            
            locations_with_distance.append({
                "ort": selected_location,
                "nu": ads_selected[0],
                "historiskt": ads_selected[1],
                "avstånd": 0})

            for location_id, distance in other_locations.items():
                ads_location = ads_occupation.get(location_id)
                if ads_location:
                    location_name = st.session_state.id_locations.get(location_id)
                    if location_name:
                        locations_with_distance.append({
                            "ort": location_name,
                            "nu": ads_location[0],
                            "historiskt": ads_location[1],
                            "avstånd": distance})
                        
            locations_with_ads = sorted(locations_with_distance, 
                                        key = operator.itemgetter("avstånd"),
                                        reverse = False)
                
            a, b = st.columns(2)

            avstånd = st.slider("Hur långt kan du tänka dig att resa i kilometer?", 0, 200, 20)

            locations_with_ads_max, alla_nu, alla_historiskt = create_maxlist(locations_with_ads, avstånd)

            skillnad_nu = alla_nu - nu_grund
            skillnad_historiska = alla_historiskt - historiskt_grund

            a.metric(label = "Platsbanken", value = alla_nu, delta = skillnad_nu)
            b.metric(label = "2024", value = alla_historiskt, delta = skillnad_historiska)

            geo_string = create_string(locations_with_ads_max, "Orter med annonser:")
            st.markdown(geo_string, unsafe_allow_html = True)

def main ():
    initiate_session_state()
    fetch_data()
    choose_geo()

if __name__ == '__main__':
    main ()
