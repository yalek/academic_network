#Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)] on win32
#Type "help", "copyright", "credits" or "license()" for more information.
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Academic Networks")
st.subheader('By Dr Kevin Chiteri and Dr Koushik Nagasubramanian')

# Create a connection object.
#conn = st.connection("gsheets", type=GSheetsConnection)

#df = conn.read()

# Print results.
#for row in df.itertuples():
 #   st.write(f"{row.name} has a :{row.pet}:")
