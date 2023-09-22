import requests
import streamlit as st
import re

@st.cache_data(max_entries=100)
def trines_get_tidID(
    url      = "https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/{tabell}/filterVerdier",
    tabell=151):

    """ Henter nyeste tilgjengelige tidID for en eksporttabell """
    
    # erstatter tabellnummer for tabeller med {}-parenteser
    if '{' in url or '}' in url:
        new_url = re.sub('{.*?}', '{}', url)
        url = new_url.format(tabell)
    
    response = requests.get(url)
    tidID = response.json()["TidID"][0]["kode"]
    return tidID
