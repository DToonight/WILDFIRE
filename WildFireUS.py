
# streamlit run 'C:\Users\fta\Desktop\PROJET WILD FIRE\Streamlit\Final\WildFireUS.py'

import streamlit as st
import pandas as pd
import numpy as np
import sqlite3 as sql

import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy.stats import chi2_contingency
from scipy.stats import linregress

import plotly.express as px
import plotly.graph_objs as go
#import plotly.io as pio
#import plotly.offline as py

#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#init_notebook_mode(connected=True)


import datetime
import warnings
import base64

import os
import io

warnings.filterwarnings("ignore", category=UserWarning) # Ignorer les messages d'avertissement


# Add the sticky header with the title and fire icon
header = st.container()
header.markdown("<h1 style='text-align: center'><i style='color: red' class='fas fa-fire'></i> US WILDFIRE </h1>", unsafe_allow_html=True)
header.markdown("<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css'>", unsafe_allow_html=True)
header.markdown("""<div class='fixed-header'/>""", unsafe_allow_html=True)
### Custom CSS for the sticky header
st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: white;
        z-index: 999;
    }
    .fixed-header {
        border-bottom: 5px solid red;
    }
</style>
    """,
    unsafe_allow_html=True
)
# Répertoire du script
script_dir = os.path.dirname(__file__) 

page = st.sidebar.radio("Selection Page", ["📃 Introduction", "🔍 Exploration", "📈 Visualisation", "💻 Modelisation", "🧧 Conclusion"])

if page == "📃 Introduction":
    # Introduction
    st.write("""
    Les incendies de forêt constituent une préoccupation majeure aux États-Unis, avec des impacts importants sur l'environnement, la santé publique et l'économie. 
    Le jeu de données "1,88 millions wildfire US" offre une occasion unique d'explorer les causes, les conséquences et les tendances des incendies de forêt à travers le pays.

    Ce jeu de données contient des informations détaillées sur plus de 1,88 millions d'incendies de forêt survenus aux États-Unis entre 1992 et 2015. 
    Il comprend des variables telles que la date et l'heure de l'incendie, sa localisation, sa cause et sa superficie brûlée.
    """)

    # Ajout du texte et du lien
    st.markdown("Le jeu de données utilisé pour cette étude est disponible et téléchargeable au lien suivant: [Kaggle Dataset](https://www.kaggle.com/rtatman/188-million-us-wildfires)", unsafe_allow_html=True)

elif page == "🔍 Exploration":
    st.write("**Dans cette section, nous décrivons le processus d'exploration des données que nous avons entrepris dans le cadre de notre étude. Cette phase cruciale nous a permis de mieux comprendre la nature des données dont nous disposions, d'identifier les tendances, les modèles et les anomalies, ainsi que de formuler des hypothèses initiales pour nos analyses ultérieures.**")
    @st.cache_data
    def load_data_ini(file_path):
        # Charger le fichier CSV
        data = pd.read_csv(file_path)
        # Définir l'index sur OBJECTID
        data.set_index('OBJECTID', inplace=True)
        return data

    @st.cache_data
    def load_data_Explo(file_path):
        # Charger le fichier CSV
        data = pd.read_excel(file_path) 
        return data

    @st.cache_data
    def load_csv_year(file_path):
        # Charger le fichier Excel
        df_Year = pd.read_excel(file_path, sheet_name='States', header=6)
        return df_Year

    @st.cache_data
    def load_csv_year_old(file_path):
        # Charger le fichier Excel
        df_Year_old = pd.read_excel(file_path, sheet_name='States', header=4)
        return df_Year_old
    file_path_Fires = os.path.join(script_dir, "Fires.csv") 
    file_path_Explo = os.path.join(script_dir, "rapport_exploratoire.xlsx") 
    file_path_year = os.path.join(script_dir, "Popest-annual.xls") 
    file_path_year_old = os.path.join(script_dir, "Popest-annual-historical.xls") 
    # Appeler la fonction pour charger les données
    df_fires_ini = load_data_ini(file_path_Fires)
    rapport_exploratoire = load_data_Explo(file_path_Explo)
    df_Year = load_csv_year(file_path_year)
    df_Year_old = load_csv_year_old(file_path_year_old)

    st.write("### Exploration") 
    
    tab1, tab2, tab3 = st.tabs(["Data Frame", "Rapport exploratoire","Intégration de la population"])

    with tab1:
        st.write("*Cet onglet affiche les informations du dataset. Vous pouvez y trouver des informations telles que les dimensions du jeu de données, le nombre de doublons et de valeure manquantes*")
        
        option = st.selectbox("sélectionner une information:", 
                              ["Afficher les premières lignes du DataFrame",
                               "Informations supplémentaires",
                               "Informations du dataset",
                               "Statistiques descriptives",  
                               "Détail des valeurs manquantes"
                               ])
        
        if option == "Afficher les premières lignes du DataFrame":
           st.table(df_fires_ini.head(10))
        elif option == "Informations supplémentaires":
            Infos_Sup_Dataset_ini='''Dimensions du jeu de données : (1151201, 38)

Nombre de doublons : 0

Nombre de valeurs manquantes au global : 13319717'''
            st.code(Infos_Sup_Dataset_ini,language="python")
            # # Afficher les dimensions du jeu de données
            # st.write("Dimensions du jeu de données :", df_fires_ini.shape)
            # # Afficher le nombre de doublons
            # st.write("Nombre de doublons :", df_fires_ini.duplicated().sum())            
            # # Afficher le nombre de valeurs manquantes au global
            # st.write("Nombre de valeurs manquantes au global :", df_fires_ini.isna().sum().sum())
        elif option == "Informations du dataset":
            df_fires_info = '''<class 'pandas.core.frame.DataFrame'>
Index: 1151201 entries, 1 to 1151201
Data columns (total 38 columns):
 #   Column                      Non-Null Count    Dtype  
---  ------                      --------------    -----  
 0   FOD_ID                      1151201 non-null  int64  
 1   FPA_ID                      1151201 non-null  object 
 2   SOURCE_SYSTEM_TYPE          1151201 non-null  object 
 3   SOURCE_SYSTEM               1151201 non-null  object 
 4   NWCG_REPORTING_AGENCY       1151201 non-null  object 
 5   NWCG_REPORTING_UNIT_ID      1151201 non-null  object 
 6   NWCG_REPORTING_UNIT_NAME    1151201 non-null  object 
 7   SOURCE_REPORTING_UNIT       1151201 non-null  object 
 8   SOURCE_REPORTING_UNIT_NAME  1151201 non-null  object 
 9   LOCAL_FIRE_REPORT_ID        312846 non-null   object 
 10  LOCAL_INCIDENT_ID           465624 non-null   object 
 11  FIRE_CODE                   227570 non-null   object 
 12  FIRE_NAME                   509247 non-null   object 
 13  ICS_209_INCIDENT_NUMBER     14102 non-null    object 
 14  ICS_209_NAME                14102 non-null    object 
 15  MTBS_ID                     7442 non-null     object 
 16  MTBS_FIRE_NAME              7442 non-null     object 
 17  COMPLEX_NAME                3321 non-null     object 
 18  FIRE_YEAR                   1151201 non-null  int64  
 19  DISCOVERY_DATE              1151201 non-null  float64
 20  DISCOVERY_DOY               1151201 non-null  int64  
 21  DISCOVERY_TIME              446258 non-null   float64
 22  STAT_CAUSE_CODE             1151201 non-null  float64
 23  STAT_CAUSE_DESCR            1151201 non-null  object 
 24  CONT_DATE                   475122 non-null   float64
 25  CONT_DOY                    475122 non-null   float64
 26  CONT_TIME                   436104 non-null   float64
 27  FIRE_SIZE                   1151201 non-null  float64
 28  FIRE_SIZE_CLASS             1151201 non-null  object 
 29  LATITUDE                    1151201 non-null  float64
 30  LONGITUDE                   1151201 non-null  float64
 31  OWNER_CODE                  1151201 non-null  float64
 32  OWNER_DESCR                 1151201 non-null  object 
 33  STATE                       1151201 non-null  object 
 34  COUNTY                      568399 non-null   object 
 35  FIPS_CODE                   568399 non-null   float64
 36  FIPS_NAME                   568399 non-null   object 
 37  Shape                       1151201 non-null  object 
dtypes: float64(11), int64(3), object(24)
memory usage: 342.5+ MB'''
            st.code(df_fires_info,language="python")
        elif option == "Statistiques descriptives":
            st.table(df_fires_ini.describe())
        elif option == "Détail des valeurs manquantes":
            na_counts = df_fires_ini.isna().sum()
            total_counts = len(df_fires_ini)
            na_percentages = (na_counts / total_counts) * 100
            na_summary = pd.DataFrame({
                'Nombre de NaN': na_counts,
                'Pourcentage de NaN': na_percentages
            })
            st.write(na_summary)
            
    with tab2:
        st.write("*Cet onglet affiche les étapes et informations du rapport exporatoire*")
        

        # Filtrage du dataframe pour les valeurs qui ne sont pas 'Trop de valeurs unique' dans 'Valeurs uniques'
        df1 = rapport_exploratoire[rapport_exploratoire["Valeurs uniques"] != "Trop de valeurs unique"][["Nom de la colonne", "Type de données", "Valeurs uniques"]]

        # Filtrage du dataframe pour les valeurs qui ne sont pas 'Pas de NA' dans 'Gestion des NA'
        df2 = rapport_exploratoire[rapport_exploratoire["Gestion des NA"] != "Pas de NA"][["Nom de la colonne", "Type de données", "Taux de NA", "Gestion des NA"]]

        option = st.selectbox("sélectionner une information:", 
                              ["Afficher le rapport exploratoire complet",
                               "Afficher uniquement la gestion des NA",
                               "Afficher uniquement la gestion valeurs uniques" 
                               ])
        
         
        if option == "Afficher le rapport exploratoire complet":
            st.table(rapport_exploratoire)
        elif option == "Afficher uniquement la gestion des NA":
            st.table(df2)            
        elif option == "Afficher uniquement la gestion valeurs uniques":
            st.table(df1)

    with tab3:
        st.write("*Dans le cadre de notre exploration de données, nous avons pris la décision d'intégrer la notion de population par état et par année afin d'enrichir notre analyse et d'apporter une perspective démographique à notre étude sur les incendies.*") 
        
        

        option = st.selectbox("sélectionner une information:", 
                              ["Afficher le dataset de population",
                               "Afficher le dataset de population des année antérieurs"
                               ])
        
        if option == "Afficher le dataset de population":
            st.table(df_Year)
        elif option == "Afficher le dataset de population des année antérieurs":
            st.table(df_Year_old)

    pass

elif page == "📈 Visualisation":
    #---------------------------------------------------------------------------------------------
    #                                BEGIN CODE DEPLACE DANS VISUALISATION
    #---------------------------------------------------------------------------------------------
    # Load your dataset (replace with your own data loading code
    
    @st.cache_data
    def load_data(filename):
        data = pd.read_csv(filename)
        return data
    
    file_path_df_fires = os.path.join(script_dir, "df_Fires_Pop.csv") 
    df_fires = load_data(file_path_df_fires)
    
    #dictionnaire code qui mappe les abréviations des États américains à leurs noms complets

    code = {
            'AK':'Alaska',
            'AL':'Alabama' ,
            'AZ':'Arizona',
            'AR':'Arkansas',
            'CA':'California',
            'CO':'Colorado',
            'CT':'Connecticut',
            'DE':'Delaware',
            'DC':'District of Columbia',
            'FL':'Florida',
            'GA':'Georgia',
            'HI':'Hawaii',
            'ID':'Idaho',
            'IL':'Illinois',
            'IN':'Indiana',
            'IA':'Iowa',
            'KS':'Kansas',
            'KY':'Kentucky',
            'LA':'Louisiana',
            'ME':'Maine',
            'MD':'Maryland',
            'MA':'Massachusetts',
            'MI':'Michigan',
            'MN':'Minnesota',
            'MS':'Mississippi',
            'MO':'Missouri',
            'MT':'Montana',
            'NE':'Nebraska',
            'NV':'Nevada',
            'NH':'New Hampshire',
            'NJ':'New Jersey',
            'NM':'New Mexico',
            'NY':'New York',
            'NC':'North Carolina',
            'ND':'North Dakota',
            'OH':'Ohio',
            'OK':'Oklahoma' ,
            'OR':'Oregon',
            'PA':'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI':'Rhode Island',
            'SC':'South Carolina',
            'SD':'South Dakota',
            'TN':'Tennessee',
            'TX':'Texas',
            'UT':'Utah',
            'VT':'Vermont',
            'VA':'Virginia',
            'WA':'Washington',
            'WV':'West Virginia',
            'WI':'Wisconsin',
            'WY':'Wyoming'
            }
 
    # remplacement des valeurs de la colonne STATE du dataframe df_fires par les noms complets des États correspondants, en utilisant le dictionnaire code comme référence.

    df_fires['STATE_NAME'] = df_fires['STATE'].map(code)
    @st.cache_data
    def create_figure():
        df_fires_Discovery_date = df_fires[['FIRE_YEAR', 'DISCOVERY_DOY']]
        Mois = ['Jan','Fev','Mars','Avril','Mai','Juin','Juil','Aout','Sept','Oct','Nov','Dec']
        #Fonction pour obtenir la date complète à partir du jour et de l'année
        def calculate_month(row): 
            year = row['FIRE_YEAR']
            day_of_year = row['DISCOVERY_DOY']
            d = datetime.datetime.strptime('{} {}'.format(day_of_year, year),'%j %Y')
            return str(d.month) +'-'+ str(d.day) + '-' + str(year)

        #Application de la fonction calculate_month
        #df_fires_Discovery_date['DISCOVERY_DATE'] = df_fires_Discovery_date.apply(calculate_month, axis=1)
        # Calculate the discovery date
        df_fires_Discovery_date['DISCOVERY_DATE'] = pd.to_datetime(df_fires_Discovery_date[['FIRE_YEAR', 'DISCOVERY_DOY']].assign(DAY=lambda x: x['DISCOVERY_DOY']).apply(lambda x: f"{x['FIRE_YEAR']}-{x['DISCOVERY_DOY']:03}", axis=1), format='%Y-%j')
        #convertion de la colonne DISCOVERY_DATE en format datetime
        df_fires_Discovery_date['DISCOVERY_DATE'] = pd.to_datetime(df_fires_Discovery_date['DISCOVERY_DATE'])

        #Extraction du jour de la date de decouverte du feu
        df_fires_Discovery_date['DISCOVERY_DAY'] = df_fires_Discovery_date['DISCOVERY_DATE'].dt.day

        #Extraction du mois de la date de decouverte du feu
        df_fires_Discovery_date['DISCOVERY_MONTH'] = df_fires_Discovery_date['DISCOVERY_DATE'].dt.month

        df_fires['DISCOVERY_MONTH'] = df_fires_Discovery_date['DISCOVERY_MONTH']
        df_cause_per_month = pd.crosstab(df_fires['DISCOVERY_MONTH'],df_fires['STAT_CAUSE_DESCR'])
        Cause_Naturel = df_cause_per_month['Lightning']
        Cause_Humaine = df_cause_per_month[['Arson','Campfire','Children','Debris Burning','Equipment Use','Fireworks','Smoking']].apply(sum,axis=1)
        Cause_Infrastructure = df_cause_per_month[['Powerline','Railroad','Structure']].apply(sum,axis=1)
        cause_Misc = df_cause_per_month[['Miscellaneous', 'Missing/Undefined']].apply(sum,axis=1)
        df_cause = pd.DataFrame({'Naturel':Cause_Naturel,'Humaine':Cause_Humaine,'Infrastructure':Cause_Infrastructure,
                            'Autre':cause_Misc})

    # Création d'une figure Plotly
        fig = go.Figure()
        fig1 = go.Figure()
        fig2 = go.Figure()
        fig3 = go.Figure()

        # Creation du grahique en Barre: nombre de feu par le mois de l'année
        fig.add_trace(go.Bar(x=sorted(df_fires_Discovery_date['DISCOVERY_MONTH'].unique()),
                            y=df_fires_Discovery_date['DISCOVERY_MONTH'].value_counts().sort_index(),
                            width=0.8,
                            marker_color='red', name = 'Nbr de Feux'))

        # mise en forme du graphique
        fig.update_layout(title='Nombre total de feux de forêt déclarés par mois',
                        title_x=0.2,
                        yaxis_title='Nombre total de feux signalés',
                        bargap=0.05,  # Espacement entre les barres
                        xaxis=dict(
                            tickvals=sorted(df_fires_Discovery_date['DISCOVERY_MONTH'].unique()),
                            ticktext=Mois
                        ))
        

        # Creation graphique qui affiche le tracés des surfaces brulés par causes en fonction des mois 
        i=0
        for col in df_cause.columns:
            fig1.add_trace(go.Scatter(x=df_cause.index,y=df_cause.iloc[:,i],mode = 'lines+markers',marker_symbol='circle',name=col))
            i+=1

        # Mise en forme du graphique
        fig1.update_layout(
            title_text='Surfaces brulées et Causes des feux de forêts par mois', # title of plot
            title_x=0.2,
            yaxis_title_text='Surface brulée (acres)', # yaxis label
            xaxis=dict( tickvals=df_cause.index,ticktext=Mois)
        )

        fig2 = px.box(df_cause, y=['Naturel','Humaine'])

        # Mise en forme du graphique
        fig2.update_layout(
            yaxis_title='Surface brulée (Acres)',
            xaxis_title="Causes Incendies")
        
        df_cause_describe = df_cause[['Naturel','Humaine']].describe()
        
    # Creation graphique qui affiche le tracés des Superficie brûlée et cause des incendies en fonction des mois de l'année
        i=0
        for col in df_cause.columns:
            fig3.add_trace(go.Scatter(x=df_cause.index,y=df_cause.iloc[:,i],mode = 'markers',name=col))
            slope, intercept = np.polyfit(df_cause.index, df_cause.iloc[:, i], 1)
            fig3.add_trace(go.Scatter(x=df_cause.index, y=slope*df_cause.index + intercept, mode='lines', name='Regression line:'+col))
            i+=1
        fig3.update_layout(
            title_text='Superficie brûlée et cause des incendies par mois', # title of plot
            title_x=0.2,
            xaxis_title_text="Mois", # xaxis label
            yaxis_title_text='Surface brulée (acres)', # yaxis label
            xaxis=dict( tickvals=df_cause.index,ticktext= Mois))

        return fig,fig1,fig2,fig3,df_cause_describe

    fig_0,fig_1,fig_2,fig_3,df = create_figure()
    

    # st.sidebar.image("wildfire_animation_flag.gif", width=150)

    # st.markdown("""
    #     <style>
    #         img {
    #             width: 150px;
    #             height: auto;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)# Code for Exploration page
    #---------------------------------------------------------------------------------------------
    #                                FIN DEPLACE DANS VISUALISATION
    #---------------------------------------------------------------------------------------------
    # Add 4 tabs
    tab1, tab2, tab3 = st.tabs(["Apercu", "Visualisation spatio-temporelles","Statistiques"])
    
    # Add content to each tab
    with tab1:
        st.write("*Cet onglet fournit une vue d’ensemble des données de feux de forêts. Vous pouvez y trouver des informations telles que le nombre total d’incendies, la superficie totale brûlée et la répartition géographique des feux*")

        fig1 = go.Figure()
        fig2 = go.Figure()
        fig3 = go.Figure()
        fig4 = go.Figure()
        fig5 = go.Figure()

    # Graphique 1 # CHOROPLETH
        fires_state_name = df_fires.groupby(['STATE','STATE_NAME'])['FIRE_SIZE_CLASS'].value_counts().groupby(['STATE','STATE_NAME']).agg(sum)
        fires_state_name = fires_state_name.sort_values(ascending=False)
        df_fire_map = fires_state_name.reset_index()

        data = dict(type = 'choropleth',
                    locations = df_fire_map['STATE'],
                    locationmode = 'USA-states',
                    colorscale= 'Reds',
                    z=df_fire_map['count'],
                    text= df_fire_map['STATE_NAME'],
                    hovertemplate='<br>'.join([
                        '<b>%{text}</b>',  # State abbreviation
                        '%{location}<br>',  # State name
                        'Count: %{z}<br>'  # Count value
                    ]),
                    colorbar = {'title':'Feux de forêt'})

        layout = dict(geo = {'scope':'usa'}
                    #title={'text': 'Representation des feux forêt signalés dans chaque état de 1992 à 2015'}
                    )

        choromap = go.Figure(data = [data],layout = layout)
        choromap.add_scattergeo(
                            locations = df_fire_map['STATE'],
                            locationmode = 'USA-states',
                            text= df_fire_map['STATE'],
                            mode = 'text',
                            hoverinfo='skip'
                            )
    # Graphique 2

    # Regroupement des incendies par nom de chaque état
        fires_state = df_fires.groupby('STATE_NAME')['FIRE_SIZE_CLASS'].value_counts().groupby('STATE_NAME').agg(sum)

        #Trie de la DataFrame fires_state dans l'ordre décroissant 
        fires_state = fires_state.sort_values(ascending=False)

        # Créer une figure Plotly
        fig1 = go.Figure()

        # Create a list of colors for the gradient
        colors = ['rgb(255, 165, 0)' if i >= 10 else f'rgb({int(255 * (1 - (i - 9) / 10))}, 0, 0)' for i in range(len(fires_state.values))]

        fig1.add_trace(go.Bar(x=fires_state.index,
                            y=fires_state.values,
                            width=0.8,
                            marker_color=colors))  # Assign the color list to marker_color

        # Mise en forme du graphique
        fig1.update_layout(
                        yaxis_title="Nombre de feux de forêt signalés",
                        #plot_bgcolor='rgba(0,0,0,0)',
                        bargap=0.05, 
                        xaxis=dict(tickmode='array',
                                    tickvals=list(range(len(fires_state.index))),
                                    ticktext=fires_state.index.tolist(),
                                    tickangle=-45)
                        )

        # Ajout d'une forme rectangulaire pour encadrer les 10 états ayant le plus d'incendies
        fig1.update_layout(
            shapes=[
                dict(
                    type="rect",
                    x0=fires_state.index[0],
                    y0=0,
                    x1=fires_state.index[9],
                    y1=fires_state.values.max(),
                    fillcolor=None,
                    line=dict(color="black"),
                    xref="x",
                    yref="y"

                )
            ]
        )

    # Graphique 3 
        Fire_per_year = df_fires['FIRE_YEAR'].value_counts().sort_index()

        fig2 = go.Figure()

        colors = []
        for value in Fire_per_year.values:
            r = min(255, int(value * 255 / max(Fire_per_year.values))) 
            couleur = f'rgb(255, {255 - r}, 0)'  
            colors.append(couleur)

        fig2.add_trace(go.Bar(x=Fire_per_year.index,
                            y=Fire_per_year.values,
                            width=0.8,
                            marker_color=colors,
                            name = 'Feux forêts')) 

        fig2.add_trace(go.Scatter(x=Fire_per_year.index,
                                y=Fire_per_year.values,
                                mode = 'lines',marker_color = 'Red',name = 'Évolution des feux de fôrets'))

        fig2.update_layout(
                        bargap=0.05,  
                        xaxis=dict(tickangle=45),  
                        font=dict(family='Arial', size=12, color='black'),  
                        width=800,  
                        height=400)

        max_value = Fire_per_year.max()
        max_year = Fire_per_year.idxmax()
        fig2.add_annotation(text=f'Max : {max_value} ({max_year})',
                            x=max_year, y=max_value,
                            showarrow=True, arrowhead=1, arrowcolor='black',
                            ax=-50, ay=-30)
      
    # Graphique 4
        # Calcul de la fréquence de chaque cause d'incendie
        fire_causes = df_fires['STAT_CAUSE_DESCR'].value_counts()

        # Creation graphique Barre qui affiche les causes et la fréquence des incendies
        fig3 = px.bar(fire_causes, x=fire_causes.index, y=fire_causes.values,
             color=fire_causes.values,  # color by values
             color_continuous_scale="reds")  # red color gradient
        
        fig3.update_layout(
                  xaxis={'title': ""},
                  yaxis={'title': ""},
                  coloraxis={'colorbar':{'title':'Feux déclarés'}}) 
    #Graphique 5
        # fig4= px.scatter(df_fires, x="STAT_CAUSE_DESCR", y="FIRE_SIZE", color='STAT_CAUSE_DESCR')
        # fig4.update_layout(
        #     #title_text="Surfaces brulées en fonction des causes d'incendies", # title of plot
        #     xaxis_title_text="", # xaxis label
        #     yaxis_title_text='Surface brulés (acres) ', # yaxis label
        #     showlegend=False)
    #Graphique 6
        # calcule de la population pour chaque état et année d'incendie
        population_growth = df_fires.groupby(['FIRE_YEAR'])['POPULATION'].mean().reset_index()

        # création d'un graphique en barres représentant la population en fonction des Etats colorées en fonction des années
        fig5 = px.bar(population_growth, y="POPULATION", x="FIRE_YEAR",color_discrete_sequence=["#447597"])

        fig5.add_trace(go.Scatter(x=population_growth.FIRE_YEAR,
                                        y=population_growth.POPULATION,
                                        mode = 'lines',marker_color = 'black',name = 'Évolution de la population'))
        fig5.update_layout(
                        xaxis_title='',
                        yaxis_title='')
    
    # Create a selection box
        option = st.selectbox("sélectionner un graphique:", 
                              ["Évolution des feux forêt",
                               "Les états les plus touchés par les feux de forêt",
                               "Représentation  de la densité des feux forêt",
                               "Principales Causes des feux de forêt",
                               #"Surfaces brulées en fonction des causes d'incendies",
                               "Croissance de la population"])
        
        if option == "Évolution des feux forêt":
            st.plotly_chart(fig2, use_container_width=True)
        elif option == "Les états les plus touchés par les feux de forêt":
            st.plotly_chart(fig1, use_container_width=True)
        elif option == "Représentation  de la densité des feux forêt":
           st.plotly_chart(choromap, use_container_width=True)
        elif option == "Principales Causes des feux de forêt":
            st.plotly_chart(fig3, use_container_width=True)
        #elif option == "Surfaces brulées en fonction des causes d'incendies":
            #st.plotly_chart(fig4, use_container_width=True)
        elif option == "Croissance de la population":
            st.plotly_chart(fig5, use_container_width=True)

    with tab2:
        st.write("*Dans cet onglet, vous explorerez les tendances temporelles des feux de forêts. Vous pourrez observer comment les incendies varient au fil des années et des mois de l'année*")

        graph_type = st.radio("", ("Vue Cartographique", "Vue Graphique en barre"),horizontal=True)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content:center;} </style>', unsafe_allow_html=True)
        if graph_type =="Vue Cartographique":
            #Création tableau croisé qui montre le nombre d'incendies qui ont eu lieu dans chaque état pour chaque année
            State_Fire = pd.crosstab(df_fires['STATE'],df_fires['FIRE_YEAR'])

            #création d'une carte choroplèthe qui représente le nombre d'incendies par état aux États-Unis
            # définition d'un dictionnaire "data" qui contient les paramètres de la carte choroplèthe.

            data = dict(type = 'choropleth',
                        locations = State_Fire.index,
                        locationmode = 'USA-states',
                        z = State_Fire.iloc[:,0],
                        colorscale= 'Reds',
                        colorbar = {'title':'Feux de forêt'},
                        text= [code[state] for state in State_Fire.index],
                        hovertemplate='<br>'.join([
                    '<b>%{text}</b>',  # State abbreviation
                    '%{location}<br>',  # State name
                    'Count: %{z}<br>'  # Count value
                        ]) 
                    )


            #définition d'un dictionnaire "layout" qui contient les paramètres de la mise en page de la carte
            layout = dict(geo = {'scope':'usa'})
            choromap2 = go.Figure(data=[data],layout=layout)
            choromap2.add_scattergeo(
                        locations = df_fire_map['STATE'],
                        locationmode = 'USA-states',
                        text= df_fire_map['STATE'],
                        mode = 'text',
                        hoverinfo='skip'
                        )
            choromap2.update_layout(
                title={'text':'Nombre de feux de fôrets dans chaque état par année ',
                    'xanchor':'center',
                    'yanchor':'top',
                    'x':0.5})



            # Creation et ajout d'un curseur qui permet de naviguer à travers les différentes années d'incendies 
            steps = []
            for i in range(len(State_Fire.columns)):
                step = dict(
                    method="restyle",
                    args=[{"z": [State_Fire.iloc[:,i]]},
                        {"title": "Year: " + str(State_Fire.columns[i])}],
                    label=str(State_Fire.columns[i])
                )
                steps.append(step)

            sliders = [dict(
                active=0,
                pad={"t": 5},
                currentvalue={"prefix": "Année: "},
                steps=steps
                
            )]
            #Mise a jour de la carte choroplèthe
            choromap2.update_layout(
                sliders=sliders
            )
            st.plotly_chart(choromap2, use_container_width=True)
        
        else:
            fig7 = go.Figure()
            colors = ['orangered']
            # Create pivot table
            pivot_df = df_fires.groupby('FIRE_YEAR')['STATE_NAME'].value_counts().reset_index(name='Fires').pivot(index='FIRE_YEAR', columns='STATE_NAME', values='Fires')
            #means = pivot_df.mean(axis=1)

            # Preparation des données pour plotly
            year_list = pivot_df.index.tolist()
            fire = pivot_df.values
            state_labels = pivot_df.columns.tolist()

            # Création d'un graphique en Barre
            fig7 = go.Figure()
            for i in np.arange(0,len(year_list),1):
                fig7.add_trace(go.Bar(x=state_labels, y=fire[i], name=str(year_list[i]), hovertemplate='State: %{x}<br>Number of Fires: %{y:,}',
                                      marker_color=colors[i % len(colors)]))

            # mise en forme du graphe
            fig7.update_layout(title_text='Nombre de feux de fôrets dans chaque état par année',
                               title_x=0.2,
                            xaxis_title='',
                            yaxis_title='Nombre total de Feux signalés',
                            xaxis=dict(tickangle=-45))

            # Create a list to store the visibility of each trace
            visibility = [False] * len(year_list)

            # Set the visibility of the first trace (year 1992) to True
            visibility[year_list.index(1992)] = True

            # Update the figure with the initial visibility
            for i, trace in enumerate(fig7.data):
                trace.visible = visibility[i]

            # Creation et ajout d'un curser qui permet de naviguer à travers les différentes années d'incendies 
            steps = []
            for i in range(len(year_list)):
                step = dict(
                    method="update",
                    args=[{"visible": [False] * len(year_list)}],
                    label=str(year_list[i])
                )
                step["args"][0]["visible"][i] = True
                steps.append(step)

            sliders = [dict(
                active=year_list.index(1992),
                pad={"t": 50},
                currentvalue={"prefix": ""},
                steps=steps
            )]

            fig7.update_layout(
                sliders=sliders
            )
            st.plotly_chart(fig7, use_container_width=True)
        st.write("<hr style='border: 1px solid black'>", unsafe_allow_html=True)
        
        graph_temp = st.radio("", ("Jour de l'année", "Mois de l'année"),horizontal=True)
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content:center;} </style>', unsafe_allow_html=True)
        ##########################################
    
        ###########################
        if graph_temp =="Jour de l'année":
        # Extraction du jour de l'année'
            DOY =df_fires['DISCOVERY_DOY']

            # Création d'une figure Plotly
            fig8 = go.Figure()

            # Creation de l'histogramme
            fig8.add_trace(go.Histogram(x=DOY,name='Doy',marker=dict(color='red')))
            fig8.update_layout(
                title_text="Feux de forêts déclarés en fonction du jour de l'année ", 
                title_x=0.2,
                xaxis_title_text="Jour de l'année", 
                yaxis_title_text='Nombre de feux de forêts ', 
                bargap=0.1, 
                bargroupgap=0.1
            )
            # jour de l'année (DOY) où le plus grand nombre de feux de forêt ont été déclarés
            max_x = df_fires['DISCOVERY_DOY'].value_counts().idxmax()

            # le plus grand nombre de feux de forêt déclarés pour un jour de l'année
            max_y = df_fires['DISCOVERY_DOY'].value_counts().max()

            #Ajout annotation graphique pour mettre en évidence le jour de l'année où le plus grand nombre de feux de forêt ont été déclarés
            fig8.add_annotation(x=max_x,
                            y=max_y,
                            text=str(max_x)+" ème jour = 4 Juillet ",
                            showarrow=True,
                            arrowhead=2,
                            ax=100,
                            ay=25,
                            arrowsize=1,
                            arrowwidth=2,
                            arrowcolor='black')
        #-------
            # DataFrame fire_size_by_doy qui résume la taille totale des feux de forêt par jour de l'année (DOY).
            fire_size_by_doy =pd.DataFrame(df_fires.groupby(['DISCOVERY_DOY']).FIRE_SIZE.sum().sort_values(ascending=False)).reset_index()

            # Création d'une figure Plotly
            fig9=go.Figure()

            # Creation de graphique en barre
            fig9.add_trace(go.Bar(x=fire_size_by_doy['DISCOVERY_DOY'],
                                y=fire_size_by_doy['FIRE_SIZE'],
                                width=0.8,
                                marker_color='red'))

            # Mise en forme du graphique
            fig9.update_layout(title="surface brulée cumulée par le jour de l'année",
                               title_x=0.2,
                            xaxis_title="Jour de l'année",
                            yaxis_title='Surface brulée (acres)'
                            )

            # Jour de l'année correspondant à la valeur maximale de la taille des feux de forêt
            max_x = fire_size_by_doy.loc[fire_size_by_doy['FIRE_SIZE'].idxmax(), 'DISCOVERY_DOY']
            st.plotly_chart(fig8, use_container_width=True)
            st.plotly_chart(fig9, use_container_width=True)
    
        elif graph_temp =="Mois de l'année":
            st.header("Y a t'il une saison des feux?")
                #extraction 3 colonnes du dataframe df_fires et les stocke dans un nouveau dataframe nommé df_fires_Discovery_date

            # fig,fig1,fig2,df = create_figure()
            st.plotly_chart(fig_0, use_container_width=True)
            st.plotly_chart(fig_1, use_container_width=True)
            
    with tab3:
        st.write("*Dans cet onglet, vous trouverez des statistiques effectués concernant les feux de forêt aux États-Unis*")

        # Create a selection box
        option_Stat = st.selectbox("sélectionner une statistique:", 
                              ["Analyse univariée: Causes des feux de forêt",
                               "Tests ANOVAs et CHI2",
                               #"ANOVA: Surfaces brulées et Cause des Feux de forêt",
                               #"ANOVA: Surfaces brulées et Etats",
                               #"CHI2: Causes et Classes de feux forêt",
                               "Analyse Multivariée: Surface brûlée en fonction de l’année",
                               "Analyse Multivariée: Superficie brûlée et cause des incendies par mois",
                               "Analyse Multivariée: Population et feux de forêt au cours des années"])
        
        
        if option_Stat == "Analyse univariée: Causes des feux de forêt":
            #fig,fig1,fig2,df = create_figure()
            st.plotly_chart(fig_2, use_container_width=True)
            st.markdown("<u><center>Statistiques descriptives causes 'Naturel' et 'Humain:</center></u>", unsafe_allow_html=True)
            st.write("<div style='text-align: center'>", unsafe_allow_html=True)
            st.dataframe(df)
            st.write("</div>", unsafe_allow_html=True)
        elif option_Stat == "Tests ANOVAs et CHI2":
            #st.write(anova1)
            st.write("")
            st.write("")
            st.markdown("<center><b><font color='red'>ANOVA: Surfaces brulées et Cause des Feux de forêt</font></b></center>", unsafe_allow_html=True)
            st.write("")
            st.write("")
            df1 = pd.read_csv('ANOVA1.csv')
            st.table(df1)
            st.write("*Aux vues de la p-valeur, la relation entre la superficie brûlée et les causes des feux de forêt est vérifié*")
            st.write("<hr style='border: 1px solid black'>", unsafe_allow_html=True)

            st.markdown("<center><b><font color='red'>ANOVA: Surfaces brulées et Etats</font></b></center>", unsafe_allow_html=True)
            st.write("")
            st.write("")
            df2 = pd.read_csv('ANOVA2.csv')
            st.table(df2)
            st.write("*Aux vues de la p-valeur, la relation entre la superficie brulée et l'état est vérifié*")
            st.write("<hr style='border: 1px solid black'>", unsafe_allow_html=True)

            st.markdown("<center><b><font color='red'>CHI2: Causes et Classes de feux forêt</font></b></center>", unsafe_allow_html=True)
            st.write("")
            st.write("")
            ct = pd.crosstab(df_fires['STAT_CAUSE_DESCR'], df_fires['FIRE_SIZE_CLASS'])
            resultats_chi2 = chi2_contingency(ct)
            statistique = resultats_chi2[0]
            p_valeur = resultats_chi2[1]
            st.write("Resultat Test Chi-2 ")
            st.write("La statistique du test est : ", statistique)
            st.write("La p-valeur du test est : ", p_valeur)
            st.write("*Aux vues de la p-valeur, la relation entre les causes de feux de forêt et les classes de feux est vérifié*")

        elif option_Stat == "Analyse Multivariée: Surface brûlée en fonction de l’année":
            Size_fire_Year = pd.DataFrame(df_fires.groupby(['FIRE_YEAR']).FIRE_SIZE.sum()).reset_index()

            #Creation nuage de point et courbe de régression linéaire 
            fig = px.scatter(
                Size_fire_Year, x='FIRE_YEAR' , y='FIRE_SIZE',trendline="ols",color_discrete_sequence=['red'])

            # Mise en forme du graphique
            fig.update_layout(
                title="Surface brûlée en fonction de l’année",
                title_x=0.2,
                coloraxis_showscale=False,
                yaxis_title='Surface brulée (Acres)',
                xaxis_title=' Année',
                #title= 'Surface brulée sur la période 1992 - 2015',
                #title_x=0.5,
                #title_font=dict(family='Arial', size=20, color='#fc3d03')
                )

            st.plotly_chart(fig, use_container_width=True)  

        elif option_Stat == "Analyse Multivariée: Superficie brûlée et cause des incendies par mois":
            st.plotly_chart(fig_3, use_container_width=True)
            
        elif "Analyse Multivariée: Population et feux de forêt au cours des années":
            
            fig_pop = go.Figure()
            # Regroupement par état et année, compter le nombre d'incendies
            fires_by_state_year = df_fires.groupby(['STATE_NAME', 'FIRE_YEAR']).size().reset_index(name='FIRE_COUNT')

            # Regroupement paretat et année, calcul moyenne de la population 
            population_by_state_year = df_fires.groupby(['STATE_NAME', 'FIRE_YEAR'])['POPULATION'].mean().reset_index()

            # Fusion des deux dataframe :population_by_state_year et  fires_by_state_year
            fires_vs_population = fires_by_state_year.merge(population_by_state_year, on=['STATE_NAME', 'FIRE_YEAR'])

            # Create a figure
            fig_pop = px.scatter(fires_vs_population, x="FIRE_COUNT", y="POPULATION", color="STATE_NAME", size="FIRE_COUNT",
                            hover_name="STATE_NAME", hover_data=["STATE_NAME", "FIRE_YEAR", "FIRE_COUNT", "POPULATION"], 
                            animation_frame="FIRE_YEAR", trendline="ols", 
                            trendline_options=dict(color="black", width=2, dash="dash"))

            fig_pop.update_layout(title={'text': "Incendies par rapport à la population par État", 'x': 0.2},
                            xaxis={'title': "Nombre incendie"},
                            yaxis={'title': "Population"})

            st.plotly_chart(fig_pop, use_container_width=True)
    pass

elif page == "💻 Modelisation":
    tab1, tab2 = st.tabs(["Préparation du Dataset", "Test de Modélisation"])

    # Add content to each tab
    with tab1:
        st.subheader(":blue[Informations du Dataset pour la modélisation et choix des variables :]")
                
        # Affichage des informations
        st.write('Il y a 0 Valeurs Manquants ')
        st.write("Il y a 18760 Doublons ")
        st.write("Le taux de doublons dans le DataFrame est de 1%")

        if st.checkbox("Afficher les informations du DataSet") :
            code00='''<class 'pandas.core.frame.DataFrame'>
Index: 1861705 entries, 0 to 1880464
Data columns (total 11 columns):
#   Column             Dtype  
---  ------             -----  
0   FIRE_YEAR          int64  
1   DISCOVERY_MONTH    int32  
2   DISCOVERY_WEEKDAY  int64  
3   DISCOVERY_DATE     float64
4   DISCOVERY_DOY      int64  
5   STAT_CAUSE_DESCR   object 
6   FIRE_SIZE_CLASS    object 
7   LATITUDE           float64
8   LONGITUDE          float64
9   STATE              object 
10  POPULATION         float64
dtypes: float64(4), int32(1), int64(3), object(3)
memory usage: 163.3+ MB'''
            st.code(code00,language="python")
                        
        st.write("La variable cible est : « FIRE_SIZE_CLASS »")

        st.subheader(":blue[Séparation du jeu des données :]")     
      
        st.write("Nous avons testé 3 types de répartitions du dataset (80,20), (75,25) et (70,30) mais celles-ci n’ont pas amélioré les performances ou la métrique « accuracy ».")
        st.write("Le résultat des test pour l'accuracy des 2 modèles de classification étaient à 42% pour Model LogisticRegression et 36% pour Model DecissionTreeClassifier.")
        st.write("Finalement nous avons choisi la répartition suivante : ")
        code01='''X_train, X_test, y_train, y_test = train_test_split(feats, target, 
                test_size=0.2, random_state=12)'''
        st.code(code01,language="python")

        st.subheader(":blue[Gestion de variables et Encodage des données :]")

        st.write("Nous avons encodés 3 variables :")
        st.write("« STATE » (Code de l’Etat) : Cette variable a été convertie en une variable représentant le nombre d’incendies par États présents dans le dataset.")
        st.write("« STAT_CAUSE_DESCR » (Causes d’incendie) :  Les 14 sous-catégories existantes ont été regroupées en 4 catégories, puis codées.")
        st.write("« FIRE_SIZE_CLASS » (Classe de feux) : Les 7 classes de feux (['A', 'B', 'G', 'C', 'D', 'F', 'E']) ont été réduites en 3 catégories (« Low », « Medium », « High »)")

        st.subheader(":blue[Standardisation :]")
        st.write("La standardisation a été appliquée à presque toutes les variables explicatives, sauf à la variable « STAT_CAUSE_DESCR » (encodée à l’étape précédente).")
        if st.checkbox("Afficher le DataSet(X_train) avec standardisation") :
            code02='''   ID            FIRE	       DISCOVERY 	DISCOVERY 	DISCOVERY 	DISCOVERY 	STAT_CAUSE 	LATITUDE 	LONGITUDE 	STATE 	    POPULATION
              YEAR         MONTH         WEEKDAY       DATE          DOY          DESCR
1287687 	0.789362 	1.714210 	-0.022616 	0.854198 	1.756478 	    3 	    1.026474 	       1.284176 	-0.055927 	0.835573
1517241 	1.089645 	-1.332803 	1.460642 	1.039522 	-1.343487 	    1 	    -0.127073 	0.453578 	-0.922273 	-0.393746
774970 	-1.462757 	-1.332803 	-1.011455 	-1.511048 	-1.321265 	    3 	    -0.059514 	0.050152 	-0.722670 	-0.690853
339297 	0.639221 	0.021425 	-1.505874 	0.637233 	-0.043502 	    3 	    -0.756480 	-0.689539 	-0.810536 	-0.811842
459299 	0.789362 	-1.671360 	-0.517036 	0.724348 	-1.754594 	    3 	    -0.690421 	0.766056 	1.430383 	-0.087001
... 	... 	... 	... 	... 	... 	... 	... 	... 	... 	...
568892 	0.489080 	-0.994246 	0.471803 	0.451909 	-0.999047 	    3 	    -0.210035 	0.071385 	-0.722670 	-0.657192
1477050 	1.089645 	-1.671360 	0.966222 	1.033359 	-1.510152 	    1 	    -0.297885 	0.046461 	-0.722670 	-0.642479
1316386 	-0.561909 	-0.994246 	-1.011455 	-0.602097 	-1.087935 	    1 	    0.467928 	       0.959321 	-1.080965 	-0.831238
1826490 	1.690210 	0.021425 	-1.505874 	1.690006 	0.012053 	    1 	    1.355260 	       -1.603035 	-0.400599 	-0.620599
1537152 	0.789362 	0.359982 	0.966222 	0.800368 	0.300939 	    3 	    -1.058004 	-0.049489 	1.017468 	1.358921

1489364 rows × 10 columns'''
            st.code(code02,language="python")
    
    with tab2:
        st.subheader(":blue[Modèles Initiaux :]")

        st.write("Model « LogisticRegression » et Model « RandomForest » : Ces modèles produisent des prédictions déséquilibrées des clases pour la variable cible.")
        st.write("Model « DecisionTreeClassifier » : Il prédit bien les trois classes, mais avec une « accuracy » de 0.79 et des précisions moins bonnes pour les autres classes non prédites précédemment.")

        tabMI1, tabMI2, tabMI3 = st.tabs(["Logistic Regression", "Random Forest", "Decision Tree Classifier"])

        # Add content to each tab
        with tabMI1:
            st.write("Accuracy :")   
            code03='''0.85'''
            st.code(code03,language="python")
            st.write("Confusion matrix :")
            code04='''Prédiction 	1
Realité 	
0 	    5059
1 	    317496
2 	    49786'''
            st.code(code04,language="python")
        with tabMI2:
            st.write("Accuracy :")   
            code05='''0.85'''
            st.code(code05,language="python")
            st.write("Confusion matrix :")
            code06='''Prédiction 	1
Realité 	
0 	    5059
1 	    317496
2 	    49786'''
            st.code(code06,language="python")
        with tabMI3:
            st.write("Accuracy :")   
            code07='''0.79'''
            st.code(code07,language="python")
            st.write("Confusion matrix :")
            code08='''Prédiction 	0 	 1 	    2
Realité 			
0 	    937 	2678 	    1444
1 	    3158 	278770     35568
2 	    1517 	32847 	    15422'''
            st.code(code08,language="python")

        st.subheader(":blue[Modèles avec Random Over Sample :]")

        st.write("Model « LogisticRegression » : Faible performance avec seulement 0.42 de bonnes prédictions.")
        st.write("Model « RandomForest » : Les performances de classification sont meilleures.")
        st.write("Model « DecisionTreeClassifier » : Les performances de classification sur l’ensemble de test diminue par rapport au modèle précèdent. Il maintien à l'hauteur de 0.80 la métrique de l'accuracy.")

        tabOS1, tabOS2, tabOS3 = st.tabs(["Logistic Regression", "Random Forest", "Decision Tree Classifier"])

        # Add content to each tab
        with tabOS1:
            st.write("Accuracy :")   
            code09='''0.42'''
            st.code(code09,language="python")
            st.write("Confusion matrix :")
            code10='''Prédiction 	0 	1 	    2
Realité 			
0 	    2954 	947 	    1158
1 	    103151 	126513     87832
2 	    10620 	13180 	    25986'''
            st.code(code10,language="python")
        with tabOS2:
            st.write("Accuracy :")   
            code11='''0.84'''
            st.code(code11,language="python")
            st.write("Confusion matrix :")
            code12='''Prédiction 	0 	1 	    2
Realité 			
0 	    812 	2911 	    1336
1 	    962 	296014     20520
2 	    818 	34828 	    14140'''
            st.code(code12,language="python")
        with tabOS3:
            st.write("Accuracy :")   
            code13='''0.80'''
            st.code(code13,language="python")
            st.write("Confusion matrix :")
            code14='''Prédiction 	0 	1 	    2
Realité 			
0 	    829 	2824 	    1406
1 	    2615 	281249     33632
2 	    1378 	33917 	    14491'''
            st.code(code14,language="python")

        st.subheader(":blue[Hyperparamètres pour le « Decision Tree Classifier » :]")

        st.write("Pour optimiser la modélisation nous avons chercher les hyperparamètres et obtenu comme résultat :")

        code02='''Meilleurs hyperparamètres: {'max_depth': 20, 'max_features': None, 
            'min_samples_leaf': 1, 'min_samples_split': 2}
Meilleur score: 0.8168431912233691'''
        st.code(code02,language="python")

        st.write("En re entrainant avec les variables ci-dessus et un random_state=12 nous avons obtenu une accuracy de 0.68")
        st.write("Suite à ce calcul nous avons analysé les variables selon leur importance pour faire une réduction des variables par la suite et comparer les résultats. Pour information nous avons à la base 10 variables explicatives.")
        
        tabHP1, tabHP2, tabHP3 = st.tabs(["HP1", "HP2", "HP3"])

        # Add content to each tab
        with tabHP1:
            st.write("Sélection des 4 caractéristiques les plus importantes :")
            code50='''top_4 = ["LONGITUDE", "LATITUDE", "DISCOVERY_DATE", "DISCOVERY_DOY"]'''
            st.code(code50,language="python")
           
            st.write("Accuracy :")   
            code15='''0.67'''
            st.code(code15,language="python")
            st.write("Confusion matrix :")
            code16='''Prédiction 	0 	1 	    2
Realité 			
0 	    2425 	1337 	    1297
1 	    24534 	220588     72374
2 	    5837 	17228 	    26721'''
            st.code(code16,language="python")
        with tabHP2:
            st.write("Sélection des 8 caractéristiques les plus importantes :")
            code51='''top_8 = ["LONGITUDE", "LATITUDE", "DISCOVERY_DATE", "DISCOVERY_DOY", 
            "STATE", "DISCOVERY_WEEKDAY", "POPULATION", "STAT_CAUSE_DESCR"]'''
            st.code(code51,language="python")
          
            st.write("Accuracy :")   
            code17='''0.77'''
            st.code(code17,language="python")
            st.write("Confusion matrix :")
            code18='''Prédiction 	0 	1 	    2
Realité 			
0 	    1040 	2564 	    1455
1 	    4435 	268717     44344
2 	    1799 	29554 	    18433'''
            st.code(code18,language="python")
        with tabHP3:
            st.write("Paramètres  : (max_depth=60, random_state=12) et toutes les variables explicatives") 
            st.write("Accuracy :")   
            code17='''0.80'''
            st.code(code17,language="python")
            st.write("Confusion matrix :")
            code18='''Prédiction 	0 	1 	    2
Realité 			
0 	    816 	2825 	    1418
1 	    2806 	281046     33644
2 	    1345 	33854 	    14587'''
            st.code(code18,language="python")
    pass

elif page == "🧧 Conclusion":
    # Code for Conclusion page
    pass
