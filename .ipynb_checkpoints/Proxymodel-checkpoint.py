# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 10:52:39 2024

@author: 28604
"""

import sklearn
import streamlit as st
import sys
import requests
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
#matplotlib.rcParams['axes.unicode_minus']=False
from sklearn import datasets
from numpy import argsort
import warnings
warnings.filterwarnings("ignore")
import seaborn as sns ## 设置绘图的主题
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


from streamlit_echarts import st_echarts
import json
from streamlit_echarts import Map
from streamlit_echarts import JsCode






pd.set_option("max_colwidth",100)
st.markdown("# Main page 🎈")
st.sidebar.markdown("# Main page 🎈")


choice = st.sidebar.selectbox('What do you want to predict', ["Plume radius","Injectivity","Cost with drill new well","Cost with use old well","Upload Data"])
if choice == "Injectivity":
    enbdf = pd.read_excel(Path(__file__).parent / "Data/1CCUS_injectivity.xlsx")
elif choice == 'Plume radius':
    enbdf = pd.read_excel(Path(__file__).parent / "Data/2CCUS_plume_radius.xlsx")
elif choice == 'Cost with drill new well':
    enbdf = pd.read_excel(Path(__file__).parent / "Data/3CCUS_Cost_drill_new_well.xlsx")
elif choice == 'Cost with use old well':
    enbdf = pd.read_excel(Path(__file__).parent / "Data/4CCUS_Cost_use_old_well.xlsx")
elif choice == "Upload Data":
    enbdf = st.file_uploader("Please upload your data (xlsx)")

#获取训练集最大最小值
yc=enbdf["Target"].values
yc_min = yc.min()
yc_max = yc.max()
xc=enbdf.drop(axis=1,columns="Target").values
xc_min = xc.min()
xc_max = xc.max()

enbdf_n = (enbdf-enbdf.min())/(enbdf.max()-enbdf.min())
y=enbdf_n["Target"].values
x=enbdf_n.drop(axis=1,columns="Target").values

## 计算相关系数
datacor = enbdf_n.corr()  
fig1, ax1 = plt.subplots(figsize=(16, 12))
sns.heatmap(datacor,square=True,annot=True,fmt = ".2f",
                linewidths=.5,cmap="YlGnBu",
                cbar_kws={"fraction":0.046,"pad":0.03})
ax1.set_title("Correlation coefficients between reservoir parameters")
# Show the plot



# 归一化
# x_minmax = preprocessing.MinMaxScaler() # 初始化x的归一
# x_minmax.fit(x)
# x_scaled = x_minmax.transform(x) # 归一化x

# y_minmax = preprocessing.MinMaxScaler() # 初始化y的归一
# y_minmax.fit(y)
# y_scaled = y_minmax.transform(y)


X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=1234)
# X_train = std.fit_transform(X_train)
# X_test = std.transform(X_test)

choice0 = st.sidebar.selectbox('Choose the machine learning model', ["Random Forest Regressor", "DecisionTreeRegressor", "MLR", "Ridge","Lasso","LassoLars","ElasticNetCV", "SVR","KNeighbors Regressor", "Neural network", "AdaBoostRegressor", "GradientBoostingRegressor"])

if choice0 == "MLR":
    model = LinearRegression()
elif choice0 == "Ridge":
    model=Ridge(5, max_iter=100000)
if choice0 == "Lasso":
    model=Lasso(0.0001, max_iter=100000)
elif choice0 == "LassoLars":
    model = LassoLars()
elif choice0 == "ElasticNetCV":
    model = ElasticNetCV(cv=5,
                    random_state = 12)
# elif choice0 == "MARS(degree=1)":
#     model = Earth(max_terms = 200,max_degree = 1,feature_importance_type = "gcv")
# elif choice0 == "MARS(degree=5)":
#    model = Earth(max_terms = 200,max_degree = 5,feature_importance_type = "gcv")
elif choice0 == "SVR":
    model = SVR(kernel = "rbf",gamma = 0.01)
elif choice0 == "GradientBoostingRegressor":
    model = GradientBoostingRegressor(random_state=1)    
elif choice0 == "AdaBoostRegressor":
    model = AdaBoostRegressor(n_estimators =800,
                        learning_rate = 0.9,
                        random_state=1234)    
elif choice0 == "DecisionTreeRegressor":
    model = DecisionTreeRegressor(random_state=1)
#elif choice0 == "Polynomial Regression":
#    model = polynomial_features()
elif choice0 == "KNeighbors Regressor":
    model = KNeighborsRegressor(n_neighbors = 15,weights = "distance",n_jobs = 4)
elif choice0 == "Random Forest Regressor":
    model = RandomForestRegressor(n_estimators=600, max_features = 'sqrt', max_depth=15, random_state =1234) 
elif choice0 == "Neural network":
    model = MLPRegressor(hidden_layer_sizes = (100,100),
                     activation = "tanh",batch_size = 128,
                     learning_rate = "adaptive",random_state = 12,
                     max_iter = 2000)    
#model = RandomForestRegressor(n_estimators=300, max_features = 'sqrt', max_depth=5, random_state =1234)
#将数据放入模型中
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

## 计算预测精度R2
r2 = r2_score(y_test, y_pred)
r2_n = round(r2, 4)
MSE1 = MSE(y_test, y_pred)
MSE1_n = round (MSE1, 4)
## 可视化R2 EVS MSE
##num_regress = len(y_pred)
##plt.subplots(f'n={num_regress}')
##plt.subplots(f'R^2={r2}')
##plt.subplots(X_test, EVS1)
##plt.subplots(X_test, MSE1)




## 可视化预测结果和真实值之间的差距
## 可视化出参数搜索找的的模型在训练集和测试集上的预测效果
fig2, ax2 = plt.subplots(figsize=(9,9))
ax2.scatter(y_test, y_pred, label='Actual')
ax2.text(0.4,0.17,s = "r2 score:"+str(r2_n))
ax2.text(0.4,0.1,s = "Mean squared error:"+str(MSE1_n))
ax2.set_xlabel('True Values')
ax2.set_ylabel('Predictions')
ax2.set_title('True vs Predicted')


fig1
fig2



#plt.subplot(1,2,1) ## 训练数据结果可视化
#rmse = round(mean_squared_error(y_train,model.predict(X_train)),4)
#plt.plot(X_train,y_train.values[index],"r", linewidth=2, label = "原始数据")
## plt.plot(X_train,model.predict(X_train)[index],"bo",
##          markersize=3,label = "预测值")
## plt.text(200,35,s = "均方根误差:"+str(rmse))
## plt.legend()
## plt.grid()
## plt.xlabel("Index")
## plt.ylabel("Y")
## plt.title("支持向量机回归(训练集)")

## 测试数据结果可视化 
## fig3, ax3 = plt.subplots(1,2,2)   
## rmse = round(mean_squared_error(y_test,model.predict(X_test),4)
## plt.plot(X_test,y_test, linewidth=2, label = "原始数据")
## plt.plot(X_test,model.predict(X_test), markersize=3,label = "预测值")
## plt.text(50,35,s = "均方根误差:"+str(rmse))
## plt.legend()
## plt.grid()
## plt.xlabel("Index")
## plt.ylabel("Y")
## plt.title("支持向量机回归(测试集)")
## plt.tight_layout()
## plt.show()






st.table(enbdf.head())
df=enbdf_n
df_copy=df.copy()
st.table(df_copy.head())




# if st.button("Save model"):
#     pkl_filename = "C:\\Users\\28604\\1 Enverus 回归拟合数据\\14th meeting\\0 CCUS APP18\\pickle_model1.pkl"
#     with open(pkl_filename, 'wb') as file:
#         pickle.dump(model, file)
#     st.write("Saved successfully")


# uploaded_file0 = st.file_uploader("Select local model")
uploaded_file = st.file_uploader("Select a file (.csv)")
if (uploaded_file is not None):
    # pickle_model = pickle.load(uploaded_file0)  
    df_new = pd.read_csv(uploaded_file)
#df_new=pd.read_csv(r"F:\notebooks1\streamlit\data\new.csv")
    st.table(df_new.head())
#深度拷贝
    df_new_copy=df_new.copy()
    df_new_copy_n = (df_new_copy-xc.min())/(xc.max()-xc.min())    
    st.table(df_new_copy_n.head())
    
    y_pred = model.predict(df_new_copy_n.values)
    st.text('The normalized predicted value')
    df_new["predict_stander"]=y_pred
    st.dataframe((df_new["predict_stander"]).head())
# =============================================================================
#     file_path = r'C:\Users\28604\1 Enverus 回归拟合数据\14th meeting\Canada CO2 emission\williston\test1.txt'
#     file_label = 'Normalized prediction results'
#     st.markdown(df_new["predict_stander"][file_path, file_label],
#                 unsafe_allow_html=True)
# =============================================================================
    
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(df_new["predict_stander"])
    
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='predict_stander.csv',
        mime='text/csv',
    )    
    
    
    
    
    st.text('Returns a non-normalized predicted value')
    df_new["predict_unstander"]=y_pred*(yc.max()-yc.min())+yc.min()
    st.dataframe((df_new["predict_unstander"]).head())
    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')
    
    csv = convert_df(df_new["predict_unstander"])
    
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='predict_unstander.csv',
        mime='text/csv',
    ) 
# =============================================================================
#     file_path = r'C:\Users\28604\1 Enverus 回归拟合数据\14th meeting\Canada CO2 emission\williston\test2.txt'
#     file_label = 'Non-normalized prediction results'
#     st.markdown(df_new["predict_unstander"][file_path, file_label],
#                 unsafe_allow_html=True)
# =============================================================================

    #y_pred_n = y_pred.copy
    #y_pred_ncopy=(y_pred_n)*(yc.max()-yc.min())+yc.min()
    #df_new_copy["predict"]=y_pred_ncopy
    #st.table(df_new_copy[["predict"]])


#if st.button("Save predict"):
#    pkl_filename = "C:\\Users\\28604\\1 Enverus 回归拟合数据\\13th meeting\\0 CCUS APP05\\Predict.csv"
#    with open(pkl_filename, 'wb') as file:
#        pickle.dump(table, file)
#    st.write("Saved successfully")



