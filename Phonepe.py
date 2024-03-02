import json
import streamlit as st
import pandas as pd
import requests
import pymysql
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from PIL import Image
import base64
from streamlit.components.v1 import html

#CREATE DATAFRAMES FROM SQL
#sql connection

mydb=pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="root",
                    database="phonepe_data")
cursor=mydb.cursor()


#Aggregated_insurance
cursor.execute("select * from aggregated_insurance;")
mydb.commit()
table7 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#Aggregated_transsaction
cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table1 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
cursor.execute("select * from aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_insurance
cursor.execute("select * from map_insurance")
mydb.commit()
table3 = cursor.fetchall()

Map_insurance = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#Map_transaction
cursor.execute("select * from map_transaction")
mydb.commit()
table3 = cursor.fetchall()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
mydb.commit()
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_insurance
cursor.execute("select * from top_insurance")
mydb.commit()
table5 = cursor.fetchall()

Top_insurance = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_transaction
cursor.execute("select * from top_transaction")
mydb.commit()
table5 = cursor.fetchall()
Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
cursor.execute("select * from top_user")
mydb.commit()
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))



def Aggre_insurance_Y(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy


def Aggre_insurance_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_amount", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Transaction_count", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_amount"].min(),aiyqg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_count"].min(),aiyqg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return aiyq

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 600, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)
        
def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_insure_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_amount",
                              width=600, height=500, title= f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["RegisteredUser","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["RegisteredUser", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUser",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUser", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUser"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "RegisteredUser",barmode= "group",
                           width=1000, height= 800,color= "Pincodes",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)




#Streamlit part

st.set_page_config(layout= "wide")

# Column layout for logos
col1, col2, col3 = st.columns([1,6,1])

# Load and display YouTube logo
with col1:
    image = Image.open("C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\guvi_logo.png")

    new_size = (100, 60) 
    resized_image = image.resize(new_size)
    st.image(resized_image)

# Display the main header: Using Markdown with HTML for center alignment
st.markdown("<h1 style='text-align: center;'>PHONEPE DATA VISUALIZATION AND EXPLORATION</h1>", unsafe_allow_html=True)
st.markdown("##")

select = option_menu(
    menu_title = None,
    options = ["About","Home","Top Charts","Data Exploration","Contact"],
    icons =["exclamation-circle","house","bar-chart","toggles","envelope"],
    default_index=2,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100"},
        "icon": {"color": "black", "font-size": "20px"},
            
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD",  "font-family": "YourFontFamily"}})


if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        image = Image.open("C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\PhonePe-Logo.png")
        new_size = (250, 120)
        resized_image = image.resize(new_size)
        st.image(resized_image) 

        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")

        # Define the URL you want to redirect to
        url = "https://www.phonepe.com/app-download/"

        # This HTML uses inline styling to make the link look more like a button and automatically redirects when clicked
        st.markdown(f"<a href='{url}' target='_blank'><button style='color: white; background-color: #6739B7; padding: 10px 24px; border: none; cursor: pointer; border-radius: 12px; text-align: center;'>Download the App</button></a>", unsafe_allow_html=True)

    with col2:

        # Read the local GIF file
        file_path = "C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\upi.gif"
        with open(file_path, "rb") as file:
            contents = file.read()
            data_url = base64.b64encode(contents).decode("utf-8")
        # Display the GIF
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="GIF">', unsafe_allow_html=True)


    col3,col4= st.columns(2)
    
    with col3:
        # Read the local GIF file
        file_path = "C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\PhonePe_Motion_Graphics_1.gif"
        with open(file_path, "rb") as file:
            contents = file.read()
            data_url = base64.b64encode(contents).decode("utf-8")
        # Specify the width and height in the style attribute
        width = 500
        height = 400

        # Display the GIF with adjusted size
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="GIF" style="width:{width}px;height:{height}px;">', unsafe_allow_html=True)

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write('<div style="margin-left: 20px;">1. Direct Transfer & More</div>', unsafe_allow_html=True)
        st.write('<div style="margin-left: 20px;">2. QR Code</div>', unsafe_allow_html=True)


    col5,col6= st.columns(2)

    with col5:

        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****Earn Great Rewards****")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        # Read the local GIF file
        file_path = "C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\PhonePe_Motion_Graphics_2.gif"
        with open(file_path, "rb") as file:
            contents = file.read()
            data_url = base64.b64encode(contents).decode("utf-8")
        # Specify the width and height in the style attribute
        width = 300
        height = 400

        # Display the GIF with adjusted size
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="GIF" style="width:{width}px;height:{height}px;">', unsafe_allow_html=True)

if select == "Data Exploration":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year**", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())

            df_agg_insur_Y= Aggre_insurance_Y(Aggre_insurance,years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter**", df_agg_insur_Y["Quarter"].min(), df_agg_insur_Y["Quarter"].max(),df_agg_insur_Y["Quarter"].min())

            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)

            
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at= st.slider("**Select the Year**", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())

            df_agg_tran_Y= Aggre_insurance_Y(Aggre_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

            df_agg_tran_Y_Q= Aggre_insurance_Y_Q(df_agg_tran_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)


        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year_AU",Aggre_user["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(Aggre_user,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.slider("**Select the Year_mi**", Map_insurance["Years"].min(), Map_insurance["Years"].max(),Map_insurance["Years"].min())

            df_map_insur_Y= Aggre_insurance_Y(Map_insurance,years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y,state_m1)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m1= st.slider("**Select the Quarter_mi**", df_map_insur_Y["Quarter"].min(), df_map_insur_Y["Quarter"].max(),df_map_insur_Y["Quarter"].min())

            df_map_insur_Y_Q= Aggre_insurance_Y_Q(df_map_insur_Y, quarters_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m2= st.selectbox("Select the State_miy", df_map_insur_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_insur_Y_Q, state_m2)

        elif method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.slider("**Select the Year_mi**", Map_transaction["Years"].min(), Map_transaction["Years"].max(),Map_transaction["Years"].min())

            df_map_tran_Y= Aggre_insurance_Y(Map_transaction, years_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

            map_insure_plot_1(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.slider("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(),df_map_tran_Y["Quarter"].min())

            df_map_tran_Y_Q= Aggre_insurance_Y_Q(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_tran_Y_Q, state_m4)

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",Map_user["Years"].unique())
            map_user_Y= map_user_plot_1(Map_user, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)

    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year_ti**", Top_insurance["Years"].min(), Top_insurance["Years"].max(),Top_insurance["Years"].min())
 
            df_top_insur_Y= Aggre_insurance_Y(Top_insurance,years_t1)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.slider("**Select the Quarter_ti**", df_top_insur_Y["Quarter"].min(), df_top_insur_Y["Quarter"].max(),df_top_insur_Y["Quarter"].min())

            df_top_insur_Y_Q= Aggre_insurance_Y_Q(df_top_insur_Y, quarters_t1)

        
        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.slider("**Select the Year_tt**", Top_transaction["Years"].min(), Top_transaction["Years"].max(),Top_transaction["Years"].min())
 
            df_top_tran_Y= Aggre_insurance_Y(Top_transaction,years_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.slider("**Select the Quarter_tt**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(),df_top_tran_Y["Quarter"].min())

            df_top_tran_Y_Q= Aggre_insurance_Y_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", Top_user["Years"].unique())

            df_top_user_Y= top_user_plot_1(Top_user,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["States"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)


if select == "Top Charts":

    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 Districts With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()


#----------------About-----------------------#

if select == "About":
    col1, col2 = st.columns(2)
    with col1:
        # Read the local GIF file
        file_path = "C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\pulse-video.gif"
        with open(file_path, "rb") as file:
            contents = file.read()
            data_url = base64.b64encode(contents).decode("utf-8")
        # Display the GIF
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="GIF">', unsafe_allow_html=True)


    with col2:
        st.write("---")
        st.markdown(" ")
        st.markdown(" ")
        st.write("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government.")
        st.write(" Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    col1,col2 = st.columns(2)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.write("---")
        st.subheader("Phonepe became a leading digital payments company")
        st.image(Image.open("C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\about_phonepe.jpg"),width = 400)
        with open("C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\about_phonepe1.png","rb") as f:
            data = f.read()
        
                # URL of the PDF file you want to make available for download
        pdf_url = "https://www.phonepe.com/pulsestatic/775/pulse/static/83bc2c9e9038369af2eb9eb7d62cb49f/PhonePe_Pulse_BCG_report.pdf"

        # Download the file using requests
        response = requests.get(pdf_url)
        filename = pdf_url.split('/')[-1]  # Extracts filename from URL

        # Ensure the request was successful
        if response.status_code == 200:
            # Make the content of the file available as a download button
            st.download_button(label="Download Report", 
                            data=response.content,
                            file_name=filename,
                            mime='application/pdf')
        else:
            st.write("Failed to download file.")
        
    with col2:
        st.image(Image.open("C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\about_phonepe1.png"),width = 700)


#----------------------Contact---------------#


if select == "Contact":
    Name = (f'{"Name :"}  {"PUGAZHENTHI L"}')
    mail = (f'{"Mail :"}  {"pugazzh2802@gmail.com"}')
    description = "Data Scientist excelling in analytics, Python, SQL, and PowerBI optimization."
    social_media = {
        "YouTube": "https://youtube.com/@pugazhenthi_l",
        "GITHUB": "https://github.com/pugazhenthi-l",
        "LINKEDIN": "https://www.linkedin.com/in/pugazhenthi-l/"}
    
    col1, col2, col3 = st.columns(3)
    col3.image(Image.open("C:\\Users\\Hxtreme\\Documents\\New folder\\Phonepe-pulse-main\\attachments\\pugazh.png"), width=300)
    st.subheader(Name)
    st.subheader(mail)
    with col1:
        st.title('Phonepe Pulse data visualisation')
        st.write("The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, with at least 10 different dropdown options for users to select different facts and figures to display. The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
        st.write("---")
        
        
    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")
