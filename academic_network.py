#Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)] on win32
#Type "help", "copyright", "credits" or "license()" for more information.
import streamlit as st
from streamlit_gsheets import GSheetsConnection

import janitor

from pyvis import network as net
import networkx as nx
import streamlit.components.v1 as components

col1, col2, col3 = st.columns(3)
with col2:
    st.title("Academic Networks")
    st.write('By Dr. Kevin Chiteri and Dr. Koushik Nagasubramanian')

st.subheader('Acknowledgement', divider = 'rainbow')
col1, col2, col3 = st.columns(3)

with col1:
    st.link_button("Jeanna Schoonmaker", 'https://jeanna-schoonmaker.medium.com/how-i-built-an-app-for-creating-interactive-linkedin-network-graphs-451140a498cf')

with col2:
    st.link_button("Benedict Neo", 'https://medium.com/bitgrit-data-science-publication/visualize-your-linkedin-network-with-python-59a213786c4')

with col3:
    st.link_button("Bradley Schoeneweis", 'https://bradley-schoeneweis.medium.com/visualizing-your-linkedin-connections-with-python-pandas-networkx-pyvis-40bf846a532')


st.subheader('Data tables', divider = 'rainbow')
# Create a connection object.

#This is for trial. Try to make  away people can input the data without seeing the whole table

url = "https://docs.google.com/spreadsheets/d/1f6mfsbANT3z7ATbFUokvW0oLfnTuLeptZH_UVq8I4uo/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url)

st.dataframe(data) #comment to prevent showing the data

#data cleaning
#Need to make sure the data that people enter is consistent
data = (
    data
    .clean_names() # remove spacing and capitalization
    .dropna(subset=['professor', 'student']) # drop missing values

  )
st.dataframe(data)
df = data

#dataframe size (row, col)
st.write(df.shape)

#Exploratory analysis
df = df['professor'].value_counts().reset_index()
df.columns = ['professor', 'count']
df = df.sort_values(by="count", ascending=False)

st.dataframe(df)



#Creating network connections
#https://medium.com/bitgrit-data-science-publication/visualize-your-linkedin-network-with-python-59a213786c4

# initialize graph
g = nx.Graph()
g.add_node('root') # intialize yourself as central

# use iterrows tp iterate through the data frame
for _, row in df.iterrows():

  # store company name and count
  professor = row['professor']
  count = row['count']

  title = f"<b>{professor}</b> – {count}"
  #title = f"<b>{professor}</b>"
  institution = set([x for x in data[professor == data['professor']]['training_institution']])
  institution = ''.join('<li>{}</li>'.format(x) for x in institution)

  institution_list = f"<ul>{institution}</ul>"
  hover_info = title + institution_list

  g.add_node(professor, size=count*2, title=hover_info, color='#3449eb')
  g.add_edge('root', professor, color='grey')

# generate the graph
nt = net.Network(height='700px', width='700px', bgcolor="black", font_color='white')
nt.from_nx(g)
nt.hrepulsion() #comment out and see what happens

# more customization https://tinyurl.com/yf5lvvdm
#nt.show('company_graph.html')

#display(HTML('company_graph.html'))

#str_to_option(graph_option) # user option for either a spoked or packed graph
nt.save_graph(f'academic_graph.html')

st.subheader('Academic Network Graph', divider = 'rainbow')

HtmlFile = open(f'academic_graph.html','r',encoding='utf-8')

# Load HTML into HTML component for display on Streamlit
components.html(HtmlFile.read(), height=800, width=1000)


st.subheader('Contribute', divider = 'rainbow')
st.write('Add any similar connections you are aware of. Click below')
st.link_button("Populate", 'https://docs.google.com/spreadsheets/d/1f6mfsbANT3z7ATbFUokvW0oLfnTuLeptZH_UVq8I4uo/edit?usp=sharing')







