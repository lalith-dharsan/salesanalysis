pip install plotly

import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import sqlite3
import mysql.connector
import pyodbc
import numpy as np
import math



conn = pyodbc.connect('DRIVER={SQL Server};'
                      'SERVER=LAPTOP-1C13RR2T\SQLEXPRESS;'
                      'DATABASE=Sales_Analysis_Data;'
                      'Trusted_Connection=yes;')


# Create a cursor from the connection
cursor = conn.cursor()

# Execute a query to retrieve data from the server
cursor.execute('SELECT * FROM dbo.Reports')

# Fetch all rows from the executed query
rows = [list(row) for row in cursor.fetchall()]
columns=[column[0] for column in cursor.description]
df_participants = pd.DataFrame(rows,columns = columns)

cursor.close()
conn.close()
Refund = df_participants['Refunds'].tolist()
Dis = df_participants['Discounts'].tolist()
Tax = df_participants['Taxes'].tolist()
Maintenance = df_participants['MaintenanceCosts'].tolist()
#date conversion
df_participants['ReportDate'] =  pd.to_datetime(df_participants['ReportDate'])
date = df_participants['ReportDate']
age_selection = st.slider('ReportDate:',
                        min_value= min(Refund),
                        max_value= max(Refund),
                        value=(min(Refund),max(Refund)))




mask = (df_participants['Refunds'] >= age_selection[0]) & (df_participants['Refunds'] <= age_selection[1])
df_filtered = df_participants[mask]

pie_chart = px.pie(df_filtered,
                    title='Total No. of Participants',
                    values='Refunds',
                    names='ReportId')

# Display the pie chart
st.plotly_chart(pie_chart)
#department = cursor['Department'].unique().tolist()




report = [sum(Dis),sum(Refund),sum(Tax),sum(Maintenance)]

ran = np.arange(0, sum(Refund), sum(Refund)/4)
# Create a list of bar charts
chart_data = pd.DataFrame(
   {       
       "Reports":report,
       "col2":ran
   }   
)

st.bar_chart(chart_data, x="Reports", y="col2")

# code to display table
if len(columns) > 0:
        # Convert data to DataFrame
        #df_ssms = pd.DataFrame(rows, columns=columns)
        
        # Display DataFrame
        st.dataframe(df_filtered)
else:
        st.warning("No data returned from the query.")
