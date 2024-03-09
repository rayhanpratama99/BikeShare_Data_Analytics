
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Create the web
df = pd.read_csv('Cleaned Bike Sharing Hour.csv')
df['date'] = pd.to_datetime(df['date'])

#Define a function of BikeShare Usage
def create_monthly_users_df(df):
    monthly_users_df = df.resample(rule='ME', on='date').agg({
        'registered_user': 'sum',
        'casual_user': 'sum',
        'total_users': 'sum'
    })
    
    monthly_users_df.index = monthly_users_df.index.strftime('%b, %y')
    monthly_users_df  = monthly_users_df.reset_index()
    monthly_users_df.rename(columns={
        'registered_user': 'Registered Users', 
        'casual_user': 'Casual Users', 
        'total_users': 'Total Users'
    }, inplace=True)
    
    monthly_users_df = pd.melt(monthly_users_df, id_vars='date',
                                 value_vars=['Total Users', 'Registered Users', 'Casual Users'], 
                                 var_name='Type of Users', value_name='TotalUsers')
    
    return monthly_users_df

def create_seasonly_users_df(df):
    seasonly_users_df = df.groupby('season').agg({
        'registered_user': 'sum',
        'casual_user': 'sum',
        'total_users': 'sum'
    })

    seasonly_users_df = seasonly_users_df.reset_index()
    seasonly_users_df.rename(columns={
        'registered_user': 'Registered Users', 
        'casual_user': 'Casual Users', 
        'total_users': 'Total Users'
    }, inplace=True)

    seasonly_users_df = pd.melt(seasonly_users_df, id_vars=['season'],
                                  value_vars=['Registered Users', 'Casual Users'],
                                  var_name= 'Type of Users', value_name='TotalUsers')
    seasonly_users_df['season'] = pd.Categorical(seasonly_users_df['season'], categories=[
        'Winter', 'Springer', 'Summer', 'Fall'], ordered=True)
    
    seasonly_users_df = seasonly_users_df.sort_values('season')
    return seasonly_users_df

def create_weekday_users_df(df):
    weekday_users_df = df.groupby('weekday').agg({
        'registered_user': 'sum',
        'casual_user': 'sum',
        'total_users': 'sum' 
    })

    weekday_users_df = weekday_users_df.reset_index()
    weekday_users_df.rename(columns={
        'registered_user': 'Registered Users', 
        'casual_user': 'Casual Users', 
        'total_users': 'Total Users'  
    }, inplace=True)

    weekday_users_df = pd.melt(weekday_users_df, id_vars=['weekday'],
                                  value_vars=['Registered Users', 'Casual Users'],
                                  var_name= 'Type of Users', value_name='TotalUsers')
    weekday_users_df['weekday'] = pd.Categorical(weekday_users_df['weekday'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
    
    weekday_users_df = weekday_users_df.sort_values('weekday')
    return weekday_users_df

def create_weather_users_df(df):
    weather_users_df = df.groupby('weather_cond').agg({
        'registered_user': 'sum',
        'casual_user': 'sum',
        'total_users': 'sum'
    })

    weather_users_df = weather_users_df.reset_index()
    weather_users_df.rename(columns={
        'registered_user': 'Registered Users',
        'casual_user': 'Casual Users',
        'total_users': 'Total Users'
    }, inplace=True)

    weather_users_df = pd.melt(weather_users_df, id_vars=['weather_cond'],
                               value_vars=['Registered Users', 'Casual Users'],
                               var_name='Type of Users', value_name='TotalUsers')
    weather_users_df['weather_cond'] = pd.Categorical(weather_users_df['weather_cond'], categories=[
        'Clear/Partly Cloudy', 'Misty/Cloudy', 'Light Snow/Rain', ' Heavy Rain/Thunderstorm'
    ], ordered=True)

    weather_users_df = weather_users_df.sort_values('weather_cond')
    return weather_users_df


# Make the date filter for the Dashboard
min_date = df['date'].min()
max_date = df['date'].max()

# Make the SideBar in the Dashboard
with st.sidebar:
    st.image('https://raw.githubusercontent.com/rayhanpratama99/BikeShare_Data_Analytics/main/dashboard/cb.jpg')
    st.sidebar.header('Date:')
    # Make the input start and end to choose which date data will show in the dashboard
    start_date, end_date = st.date_input(
        label= 'Choose Date', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

st.sidebar.header("Visit my Profile:")

st.sidebar.markdown("Rayhan Arlistya Pratama")

col1, col2 = st.sidebar.columns(2)

with col1:
    st.markdown("[![LinkedIn](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](https://www.linkedin.com/in/rayhanarlistyapratama/)")
with col2:
    st.markdown("[![Github](https://img.icons8.com/glyph-neue/64/FFFFFF/github.png)](https://github.com/rayhanpratama99)")

# Connecting the Date filter with DF that will be use
main_df = df[
    (df['date'] >= str(start_date)) &
    (df['date'] <= str(end_date)) 
]

#Calling the function
monthly_df = create_monthly_users_df(main_df)
seasonly_df = create_seasonly_users_df(main_df)
weekday_df = create_weekday_users_df(main_df)
weather_df = create_weather_users_df(main_df)

#Visualizing the Data to Dashboard
st.header("Bike Share Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    TotalUsers = main_df['total_users'].sum()
    st.metric("Total Users", value=TotalUsers)

with col2:
    TotalCasual = main_df['casual_user'].sum()
    st.metric('Casual users', value=TotalCasual)

with col3:
    TotalRegistered = main_df['registered_user'].sum()
    st.metric('Registered Users', value=TotalRegistered)

st.markdown("---")

# Create Line Plot for Bike Share Monthly Users
fig, ax =plt.subplots(figsize=(16,6))
sns.set_style("dark")
sns.lineplot( x='date', y='TotalUsers', data=monthly_df, hue='Type of Users', marker='o',
             palette=['#e60049', '#0bb4ff', '#edbf33'])

ax.set_xlabel("Monthly", size = 17)
ax.set_ylabel('Total Users', size = 17)
ax.set_title("Bike Share Based on Monthly Users", size = 25)
plt.xticks(size = 13,rotation=90)
plt.yticks([0, 50000, 100000, 150000, 200000], [0, '50k', '100k', '150k', '200k'], size=13)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper left')

st.pyplot(fig, use_container_width=True)
st.markdown('')

# Create Bar Plot for Bike Share Based on Season
fig1, ax = plt.subplots(figsize=(16,6))
sns.set_style("dark")
sns.barplot( x='season', y='TotalUsers', data=seasonly_df, hue='Type of Users', 
            palette=['#0bb4ff', '#edbf33'], ax=ax)

for p in ax.patches:
    if p.get_height() != 0:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 10), 
                    textcoords = 'offset points',
                    fontsize=12
                   )
    
plt.yticks([0, 200000, 400000, 600000, 800000, 1000000], ['0', '200k','400k', '600k', '800k', '1000k'], size=13)
plt.ylabel('Total Users', size= 17)
plt.xlabel('Season', size = 17)
plt.xticks(size=16)
plt.grid(True, linestyle='--', alpha=0.5)
plt.title('Bike Share Users Based on Season', size=25)

st.pyplot(fig1, use_container_width=True)
st.markdown("")

#Create Bar Plot for Bike Share Based on Weekday
fig2, ax = plt.subplots(figsize=(16,6))
sns.set_style("dark")
sns.barplot(x='weekday', y='TotalUsers', data=weekday_df, hue='Type of Users',
            palette=['#0bb4ff', '#edbf33'], ax=ax)

for p in ax.patches:
    if p.get_height() != 0:
      ax.annotate(format(p.get_height(), '.0f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()), 
                  ha='center', va='center', 
                  xytext=(0, 10), 
                  textcoords='offset points',
                  fontsize=12
               )

plt.yticks([0, 100000, 200000, 300000, 400000], ['0', '100k', '200k', '300k', '400k'], size=13)
plt.ylabel('Total Users', size= 17)
plt.xlabel('Weekday', size = 17)
plt.xticks(size=15)
plt.grid(True, linestyle='--', alpha=0.5)
plt.title('Bike Share Users Based on Weekday', size=25)

st.pyplot(fig2, use_container_width=True)
st.markdown("")

#Create Bar Plot for Bike Share Based on Weather
fig3, ax = plt.subplots(figsize=(16,6))
sns.set_style("dark")
sns.barplot(x='weather_cond', y='TotalUsers', data=weather_df, hue='Type of Users',
            palette=['#0bb4ff', '#edbf33'], ax=ax)

for p in ax.patches:
    if p.get_height() != 0:
      ax.annotate(format(p.get_height(), '.0f'), 
                  (p.get_x() + p.get_width() / 2., p.get_height()), 
                  ha='center', va='center', 
                  xytext=(0, 10), 
                  textcoords='offset points',
                  fontsize=12
               )

plt.yticks([0, 500000, 1000000, 1500000, 2000000], ['0', '0.5M', '1M', '1.5M', '2M'], size=13)
plt.ylabel('Total Users', size= 17)
plt.xlabel('Weather', size = 17)
plt.xticks(size=15)
plt.grid(True, linestyle='--', alpha=0.5)
plt.title('Bike Share Users Based on Weather', size=25)

st.pyplot(fig3, use_container_width=True)
st.markdown("")

st.caption('Copyright (c), created by Rayhan Arlistya Pratama')
