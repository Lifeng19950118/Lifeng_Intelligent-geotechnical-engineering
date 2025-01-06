# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 09:12:09 2023
@author: Lifeng Xu, Bo Zhang, Rick Chalaturnyk
"""

import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Line, Pie, Bar
from pyecharts.faker import Faker
from streamlit_echarts import st_echarts
from streamlit_echarts import st_pyecharts
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium, folium_static
import sys,os
sys.path.append(os.getcwd())
from pathlib import Path
import plotly.express as px






d11, d12, d13, d14, d15, d16, d17, d18=st.columns(8) 
with d11:
    st.page_link("pages/Predict.py", label="Predict", icon="🎯")
with d12:    
    st.page_link("pages/GlobalCCS.py", label="GlobalCCS", icon="🗺")
with d18: 
    st.page_link("Proxymodel.py", label="Home", icon="🏠")
 

a=pd.read_csv(Path(__file__).parent / "Data/Williston_Vertical_Wells_All.csv")
z1=a.Last12MonthOilProduction_BBL
z1.name="xse"
a=pd.concat([a,z1],axis=1)
xse=a.groupby("StateProvince").Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
xse_cum=xse.cumsum()/xse.sum()    


y1,x1=np.histogram(a.MonthsToPeakProduction.values,np.linspace(a.MonthsToPeakProduction.min(),a.MonthsToPeakProduction.max(),500),weights=a.MonthsToPeakProduction.values)#商品销量
y2,x2=np.histogram(a.MonthsToPeakProduction.values,np.linspace(a.MonthsToPeakProduction.min(),a.MonthsToPeakProduction.max(),500))#商品数量
data1=[]
for i in range(0,len(y1)):
    data1.append([x1[i],int(y1[i])])
data2=[]
for i in range(0,len(y2)):
    data2.append([x2[i],int(y2[i])])


shoe_xm=a.groupby('ENVFluidType').Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
shoe_fg=a.groupby('ENVProdWellType').Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
shoe_13=a.groupby('StateWellType').Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
shoe_14=a.groupby('ENVFracJobType').Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
shoe_15=a.groupby('ENVWellboreType').Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
data_xm=[]
for i in shoe_xm.items():
    data_xm.append({"value":i[1],"name":i[0]})
data_fg=[]
for i in shoe_fg.items():
    data_fg.append({"value":i[1],"name":i[0]})
data_13=[]
for i in shoe_13.items():
    data_13.append({"value":i[1],"name":i[0]})
data_14=[]
for i in shoe_14.items():
    data_14.append({"value":i[1],"name":i[0]})
data_15=[]
for i in shoe_15.items():
    data_15.append({"value":i[1],"name":i[0]})    
def Overview():    
    def paleituo(xse,xse_cum):
        option = {
          "xAxis": {
            "type": 'category',
            "data": [0]+xse.index.tolist()
          },
          "yAxis": [
              {
            "type":'value'
          },          
            {
                  "type":'value'
                }
            ],
          # "visualMap": {
          #   "orient": 'horizontal',
          #   "left": 'center',
          #   "min": xse.min(),
          #   "max": xse.max(),
          #   "text": ['High', 'Low'],
          #       # Map the score column to color
          #   "dimension": 0,
          #   "inRange": {
          #     "color": ['#65B581', '#FFCE34', '#FD665F']
          #   },
          # },
        "legend":{},          
        "series": [
            {
              "data": [0]+xse.tolist(),                         
              "type": 'bar',
              "showBackground": True,
              "backgroundStyle": {
                "color": ["#313695"
                ]
              },
              "name":"Country"
            },
            {
              "data": [0]+xse_cum.tolist(),
              "type": 'line',
              "yAxisIndex": 1,
              "name":"Country_cum"
            }
          ]
        };
        
        return option



    def price_sales(d1,d2):
        option = {
          "xAxis": {
              "min":0,
              "max":12
              },
          "yAxis": [{"splitLine":False},{}],
          "legend":{},
          "series": [
            {
              "data": d1,
              "type": 'line',
              "name":"InjectionSize_M",

            },
            {
              "data": d2,
              "type": 'line',
              "yAxisIndex": 1,
              "name":"InjectionSize_M number"
            },
          ]
        };
            
        return option



    def tz_pie(data):
        option = {
          "tooltip": {
            "trigger": 'item'
          },
          "legend": {
            "top": '60%',
            "x":"left",
            "orient": 'vertical',
          },
          "series": [
            {
              #"name": '类别销量',
              "type": 'pie',
              "radius": ['40%', '70%'],
              "avoidLabelOverlap": False,
              "itemStyle": {
                "borderRadius": 10,
                "borderColor": '#fff',
                "borderWidth": 2
              },
              "label": {
                "show": False,
                "position": 'center'
              },
              "emphasis": {
                "label": {
                  "show": True,
                  "fontSize": 40,
                  "fontWeight": 'bold'
                }
              },
              "labelLine": {
                "show": True
              },
              "data": data
            }
          ]
        };
            
        return option







    

    c51,c52,c53,c54=st.columns(4)
    c41,c42,c43,c44=st.columns(4)
    c31,c32,c33=st.columns([1,2,1])
    c21,c22,c23=st.columns([1,2,1])
    # c41.metric("CCS projects",len(a))
    # c42.metric("Countries involved",len(a.Country.unique()))
    # c43.metric("Total injection Mt",round(a.InjectionSize_Mt.sum()))
    # c44.metric("Injection rate Mt/y",round(a.Injection.mean()))


    with c31:
        st_echarts(tz_pie(data_xm),theme='white')
        st_echarts(tz_pie(data_fg),theme='white')
    with c32:
        fig1 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color='ElevationKB_FT',
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(50, 3500),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=3)
        #st.plotly_chart(figure_or_data, use_container_width=False, sharing="streamlit", theme="streamlit", **kwargs) 
        st.plotly_chart(fig1)
        #st.write ("Figure 1. The ElevationKB_FT of Williston wells")
    with c23:
        st_echarts(tz_pie(data_15),theme='white')
    with c21:
        st_echarts(paleituo(xse,xse_cum),theme='white')
    with c22:
        st_echarts(price_sales(data1,data2),theme='white')
    with c33:
        st_echarts(tz_pie(data_13),theme='white')
        
        
        st_echarts(tz_pie(data_14),theme='white')
def reservoir():
    def paleituo(xse,xse_cum):
        option = {
          "xAxis": {
            "type": 'category',
            "data": [0]+xse.index.tolist()
          },
          "yAxis": [
              {
            "type":'value'
          },          
            {
                  "type":'value'
                }
            ],
          # "visualMap": {
          #   "orient": 'horizontal',
          #   "left": 'center',
          #   "min": xse.min(),
          #   "max": xse.max(),
          #   "text": ['High', 'Low'],
          #       # Map the score column to color
          #   "dimension": 0,
          #   "inRange": {
          #     "color": ['#65B581', '#FFCE34', '#FD665F']
          #   },
          # },
        "legend":{},          
        "series": [
            {
              "data": [0]+xse.tolist(),                         
              "type": 'bar',
              "showBackground": True,
              "backgroundStyle": {
                "color": ["#313695"
                ]
              },
              "name":choice81
            },
            {
              "data": [0]+xse_cum.tolist(),
              "type": 'line',
              "yAxisIndex": 1,
              "name":choice81 + "_cum"
            }
          ]
        };
        
        return option
    def re_pie(data):
        option = {
          "tooltip": {
            "trigger": 'item'
          },
          "legend": {
            "top": '60%',
            "x":"left",
            "orient": 'vertical',
          },
          "series": [
            {
              #"name": '类别销量',
              "type": 'pie',
              "radius": ['40%', '70%'],
              "avoidLabelOverlap": False,
              "itemStyle": {
                "borderRadius": 10,
                "borderColor": '#fff',
                "borderWidth": 2
              },
              "label": {
                "show": False,
                "position": 'center'
              },
              "emphasis": {
                "label": {
                  "show": True,
                  "fontSize": 40,
                  "fontWeight": 'bold'
                }
              },
              "labelLine": {
                "show": True
              },
              "data": data
            }
          ]
        };
            
        return option
       
        
    
    c81, c82,c83 = st.columns([5,0.5,5])
    c881, c882,c883 = st.columns([5,0.5,5])
    with c81:        
       choice81 = st.selectbox('Select data', ["Bottom_Hole_Temp","Porosity", "TestRate_BOEPerDAY"])
       if choice81 == "Bottom_Hole_Temp":
         enbdf81 = a.Bottom_Hole_Temp_DEGF
       elif choice81 == 'Porosity':
           enbdf81 = a.DensityPorosity_PCT  
       elif choice81 == 'TestRate_BOEPerDAY':
           enbdf81 = a.TestRate_BOEPerDAY
       xse=a.groupby(enbdf81).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum()      
       fig81 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color= enbdf81,
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(enbdf81.min(), enbdf81.max()),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=4.)
    with c81:  
      st.plotly_chart(fig81)
    #st.write ("Figure 2. The Bottom_Hole_Temp_DEGF of Williston wells")
    with c881:
      st_echarts(paleituo(xse,xse_cum),theme='white')
    
    with c83:        
       choice83 = st.selectbox('Select data', ["WellGrouping","ProducingMethod", "Formation", "FluidType"])
       if choice83 == "ProducingMethod":
         enbdf83 = a.ENVProducingMethod
       elif choice83 == 'FluidType':
           enbdf83 = a.ENVFluidType
       elif choice83 == 'WellGrouping':
           enbdf83 = a.ENVWellGrouping            
       elif choice83 == 'Formation':
           enbdf83 = a.Formation           
       shoe_xm=a.groupby(enbdf83).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       data_xm=[]
       for i in shoe_xm.items():
               data_xm.append({"value":i[1],"name":i[0]})      

          
    fig83 = px.scatter_mapbox(a, 
                            lat='Latitude', 
                            lon='Longitude', 
                            color= enbdf83,
                            color_continuous_scale=[                
                                "#313695",
                                "#4575b4",
                                "#74add1",
                                "#abd9e9",
                                "#e0f3f8",
                                "#ffffbf",
                                "#fee090",
                                "#fdae61",
                                "#f46d43",
                                "#d73027",
                                "#a50026",
                            ],
                            range_color=(1, 100),
                            mapbox_style="carto-positron",
                            opacity=0.5, 
                            labels={'diff_percentage':'Difference Percentage'},
                            center={"lat": 47, "lon": -103},
                            zoom=4.)
    with c83:
        st.plotly_chart(fig83)       
    with c883:
        st_echarts(re_pie(data_xm),theme='white')  
        
def Production():
    def paleituo(xse,xse_cum):
        option = {
          "xAxis": {
            "type": 'category',
            "data": [0]+xse.index.tolist()
          },
          "yAxis": [
              {
            "type":'value'
          },          
            {
                  "type":'value'
                }
            ],
          # "visualMap": {
          #   "orient": 'horizontal',
          #   "left": 'center',
          #   "min": xse.min(),
          #   "max": xse.max(),
          #   "text": ['High', 'Low'],
          #       # Map the score column to color
          #   "dimension": 0,
          #   "inRange": {
          #     "color": ['#65B581', '#FFCE34', '#FD665F']
          #   },
          # },
        "legend":{},          
        "series": [
            {
              "data": [0]+xse.tolist(),                         
              "type": 'bar',
              "showBackground": True,
              "backgroundStyle": {
                "color": ["#313695"
                ]
              },
              "name":choice
            },
            {
              "data": [0]+xse_cum.tolist(),
              "type": 'line',
              "yAxisIndex": 1,
              "name":choice + "_cum"
            }
          ]
        };
        
        return option
    def re_pie(data):
        option = {
          "tooltip": {
            "trigger": 'item'
          },
          "legend": {
            "top": '60%',
            "x":"left",
            "orient": 'vertical',
          },
          "series": [
            {
              #"name": '类别销量',
              "type": 'pie',
              "radius": ['40%', '70%'],
              "avoidLabelOverlap": False,
              "itemStyle": {
                "borderRadius": 10,
                "borderColor": '#fff',
                "borderWidth": 2
              },
              "label": {
                "show": False,
                "position": 'center'
              },
              "emphasis": {
                "label": {
                  "show": True,
                  "fontSize": 40,
                  "fontWeight": 'bold'
                }
              },
              "labelLine": {
                "show": True
              },
              "data": data
            }
          ]
        };
            
        return option
    
    
    
    c111, c112,c113 = st.columns([5,0.5,5])
    c1111, c1112,c1113 = st.columns([5,0.5,5])
    c121, c122,c123 = st.columns([5,0.5,5])
    c1121, c1122,c1123 = st.columns([5,0.5,5])
    with c111:        
       choice = st.selectbox('Select data', ["First3MonthProd_BOE","TotalWaterPumped_GAL","TotalFluidPumped_BBL","AcidVolume_BBL", 
                                             "First3MonthGas_MCF","First3MonthProd_MCFE","First3MonthWater_BBL","First6MonthProd_BOE"])
       if choice == "First3MonthProd_BOE":
         enbdf111 = a.First3MonthProd_BOE
       elif choice == 'TotalWaterPumped_GAL':
           enbdf111 = a.TotalWaterPumped_GAL
       elif choice == 'TotalFluidPumped_BBL':
           enbdf111 = a.TotalFluidPumped_BBL 
       elif choice == 'AcidVolume_BBL':
           enbdf111 = a.AcidVolume_BBL
       elif choice == 'First3MonthGas_MCF':
           enbdf111 = a.First3MonthGas_MCF
       elif choice == 'First3MonthProd_MCFE':
           enbdf111 = a.First3MonthProd_MCFE          
       elif choice == 'First3MonthWater_BBL':
           enbdf111 = a.First3MonthWater_BBL      
       elif choice == 'First6MonthProd_BOE':
           enbdf111 = a.First6MonthProd_BOE                 
       xse=a.groupby(enbdf111).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum()                   
       fig111 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color= enbdf111,
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(enbdf111.min(), enbdf111.max()),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=4.)
    with c111:  
      st.plotly_chart(fig111)
    #st.write ("Figure 2. The Bottom_Hole_Temp_DEGF of Williston wells")
    with c1111:
      st_echarts(paleituo(xse,xse_cum),theme='white') 


    with c113:        
       choice = st.selectbox('Select data', ["First6MonthGas_MCF","First6MonthProd_MCFE","First6MonthWater_BBL","First9MonthProd_BOE"
                                             ,"First9MonthGas_MCF","First9MonthProd_MCFE","First9MonthWater_BBL"
                                             ,"First12MonthProd_BOE","First12MonthGas_MCF"])
       if choice == "First6MonthGas_MCF":
         enbdf113 = a.First6MonthGas_MCF
       elif choice == 'First6MonthProd_MCFE':
           enbdf113 = a.First6MonthProd_MCFE
       elif choice == 'First6MonthWater_BBL':
           enbdf113 = a.First6MonthWater_BBL
       elif choice == 'First9MonthProd_BOE':
           enbdf113 = a.First9MonthProd_BOE
       elif choice == 'First9MonthGas_MCF':
           enbdf113 = a.First9MonthGas_MCF 
       elif choice == 'First9MonthProd_MCFE':
           enbdf113 = a.First9MonthProd_MCFE
       elif choice == 'First9MonthWater_BBL':
           enbdf113 = a.First9MonthWater_BBL            
       elif choice == 'First12MonthProd_BOE':
           enbdf113 = a.First12MonthProd_BOE
       elif choice == 'First12MonthGas_MCF':
           enbdf113 = a.First12MonthGas_MCF 
       xse=a.groupby(enbdf113).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum() 

                  
    fig113 = px.scatter_mapbox(a, 
                            lat='Latitude', 
                            lon='Longitude', 
                            color= enbdf113,
                            color_continuous_scale=[                
                                "#313695",
                                "#4575b4",
                                "#74add1",
                                "#abd9e9",
                                "#e0f3f8",
                                "#ffffbf",
                                "#fee090",
                                "#fdae61",
                                "#f46d43",
                                "#d73027",
                                "#a50026",
                            ],
                            range_color=(enbdf113.min(), enbdf113.max()),
                            mapbox_style="carto-positron",
                            opacity=0.5, 
                            labels={'diff_percentage':'Difference Percentage'},
                            center={"lat": 47, "lon": -103},
                            zoom=4.)
    with c113:
        st.plotly_chart(fig113)  
    with c1113:
      st_echarts(paleituo(xse,xse_cum),theme='white') 



    with c121:        
       choice = st.selectbox('Select data', ["First12MonthProd_MCFE","First12MonthWater_BBL","First36MonthProd_BOE","First36MonthGas_MCF"
                                             ,"First36MonthProd_MCFE","First36MonthWater_BBL","MonthsToPeakProduction"
                                             ,"PeakProd_BOE","PeakGas_MCF"])
       if choice == "First12MonthProd_MCFE":
         enbdf121 = a.First12MonthProd_MCFE
       elif choice == 'First12MonthWater_BBL':
           enbdf121 = a.First12MonthWater_BBL
       elif choice == 'First36MonthProd_BOE':
           enbdf121 = a.First36MonthProd_BOE
       elif choice == 'First36MonthGas_MCF':
           enbdf121 = a.First36MonthGas_MCF
       elif choice == 'First36MonthProd_MCFE':
           enbdf121 = a.First36MonthProd_MCFE
       elif choice == 'First36MonthWater_BBL':
           enbdf121 = a.First36MonthWater_BBL
       elif choice == 'MonthsToPeakProduction':
           enbdf121 = a.MonthsToPeakProduction            
       elif choice == 'PeakProd_BOE':
           enbdf121 = a.PeakProd_BOE
       elif choice == 'PeakGas_MCF':
           enbdf121 = a.PeakGas_MCF  
       xse=a.groupby(enbdf121).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum()           
    fig121 = px.scatter_mapbox(a, 
                            lat='Latitude', 
                            lon='Longitude', 
                            color= enbdf121,
                            color_continuous_scale=[                
                                "#313695",
                                "#4575b4",
                                "#74add1",
                                "#abd9e9",
                                "#e0f3f8",
                                "#ffffbf",
                                "#fee090",
                                "#fdae61",
                                "#f46d43",
                                "#d73027",
                                "#a50026",
                            ],
                            range_color=(enbdf121.min(), enbdf121.max()),
                            mapbox_style="carto-positron",
                            opacity=0.5, 
                            labels={'diff_percentage':'Difference Percentage'},
                            center={"lat": 47, "lon": -103},
                            zoom=4.)
    with c121:
        st.plotly_chart(fig121)
    with c1121:
      st_echarts(paleituo(xse,xse_cum),theme='white')                

    

    with c123:        
       choice = st.selectbox('Select data', ["PeakOil_BBL","PeakWater_BBL","CumProd_BOE","CumGas_MCF"
                                             ,"CumOil_BBL","CumWater_BBL","Last12MonthBOEProduction"
                                             ,"Last12MonthGasProduction_MCF","Last12MonthOilProduction_BBL","Last12MonthWaterProduction_BBL"])
       if choice == "PeakOil_BBL":
         enbdf123 = a.PeakOil_BBL
       elif choice == 'PeakWater_BBL':
           enbdf123 = a.PeakWater_BBL
       elif choice == 'CumProd_BOE':
           enbdf123 = a.CumProd_BOE 
       elif choice == 'CumGas_MCF':
           enbdf123 = a.CumGas_MCF
       elif choice == 'CumOil_BBL':
           enbdf123 = a.CumOil_BBL
       elif choice == 'CumWater_BBL':
           enbdf123 = a.CumWater_BBL
       elif choice == 'Last12MonthBOEProduction':
           enbdf123 = a.Last12MonthBOEProduction            
       elif choice == 'Last12MonthGasProduction_MCF':
           enbdf123 = a.Last12MonthGasProduction_MCF
       elif choice == 'Last12MonthOilProduction_BBL':
           enbdf123 = a.Last12MonthOilProduction_BBL
       elif choice == 'Last12MonthWaterProduction_BBL':
           enbdf123 = a.Last12MonthWaterProduction_BBL
       xse=a.groupby(enbdf123).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum()       
    fig123 = px.scatter_mapbox(a, 
                            lat='Latitude', 
                            lon='Longitude', 
                            color= enbdf123,
                            color_continuous_scale=[                
                                "#313695",
                                "#4575b4",
                                "#74add1",
                                "#abd9e9",
                                "#e0f3f8",
                                "#ffffbf",
                                "#fee090",
                                "#fdae61",
                                "#f46d43",
                                "#d73027",
                                "#a50026",
                            ],
                            range_color=(enbdf123.min(), enbdf123.max()),
                            mapbox_style="carto-positron",
                            opacity=0.5, 
                            labels={'diff_percentage':'Difference Percentage'},
                            center={"lat": 47, "lon": -103},
                            zoom=4.)
    with c123:
        st.plotly_chart(fig123)
    with c1123:
      st_echarts(paleituo(xse,xse_cum),theme='white')     

def Operation():
    def paleituo(xse,xse_cum):
        option = {
          "xAxis": {
            "type": 'category',
            "data": [0]+xse.index.tolist()
          },
          "yAxis": [
              {
            "type":'value'
          },          
            {
                  "type":'value'
                }
            ],
          # "visualMap": {
          #   "orient": 'horizontal',
          #   "left": 'center',
          #   "min": xse.min(),
          #   "max": xse.max(),
          #   "text": ['High', 'Low'],
          #       # Map the score column to color
          #   "dimension": 0,
          #   "inRange": {
          #     "color": ['#65B581', '#FFCE34', '#FD665F']
          #   },
          # },
        "legend":{},          
        "series": [
            {
              "data": [0]+xse.tolist(),                         
              "type": 'bar',
              "showBackground": True,
              "backgroundStyle": {
                "color": ["#313695"
                ]
              },
              "name":choice
            },
            {
              "data": [0]+xse_cum.tolist(),
              "type": 'line',
              "yAxisIndex": 1,
              "name":choice + "_cum"
            }
          ]
        };
        
        return option
    c211, c212,c213 = st.columns([5,0.5,5])
    c2111, c2112,c2113 = st.columns([5,0.5,5])    
    with c213:        
       choice = st.selectbox('Select data', ["AvgBreakdownPressure_PSI","AvgFracGradient_PSIPerFT","AvgPortSleeveOpeningPressure_PSI"
                                             ,"AvgTreatmentPressure_PSI", "AvgTreatmentRate_BBLPerMin", "AvgFluidPerCluster_BBL", "FrictionReducer_LBS"])
       if choice == "AvgBreakdownPressure_PSI":
         enbdf211 = a.AvgBreakdownPressure_PSI
       elif choice == 'AvgFracGradient_PSIPerFT':
           enbdf211 = a.AvgFracGradient_PSIPerFT
       elif choice == 'AvgPortSleeveOpeningPressure_PSI':
           enbdf211 = a.AvgPortSleeveOpeningPressure_PSI  
       elif choice == 'AvgTreatmentPressure_PSI':
           enbdf211 = a.AvgTreatmentPressure_PSI
       elif choice == 'AvgTreatmentRate_BBLPerMin':
           enbdf211 = a.AvgTreatmentRate_BBLPerMin
       elif choice == 'AvgFluidPerCluster_BBL':
           enbdf211 = a.AvgFluidPerCluster_BBL   
       elif choice == 'FrictionReducer_LBS':
           enbdf211 = a.FrictionReducer_LBS           
       xse=a.groupby(enbdf211).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum()   
       fig211 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color= enbdf211,
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(enbdf211.min(), enbdf211.max()),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=4.)
  
    with c213:
        st.plotly_chart(fig211)
    with c2113:
      st_echarts(paleituo(xse,xse_cum),theme='white')

    with c211:        
       choice = st.selectbox('Select data', ["OilTestRate_BBLPerDAY","GasTestRate_MCFPerDAY","WaterTestRate_BBLPerDAY"
                                             ,"CasingPressure_PSI", "FlowingTubingPressure_PSI", "ShutInPressure_PSI"])
       if choice == "OilTestRate_BBLPerDAY":
         enbdf213 = a.OilTestRate_BBLPerDAY
       elif choice == 'GasTestRate_MCFPerDAY':
           enbdf213 = a.GasTestRate_MCFPerDAY
       elif choice == 'WaterTestRate_BBLPerDAY':
           enbdf213 = a.WaterTestRate_BBLPerDAY  
       elif choice == 'CasingPressure_PSI':
           enbdf213 = a.CasingPressure_PSI
       elif choice == 'FlowingTubingPressure_PSI':
           enbdf213 = a.FlowingTubingPressure_PSI
       elif choice == 'ShutInPressure_PSI':
           enbdf213 = a.ShutInPressure_PSI 
       xse=a.groupby(enbdf213).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum()   
         
       fig213 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color= enbdf213,
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(enbdf213.min(), enbdf213.max()),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=4.)
  
    with c211:
        st.plotly_chart(fig213)
    with c2111:
      st_echarts(paleituo(xse,xse_cum),theme='dark')



def Well():
    def paleituo(xse,xse_cum):
        option = {
          "xAxis": {
            "type": 'category',
            "data": [0]+xse.index.tolist()
          },
          "yAxis": [
              {
            "type":'value'
          },          
            {
                  "type":'value'
                }
            ],
          # "visualMap": {
          #   "orient": 'horizontal',
          #   "left": 'center',
          #   "min": xse.min(),
          #   "max": xse.max(),
          #   "text": ['High', 'Low'],
          #       # Map the score column to color
          #   "dimension": 0,
          #   "inRange": {
          #     "color": ['#65B581', '#FFCE34', '#FD665F']
          #   },
          # },
        "legend":{},          
        "series": [
            {
              "data": [0]+xse.tolist(),                         
              "type": 'bar',
              "showBackground": True,
              "backgroundStyle": {
                "color": ["#313695"
                ]
              },
              "name":choice
            },
            {
              "data": [0]+xse_cum.tolist(),
              "type": 'line',
              "yAxisIndex": 1,
              "name":choice + "_cum"
            }
          ]
        };
        
        return option
    def re_pie(data):
        option = {
          "tooltip": {
            "trigger": 'item'
          },
          "legend": {
            "top": '60%',
            "x":"left",
            "orient": 'vertical',
          },
          "series": [
            {
              #"name": '类别销量',
              "type": 'pie',
              "radius": ['40%', '70%'],
              "avoidLabelOverlap": False,
              "itemStyle": {
                "borderRadius": 10,
                "borderColor": '#fff',
                "borderWidth": 2
              },
              "label": {
                "show": False,
                "position": 'center'
              },
              "emphasis": {
                "label": {
                  "show": True,
                  "fontSize": 40,
                  "fontWeight": 'bold'
                }
              },
              "labelLine": {
                "show": True
              },
              "data": data
            }
          ]
        };
            
        return option

    c311, c312,c313 = st.columns([5,0.5,5])
    c3111, c3112,c3113 = st.columns([5,0.5,5])    
    with c311:        
       choice = st.selectbox('Select data', ["TotalWellCostHistorical_USDMM","TVD_FT","SpudToCompletion_DAYS", "NumberOfStrings","UpperPerf_FT", "LowerPerf_FT", "WellDensitySameZone"])
       if choice == "TotalWellCostHistorical_USDMM":
         enbdf311 = a.TotalWellCostHistorical_USDMM
       elif choice == 'TVD_FT':
           enbdf311 = a.TVD_FT
       elif choice == 'SpudToCompletion_DAYS':
           enbdf311 = a.SpudToCompletion_DAYS   
       elif choice == 'NumberOfStrings':
           enbdf311 = a.NumberOfStrings
       elif choice == 'UpperPerf_FT':
           enbdf311 = a.UpperPerf_FT
       elif choice == 'LowerPerf_FT':
           enbdf311 = a.LowerPerf_FT
       elif choice == 'WellDensitySameZone':
           enbdf311 = a.WellDensitySameZone
       xse=a.groupby(enbdf311).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum()          
         
       fig311 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color= enbdf311,
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(enbdf311.min(), enbdf311.max()),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=4.)
  
    with c311:
        st.plotly_chart(fig311)
    with c3111:
      st_echarts(paleituo(xse,xse_cum),theme='dark')


    with c313:        
       choice = st.selectbox('Select data', ["ENVWellboreType","ENVFracJobType", "ENVProdWellType", "OilTestMethodName","ENVWellStatus"])
       if choice == "ENVWellboreType":
         enbdf313 = a.ENVWellboreType
       elif choice == 'ENVFracJobType':
           enbdf313 = a.ENVFracJobType
       elif choice == 'ENVProdWellType':
           enbdf313 = a.ENVProdWellType
       elif choice == 'OilTestMethodName':
           enbdf313 = a.OilTestMethodName           
       elif choice == 'ENVWellStatus':
           enbdf313 = a.ENVWellStatus
       shoe_xm=a.groupby(enbdf313).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       data_xm=[]
       for i in shoe_xm.items():
               data_xm.append({"value":i[1],"name":i[0]})  
           
       fig313 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color= enbdf313,
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(1, 100),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=4.)
  
    with c313:
        st.plotly_chart(fig313)
    with c3113:
        st_echarts(re_pie(data_xm),theme='white')          


    
def Cost():
    def paleituo(xse,xse_cum):
        option = {
          "xAxis": {
            "type": 'category',
            "data": [0]+xse.index.tolist()
          },
          "yAxis": [
              {
            "type":'value'
          },          
            {
                  "type":'value'
                }
            ],
          # "visualMap": {
          #   "orient": 'horizontal',
          #   "left": 'center',
          #   "min": xse.min(),
          #   "max": xse.max(),
          #   "text": ['High', 'Low'],
          #       # Map the score column to color
          #   "dimension": 0,
          #   "inRange": {
          #     "color": ['#65B581', '#FFCE34', '#FD665F']
          #   },
          # },
        "legend":{},          
        "series": [
            {
              "data": [0]+xse.tolist(),                         
              "type": 'bar',
              "showBackground": True,
              "backgroundStyle": {
                "color": ["#313695"
                ]
              },
              "name":choice
            },
            {
              "data": [0]+xse_cum.tolist(),
              "type": 'line',
              "yAxisIndex": 1,
              "name":choice + "_cum"
            }
          ]
        };
        
        return option
    def re_pie(data):
        option = {
          "tooltip": {
            "trigger": 'item'
          },
          "legend": {
            "top": '60%',
            "x":"left",
            "orient": 'vertical',
          },
          "series": [
            {
              #"name": '类别销量',
              "type": 'pie',
              "radius": ['40%', '70%'],
              "avoidLabelOverlap": False,
              "itemStyle": {
                "borderRadius": 10,
                "borderColor": '#fff',
                "borderWidth": 2
              },
              "label": {
                "show": False,
                "position": 'center'
              },
              "emphasis": {
                "label": {
                  "show": True,
                  "fontSize": 40,
                  "fontWeight": 'bold'
                }
              },
              "labelLine": {
                "show": True
              },
              "data": data
            }
          ]
        };
            
        return option
    c411, c412,c413 = st.columns([5,0.5,5])
    c4111, c4112,c4113 = st.columns([5,0.5,5])    
    with c411:        
       choice = st.selectbox('Select data', ["CompletionCost_USDMM","DrillingCost_USDMM","TransportationCost_USDPerBOE","ProcessingFee_USDPerMCF", "TieInCost_USDMM"])
       if choice == "CompletionCost_USDMM":
         enbdf411 = a.CompletionCost_USDMM
       elif choice == 'DrillingCost_USDMM':
           enbdf411 = a.DrillingCost_USDMM
       elif choice == 'TransportationCost_USDPerBOE':
           enbdf411 = a.TransportationCost_USDPerBOE   
       elif choice == 'ProcessingFee_USDPerMCF':
           enbdf411 = a.ProcessingFee_USDPerMCF
       elif choice == 'TieInCost_USDMM':
           enbdf411 = a.TieInCost_USDMM
       xse=a.groupby(enbdf411).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum()             
         
       fig411 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color= enbdf411,
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(enbdf411.min(), enbdf411.max()),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=4.)
  
    with c411:
        st.plotly_chart(fig411)    
    with c4111:
      st_echarts(paleituo(xse,xse_cum),theme='dark')




    with c413:        
       choice = st.selectbox('Select data', ["TotalWellCost_USDMM","DrillingCostHistorical_USDMM","CompletionCostHistorical_USDMM",
                                             "TotalWellCostHistorical_USDMM","NPVPerWELLAt50And200_USDMM", "NPVPerWELLAt55And300_USDMM"])
       if choice == "TotalWellCost_USDMM":
         enbdf413 = a.TotalWellCost_USDMM
       elif choice == 'DrillingCostHistorical_USDMM':
           enbdf413 = a.DrillingCostHistorical_USDMM
       elif choice == 'CompletionCostHistorical_USDMM':
           enbdf413 = a.CompletionCostHistorical_USDMM  
       elif choice == 'TotalWellCostHistorical_USDMM':
           enbdf413 = a.TotalWellCostHistorical_USDMM
       elif choice == 'NPVPerWELLAt50And200_USDMM':
           enbdf413 = a.NPVPerWELLAt50And200_USDMM
       elif choice == 'NPVPerWELLAt55And300_USDMM':
           enbdf413 = a.NPVPerWELLAt55And300_USDMM  
       xse=a.groupby(enbdf413).Last12MonthOilProduction_BBL.sum().sort_values(ascending=False)
       xse_cum=xse.cumsum()/xse.sum() 
       for i in shoe_xm.items():
               data_xm.append({"value":i[1],"name":i[0]})          
         
       fig413 = px.scatter_mapbox(a, 
                                lat='Latitude', 
                                lon='Longitude', 
                                color= enbdf413,
                                color_continuous_scale=[                
                                    "#313695",
                                    "#4575b4",
                                    "#74add1",
                                    "#abd9e9",
                                    "#e0f3f8",
                                    "#ffffbf",
                                    "#fee090",
                                    "#fdae61",
                                    "#f46d43",
                                    "#d73027",
                                    "#a50026",
                                ],
                                range_color=(enbdf413.min(), enbdf413.max()),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                center={"lat": 47, "lon": -103},
                                zoom=4.)
  
    with c413:
        st.plotly_chart(fig413)    
    with c4113:
      st_echarts(paleituo(xse,xse_cum),theme='dark')           

def Analyze():
    a=pd.read_csv(Path(__file__).parent / "Data/Williston_Vertical_Wells_All.csv")
    st.text_input("Type the interested item", key="columns")

    # You can access the value at any point with:
    if st.session_state.columns:
        r1=a.groupby(st.session_state.columns).size()
        
        options1 = {
            "color":'#ff4060',
            "tooltip": {
          "trigger": 'axis',
          "axisPointer": {
            "type": 'shadow'
          }
        },
            "xAxis": {
                "type": "category",
                "data": r1.index.tolist(),
                "axisTick": {"alignWithLabel": True},
            },
            "yAxis": {"type": "value"},
            "series": [
                {"data": r1.values.tolist(), "type": "bar"}
            ],
        }
        st_echarts(options=options1)




    # Throught the selectbox to dreaw the echart
    optionA1 = st.selectbox(
        'Which item do you like best?',
        a.columns.tolist())
    r1=a.groupby(optionA1).size()

    options1 = {
        "color":'#ff4060',
        "tooltip": {
      "trigger": 'axis',
      "axisPointer": {
        "type": 'shadow'
      }
    },
        "xAxis": {
            "type": "category",
            "data": r1.index.tolist(),
            "axisTick": {"alignWithLabel": True},
        },
        "yAxis": {"type": "value"},
        "series": [
            {"data": r1.values.tolist(), "type": "bar"}
        ],
    }
    st_echarts(options=options1)




    optionB1 = st.selectbox(
        'Which parameter are you interested in?',
        a["Formation"].unique())
    optionB2 = st.slider('Latitude',60.,a.Latitude.max(),(40.,53.))
    optionB3 = st.slider('Longitude',-98.,a.Longitude.max(),(-110.,-98.))
    optionB4 = st.multiselect(
        'Which item are you interested in?',
        a.columns,
        ['Country', 'ENVElevationKB_FT', 'Bottom_Hole_Temp_DEGF'])
    FinalSelect=a[(a["Formation"]==optionB1)&(a.Latitude>optionB2[0])&(a.Latitude<optionB2[1])
                  &(a.Longitude>optionB3[0])&(a.Longitude<optionB3[1])]

    FinalSelect


    st.write(a.iloc[0:3])
    st.dataframe(a[['Country', 'ENVElevationKB_FT', 'Bottom_Hole_Temp_DEGF']].style.highlight_max(axis=0))


    st.text("Williston Vertical Wells location, Data provide by ENVERUS")

    df = pd.read_csv(Path(__file__).parent / "Data/Williston_Vertical_Wells_All.csv", 
                      usecols=['WellPadID', 'Latitude', 'Longitude'])

    df.columns = ['Well Name', 'latitude', 'longitude']


    st.map(df)



    m = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], 
                     zoom_start=3, control_scale=True)

    #Loop through each row in the dataframe
    for i,row in df.iterrows():
        #Setup the content of the popup
        iframe = folium.IFrame('Well Name:' + str(row["Well Name"]))
        
        #Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=300, max_width=300)
        
        #Add each row to the map
        folium.Marker(location=[row['latitude'],row['longitude']],
                      popup = popup, c=row['Well Name']).add_to(m)

    st_data = st_folium(m, width=700)
    folium_static(m, width=700)
    
def main():
    st.sidebar.title('Navigation：')

    # 设置菜单项列表
    menu = ['Overview', 'Cost', 'Reservoir parameters', 'Production status', 'Well information', "Operation", 'Analyze tools']
    choice = st.sidebar.selectbox('Select', menu)

    # 显示选定页面的内容
    if choice == 'Overview':
        Overview()
    elif choice == 'Cost':
        Cost()
    elif choice == 'Reservoir parameters':
        reservoir()
    elif choice == 'Production status':
        Production()
    elif choice == 'Well information':
        Well()
    elif choice == 'Operation':
        Operation()   
    elif choice == 'Analyze tools':
        Analyze()          
    else:
        Overview()

if __name__ == '__main__':
    main()

# a=pd.read_csv(Path(__file__).parent / "Data/Williston_Vertical_Wells_All.csv")
# data0=[]
# for i in a.groupby("ENVWellStatus").size().items():
#     data0.append({"name":i[0],"value":i[1]})



# df = pd.read_csv(Path(__file__).parent / "Data/Williston_Vertical_Wells_All.csv", 
#                   usecols=['WellPadID', 'Latitude', 'Longitude'])
# df.columns = ['Well Name', 'latitude', 'longitude']
# st.map(df)




