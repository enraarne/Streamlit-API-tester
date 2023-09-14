
import streamlit as st
import csv
import pandas as pd

# Laster inn orgnummer
@st.cache_data(max_entries=100)
def get_orgnummer():
    file = open('data/organisasjonsnumre.csv')
    csvreader = csv.reader(file)
    rows = []
    for row in csvreader:
        rows.append(row)
    orgnummer = [val for sublist in rows for val in sublist]
    orgnummer = orgnummer[1:]
    return orgnummer

# Laster inn fylkesnummere
@st.cache_data(max_entries=100)
def get_fylker():
    df_fylke = pd.read_html("https://no.wikipedia.org/wiki/Fylkesnummer")
    fylker = df_fylke[0]['Fylkesnummer'].to_list()
    fylker[1] = '03'
    return fylker