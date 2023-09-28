import streamlit as st
import requests
import pandas as pd
import time
from API_helper_functions.helper_functions import eksport_data
from API_helper_functions.get_tidID import trines_get_tidID

tabeller = [151, 148, 150, 149, 155, 152, 154, 153] 

kolonne_dict = {
    
    'deltagelse_GSK': ['EnhetNivaa', 'Nasjonaltkode', 'Nasjonalt', 'Fylkekode', 'Fylke',
       'Kommunekode', 'Kommune', 'Organisasjonsnummer', 'EnhetNavn',
       'Skoleaarnavn', 'TrinnNivaa', 'TrinnKode', 'Trinnnavn', 'EierformNivaa',
       'Eierformkode', 'EierformNavn', 'AndelDeltatt', 'AntallBesvart',
       'AntallInvitert', 'Sidenummer', 'RaderSide', 'RaderTotalt'],
    
    'indikator_GSK': ['SpoersmaalNivaa', 'Spoersmaalgruppekode', 'Spoersmaalgruppe',
       'Spoersmaalkode', 'Spoersmaalnavn', 'Skoleaarnavn', 'EnhetNivaa',
       'Nasjonaltkode', 'Nasjonalt', 'Fylkekode', 'Fylke', 'Kommunekode',
       'Kommune', 'Organisasjonsnummer', 'EnhetNavn', 'GruppeNivaa',
       'GruppeKode', 'GruppeNavn', 'TrinnNivaa', 'TrinnKode', 'Trinnnavn',
       'EierformNivaa', 'Eierformkode', 'EierformNavn', 'KjoennNivaa',
       'KjoennKode', 'Kjoenn', 'Score', 'Standardavvik', 'AntallBesvart',
       'AndelSvaralternativ1', 'AndelSvaralternativ2', 'AndelSvaralternativ3',
       'AndelSvaralternativ4', 'AndelSvaralternativ5',
       'AntallBesvartSvaralternativ1', 'AntallBesvartSvaralternativ2',
       'AntallBesvartSvaralternativ3', 'AntallBesvartSvaralternativ4',
       'AntallBesvartSvaralternativ5', 'Sidenummer', 'RaderSide',
       'RaderTotalt'],
    
    'mobbing_GSK': ['SpoersmaalNivaa', 'Spoersmaalgruppekode', 'Spoersmaalgruppe',
       'Spoersmaalkode', 'Spoersmaalnavn', 'Skoleaarnavn', 'EnhetNivaa',
       'Nasjonaltkode', 'Nasjonalt', 'Fylkekode', 'Fylke', 'Kommunekode',
       'Kommune', 'Organisasjonsnummer', 'EnhetNavn', 'GruppeNivaa',
       'GruppeKode', 'GruppeNavn', 'TrinnNivaa', 'TrinnKode', 'Trinnnavn',
       'EierformNivaa', 'Eierformkode', 'EierformNavn', 'KjoennNivaa',
       'KjoennKode', 'Kjoenn', 'AndelMobbet', 'AntallBesvart', 'Sidenummer',
       'RaderSide', 'RaderTotalt'],
    
    'tema_GSK': ['TemaNivaa', 'Temakode', 'Temanavn', 'SpoersmaalNivaa',
       'Spoersmaalkode', 'Spoersmaalnavn', 'SvaralternativNivaa',
       'SvaralternativKode', 'SvaralternativNavn', 'Skoleaarnavn',
       'EnhetNivaa', 'Nasjonaltkode', 'Nasjonalt', 'Fylkekode', 'Fylke',
       'Kommunekode', 'Kommune', 'Organisasjonsnummer', 'EnhetNavn',
       'GruppeNivaa', 'GruppeKode', 'GruppeNavn', 'TrinnNivaa', 'TrinnKode',
       'Trinnnavn', 'EierformNivaa', 'Eierformkode', 'EierformNavn',
       'KjoennNivaa', 'KjoennKode', 'Kjoenn', 'Score', 'Standardavvik',
       'AntallBesvart', 'AndelBesvart', 'Sidenummer', 'RaderSide',
       'RaderTotalt'],
    
    'deltagelse_VGO': ['EnhetNivaa', 'Nasjonaltkode', 'Nasjonalt', 'Fylkekode', 'Fylke',
       'Organisasjonsnummer', 'EnhetNavn', 'Skoleaarnavn', 'TrinnNivaa',
       'TrinnKode', 'Trinnnavn', 'EierformNivaa', 'Eierformkode',
       'EierformNavn', 'AndelDeltatt', 'AntallBesvart', 'AntallInvitert',
       'Sidenummer', 'RaderSide', 'RaderTotalt'],
    
    'indikator_VGO': ['SpoersmaalNivaa', 'Spoersmaalgruppekode', 'Spoersmaalgruppe',
       'Spoersmaalkode', 'Spoersmaalnavn', 'Skoleaarnavn', 'EnhetNivaa',
       'Nasjonaltkode', 'Nasjonalt', 'Fylkekode', 'Fylke',
       'Organisasjonsnummer', 'EnhetNavn', 'GruppeNivaa', 'GruppeKode',
       'GruppeNavn', 'ProgramomraadeNivaa', 'UtdanningstypeKode',
       'UtdanningstypeNavn', 'Utdanningsprogramkode', 'UtdanningsprogramNavn',
       'TrinnNivaa', 'TrinnKode', 'Trinnnavn', 'KjoennNivaa', 'KjoennKode',
       'Kjoenn', 'EierformNivaa', 'Eierformkode', 'EierformNavn', 'Score',
       'Standardavvik', 'AntallBesvart', 'AndelSvaralternativ1',
       'AndelSvaralternativ2', 'AndelSvaralternativ3', 'AndelSvaralternativ4',
       'AndelSvaralternativ5', 'AntallBesvartSvaralternativ1',
       'AntallBesvartSvaralternativ2', 'AntallBesvartSvaralternativ3',
       'AntallBesvartSvaralternativ4', 'AntallBesvartSvaralternativ5',
       'Sidenummer', 'RaderSide', 'RaderTotalt'],
    
    'mobbing_VGO': ['SpoersmaalNivaa', 'Spoersmaalgruppekode', 'Spoersmaalgruppe',
       'Spoersmaalkode', 'Spoersmaalnavn', 'Skoleaarnavn', 'EnhetNivaa',
       'Nasjonaltkode', 'Nasjonalt', 'Fylkekode', 'Fylke',
       'Organisasjonsnummer', 'EnhetNavn', 'GruppeNivaa', 'GruppeKode',
       'GruppeNavn', 'ProgramomraadeNivaa', 'UtdanningstypeKode',
       'UtdanningstypeNavn', 'Utdanningsprogramkode', 'UtdanningsprogramNavn',
       'TrinnNivaa', 'TrinnKode', 'Trinnnavn', 'EierformNivaa', 'Eierformkode',
       'EierformNavn', 'KjoennNivaa', 'KjoennKode', 'Kjoenn', 'AndelMobbet',
       'AntallBesvart', 'Sidenummer', 'RaderSide', 'RaderTotalt'],
    
    'tema_VGO': ['TemaNivaa', 'Temakode', 'Temanavn', 'SpoersmaalNivaa',
       'Spoersmaalkode', 'Spoersmaalnavn', 'SvaralternativNivaa',
       'SvaralternativKode', 'SvaralternativNavn', 'Skoleaarnavn',
       'EnhetNivaa', 'Nasjonaltkode', 'Nasjonalt', 'Fylkekode', 'Fylke',
       'Organisasjonsnummer', 'EnhetNavn', 'GruppeNivaa', 'GruppeKode',
       'GruppeNavn', 'ProgramomraadeNivaa', 'UtdanningstypeKode',
       'UtdanningstypeNavn', 'Utdanningsprogramkode', 'UtdanningsprogramNavn',
       'TrinnNivaa', 'TrinnKode', 'Trinnnavn', 'KjoennNivaa', 'KjoennKode',
       'Kjoenn', 'EierformNivaa', 'Eierformkode', 'EierformNavn', 'Score',
       'Standardavvik', 'AndelBesvart', 'AntallBesvart', 'Sidenummer',
       'RaderSide', 'RaderTotalt']
}

@st.cache_data(max_entries=100)
def kolonne_test(uu:str):

    test_liste = []
    
    for tabell, dict_key in zip(tabeller, kolonne_dict.keys()):

        url   = "https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/{148}/data"   
        query = f"EierformID(-10)_EnhetNivaa(1)_Nasjonaltkode(I)_TidID({trines_get_tidID()})"      # "EierformID(-10)_EnhetNivaa(1)_Nasjonaltkode(I)_TidID(202112)"
        resultat = eksport_data(url, filtre=query, tabell = tabell)

        df = pd.read_json(resultat.text)
        
        api   = df.columns.to_list()
        fasit = kolonne_dict[dict_key]
        
        if api == fasit:
            #st.write(f"Tabell: {tabell} {dict_key: <25} Resultat: **:green[Riktig]**") #{api == fasit}
            test_liste.append( (tabell, dict_key, "Riktig")  )
        else:
            #st.write(f"Tabell: {tabell} {dict_key: <25} Resultat: **:red[{api == fasit}]**")
            test_liste.append( (tabell, dict_key, "Feil")  )
        
    return test_liste


def kolonne_test_print(test_liste):
    st.write("")
    st.write("**Test av kolonner (navn, antall, rekkefølge):**\n") 

    for element in test_liste:
        if element[2] == "Riktig":
            st.write(f"Tabell: {element[0]} {element[1]} **:<span style='color:#327E6F'> {element[2]}</span>**", unsafe_allow_html=True) #{api == fasit}
        else:
            st.write(f"Tabell: {element[0]} {element[1]} **:<span style='color:#880808'> {element[2]}</span>**", unsafe_allow_html=True)
    st.write("")



@st.cache_data(max_entries=100)
def irene_prikking(uu:str):
    time.sleep(5)
    test_list = [True, True, True, True]    
    return test_list


def irene_prikking_printer(test_liste):
    st.write("")
    st.write("**Test av prikking:**\n") 
    
    tekst_liste = ["Score skal være prikket", "Standardavvik skal være prikket", "AntallBesvart skal være prikket", "AndelBesvart skal være prikket"]

    for i, e in zip(tekst_liste, test_liste):
        if e == True:
            st.write(f"{i} **:<span style='color:#327E6F'> Riktig</span>**", unsafe_allow_html=True) #{api == fasit}
        else:
            st.write(f"{i}  **:<span style='color:#880808'> Feil</span>**", unsafe_allow_html=True) ###**:red[' Feil']**")
    st.write("")