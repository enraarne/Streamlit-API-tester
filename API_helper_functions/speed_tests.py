import time
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import streamlit as st
import random
import statsmodels.formula.api as smf
import statsmodels.api as sm
import copy

from API_helper_functions.helper_functions import eksporttabeller, eksport_format, eksport_filtere, eksport_filterverdier, \
    eksport_filterstatus, eksport_rader_sider, eksport_data
from API_helper_functions.load_data import get_fylker, get_orgnummer
from API_helper_functions.get_tidID import trines_get_tidID

API_functions = [eksporttabeller, eksport_format, eksport_filtere, eksport_filterverdier, eksport_filterstatus, eksport_rader_sider, \
    eksport_data]



# Set colors for several of the functions. It is placed here because of trouble displaying right color at inital run.
colors = ["#51698F", "#8f5169"]  #8f7751
sns.set_palette(sns.color_palette(colors))


@st.cache_data(max_entries=100)
def speed_test_1(slider_2_1: int, uu: str):
    
    orgnummer = get_orgnummer()
    fylker    = get_fylker()
    TidID     = trines_get_tidID()
    orgnum = random.choice(orgnummer)
    fylke  = random.choice(fylker)
    query = f"Fylkekode({fylke})_Organisasjonsnummer({orgnum})_TidID({TidID})"
    
    # Progress bar
    speed_1_bar = st.progress(0.0)
    complete = 0.0

    time_list = []
    for request in range(slider_2_1):
        
        # Progress bar
        complete += (1/slider_2_1)
        if complete >= 1.0:
            complete = 1.0
        speed_1_bar.progress(complete)
        
        start = time.perf_counter()
        response = eksport_data(query=query)
        end = time.perf_counter()
        time_list.append( (request, response.elapsed.microseconds / 1000000, end-start, len(response.json())) )
        sys.stdout.flush()

    # Progress bar
    speed_1_bar.progress(1.0)

    df = pd.DataFrame(time_list, columns =['Request', 'Time_request', 'Time_measured', 'Size'])
    assert(len(set(df['Size'])) == 1)
    return df, query


def speed_test_1_print(query, df):
    #df = first_timer(query)

    st.text("")
    plt.rc('font',family=""" "Source Sans Pro", sans-serif """)
    plt.figure(figsize=(22, 10))

    # Font ticks size
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)

    plt.text(5.5, 1.95, f'Antall rader i "response body": {df["Size"].iloc[0]}', fontsize=18,
            verticalalignment='top')

    # Create an array with the colors you want to use
    colors = ["#51698F", "#8f5169"]  #8f7751
    # Set your custom color palette
    sns.set_palette(sns.color_palette(colors))

    sns.scatterplot(x=df['Request'], y=df['Time_request'], s=80)
    sns.scatterplot(x=df['Request'], y=df['Time_measured'], s=80)
    plt.plot('Request', 'Time_request', data=df)
    plt.plot('Request', 'Time_measured', data=df)

    plt.title(f"Figur 2.1: Responstid for filter={query}", size=26, pad=16)  # , loc='left'
    plt.xlabel('GET request nummer', size=18)
    plt.ylabel('Tid i sekunder', size=18)

    plt.legend(labels=['Tid forløpt til header mottatt', 'Total kjøretid'], prop={'size': 14}) #Time elapsed to header received, Total execution time

    st.pyplot()
    st.text("")


@st.cache_data(max_entries=100)
def speed_test_2(slider_2_2:int, uu: str):
    time_list = []
    orgnummer = get_orgnummer()

    # Progress bar
    speed_2_bar = st.progress(0.0)
    complete = 0.0

    for request in range(slider_2_2):
        
        # Progress bar
        complete += (1/slider_2_2)
        if complete >= 1.0:
            complete = 1.0
        speed_2_bar.progress(complete)
        
        orgnum = random.choice(orgnummer)
        start = time.perf_counter()
        response = eksport_data(query=f"Organisasjonsnummer({orgnum})")
        end = time.perf_counter()
        time_list.append( (request, response.elapsed.microseconds / 1000000, end-start, len(response.json()), orgnum ))

    # Progress bar
    speed_2_bar.progress(1.0)

    df = pd.DataFrame(time_list, columns =['Request', 'Time_request', 'Time_measured', 'Size', 'Orgnummer'])
    return df.copy()


def speed_test_2_print(df):
    st.text("")

    plt.figure(figsize=(22, 10))
    sns.scatterplot(x=df['Request'], y=df['Time_request'], size=df['Size'])
    sns.scatterplot(x=df['Request'], y=df['Time_measured'], size=df['Size'])
    plt.plot('Request', 'Time_request', data=df)
    plt.plot('Request', 'Time_measured', data=df)

    yellow_patch = mpatches.Patch(color="#8f5169", label='Total kjøretid')
    blue_patch = mpatches.Patch(color="#51698F", label='Tid forløpt til header mottatt')
    plt.legend(handles=[yellow_patch, blue_patch], prop={'size': 14}, loc="upper right")

    # Font ticks size
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)

    plt.title("Figur 2.2: Responstid for API med randomiserte org.nummere", size=26, pad=16)
    plt.xlabel('GET request nummer', size=18)
    plt.ylabel('Tid i sekunder', size=18)

    st.pyplot()
    st.text("")


@st.cache_data(max_entries=100)
def speed_test_3(df, uu:str):
    # Regresjonsanalyse

    Y = df['Time_request']
    X = df['Size']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    result1 = model.fit()

    Y = df['Time_measured']
    X = df['Size']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    result2 = model.fit()

    return copy.deepcopy(result1), copy.deepcopy(result2)


def speed_test_3_print(result1, result2, df):
    st.text("")
    plt.figure(figsize=(22, 10))
    sns.scatterplot(x=df['Size'], y=df['Time_request'], s=170)
    sns.scatterplot(x=df['Size'], y=df['Time_measured'], s=170)

    yellow_patch = mpatches.Patch(color="#8f5169", label='Total kjøretid')
    blue_patch = mpatches.Patch(color="#51698F", label='Tid forløpt til header mottatt')
    plt.legend(handles=[yellow_patch, blue_patch], prop={'size': 14}, loc="upper right")

    # Font ticks size
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)

    plt.title("Figur 2.3: Responstid som en funksjon av antall rader", size=26, pad=16)
    plt.xlabel('Antall rader', size=18)
    plt.ylabel('Tid i sekunder', size=18)

    x = np.arange(1, 6000)
    #### add linear regression line to scatterplot 
    plt.plot(result1.params.const + result1.params.Size * x, linewidth=2.5)
    plt.plot(result2.params.const + result2.params.Size * x, linewidth=2.5)

    st.pyplot()
    st.text("")

@st.cache_data(max_entries=100)
def speed_test_4(slider_2_4:int, uu:str):
    # Progress bar
    speed_4_bar = st.progress(0.0)
    complete = 0.0
    
    time_list = []

    # Progress bar
    complete += (1/slider_2_4)
    if complete >= 1.0:
        complete = 1.0
    speed_4_bar.progress(complete)

    for request in range(slider_2_4):
        response = random.choice(API_functions)()
        time_list.append( (request, response.elapsed.microseconds / 1000000, response.description) )
        sys.stdout.flush()

    # Progress bar
    speed_4_bar.progress(1.0)

    df = pd.DataFrame(time_list, columns =['Request', 'Time', 'Type'])
    return df


def speed_test_4_print(df):
    st.text("")
    plt.figure(figsize=(22, 10))
    
    # Font ticks size
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)

    plt.xlabel('Antall rader', size=18)
    plt.ylabel('Tid i sekunder', size=18)
    plt.ylim(0, df['Time'].max() + .35*df['Time'].max())
    plt.title("Figur 2.4: Test av tidsbruk for tilfeldige valgte API-er", size=26, pad=16)
    sns.scatterplot(x=df['Request'], y=df['Time'], hue=df['Type'], s=110)
    plt.plot('Request', 'Time', data=df)
    plt.legend(loc='upper right', prop={'size': 12})
    
    st.pyplot()
    st.text("")