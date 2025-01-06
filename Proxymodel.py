

import sklearn
import streamlit as st
import requests
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.rcParams['axes.unicode_minus']=False
from sklearn import datasets
from numpy import argsort
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns ## 设置绘图的主题
import sys
import os
sys.path.append(os.getcwd())
from pathlib import Path
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import preprocessing
from sklearn.preprocessing import QuantileTransformer,StandardScaler
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import train_test_split, cross_val_score, KFold, GridSearchCV,StratifiedKFold
from sklearn import linear_model
from sklearn.linear_model import LinearRegression, Ridge, Lasso,LassoLars,ElasticNetCV,LogisticRegression,LogisticRegressionCV
from sklearn import metrics
from sklearn.metrics import r2_score, explained_variance_score as EVS, mean_squared_error as MSE
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score, mean_absolute_error,classification_report
from sklearn.neural_network import MLPClassifier,MLPRegressor
from statsmodels.graphics.mosaicplot import mosaic
from scipy.stats import chi2_contingency
from pandas.plotting import parallel_coordinates
from sklearn.pipeline import Pipeline
from scipy import stats
from sklearn.svm import SVC
from sklearn.svm import SVR
from sklearn import ensemble
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from scipy.spatial import distance
from pyecharts.faker import Faker
import json
from streamlit_echarts import Map
from streamlit_echarts import JsCode
import streamlit as st
from streamlit_echarts import st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from pyecharts.charts import Line, Pie, Bar
import pandas as pd
import numpy as np
from PIL import Image
import os
import sys
sys.path.append(os.getcwd())
from pathlib import Path
import pickle
import joblib


st.set_page_config(page_title="CCS site selection", layout="wide")
st.markdown("<h1 style='text-align: center; color: white;'>CCS project distribution </h1>", unsafe_allow_html=True)
bg_img="""
<style>
[data-testid="stAppViewContainer"]{ 
    background-color:black
}
[data-testid="metric-container"]{
    color: white;
    }
[data-testid="stMarkdownContainer"]{
    color: white;
    }
[data-testid="stHeader"]{
    background-color:rgba(0, 0, 0, 0)
    }
</style>
  """

st.markdown(bg_img, unsafe_allow_html=True)


d11, d12, d13, d14, d15, d16, d17, d18=st.columns(8) 
with d11:
    st.page_link("pages/Predict.py", label="Predict", icon="🎯")
with d12:    
    st.page_link("pages/GlobalCCS.py", label="GlobalCCS", icon="🌎")
with d13: 
    st.page_link("pages/Williston.py", label="Williston", icon="🗺")





def map_Continent(data0):
    with open(Path(__file__).parent / "Data/Continent.geojson", "r",encoding="utf-8") as f:
        map = Map(
            "world",
            json.loads(f.read())
        )
    
    options = {
        "tooltip": {
              "trigger": 'item',
              "showDelay": 0,
              "transitionDuration": 0.2,
            },
        "visualMap": {
            "show": False,
            "left": "right",
            "min": 0,
            "max": 123,
            "inRange": {
                "color": [
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
                ]
            },
            "text": ["High", "Low"],
            "calculable": True,
        },
        "series": [
            {
                "name": "Number of CCS projects",
                "type": "map",
                "roam": True,
                "map": "world",
                "emphasis": {"label": {"show": True}},
                "data": data0,
            }
        ],
    }
    
    events = {
    "click": "function(params) {return params.name }",
}
    
    return options,map,events


def map_Country(Continent):
    
    data_Country=[]
    for i in a[a["Continent"]==Continent].groupby("Country").size().items():
        data_Country.append({"name":i[0],"value":i[1]})
        
    
    dir0=str(Path(__file__).parent / "Data/Continent/")
    dir1=dir0+ "/"+ Continent +".geojson"
    with open(dir1, "r",encoding="utf-8") as f:
        map = Map(
            "North America",
            json.loads(f.read())
        )
    
    options = {
        "tooltip": {
              "trigger": 'item',
              "showDelay": 0,
              "transitionDuration": 0.2,
            },
        "visualMap": {
            "show": False,
            "left": "right",
            "min": 0,
            "max": 40,
            "inRange": {
                "color": [
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
                ]
            },
            "text": ["High", "Low"],
            "calculable": True,
        },
        "series": [
            {
                "name": "Number of CCS projects",
                "type": "map",
                "roam": True,
                "map": "North America",
                "emphasis": {"label": {"show": True}},
                "data": data_Country,
            }
        ],
    }
    
    return options,map








  
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
      "legend":{},
      "series": [
        {
          "data": [0]+xse.tolist(),
          "type": 'bar',
          "showBackground": True,
          "backgroundStyle": {
            "color": 'rgba(180, 180, 180, 0.2)'
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
        "top": '5%',
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


shoe_xm=a.groupby('Transpor_Method').Injection.sum().sort_values(ascending=False)
shoe_fg=a.groupby('Status').Injection.sum().sort_values(ascending=False)
shoe_lx=a.groupby('Fate').Injection.sum().sort_values(ascending=False)

data_xm=[]
for i in shoe_xm.items():
    data_xm.append({"value":i[1],"name":i[0]})
data_fg=[]
for i in shoe_fg.items():
    data_fg.append({"value":i[1],"name":i[0]})
data_lx=[]
for i in shoe_lx.items():
    data_lx.append({"value":i[1],"name":i[0]})
data_Continent=[]
for i in a.groupby("Continent").size().items():
    data_Continent.append({"name":i[0],"value":i[1]})

c51,c52,c53,c54=st.columns(4)
c41,c42,c43,c44=st.columns(4)
c31,c32,c33=st.columns([1,2,1])
c21,c22=st.columns(2)
c41.metric("CCS projects",len(a))
c42.metric("Countries involved",len(a.Country.unique()))
c43.metric("Total injection Mt",round(a.InjectionSize_Mt.sum()))
c44.metric("Injection rate Mt/y",round(a.Injection.mean()))


with c31:
    st_echarts(tz_pie(data_lx),theme='dark')
    st_echarts(tz_pie(data_fg),theme='dark')
with c32:
    option_Continent, map_Continent,events_Continent=map_Continent(data_Continent)
    Continent=st_echarts(option_Continent,map=map_Continent,events=events_Continent, height=625, width=1050,theme='dark')
with c21:
    st_echarts(paleituo(xse,xse_cum),theme='dark')
with c22:
    st_echarts(price_sales(data1,data2),theme='dark')
with c33:
    if Continent:
        pro=Continent
    else:
        pro="North America"
    option_Country, map_Country0=map_Country(pro)
    st_echarts(option_Country,map=map_Country0, theme='dark')
    st_echarts(tz_pie(data_xm),theme='dark')