
import streamlit as st
import csv
import pandas as pd
import requests

from API_helper_functions.get_tidID import trines_get_tidID


# Laster inn orgnummer
@st.cache_data(max_entries=10)
def get_orgnummer():
    """
    Den første spørringen henter alle orgnummer i den valgte tabellen. Den andre henter gyldige enhetIDer for et
    spesifikt år. Deretter filtreres orgnummerne mot gyldige enhetIDer.
    """
    
    TidID     = trines_get_tidID()
    
    url = "https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/148/filterVerdier"
    response = requests.get(url)
    orgnummer = []
    for enhet in response.json()['EnhetID']:
        orgnummer.append(( enhet['id'], enhet['kode']))
    
    
    url = f"https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/148/filterStatus?filterId=EnhetID&filtre=TidID({TidID})"
    response = requests.get(url)
    enhetIDer = []
    for enhet in response.json()['EnhetID']:
        enhetIDer.append(enhet)
        
    gyldige_enheter = []
    
    for item in orgnummer:
        if item[0] in enhetIDer:
            gyldige_enheter.append(item[1])
        
    return gyldige_enheter

# Laster inn fylkesnummere
@st.cache_data(max_entries=100)
def get_fylker():
    url = "https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/155/data?filter=EierformID(-10)_EnhetNivaa(2)_TidID(202212)_TrinnID(10)&format=0&sideNummer=1"
    response = requests.get(url)
    fylker = []
    for fylke in response.json():
        fylker.append(fylke['Fylkekode'])
    return fylker