# Bibliotek
import requests
import streamlit as st
import re


def eksporttabeller(url="https://api.statistikkbanken.udir.no//api/rest/v2/Eksport/"):
    """ Spørring går mot domenenavn + /api/rapportering/rest/v2/Eksport """
    
    url      = url
    response = requests.get(url)
    
    # Legger inn navn og tekst i responsobjektet
    response.name        = "Utvikler API 1"
    response.description = "Returnerer en liste av tilgjengelige eksporttabeller"
    
    return response


def eksport_format(url="https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/format"):
    """ Spørring går mot domenenavn + /api/rapportering/rest/v2/Eksport/format"""
    
    url      = url
    response = requests.get(url)
    
    # Legger inn navn og tekst i responsobjektet
    response.name        = "Utvikler API 2"
    response.description = "Returnerer en liste av tilgjengelige formater"
    
    return response


def eksport_filtere(url="https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/152/filterSpec",
                    tabell=145):
    """ Spørring går mot domenenavn + /api/rapportering/rest/v2/Eksport/{tabell}/filterSpec"""
    
    # erstatter tabellnummer for tabeller med {}-parenteser
    if '{' in url or '}' in url:
        new_url = re.sub('{.*?}', '{}', url)
        url = new_url.format(tabell)
    
    url      = url
    response = requests.get(url)
    
    # Legger inn navn og tekst i responsobjektet
    response.name        = "Utvikler API 3"
    response.description = "Returnerer alle definerte filtre for en eksportversjon"
    
    return response


def eksport_filterverdier(url="https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/152/filterVerdier", 
                          tabell=145):
    """ Spørring går mot domenenavn + /api/rapportering/rest/v2/Eksport/{tabell}/filterVerdier """
    
    # erstatter tabellnummer for tabeller med {}-parenteser
    if '{' in url or '}' in url:
        new_url = re.sub('{.*?}', '{}', url)
        url = new_url.format(tabell)
    
    url      = url
    response = requests.get(url)
    
    # Legger inn navn og tekst i responsobjektet
    response.name        = "Utvikler API 4"
    response.description = "Returnerer alle definerte filterverdier for til en eksportversjon"
    
    return response


def eksport_filterstatus(url="https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/152/filterStatus", 
                         tabell=151,
                         filterId="TidID", 
                         filtre="EierformID(-10)_EnhetID(-538_-536_-12)_TidID(202112)_TrinnID(6_9)"):
    """ 
    Spørring går mot domenenavn + /api/rapportering/rest/v2/Eksport/{tabell}/filterStatus
    Query-parameterene settes til filterId=EierformID og filtre=EierformID(-10) som default
    """
    
    # erstatter tabellnummer for tabeller med {}-parenteser
    if '{' in url or '}' in url:
        new_url = re.sub('{.*?}', '{}', url)
        url = new_url.format(tabell)
    
    params   = {"filterId": filterId, "filtre": filtre}
    url      = url
    response = requests.get(url, params)
    
    # Legger inn navn og tekst i responsobjektet
    response.name        = "Utvikler API 5"
    response.description = "Returnerer gyldige filtervalg for ett bestemt filter basert på det totale filtervalget ditt"
    
    return response


def eksport_rader_sider(url="https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/148/sideData", 
                        tabell=145,
                        query="EierformID(-10)_Fylkekode(42)_KjoennID(-10)_Kommunekode(4203)_Nasjonaltkode(I)_Organisasjonsnummer(974622882)_TidID(202101)_TrinnID(6_9)"
                        ):
    """ Spørring går mot domenenavn +  /api/rapportering/rest/v2/Eksport/{tabell}/sideData"""
    
    # erstatter tabellnummer for tabeller med {}-parenteser
    if '{' in url or '}' in url:
        new_url = re.sub('{.*?}', '{}', url)
        url = new_url.format(tabell)
    
    params   = {"filter": query}
    url      = url
    response = requests.get(url, params)
    
    # Legger inn navn og tekst i responsobjektet
    response.name        = "Utvikler API 6"
    response.description = "Returnerer antall rader/side, antall sider og totalt antall bytes data som vil bli returnert av et tilsvarende kall til «data»"
    
    return response


def eksport_data(url="https://api.statistikkbanken.udir.no/api/rest/v2/Eksport/148/data", 
                 tabell=145,
                 query="EierformID(-10)_Fylkekode(42)_KjoennID(-10)_Kommunekode(4203)_Nasjonaltkode(I)_Organisasjonsnummer(974622882)_TidID(202112)_TrinnID(6_9)", 
                 format=0,
                 sideNummer=1):
    """ 
    Spørring går mot domenenavn + /api/rapportering/rest/v2/Eksport/{tabell}/data
    Query-parameterene settes til query og sideNummer som default 
    """
    
    # erstatter tabellnummer for tabeller med {}-parenteser
    if '{' in url or '}' in url:
        new_url = re.sub('{.*?}', '{}', url)
        url = new_url.format(tabell)
        
    
    params   = {"filter": query, "format": format, "sideNummer": sideNummer}
    url      = url
    response = requests.get(url, params)
    
    # Legger inn navn og tekst i responsobjektet
    response.name        = "Data API 1"
    response.description = "Henter ut data fra API-et"
    
    return response

@st.cache_resource()
def run_all_functions(_API_functions: list, uu: str):
    #st.write("DEBUG: ", uu)
    response_list = [function() for function in _API_functions]
    return response_list


def API_funksjonstester(API_functions: list, uu: str):
    
    response_list = run_all_functions(API_functions, uu)
            
    # printing results
    for response in response_list:
        st.subheader(f"{response.name}")
        st.write(f"**Beskrivelse:** {response.description}")
        
        if response.ok == False:
            st.write(f"**Status kode: :red[{response.status_code}]**")
        else:
            #st.write(f"**Status kode: :green[{response.status_code}]**") # <span style='color:#1C705F'>{response.status_code}</span>**", unsafe_allow_html=True)
            st.write(f"**Status kode: <span style='color:#327E6F'>{response.status_code}</span>**", unsafe_allow_html=True)

        if response.elapsed.microseconds / 1000000 > 1:
            st.write(f"**Tid (sekunder): :red[{response.elapsed.microseconds/1000000}]**")
        else:
            #st.write(f"**Tid (sekunder): :green[{response.elapsed.microseconds/1000000}]**") # <span style='color:#1C705F'>{response.elapsed.microseconds/1000000}</span>**", unsafe_allow_html=True)
            st.write(f"**Tid (sekunder): <span style='color:#327E6F'>{response.elapsed.microseconds/1000000}</span>**", unsafe_allow_html=True)

        st.write("")