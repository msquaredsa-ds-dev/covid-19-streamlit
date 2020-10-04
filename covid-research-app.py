#import packges to be used 
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import date

alt.data_transformers.disable_max_rows()

#setting variables which will contain geojson for county boundaries/mapping and COVID-19 case data from Texas Department of Health and Human Services
counties = alt.topo_feature('https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/TX-48-texas-counties.json','cb_2015_texas_county_20m')

url = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/compiled-covid-cases.csv'
source = pd.read_csv(url,parse_dates=['date'])

min_date = source['date'].min()
max_date = source['date'].max()

date_slider = st.sidebar.slider('Date',min_value=min_date.date(),max_value=max_date.date())
date_value = date_slider.strftime('%B %d, %Y')


selection = alt.selection_single(on='mouseover', empty='none')

#chloropleth map for all of Texas
tx_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=700,
    height=500
).add_selection(
    selection
)

st.title('COVID-19 Research')
st.title('Texas')

st.altair_chart(tx_chart,use_container_width=True)

#chloropleth map for San Antonio (Bexar) and surrounding counties
st.title('San Antonio')

sa_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=700,
    height=500
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Bexar', 'Medina', 'Bandera','Kendall','Comal','Guadalupe','Wilson','Atascosa'])
)

st.altair_chart(sa_chart,use_container_width=True)

#chloropleth map for Austin (Travis) and surrounding counties
st.title('Austin')

aus_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=700,
    height=500
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Travis', 'Hays', 'Blanco','Burnet','Williamson','Lee','Bastrop','Caldwell'])
)

st.altair_chart(aus_chart,use_container_width=True)

#chloropleth map for Houston (Harris) and surrounding counties
st.title('Houston')

hou_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=700,
    height=500
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Waller', 'Montgomery', 'Harris','Liberty','Chambers','Galveston','Brazoria','Fort Bend'])
)

st.altair_chart(hou_chart,use_container_width=True)

#chloropleth map for Dallas (Dallas) and surrounding counties
st.title('Dallas')

dal_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=700,
    height=500
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Dallas', 'Tarrant', 'Denton','Collin','Rockwall','Kaufman','Ellis','Johnson'])
)

st.altair_chart(dal_chart,use_container_width=True)

#Interventions based on date - To Be Developed
if date_slider == date(2020,3,4):
    st.sidebar.write('Intervention measure 1, 2, and 3')
elif date_slider == date(2020,5,7):
    st.sidebar.write('Intervention measure 4, 5, and 6')
elif date_slider == date(2020,7,9):
    st.sidebar.write('Intervention measure 7, 8, and 9')
