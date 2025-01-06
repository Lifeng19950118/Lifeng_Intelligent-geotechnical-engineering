import streamlit as st
import numpy as np
import pandas as pd
import json
from streamlit_echarts import Map
from streamlit_echarts import JsCode
from streamlit_echarts import st_echarts
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from streamlit_globe import streamlit_globe
import sys,os
sys.path.append(os.getcwd())
from pathlib import Path


#st.text("Williston Vertical Wells location, Data provide by ENVERUS")
a=pd.read_csv(Path(__file__).parent / "Data/PredictionMADISON1000_25.csv")

fig1 = px.scatter_mapbox(a, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color='Injectivity_ton/(day*MPa)',
                        color_continuous_scale=[                
                            '#E6E6FA',
                            '#8470FF',
                            '#7B68EE',
                            '#6A5ACD',                   
                            '#483D8B',
                            '#191970',
                        ],
                        range_color=(100, 900),
                        mapbox_style="carto-positron",
                        opacity=0.5, 
                        labels={'diff_percentage':'Difference Percentage'},
                        center={"lat": 47, "lon": -103},
                        zoom=6.)

st.plotly_chart(fig1)
st.write ("Figure 1. Predict injectivity of Madison Group CCS in Williston basin")
# a=pd.read_csv(Path(__file__).parent / "Data/PredictionMADISON1000_25.csv")

fig2 = px.scatter_mapbox(a, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color='PlumeRadius_m',
                        color_continuous_scale=[                
                            '#E6E6FA',
                            '#8470FF',
                            '#7B68EE',
                            '#6A5ACD',                   
                            '#483D8B',
                            '#191970',
                        ],
                        range_color=(198, 206.5),
                        mapbox_style="carto-positron",
                        opacity=0.5, 
                        labels={'diff_percentage':'Difference Percentage'},
                        center={"lat": 47, "lon": -103},
                        zoom=6.)

st.plotly_chart(fig2)
st.write ("Figure 2. Predict CO2 plume radius of Madison Group CCS in Williston basin")

fig3 = px.scatter_mapbox(a, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color='Cost_M$',
                        color_continuous_scale=[                
                            '#E6E6FA',
                            '#8470FF',
                            '#7B68EE',
                            '#6A5ACD',                   
                            '#483D8B',
                            '#191970',
                        ],
                        range_color=(11, 14),
                        mapbox_style="carto-positron",
                        opacity=0.5, 
                        labels={'diff_percentage':'Difference Percentage'},
                        center={"lat": 47, "lon": -103},
                        zoom=6.)

st.plotly_chart(fig3)
st.write ("Figure 3. Predict costs when use existing well of Madison Group CCS in Williston basin")

fig4 = px.scatter_mapbox(a, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color='Perm',
                        color_continuous_scale=[                
                            '#E6E6FA',
                            '#8470FF',
                            '#7B68EE',
                            '#6A5ACD',                   
                            '#483D8B',
                            '#191970',
                        ],
                        range_color=(8, 50),
                        mapbox_style="carto-positron",
                        opacity=0.5, 
                        labels={'diff_percentage':'Difference Percentage'},
                        center={"lat": 47, "lon": -103},
                        zoom=6.)

st.plotly_chart(fig4)
st.write ("Figure 5. Permeability of Madison Group CCS in Williston basin")


fig5 = px.scatter_mapbox(a, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color='Thick',
                        color_continuous_scale=[                
                            '#E6E6FA',
                            '#8470FF',
                            '#7B68EE',
                            '#6A5ACD',                   
                            '#483D8B',
                            '#191970',
                        ],
                        range_color=(100, 850),
                        mapbox_style="carto-positron",
                        opacity=0.5, 
                        labels={'diff_percentage':'Difference Percentage'},
                        center={"lat": 47, "lon": -103},
                        zoom=6.)

st.plotly_chart(fig5)
st.write ("Figure 6. The reservoir thickness of Madison Group CCS in Williston basin")

fig6 = px.scatter_mapbox(a, 
                        lat='Latitude', 
                        lon='Longitude', 
                        color='Temp',
                        color_continuous_scale=[                
                            '#E6E6FA',
                            '#8470FF',
                            '#7B68EE',
                            '#6A5ACD',                   
                            '#483D8B',
                            '#191970',
                        ],
                        range_color=(30, 140),
                        mapbox_style="carto-positron",
                        opacity=0.5, 
                        labels={'diff_percentage':'Difference Percentage'},
                        center={"lat": 47, "lon": -103},
                        zoom=6.)

st.plotly_chart(fig6)
st.write ("Figure 6. The reservoir temperature of Madison Group CCS in Williston basin")




