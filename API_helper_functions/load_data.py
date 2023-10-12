
import streamlit as st
import csv
import pandas as pd
import requests

# Laster inn orgnummer
@st.cache_data(max_entries=10)
def get_orgnummer(url = "https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/148/filterVerdier"):
    response = requests.get(url)
    orgnummer = []
    for enhet in response.json()['EnhetID']:
        orgnummer.append(enhet['kode'])
    return orgnummer

# Laster inn fylkesnummere
@st.cache_data(max_entries=100)
def get_fylker():
    url = "https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/155/data?filter=EierformID(-10)_EnhetNivaa(2)_TidID(202212)_TrinnID(10)&format=0&sideNummer=1"
    response = requests.get(url)
    fylker = []
    for fylke in response.json():
        fylker.append(fylke['Fylkekode'])
    return fylker