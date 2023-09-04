import streamlit as st
import requests
import pandas as pd
import random

from API_helper_functions.helper_functions import eksport_data
from API_helper_functions.load_data import get_fylker, get_orgnummer

@st.experimental_memo()
def paginering(slider_3_1: int, uu:str):
    
    # Progress bar
    speed_5_bar = st.progress(0.0)
    complete = 0.0

    response_dict = dict()
    response_dict['validation'] = []

    orgnummer = get_orgnummer()
    fylker    = get_fylker()
    orgnum = random.choice(orgnummer)
    fylke  = random.choice(fylker)
    query = f"Fylkekode({fylke})_Organisasjonsnummer({orgnum})"

    df = pd.read_json(eksport_data(query=query, sideNummer=1).text)
    antall_sider = int(round(df['RaderTotalt'].iloc[0] / df['RaderSide'].iloc[0], 1)) -1

    response_dict['query'] = query
    response_dict['antall_sider'] = antall_sider + 1


    if slider_3_1 < antall_sider:
        sider = random.choices( range(1, antall_sider), k=slider_3_1 )
    else:
        sider = [i for i in range(1, antall_sider)]

    #response_dict['sider_testet'] = sider

    for side in sider:
        
        df1 = pd.read_json(eksport_data(query=query, sideNummer=side).text)
        df2 = pd.read_json(eksport_data(query=query, sideNummer=side).text)

        # Progress bar
        complete += (1/slider_3_1)
        if complete >= 1.0:
            complete = 1.0
        speed_5_bar.progress(complete)


        if len(df1['Organisasjonsnummer']) == len(df2['Organisasjonsnummer']):
            test_1 = "Riktig" 
        else:
            test_1 = "Feil"
        
        if set(df1['Organisasjonsnummer']) == set(df2['Organisasjonsnummer']):
            test_2 = "Riktig" 
        else:
            test_2 = "Feil"
            
        if len( df1[df1['Organisasjonsnummer'] != df2['Organisasjonsnummer']]) == 0:
            test_3 = "Riktig" 
        else:
            test_3 = "Feil"

        response_dict['validation'].append( (side, test_1, test_2, test_3) )


    #st.write(response_dict)
    return response_dict


def paginering_printer(response_dict):
    
    st.write(f"**Pagineringstesten er gjennomført for følgende spørrestreng:<span style='color:#327E6F'> {response_dict['query']}</span>. Responsen fra spørringen genererte <span style='color:#327E6F'>{response_dict['antall_sider']}</span> sider.**", unsafe_allow_html=True)
    
    df = pd.DataFrame(response_dict['validation'], columns=['Sidenummer', "Har de samme antall rader?      ", "Inneholder de de samme radene?  ", "Har radene den samme rekkefølgen?"])
    
    def farge(svar:str):
        farge = '#327E6F' if svar == "Riktig" else '#880808'
        return f'color: {farge}; font-weight: bold;'

    st.dataframe(df.style.applymap(farge, subset=["Har de samme antall rader?      ", "Inneholder de de samme radene?  ", "Har radene den samme rekkefølgen?"]))


    #for first, second in response_dict['validation']:
    #    st.write(first, second)