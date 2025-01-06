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
    st.page_link("pages/Williston.py", label="Williston", icon="🗺")
with d18: 
    st.page_link("Proxymodel.py", label="Home", icon="🏠")
 
a=pd.read_csv(Path(__file__).parent / "Data/CCSData.csv")
z1=a.Injection
z1.name="xse"
a=pd.concat([a,z1],axis=1)
a["Continent"]=a.Continent
a["Country"]=a.Country

xse=a.groupby("Country").Injection.sum().sort_values(ascending=False)
xse_cum=xse.cumsum()/xse.sum()    


y1,x1=np.histogram(a.InjectionSize_Mt.values,np.linspace(a.InjectionSize_Mt.min(),a.InjectionSize_Mt.max(),500),weights=a.InjectionSize_Mt.values)#商品销量
y2,x2=np.histogram(a.Injection.values,np.linspace(a.Injection.min(),a.Injection.max(),500))#商品数量
data1=[]
for i in range(0,len(y1)):
    data1.append([x1[i],int(y1[i])])
data2=[]
for i in range(0,len(y2)):
    data2.append([x2[i],int(y2[i])])


shoe_xm=a.groupby('Country').Injection.sum().sort_values(ascending=False)
shoe_fg=a.groupby('Scale').Injection.sum().sort_values(ascending=False)
shoe_13=a.groupby('Purpose').Injection.sum().sort_values(ascending=False)
shoe_14=a.groupby('Status').Injection.sum().sort_values(ascending=False)
shoe_15=a.groupby('Fate').Injection.sum().sort_values(ascending=False)
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
                                color='Project_ID',
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
                                range_color=(a.Project_ID.min(), a.Project_ID.max()),
                                mapbox_style="carto-positron",
                                opacity=0.5, 
                                labels={'diff_percentage':'Difference Percentage'},
                                #center={"lat": 47, "lon": -103},
                                zoom=3)
        #st.plotly_chart(figure_or_data, use_container_width=False, sharing="streamlit", theme="streamlit", **kwargs) 
        st.plotly_chart(fig1)
        #st.write ("Figure 1. The ElevationKB_FT of Williston Storages")
    with c23:
        st_echarts(tz_pie(data_15),theme='white')
    with c21:
        st_echarts(paleituo(xse,xse_cum),theme='white')
    with c22:
        st_echarts(price_sales(data1,data2),theme='white')
    with c33:
        st_echarts(tz_pie(data_13),theme='white')
        
        
        st_echarts(tz_pie(data_14),theme='white')
def Injection():
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
       
        
    
    c81, c82,c83 = st.columns([5,0.5,5])
    c881, c882,c883 = st.columns([5,0.5,5])
    with c81:        
       choice = st.selectbox('Select data', ["Injection","InjectionSize_Mt", "Total_Injection_Mt"])
       if choice == "Injection":
         enbdf81 = a.Injection
       elif choice == 'InjectionSize_Mt':
           enbdf81 = a.InjectionSize_Mt 
       elif choice == 'Total_Injection_Mt':
           enbdf81 = a.Total_Injection_Mt
       xse=a.groupby(enbdf81).Injection.sum().sort_values(ascending=False)
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
       choice83 = st.selectbox('Select data', ["Production_Capacity","Capacity"])
       if choice83 == "Production_Capacity":
         enbdf83 = a.Production_Capacity
       elif choice83 == 'Capacity':
           enbdf83 = a.Capacity                 
       shoe_xm=a.groupby(enbdf83).Injection.sum().sort_values(ascending=False)
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
        
def Company():
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
    with c111:        
       choice = st.selectbox('Select data', ["Project Website","Public Funding Comment", "Non Commercial Org","Source Company","Permit","Feedstock" ])
       if choice == "Project Website":
           enbdf1113 = a.loc[:,['Project_Name','Project_Website']]
       elif choice == 'Public Funding Comment':
           enbdf1113 = a.loc[:,['Project_Name','Public Funding Comment']]
       elif choice == 'Non Commercial Org':
           enbdf1113 = a.loc[:,['Project_Name','Non_Commercial_Org']]  
       elif choice == 'Source Company':
           enbdf1113 = a.loc[:,['Project_Name','Source Company']]
       elif choice == 'Permit':
           enbdf1113 = a.loc[:,['Project_Name','Permit']]  
       elif choice == 'Feedstock':
           enbdf1113 = a.loc[:,['Project_Name','Feedstock']]             
       st.dataframe(enbdf1113)         
           

    #st.write ("Figure 2. The Bottom_Hole_Temp_DEGF of Williston wells")



    with c113:        
       choice = st.selectbox('Select data', ["Non Commercial Org","Source Company","Permit","Feedstock"])
       if choice == "Non Commercial Org":
         enbdf113 = a.Non_Commercial_Org
       elif choice == 'Source Company':
           enbdf113 = a.Source_Company
       elif choice == 'Permit':
           enbdf113 = a.Permit
       elif choice == 'Feedstock':
           enbdf113 = a.Feedstock

       shoe_xm=a.groupby(enbdf113).Injection.sum().sort_values(ascending=False)
       data_xm=[]
       for i in shoe_xm.items():
               data_xm.append({"value":i[1],"name":i[0]})      
                  

    with c113:
        st_echarts(re_pie(data_xm),theme='white')   


    

def Capture():
    
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
    c2111, c2112,c2113 = st.columns([5,0.5,5])
    c211, c212 = st.columns([6,0.1])
         
    choice = st.selectbox('Select data', ["Construction","Separation Type","Separation Technology"
                                          ,"Capture Company", "Purpose", "Fuel Capacity"])
    if choice == "Construction":
      enbdf211 = a.Construction
      enbdf2111 = a.loc[:,['Project_Name','Construction']]
    elif choice == 'Separation Type':
        enbdf211 = a.Separation_Type
        enbdf2111 = a.loc[:,['Project_Name','Separation_Type']]  
    elif choice == 'Separation Technology':
        enbdf211 = a.Separation_Technology 
        enbdf2111 = a.loc[:,['Project_Name','Separation_Technology']]           
    elif choice == 'Capture Company':
        enbdf211 = a.Capture_Company
        enbdf2111 = a.loc[:,['Project_Name','Capture_Company']]           
    elif choice == 'Purpose':
        enbdf211 = a.Purpose
        enbdf2111 = a.loc[:,['Project_Name','Purpose']]           
    elif choice == 'Fuel Capacity':
        enbdf211 = a.Fuel_Capacity  
        enbdf2111 = a.loc[:,['Project_Name','Fuel_Capacity']]           
    shoe_xm=a.groupby(enbdf211).Injection.sum().sort_values(ascending=False)
    data_xm=[]
    for i in shoe_xm.items():
            data_xm.append({"value":i[1],"name":i[0]})      
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
                             range_color=(1, 100),
                             mapbox_style="carto-positron",
                             opacity=0.5, 
                             labels={'diff_percentage':'Difference Percentage'},
                             center={"lat": 47, "lon": -103},
                             zoom=4.)       
      
      
    with c211:
        st.plotly_chart(fig211)
    with c2111:
        st.dataframe(enbdf2111)       
    with c2113:
        st_echarts(re_pie(data_xm),theme='white')     

def Storage():
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
    c2111, c2112,c2113 = st.columns([5,0.5,5])
    c211, c212 = st.columns([6,0.1])
         
    choice = st.selectbox('Select data', ["Storage Company","Storage Monitoring","Storage Distance"
                                          ,"Fate", "On or Offshore", "Scale"])
    if choice == "Storage Company":
      enbdf211 = a.Storage_Company
      enbdf2111 = a.loc[:,['Project_Name','Storage_Company']]
    elif choice == 'Storage Monitoring':
        enbdf211 = a.Storage_Monitoring
        enbdf2111 = a.loc[:,['Project_Name','Storage_Monitoring']]  
    elif choice == 'Storage Distance':
        enbdf211 = a.Storage_Distance
        enbdf2111 = a.loc[:,['Project_Name','Storage_Distance']]           
    elif choice == 'Fate':
        enbdf211 = a.Fate
        enbdf2111 = a.loc[:,['Project_Name','Fate']]           
    elif choice == 'On or Offshore':
        enbdf211 = a.On_Offshore
        enbdf2111 = a.loc[:,['Project_Name','On_Offshore']]           
    elif choice == 'Scale':
        enbdf211 = a.Scale 
        enbdf2111 = a.loc[:,['Project_Name','Scale']]         
    shoe_xm=a.groupby(enbdf211).Injection.sum().sort_values(ascending=False)
    data_xm=[]
    for i in shoe_xm.items():
            data_xm.append({"value":i[1],"name":i[0]})      
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
                             range_color=(1, 100),
                             mapbox_style="carto-positron",
                             opacity=0.5, 
                             labels={'diff_percentage':'Difference Percentage'},
                             center={"lat": 47, "lon": -103},
                             zoom=4.)       
      
      
    with c211:
        st.plotly_chart(fig211)
    with c2111:
        st.dataframe(enbdf2111)       
    with c2113:
        st_echarts(re_pie(data_xm),theme='white')  
    
def Cost():
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
    c2111, c2112,c2113 = st.columns([5,0.5,5])
    c211, c212 = st.columns([6,0.1])
         
    choice = st.selectbox('Select data', ["Estimated Cost","Intended_Operational_Year","Operation Year"
                                          ,"End Operation Year"])
    if choice == "Estimated Cost":
      enbdf211 = a.Estimated_Cost
      enbdf2111 = a.loc[:,['Project_Name','Estimated_Cost']]
    elif choice == 'Intended_Operational_Year':
        enbdf211 = a.Intended_Operational_Year
        enbdf2111 = a.loc[:,['Project_Name','Intended_Operational_Year']]  
    elif choice == 'Operation Year':
        enbdf211 = a.Operation_Year
        enbdf2111 = a.loc[:,['Project_Name','Operation_Year']]           
    elif choice == 'End Operation Year':
        enbdf211 = a.End_Operation_Year
        enbdf2111 = a.loc[:,['Project_Name','End_Operation_Year']]                   
    shoe_xm=a.groupby(enbdf211).Injection.sum().sort_values(ascending=False)
    data_xm=[]
    for i in shoe_xm.items():
            data_xm.append({"value":i[1],"name":i[0]})      
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
                             range_color=(1, 100),
                             mapbox_style="carto-positron",
                             opacity=0.5, 
                             labels={'diff_percentage':'Difference Percentage'},
                             center={"lat": 47, "lon": -103},
                             zoom=4.)       
      
      
    with c211:
        st.plotly_chart(fig211)
    with c2111:
        st.dataframe(enbdf2111)       
    with c2113:
        st_echarts(re_pie(data_xm),theme='white')        

def Analyze():
    a=pd.read_excel(Path(__file__).parent / "Data/5_2023WorldCCS state_all20240104.xlsx")
    st.write("Item type: Estimated Cost, Injection (MT CO2/yr), Production Capacity, Storage Distance...")
    st.text_input("Type the interested item", key="columns")
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
        'Which type CCS are you interested in?',
        a["Fate"].unique())
    optionB2 = st.slider('latitude',-90.,a.Latitude.max(),(48.,57.))
    optionB3 = st.slider('lLongitude',-180.,a.Longitude.max(),(-115.,-90.))
    optionB4 = st.multiselect(
        'Please select items you are interested in',
        a.columns,
        ['Country', 'Fate', 'Storage Distance', "Estimated Cost", "Injection (MT CO2/yr)", "Production Capacity"])
    FinalSelect=a[(a["Fate"]==optionB1)&(a.Latitude>optionB2[0])&(a.Latitude<optionB2[1])
                  &(a.Longitude>optionB3[0])&(a.Longitude<optionB3[1])][optionB4]

    FinalSelect




    
def main():
    st.sidebar.title('Navigation：')

    # 设置菜单项列表
    menu = ['Overview', 'Injection', 'Cost', 'Company', 'Storage', "Capture", "Analyze"]
    choice = st.sidebar.selectbox('Select', menu)

    # 显示选定页面的内容
    if choice == 'Overview':
        Overview()
    elif choice == 'Cost':
        Cost()
    elif choice == 'Injection':
        Injection()
    elif choice == 'Company':
        Company()
    elif choice == 'Storage':
        Storage()
    elif choice == 'Capture':
        Capture() 
    elif choice == 'Analyze':
        Analyze()            
    else:
        Overview()

if __name__ == '__main__':
    main()

# a=pd.read_csv(Path(__file__).parent / "Data/Williston_Vertical_Storages_All.csv")
# data0=[]
# for i in a.groupby("ENVStorageStatus").size().items():
#     data0.append({"name":i[0],"value":i[1]})



# df = pd.read_csv(Path(__file__).parent / "Data/Williston_Vertical_Storages_All.csv", 
#                   usecols=['StoragePadID', 'Latitude', 'Longitude'])
# df.columns = ['Storage Name', 'latitude', 'longitude']
# st.map(df)




