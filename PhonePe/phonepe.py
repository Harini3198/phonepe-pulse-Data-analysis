import streamlit as st
from streamlit_option_menu import option_menu
import pymysql
import pandas as pd
import plotly.express as px
import requests
import json
from streamlit_lottie import st_lottie
from PIL import Image
from streamlit.components.v1 import html

#mysql connection
data_base=pymysql.connect(host='localhost',
                    user='root',
                    password='1234',
                    database='phonepe_db',
                    port=3306)
cur=data_base.cursor()

#aggregated_transaction Table to Dataframe

cur.execute("select * from aggregated_transaction")
data_base.commit()
table1=cur.fetchall()

aggre_transaction=pd.DataFrame(table1, columns=("States", "Years", "Quater", "Transaction_name", "Transaction_count", "Transaction_amount"))

#aggregated_users table to Dataframe

cur.execute("select * from aggregated_users")
data_base.commit()
table2=cur.fetchall()

aggre_users=pd.DataFrame(table2, columns=("States", "Years", "Quater", "Brand_name", "Transaction_count", "Percentage"))

#map_transaction table to Dataframe

cur.execute("select * from map_transaction")
data_base.commit()
table3=cur.fetchall()

map_trans=pd.DataFrame(table3, columns=("States", "Years", "Quater", "District", "Transaction_count", "Transaction_amount"))

# map_user table to Dataframe

cur.execute("select * from map_user")
data_base.commit()
table4=cur.fetchall()

map_users=pd.DataFrame(table4, columns=("States", "Years", "Quater", "District", "Registered_Users", "OpenApps_Count"))

# top_transaction table to Dataframe

cur.execute("select * from top_transaction")
data_base.commit()
table5=cur.fetchall()

top_trans=pd.DataFrame(table5, columns=("States", "Years", "Quater", "District", "Transaction_count", "Transaction_amount"))

# top_users table to Dataframe

cur.execute("select * from top_users")
data_base.commit()
table6=cur.fetchall()

top_user=pd.DataFrame(table6, columns=("States", "Years", "Quater", "Pincodes", "Registered_Users"))

# Aggregated transaction year chart creation

def trans_amt_count_Y(year):
    tacy=f'''select * from aggregated_transaction where Years = {year}'''
    cur.execute(tacy)
    data_base.commit()
    t1=cur.fetchall()
    tacydf=pd.DataFrame(t1, columns=("States", "Years", "Quater", "Transaction_name", "Transaction_count", "Transaction_amount"))

    tacyg=f'''select States, sum(Transaction_count) as Transaction_count, sum(Transaction_amount) as Transaction_amount from 
              aggregated_transaction where Years = {year} group by States'''
    cur.execute(tacyg)
    data_base.commit()
    t2=cur.fetchall()
    tacygdf=pd.DataFrame(t2, columns=("States","Transaction_count","Transaction_amount"))
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    st.subheader(":blue[Yearly Analysis of Transaction Amount]")
    fig_amount= px.area(tacygdf, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
    st.plotly_chart(fig_amount)

    fig_india_1= px.choropleth(tacygdf, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_amount", color_continuous_scale="Cividis",
                            range_color=(tacygdf["Transaction_amount"].min(),tacygdf["Transaction_amount"].max()), hover_name="States", 
                            title=f"{year} TRANSACTION AMOUNT", 
                            fitbounds= "locations",
                            height=600, width=600)
    fig_india_1.update_geos(visible= False)
    st.plotly_chart(fig_india_1)
    st.subheader(":blue[Yearly Analysis of Transaction Count]")

    fig_count= px.area(tacygdf, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
    st.plotly_chart(fig_count)

    fig_india_2= px.choropleth(tacygdf, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_count", 
                                color_continuous_scale="Inferno",
                            range_color=(tacygdf["Transaction_count"].min(),tacygdf["Transaction_count"].max()), hover_name="States", 
                            title=f"{year} TRANSACTION COUNT", 
                            fitbounds= "locations",
                            height=600, width=600)
    fig_india_2.update_geos(visible= False)
    st.plotly_chart(fig_india_2)
    return tacydf
    
# Aggregated transaction Quater chart creation
def trans_amt_count_Y_Q(df, quater):
    tacy=df[df["Quater"]==quater]
    tacy.reset_index(drop= True, inplace= True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()
    st.subheader(":blue[Quaterly Analysis of Transaction Amount]")

    fig_amount= px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quater} QUARTER TRANSACTION AMOUNT", 
                        color_discrete_sequence=px.colors.sequential.Inferno, height=650, width=600)
    st.plotly_chart(fig_amount)

    fig_india_1= px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_amount", 
                            color_continuous_scale="viridis",
                            range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()), hover_name="States", 
                            title=f"{tacy['Years'].min()} YEAR {quater} QUARTER TRANSACTION AMOUNT", 
                            fitbounds= "locations",
                            height=600, width=600)
    fig_india_1.update_geos(visible= False)
    st.plotly_chart(fig_india_1)
    st.subheader(":blue[Quaterly Analysis of Transaction Count]")
    fig_count= px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quater} QUARTER TRANSACTION COUNT", 
                        color_discrete_sequence=px.colors.sequential.algae_r, height=650, width=600)
    st.plotly_chart(fig_count)

    fig_india_2= px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_count", 
                            color_continuous_scale="Twilight",
                            range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()), hover_name="States", 
                            title=f"{tacy['Years'].min()} YEAR {quater} QUARTER TRANSACTION COUNT", 
                            fitbounds= "locations",
                            height=600, width=600)
    fig_india_2.update_geos(visible= False)
    st.plotly_chart(fig_india_2)
    return tacy

# Aggregated transaction state wise chart creation
def trans_type(df, state):
    tacy=df[df["States"]==state]
    tacy.reset_index(drop= True, inplace= True)

    tacyg=tacy.groupby("Transaction_name")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    st.subheader(":blue[Statewise Analysis of Transaction Amount in Transaction Type]")

    fig_pie1=px.pie(data_frame=tacyg, names="Transaction_name", values="Transaction_amount", width=600, title=f"{state.upper()} TRANSACTION AMOUNT", 
                    color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie1)
    st.subheader(":blue[Statewise Analysis of Transaction Count in Transaction Type]")
    fig_pie2=px.pie(data_frame=tacyg, names="Transaction_name", values="Transaction_count", width=600, title=f"{state.upper()} TRANSACTION COUNT",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl_r)
    st.plotly_chart(fig_pie2)

# AGGREGATED USER
# Aggregated user year wise chart creation

def agg_user_count(year):
    auc=f'''select * from aggregated_users where Years = {year}'''
    cur.execute(auc)
    data_base.commit()
    t1=cur.fetchall()
    aucdf=pd.DataFrame(t1, columns=("States", "Years", "Quater", "Brand_name", "Transaction_count", "Percentage"))
    aucg=f'''select Brand_name, sum(Transaction_count) from aggregated_users where Years = {year} group by Brand_name'''
    cur.execute(aucg)
    data_base.commit()
    t2=cur.fetchall()
    aucgdf=pd.DataFrame(t2,columns=("Brand_name","Transaction_count"))

    fig_count= px.area(aucgdf, x="Brand_name", y="Transaction_count", title=f"{year} YEAR, BRAND AND TRANSACTION COUNT", 
                       color_discrete_sequence=px.colors.sequential.Darkmint_r, height=650, width=1000, hover_name="Brand_name")
    st.plotly_chart(fig_count)
    return aucdf

# Aggregated user quater wise chart creation
def agg_user_count_Q(df, quater):
    aucq=df[df["Quater"]==quater]
    aucq.reset_index(drop= True, inplace= True)

    aucyq=pd.DataFrame(aucq.groupby("Brand_name")["Transaction_count"].sum())
    aucyq.reset_index(inplace=True)

    fig_count_q= px.area(aucyq, x="Brand_name", y="Transaction_count", title=f"{df['Years'].min()} YEAR {quater} QUARTER, BRAND AND TRANSACTION AMOUNT", 
                        color_discrete_sequence=px.colors.sequential.BuPu_r, height=650, width=1000)
    st.plotly_chart(fig_count_q)
    return aucq

# Aggregated user state wise chart creation
def agg_user_states(ag_df, ag_state):
    aucs=ag_df[ag_df["States"]==ag_state]
    aucs.reset_index(drop= True, inplace= True)

    aucsq=pd.DataFrame(aucs.groupby("Brand_name")["Transaction_count"].sum())
    aucsq.reset_index(inplace=True)

    agg_user_pie=px.pie(data_frame=aucsq, names="Brand_name", values="Transaction_count", width=600, title=f"{ag_state.upper()} BRAND AND TRANSACTION COUNT", hole=0.5)
    st.plotly_chart(agg_user_pie)

# Map transaction year wise chart creation
def map_trans_amt_count_Y(year):
    mtacy=f'''select * from map_transaction where Years = {year}'''
    cur.execute(mtacy)
    data_base.commit()
    t1=cur.fetchall()
    mtacydf=pd.DataFrame(t1, columns=("States", "Years", "Quater", "District", "Transaction_count", "Transaction_amount"))

    mtacyg=f'''select States, sum(Transaction_count) as Transaction_count, sum(Amount) as Transaction_amount from 
              map_transaction where Years = {year} group by States'''
    cur.execute(mtacyg)
    data_base.commit()
    t2=cur.fetchall()
    mtacygdf=pd.DataFrame(t2, columns=("States","Transaction_count","Transaction_amount"))
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    st.subheader(":blue[Yearly Analysis of Transaction Amount]")
    fig_amount= px.area(mtacygdf, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
    st.plotly_chart(fig_amount)

    fig_india_1= px.choropleth(mtacygdf, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_amount", color_continuous_scale="Cividis",
                            range_color=(mtacygdf["Transaction_amount"].min(),mtacygdf["Transaction_amount"].max()), hover_name="States", 
                            title=f"{year} TRANSACTION AMOUNT", 
                            fitbounds= "locations",
                            height=600, width=600)
    fig_india_1.update_geos(visible= False)
    st.plotly_chart(fig_india_1)
    st.subheader(":blue[Yearly Analysis of Transaction Count]")

    fig_count= px.area(mtacygdf, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
    st.plotly_chart(fig_count)

    fig_india_2= px.choropleth(mtacygdf, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_count", 
                                color_continuous_scale="Inferno",
                            range_color=(mtacygdf["Transaction_count"].min(),mtacygdf["Transaction_count"].max()), hover_name="States", 
                            title=f"{year} TRANSACTION COUNT", 
                            fitbounds= "locations",
                            height=600, width=600)
    fig_india_2.update_geos(visible= False)
    st.plotly_chart(fig_india_2)
    return mtacydf

# Map transaction district wise chart creation
def map_trans_district(mt_df, state):
    mtd=mt_df[mt_df["States"]==state]
    mtd.reset_index(drop= True, inplace= True)

    mtdg=mtd.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    mtdg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:
        
        map_tran_bar1=px.area(mtdg, y="Transaction_amount", x="District", title=f"{state.upper()} STATE, DISTRICT AND TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Agsunset_r, height=650, width=600)
        st.plotly_chart(map_tran_bar1)
    with col2:
        
        map_tran_bar2=px.area(mtdg, y="Transaction_count", x="District", title=f"{state.upper()} STATE, DISTRICT AND TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluyl_r, height=650, width=600)
        st.plotly_chart(map_tran_bar2)
    col1,col2=st.columns(2)
    with col1:
        
        map_tran_pie1=px.pie(data_frame=mtdg, values="Transaction_amount", names="District", title=f"{state.upper()} STATE, DISTRICT AND TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Inferno, height=650, width=600)
        st.plotly_chart(map_tran_pie1)
    with col2:
        
        map_tran_pie2=px.pie(data_frame=mtdg, values="Transaction_count", names="District", title=f"{state.upper()} STATE, DISTRICT AND TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Plasma, height=650, width=600)
        st.plotly_chart(map_tran_pie2)

# Map user year wise chart creation
def map_user_count(year):
    muc=f'''select * from map_user where Years = {year}'''
    cur.execute(muc)
    data_base.commit()
    t1=cur.fetchall()
    mucdf=pd.DataFrame(t1, columns=("States", "Years", "Quater", "District", "Registered_Users", "OpenApps_Count"))    
    mucg=f'''select States, sum(Registered_Users) from map_user where Years = {year} group by States'''
    cur.execute(mucg)
    data_base.commit()
    t2=cur.fetchall()
    mucgdf=pd.DataFrame(t2, columns=("States","Registered_Users"))

    mucg_bar1=px.bar(mucgdf, x="States", y="Registered_Users",title=f"{year} YEAR, STATES AND REGISTERED USERS",
                         color_discrete_sequence=px.colors.sequential.Cividis_r, height=650, width=1000)
    st.plotly_chart(mucg_bar1)

    return mucdf

# Map user district chart creation
def map_user_Y_disrict(df, state):
    mucyd=df[df["States"]==state]
    mucyd.reset_index(drop= True, inplace= True)

    mucydg=pd.DataFrame(mucyd.groupby("District")["Registered_Users"].sum())
    mucydg.reset_index(inplace=True)

    mucydg_bar1=px.pie(mucydg, values="Registered_Users", names="District", title=f"{mucyd["Years"].min()} YEAR, {state.upper()} STATE'S, DISTRICT AND REGISTERED USERS",
                         color_discrete_sequence=px.colors.sequential.amp_r, height=650, width=1000)
    st.plotly_chart(mucydg_bar1)

# Map user quater wise chart creation
def map_user_count_Q(df, quater):
    mucq=df[df["Quater"]==quater]
    mucq.reset_index(drop= True, inplace= True)

    mucqg=pd.DataFrame(mucq.groupby("States")["Registered_Users"].sum())
    mucqg.reset_index(inplace=True)

    mucqg_bar1= px.bar(mucqg, x="States", y="Registered_Users", title=f"{df['Years'].min()} YEAR {quater} QUARTER STATES AND REGISTERED USERS", 
                        color_discrete_sequence=px.colors.sequential.Emrld_r, height=650, width=1000)
    st.plotly_chart(mucqg_bar1)
    
    return mucq

# Map user quater and district wise chart creation
def map_user_Y_Q_disrict(df, state):
    mucyqd=df[df["States"]==state]
    mucyqd.reset_index(drop= True, inplace= True)

    mucyqdg=pd.DataFrame(mucyqd.groupby("District")["Registered_Users"].sum())
    mucyqdg.reset_index(inplace=True)

    mucyqdg_bar1=px.bar(mucyqdg, x="Registered_Users", y="District",orientation="h", title=f"{mucyqd["Quater"].min()} QUARTER, {state.upper()} STATE, DISTRICT AND REGISTERED USERS",
                         color_discrete_sequence=px.colors.sequential.Jet_r, height=650, width=1000)
    st.plotly_chart(mucyqdg_bar1)

# Top transaction year wise chart creation
def top_tran_count_amt(year):
    ttacy=f'''select * from top_transaction where Years = {year}'''
    cur.execute(ttacy)
    data_base.commit()
    t1=cur.fetchall()
    ttacydf=pd.DataFrame(t1, columns=("States", "Years", "Quater", "District", "Transaction_count", "Transaction_amount"))

    ttacyg=f'''select States, sum(Transaction_count) as Transaction_count, sum(Amount) as Transaction_amount from 
              top_transaction where Years = {year} group by States'''
    cur.execute(ttacyg)
    data_base.commit()
    t2=cur.fetchall()
    ttacygdf=pd.DataFrame(t2, columns=("States","Transaction_count","Transaction_amount"))
    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    states_name=[]
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()

    st.subheader(":blue[Yearly Analysis of Transaction Amount]")
    fig_amount= px.area(ttacygdf, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Agsunset, height=650, width=600)
    st.plotly_chart(fig_amount)

    fig_india_1= px.choropleth(ttacygdf, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_amount", color_continuous_scale="Cividis",
                            range_color=(ttacygdf["Transaction_amount"].min(),ttacygdf["Transaction_amount"].max()), hover_name="States", 
                            title=f"{year} TRANSACTION AMOUNT", 
                            fitbounds= "locations",
                            height=600, width=600)
    fig_india_1.update_geos(visible= False)
    st.plotly_chart(fig_india_1)
    st.subheader(":blue[Yearly Analysis of Transaction Count]")

    fig_count= px.area(ttacygdf, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Bluered_r, height=650, width=600)
    st.plotly_chart(fig_count)

    fig_india_2= px.choropleth(ttacygdf, geojson=data1, locations="States", featureidkey="properties.ST_NM", color="Transaction_count", 
                                color_continuous_scale="Inferno",
                            range_color=(ttacygdf["Transaction_count"].min(),ttacygdf["Transaction_count"].max()), hover_name="States", 
                            title=f"{year} TRANSACTION COUNT", 
                            fitbounds= "locations",
                            height=600, width=600)
    fig_india_2.update_geos(visible= False)
    st.plotly_chart(fig_india_2)
    return ttacydf

# Top user year wise chart creation
def top_user_count(year):
    tuc=f'''select * from top_users where Years = {year}'''
    cur.execute(tuc)
    data_base.commit()
    t1=cur.fetchall()
    tucdf=pd.DataFrame(t1, columns=("States", "Years", "Quater", "Pincodes", "Registered_Users"))
    tucg=f'''select States, Quater, sum(Registered_Users) as Registered_Users from top_users where Years = {year} group by States, Quater'''
    cur.execute(tucg)
    data_base.commit()
    t2=cur.fetchall()
    tucgdf=pd.DataFrame(t2, columns=("States", "Quater", "Registered_Users"))

    tucg_bar1=px.bar(tucgdf, x="States", y="Registered_Users",color="Quater",hover_name="States",title=f"{year} YEAR, REGISTERED USERS",
                         color_discrete_sequence=px.colors.sequential.Agsunset_r, height=800, width=1500)
    st.plotly_chart(tucg_bar1)

    return tucdf

# Top user quater and state wise chart creation
def top_user_Y_Q(df, state):
    tucs=df[df["States"]==state]
    tucs.reset_index(drop= True, inplace= True)

    tucg_bar2=px.bar(tucs, x="Quater", y="Registered_Users",color="Registered_Users",hover_name="Pincodes",title="QUARTER, STATES AND REGISTERED USERS",
                         color_continuous_scale=px.colors.sequential.Magenta, height=800, width=1000)
    st.plotly_chart(tucg_bar2)

def load_lottiefile(path):
    with open(path,'r') as f:
        return json.load(f)

#streamlit part

st.set_page_config(layout="wide")
st.title(":violet[PHONEPE DATA VISUALIZATION AND EXPLORATION]")

with st.sidebar:
    select=st.radio("Main menu",["Home","Aggregated Analysis","Map Analysis","Top Analysis","Queries"])

# Home page design
if select == "Home":
    phonepe_img1=Image.open("phonepe\phonepayimage1.jpg")
    st.image(phonepe_img1,width=800)

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.header(":violet[Simple, Fast and Secure]")
        st.markdown("")
        
        st.markdown("Pay bills, recharge, send money, buy gold, invest and shop at your favourite stores.")
        st.markdown("")
        st.markdown("_________________________________________________________")
        st.header(":violet[Pay whenever you like, wherever you like]")
        st.markdown("Choose from options like UPI, the PhonePe wallet or your Debit and Credit Card.")
        st.markdown("")
        st.markdown("_________________________________________________________")
        st.header(":violet[Find all your favourite apps on PhonePe Switch.]")
        st.markdown("Book flights, order food or buy groceries. Use all your favourite apps without downloading them")
    with col2:
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        phonepe_gif1=load_lottiefile("phonepe\phonepe_gif.json")
        st_lottie(phonepe_gif1,speed=1,reverse=False,loop=True,quality="medium",width=800)
    
    col3, col4, col5 = st.columns(3)
    with col3:
        # PhonepeInsurance=Image.open("PhonepeInsurance.png")
        st.image("phonepe\PhonepeInsurance.png")
        st.markdown('<a href="https://www.phonepe.com/insurance/" target="_blank">Insurance</a>', unsafe_allow_html=True)
    with col4:
        # PhonepeInvestments=Image.open("PhonepeInvestments.png")
        st.image("phonepe\PhonepeInvestments.png")
        st.markdown('<a href="https://www.phonepe.com/investments/" target="_blank">Investment</a>', unsafe_allow_html=True)
    with col5:
        # PhonepeLending=Image.open("PhonepeLending.png")
        st.image("phonepe\phonepeLending.png")
        st.markdown('<a href="https://www.phonepe.com/lending/" target="_blank">Loans</a>', unsafe_allow_html=True)
    
    col6, col7=st.columns(2)
    with col6:
        st.header(":green[For first time introducing PhonePe Pulse!!!]")
        st.video("phonepe\Introducing PhonePe Pulse.mp4")
    with col7:
        st.header(":blue[Introducing POS device!!!]")
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.video("phonepe\PhonePe -India's POS.mp4")
    st.subheader("New City, no need to worry about transactions.....")
    st.video("phonepe\When in a new city, trust PhonePe for all your transactions..mp4")
    
# Data analysis page design
elif select == "Aggregated Analysis":

    method = st.selectbox("Select any method",["Aggregated Transaction","Aggregated User"])

    if method == "Aggregated Transaction":


        col1, col2 = st.columns(2)
        with col1:
            years=st.slider("Select the year to analyse aggregated transaction", aggre_transaction["Years"].min(),aggre_transaction["Years"].max(),aggre_transaction["Years"].min())
        tac_Y=trans_amt_count_Y(years)
        with col2:
            quarters=st.slider("Select the quarter to analyse aggregated transaction", tac_Y["Quater"].min(),tac_Y["Quater"].max(),tac_Y["Quater"].min())
        agg_trans_q=trans_amt_count_Y_Q(tac_Y, quarters)

        col1, col2 = st.columns(2)
        with col1:
            states=st.selectbox("Select the state to analyse aggregated transaction", tac_Y["States"].unique())
        trans_type(agg_trans_q, states)
        
    elif method == "Aggregated User":
        col1, col2 = st.columns(2)
        with col1:
            agg_user_years=st.slider("Select the year to analyse aggregated user", aggre_users["Years"].min(),aggre_users["Years"].max(),aggre_users["Years"].min())
        agg_user_Y=agg_user_count(agg_user_years)
        
        with col2:
            agg_user_quarters=st.slider("Select the quarter to analyse aggregated user", agg_user_Y["Quater"].min(),agg_user_Y["Quater"].max(),agg_user_Y["Quater"].min())
        agg_user_Y_Q=agg_user_count_Q(agg_user_Y, agg_user_quarters)

        col1, col2 = st.columns(2)
        with col1:
            agg_user_s=st.selectbox("Select the state to analyse aggregated user", agg_user_Y_Q["States"].unique())
        agg_user_states(agg_user_Y_Q, agg_user_s)
    
elif select == "Map Analysis":
    method2 = st.selectbox("Select any method",["Map Transaction","Map User"])

    if method2 == "Map Transaction":
        col1, col2 = st.columns(2)
        with col1:
            mty=st.slider("Select the year to analyse map transaction", map_trans["Years"].min(),map_trans["Years"].max(),map_trans["Years"].min())
        map_trans_ac=map_trans_amt_count_Y(mty)

        with col2:
            mtq=st.slider("Select the quarter to analyse map transaction", map_trans_ac["Quater"].min(),map_trans_ac["Quater"].max(),map_trans_ac["Quater"].min())
        map_trans_q=trans_amt_count_Y_Q(map_trans_ac, mtq)

        st.subheader(":green[Yearly District analysis of Transaction Amount and Transaction Count]")
        col1, col2 = st.columns(2)
        with col1:
            mtys=st.selectbox("Select the state to analyse Y_map transaction", map_trans_ac["States"].unique())
        map_trans_district(map_trans_ac, mtys)
        st.subheader(":green[Quaterly District analysis of Transaction Amount and Transaction Count]")
        col1, col2 = st.columns(2)
        with col1: 
            mtqs=st.selectbox("Select the state to analyse Q_map transaction", map_trans_q["States"].unique())
        map_trans_district(map_trans_q, mtqs)


    elif method2 == "Map User":
        col1, col2 = st.columns(2)
        with col1:
            muy=st.slider("Select the year to analyse map users", map_users["Years"].min(),map_users["Years"].max(),map_users["Years"].min())
        map_user_Y=map_user_count(muy)
        with col2:
            muq=st.slider("Select the quarter to analyse map users", map_user_Y["Quater"].min(),map_user_Y["Quater"].max(),map_user_Y["Quater"].min())
        map_user_Y_Q=map_user_count_Q(map_user_Y, muq)
        col1, col2 = st.columns(2)
        with col1:
            muys=st.selectbox("Select the state to analyse Y_map users", map_user_Y["States"].unique())
        map_user_Y_disrict(map_user_Y, muys)
        
        with col2:
            muqs=st.selectbox("Select the state to analyse Q_map users", map_user_Y_Q["States"].unique())
        map_user_Y_Q_disrict(map_user_Y_Q, muqs)

elif select == "Top Analysis":
    method3 = st.selectbox("Select any method",["Top Transaction","Top User"])

    if method3 == "Top Transaction":
        col1, col2 = st.columns(2)
        with col1:
            tty=st.slider("Select the year to analyse top transaction", top_trans["Years"].min(),top_trans["Years"].max(),top_trans["Years"].min())
        top_trans_amt_count=top_tran_count_amt(tty)

        with col2:
            ttq=st.slider("Select the quarter to analyse top transaction ", top_trans_amt_count["Quater"].min(),top_trans_amt_count["Quater"].max(),
                            top_trans_amt_count["Quater"].min())
        top_trans_q=trans_amt_count_Y_Q(top_trans_amt_count, ttq)
        
        col1, col2 = st.columns(2)
        with col1:
            ttys=st.selectbox("Select the state to analyse Y_top transaction", top_trans_q["States"].unique())
        map_trans_district(top_trans_amt_count, ttys)
        

    elif method3 == "Top User":
        
        col1, col2 = st.columns(2)
        
        with col1:
            tuy=st.slider("Select the year to analyse top users", top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min())
        top_user_Y=top_user_count(tuy)

        col1, col2 = st.columns(2)
        with col1:
            tuys=st.selectbox("Select the state to analyse Y_top users", top_user_Y["States"].unique())
        top_user_Y_Q(top_user_Y, tuys)

# Queries page design
elif select == "Queries":
    
    data_base=pymysql.connect(host='localhost',
                    user='root',
                    password='1234',
                    database='phonepe_db',
                    port=3306)
    cur=data_base.cursor()
    question=st.selectbox("SELECT YOUR QUESTION",("1. Aggregated transaction amount and count",
                                                "2. Aggregated user Brands and Transaction count",
                                                "3. Top 10 Aggregated transaction in year 2022",
                                                "4. Map Transaction count and transaction amount of all years",
                                                "5. Tamil Nadu state's transaction amount with districts from year 2023 to 2024",
                                                "6. Map Registered users and Open Apps count",
                                                "7. Top transaction count and transaction amount",
                                                "8. Minimum amount of top transaction for each state in first quater of 2019",
                                                "9. Top users pincodes and registered users",
                                                "10. Maximum registered users in year 2023 of each state"))
    if question == "1. Aggregated transaction amount and count":
        query1='''select States,Transaction_name, Transaction_count,Transaction_amount from aggregated_transaction'''
        cur.execute(query1)
        data_base.commit()
        t1=cur.fetchall()
        df=pd.DataFrame(t1,columns=["States","Payment Type","No of transactions","Amount"])
        st.write(df)
    elif question == "2. Aggregated user Brands and Transaction count":
        query2='''select Brand_name, sum(Transaction_count) from aggregated_users group by Brand_name'''
        cur.execute(query2)
        data_base.commit()
        t2=cur.fetchall()
        df=pd.DataFrame(t2,columns=["Brands","No of Transactions",])
        st.write(df)
    elif question == "3. Top 10 Aggregated transaction in year 2022":
        query3='''select Transaction_name,Transaction_amount,Years from aggregated_transaction 
                where years=2022 order by Transaction_amount desc limit 10'''
        cur.execute(query3)
        data_base.commit()
        t3=cur.fetchall()
        df=pd.DataFrame(t3,columns=["Payment Type","Amount","Year",])
        st.write(df)
    elif question == "4. Map Transaction count and transaction amount of all years":
        query4='''select Years,sum(Transaction_count), sum(Amount) from map_transaction group by Years'''
        cur.execute(query4)
        data_base.commit()
        t4=cur.fetchall()
        df=pd.DataFrame(t4,columns=["Year","No of Transactions","Amount",])
        st.write(df)
    elif question == "5. Tamil Nadu state's transaction amount with districts from year 2023 to 2024":
        query5='''select District, Amount,Quater, Years from map_transaction where States = "Tamil Nadu" and Years between 2023 and 2024 order by district asc'''
        cur.execute(query5)
        data_base.commit()
        t5=cur.fetchall()
        df=pd.DataFrame(t5,columns=["District","Amount","Quater","Year"])
        st.write(df)
    elif question == "6. Map Registered users and Open Apps count":
        query6='''select District, Registered_Users, OpenApps_Count from map_user order by District asc'''
        cur.execute(query6)
        data_base.commit()
        t6=cur.fetchall()
        df=pd.DataFrame(t6,columns=["District","No of Users","OpenApps Count"])
        st.write(df)
    elif question == "7. Top transaction count and transaction amount":
        query7='''select States, sum(Transaction_Count), sum(Amount) from top_transaction group by States'''
        cur.execute(query7)
        data_base.commit()
        t7=cur.fetchall()
        df=pd.DataFrame(t7,columns=["States","No of Transactions","Amount"])
        st.write(df)
    elif question == "8. Minimum amount of top transaction for each state in first quater of 2019":
        query8='''select States, min(Amount), Quater, Years from top_transaction where quater = 1 and Years = 2019 group by States'''
        cur.execute(query8)
        data_base.commit()
        t8=cur.fetchall()
        df=pd.DataFrame(t8,columns=["States","Amount","Quater","Year"])
        st.write(df)
    elif question == "9. Top users pincodes and registered users":
        query9='''select States,Pincodes, Registered_Users from top_users'''
        cur.execute(query9)
        data_base.commit()
        t9=cur.fetchall()
        df=pd.DataFrame(t9,columns=["States","Pincode","No of Users"])
        st.write(df)
    elif question == "10. Maximum registered users in year 2023 of each state":
        query10='''select States,max(Registered_Users), Years from top_users where Years = 2023 group by States'''
        cur.execute(query10)
        data_base.commit()
        t10=cur.fetchall()
        df=pd.DataFrame(t10,columns=["States","No of Users","Year"])
        st.write(df)
