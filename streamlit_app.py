import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

def dateAge(x):
#function for generating future bucket grouping
a = (x - np.datetime64("today","D")) / np.timedelta64(1,"D")
if a <= 0:
y = "0 or Less"
elif a >0 and a <= 5:
y = "5 days"
elif a > 5 and a <= 14:
y = "6 to 14 days"
elif a > 14 and a <= 30:
y = "15 to 30 days"
else:
y = "over 30 days"
return y

#built as a function for cache use with StreamLit later
def getData():
x = pd.read_csv(r'C:\Users\aryan.sinanan\Desktop\Python\raw_data\demand.csv')
return x

#assign data to df variable
df = getData()

#Set Org level max and role title or partial name you are looking for
org_level = ["6","7","8"]
role_title = "Data"

#Datatype convert to date from dd-MMM-yy
df["Resource Start Date"] = pd.to_datetime(df["Resource Start Date"],format="%d-%b-%y")
df["Resource End Date"] = pd.to_datetime(df["Resource End Date"],format="%d-%b-%y")

#Define Future Bucket
df["Date Bucket"] = df["Resource Start Date"].apply(dateAge)

#clean up Location names
df.loc[df["Role Work Location"] == "melbourne", "Role Work Location"] = "Melbourne"
df.loc[df["Role Work Location"] == "canberra", "Role Work Location"] = "Canberra"

#rename columns
df.rename(columns={
"Project Has Security/ Nationality Restriction":"Clearance Required",
"Resource Start Date":"Start Date",
"Resource End Date":"End Date",
"Role ID":"ID",
"Role Title":"Title",
"Role Description":"Description",
"Role Talent Segment":"Talent Segment",
"Role Career Level From":"Career Level From",
"Role Career Level To":"Career Level To",
"Role Work Location":"Work Location",
"Role Location Type":"Location Type",
"Role Fulfillment Entity L3":"Fulfillment Entity L3"
}, inplace = True)

#drop the unncessary columns
df_sub = df.loc[:,("ID","Clearance Required","Start Date","End Date","Date Bucket","Title","Description","Talent Segment","Assigned Role","Career Level To","Work Location","Location Type","Role Primary Contact","Role Primary Contact\n(Email ID)")]

#filter the dataframe using ord_level and role_title
df_filter = df_sub[(df_sub["Assigned Role"].str.contains( role_title ,case=False,na=False)) & (df_sub["Career Level To"].isin(org_level))]

#title
st.markdown("# Roles Dashbaord")

#defining side bar
st.sidebar.header("Filters:")

#placing filters in the sidebar using unique values.
location = st.sidebar.multiselect(
"Select Location:",
options=df_filter["Work Location"].unique(),
default=df_filter["Work Location"].unique()
)

#placing filters in the sidebar using unique values.
work_type = st.sidebar.multiselect(
"Select Work Type:",
options=df_filter["Location Type"].unique(),
default=df_filter["Location Type"].unique()
)
