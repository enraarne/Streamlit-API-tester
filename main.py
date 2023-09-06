# External libraries
import requests
import json
import pandas as pd
import csv
import io
import sys
import copy
from API_helper_functions.helper_functions import eksport_rader_sider
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import statsmodels.api as sm
import random
import seaborn as sns
import re
import secrets

# streamlit
import streamlit as st
st.set_page_config(layout="wide", page_title='USS API-tester', page_icon = "img/api-konsoll-logo.ico")
st.set_option('deprecation.showPyplotGlobalUse', False)
import streamlit.components.v1 as components  # Import Streamlit

# Import of functions from own modules 
from API_helper_functions.helper_functions import eksporttabeller, eksport_format, eksport_filtere, eksport_filterverdier, eksport_filterstatus, eksport_rader_sider, eksport_data, run_all_functions, API_funksjonstester
from API_helper_functions.load_data import get_orgnummer, get_fylker
from API_helper_functions.speed_tests import speed_test_1, speed_test_1_print, speed_test_2, speed_test_2_print, \
    speed_test_3, speed_test_3_print, speed_test_4, speed_test_4_print
from API_helper_functions.innholdstester import kolonne_test, kolonne_test_print, kolonne_dict, irene_prikking, irene_prikking_printer
from API_helper_functions.paginering import paginering, paginering_printer


#### Remove red/orange header line ####
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
        #MainMenu {visibility: visible;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


# code inspired by PratT-KAi, https://discuss.streamlit.io/t/session-specific-caching-and-user-specific-caching/31910/5
uu = "session_id"
if uu in st.session_state:
    uu = st.session_state[uu]
else:
    new = secrets.token_urlsafe(16)
    st.session_state[uu] = new
    uu = new

#st.write("DEBUG: ", uu)


#### Add sidebar ####
st.sidebar.markdown("# Testtjeneste for Åpent API")
st.sidebar.markdown("Denne web-appen tilbyr en rekke tester som tester ut forskjellige sider av det åpne API-et")
st.sidebar.markdown("**Innholdsfortegnelse:**")
st.sidebar.markdown("[1. Funksjonstest av utvikler- og data-APIer](#1-funksjonstest-av-utvikler-og-data-apier)")
st.sidebar.markdown("[2. Hastighetstester av APIet](#2-hastighetstester-av-apiet)")
st.sidebar.markdown("[3. Pagineringstester](#3-pagineringstester)")
st.sidebar.markdown("[4. Innholdstester](#4-innholdstester)")
st.sidebar.markdown("")
st.sidebar.markdown("**Buffer (cache):**")
st.sidebar.markdown("""Denne web-appen benytter en server-side buffer (cache) som lagrer kall mot APIene. \
    Bufferen lagrer i utgangspunktet kun resultater av kall innen samme økt (session). Du avslutter en økt når du laster inn websiden \
        på nytt eller legger ned fanen. Hvis du ønsker at kallene skal være lagret mellom økter og for alle brukere,  trykk på radioknappen \
            nedenfor som er markert 'Global' """)
mode = st.sidebar.radio("**Modus**", options=('Lokal', 'Global'))
if mode == 'Global':
    uu = 'Global'
    #st.sidebar.write("DEBUG: ", uu)
st.sidebar.markdown("""Hvis du ønsker å tømme bufferen, kan du enten trykke på knappen nedenfor eller gå inn på "hamburgermenyen" øverst \
    til høyre og trykke på "clear cache". Merk at du da vil tømme bufferen for alle brukere av tjenesten.""")
if st.sidebar.button("Tøm bufferen", type="primary"):
    st.experimental_memo.clear()
    st.runtime.legacy_caching.clear_cache()


#### Header and Introduction ####
st.title("Testredskaper for Statistikksystemets åpne API (v1.0)")
st.write("Denne web appen tilbyr fire forskjellige typer tester: funksjonstester, hastighetstester, pagineringstester og innholdstester. \
    I de fleste tilfeller kan du selv stille inn hvor omfattende du ønsker at testene skal være, f.eks. ved å sette opp antall kall mot API-et. \
        Desto flere kall mot API-et, desto bedre datagrunnlag for å vurdere ytelsen. Men desto flere kall mot API-et, desto lengre tid \
            tar det å gjennomføre testene.")
st.markdown("***")


#### Funksjonstester ####
st.markdown("""<h2 style="background-color: RGB(170 187 204); padding: 10px;">1. Funksjonstester av utvikler- og data-APIer</h2>"""\
    , unsafe_allow_html=True)
#st.header("1. Funksjonstest av utvikler- og data-APIer")
st.write(f"""Funksjonstestene tester om API-ene er operative. De tester alle seks utvikler-API-ene og data-API-et. \
    For hvert av API-ene gjennomføres det en test som ser om det får et svar med status kode 200 og at svaret mottas innen ett sekund.""")            

#st.markdown("***")

# List of helper-functions
API_functions = [eksporttabeller, eksport_format, eksport_filtere, eksport_filterverdier, eksport_filterstatus, eksport_rader_sider, eksport_data]
API_funksjonstester(API_functions, uu)        

st.markdown("***")


#### Hastighetstester ####
st.markdown("""<h2 style="background-color: RGB(170 187 204);padding: 10px;">2. Hastighetstester av APIet</h2>"""\
    , unsafe_allow_html=True)
#st.header("2. Hastighetstester av APIet") 
st.write("Denne web appen har fire hastighetstester, som på forskjellig måte måler responstiden til det åpne API-et. De fleste testene \
    tillater at brukeren bestemmer antall kall som gjøres mot API-et. Desto flere kall mot API-et, desto lengre tid tar testen. Velger \
        man få kall mot API-et kan tilfeldige variasjoner i responstid prege utfallet.")

#st.markdown("***")



#### Hastighetstest 2.1 ####
st.subheader("2.1 Test av responstid med én tilfeldig generert spørring")
st.write(f"""Denne hastighetstesten benytter seg av en spørring med et tilfeldig trukket fylke og et tilfeldig trukket \
    organisasjonsnummer. Testen måler både tiden det tar å laste ned header og tiden det tar å laste ned både header \
        og body (dvs. alle rader). Ettersom samme spørring gjentas flere ganger, vil responstiden påvirkes av caching (buffering) \
            i API-et. Er caching satt på, vil man vente at første spørring tar betraktelig lengre tid enn senere spørringer.""")


slider_2_1 = st.slider("**Velg antall kall mot APIet**", min_value=10, max_value=100, value=50, key="slider_2_1")

# We only run hastighetstest_2_1 if button is pushed or button_2_1 is in session_state
if st.button("Kjør hastighetstest 2.1", type="primary") or 'button_2_1' in st.session_state:
    if 'button_2_1' not in st.session_state:
        st.session_state['button_2_1'] = True

    df1, query = speed_test_1(slider_2_1, uu)
    st.write(f"""Figuren nedenfor er et resultat av en spørring som benytter følgende spørrestreng: <b>filter={query}</b>. \
        Totalt henter spørringen ned <b>{df1["Size"].iloc[0]} rader</b>.""", unsafe_allow_html=True)
    #st.text("")
    speed_test_1_print(query, df1)
    #st.text("")




#### Hastighetstest 2.2 ####
st.subheader("2.2 Test av responstid med tilfeldig trekte organisasjonsnummer")
st.write(f"""Denne hastighetstesten benytter seg av en spørring med et tilfeldig trukket \
    organisasjonsnummer. Testen måler både tiden det tar å laste ned header og tiden det tar å laste ned både header \
        og body (dvs. alle rader). Ettersom samme spørring gjentas flere ganger med forskjellige organisasjonsnummer, \
            vil responstiden ikke påvirkes av caching (buffering) i API-et. Om caching er satt på eller ikke, skal ikke påvirke \
                tiden det tar å gjennomføre spørringene.""")

slider_2_2 = st.slider("**Velg antall kall mot APIet**", min_value=10, max_value=100, value=50, key="slider_2_2")

# We only run hastighetstest_2_1 if button is pushed or button_2_1 is in session_state
if st.button("Kjør hastighetstest 2.2", type="primary") or 'button_2_2' in st.session_state:
    if 'button_2_2' not in st.session_state:
        st.session_state['button_2_2'] = True
    df2 = speed_test_2(slider_2_2, uu)
    speed_test_2_print(df2)



#### Hastighetstest 2.3 ####
st.subheader("2.3 Responstid som en funksjon av antall rader")
st.write("Denne hastighetstesten benytter seg av datagrunnlaget fra forrige test (Hastighetstest 2.2.). Testen gjennomfører en \
    regresjonsanalyse med responstid som avhengig variabel og antall rader mottatt som uavhengig variabel. Denne testen \
        gjennomføres både for tiden det tar å laste ned header og tiden det tar å laste ned både header og body (dvs. alle rader). \
            Hensikten med testen er å se om det tar lengre tid å kjøre kall som etterspør mange rader enn få rader. Dette kan brukes \
                som et element i en vurdering av om man har en hensiktsmessig størrelse på pagineringen.")


# We only run hastighetstest_2_3 if button is pushed or button_2_3 is in session_state
if st.button("Kjør hastighetstest 2.3", type="primary") or 'button_2_3' in st.session_state:
    if 'button_2_3' not in st.session_state:
        st.session_state['button_2_3'] = True
    df2 = speed_test_2(slider_2_2, uu)
    result1, result2 = speed_test_3(df2, uu)
    speed_test_3_print(result1, result2, df2)



#### Hastighetstest 2.4 ####
st.subheader("2.4 Test av et tilfeldig utvalg APIer")
st.write("Denne testen sammenligner hastigheten på de seks utvikler-API-ene og data-API-et. Hensikten med testen er å se om noen \
    av API-ene skiller seg ut med hensyn til responshastighet. Man vil i utgangspunktet vente at data-API-et vil ha noe høyere \
        responstid enn de andre API-ene. Denne hasighetstesten plukker API-er i tilfeldig rekkefølge.")


slider_2_4 = st.slider("**Velg antall kall mot APIet**", min_value=20, max_value=100, value=50, key="slider_2_4")

if st.button("Kjør hastighetstest 2.4", type="primary") or 'button_2_4' in st.session_state:
    if 'button_2_4' not in st.session_state:
        st.session_state['button_2_4'] = True
    df4 = speed_test_4(slider_2_4, uu)
    speed_test_4_print(df4)

st.markdown("***")




#### Pagineringstester ####
st.markdown("""<h2 style="background-color: RGB(170 187 204); ;padding: 10px;">3. Pagineringstester</h2>"""\
    , unsafe_allow_html=True)
#st.header("3. Pagineringstester") 
st.subheader("3.1 Test av et tilfeldig utvalg sider er identiske")
st.write("Pagineringstesten gjør en spørring mot API-et med ett tilfeldig valgt fylke og ett tilfeldig valgt organisasjonsnummer. \
    Denne spørringen vil vanligvis generere en respons som tar opp rundt 300 sider. Pagineringstesten gjør to kall mot samme sidenummer \
        og sammenligner sidene og ser om de er identiske. Pagineringstesten gjentar denne prosedyren et spesifisert antall ganger. Hver \
            gang trekker testen ut et nytt sidenummer. Pagineringstesten undersøker om sidene har samme antall rader, samme innhold i radene \
                og at radene er organisert i samme rekkefølge.")

slider_3_1 = st.slider("**Velg antall kall mot APIet**", min_value=1, max_value=50, value=10, key="slider_3_1")

if st.button("Kjør pagineringstest 3.1", type="primary") or 'button_3_1' in st.session_state:
    if 'button_3_1' not in st.session_state:
        st.session_state['button_3_1'] = True

    response_dict = paginering(slider_3_1, uu)
    paginering_printer(response_dict)


st.markdown("***")

#### Innholdstester ####
#st.header("4. Innholdstester")
st.markdown("""<h2 style="background-color: RGB(170 187 204); ;padding: 10px;">4. Innholdstester</h2>"""\
    , unsafe_allow_html=True) 
st.subheader("4.1 Test av kolonner og kolonnerekkefølge")
st.write("Denne innholdstesten gjør spørringer mot alle de åtte tabellene. Deretter tester den om alle variabler som burde være med i \
    de forskjellige tabellene er med. Testen undersøker også om variablene opptrer i riktig rekkefølge. På siden av testen finner du \
        en oversikt i JSON over alle variabler som skal være med i de forskjellige tabellene. Det er denne JSON-en som brukes som \
            sammenligningsgrunnlag.")

def innholdstest_4_1():
    
    if 'button_4_1' not in st.session_state:
        st.session_state['button_4_1'] = True
    test_liste = kolonne_test(uu)
    kolonne_test_print(test_liste)


col1, col2 = st.columns(2)

with col1:
    if st.button("Kjør innholdstest 4.1", type="primary", key="test") or 'button_4_1' in st.session_state:
        innholdstest_4_1()

with col2:
    st.json(kolonne_dict, expanded=False) # expanded=False


st.subheader("4.2 Test av prikking")
st.write("Test av prikking er ikke med i den offentlige versjonen av applikasjonen. For å benytte denne funksjonaliteten \
         bruk den internt tilgjengelige versjonen. I denne versjonen, vil funksjonen alltid returnere 'Riktig'")


sql_code = """
/* API-responsen sammenlignes med resultatet av 
følgende SQL-spørring: */

SELECT TOP 1000
Column_1
,Column_2
,Column_3
,*
FROM Database.School.Table
WHERE 1=1
,AND Column_1 = Value
,AND Column_2 = Value
,AND Column_3 = Value
,AND Column_4 = Value
,AND Column_5 = Value
,AND Column_6 = Value
,AND Column_7 = 'Value'
,AND Column_8 = Value
,AND Column_8 = Value
,AND Column_8 = Value
,AND Column_8 = Value
--,AND Column_8 IS NULL 
"""


col3, col4 = st.columns(2)

with col3:
    if st.button("Kjør innholdstest 4.2", type="primary") or 'button_4_1' in st.session_state:
        
        if 'button_4_2' not in st.session_state:
            st.session_state['button_4_2'] = True
        
        resultat = irene_prikking(uu)
        irene_prikking_printer(resultat)

with col4:
    st.code(sql_code) # expanded=False




#st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
#    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor \
#        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident\
#            , sunt in culpa qui officia deserunt mollit anim id est laborum.")


#st.markdown("""<div style="background-color: RGB(170 187 204);">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
#    Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor \
#        in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident\
#            , sunt in culpa qui officia deserunt mollit anim id est laborum.</div>""", unsafe_allow_html=True)


# TO DO:
# Koble funksjoner på slidebar
# Refactor vekk interne funksjoner DONE
# Legge inn pagineringstest - med max(verdi fra random) 
# Legge inn Irene prikking
