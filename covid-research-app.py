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

data_view = st.sidebar.radio('Data View:',('Map','Line'))

selection = alt.selection_single(on='mouseover', empty='none')

#chloropleth map for all of Texas
tx_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=800,
    height=600
).add_selection(
    selection
)

st.title('COVID-19 Research')
st.title('Texas')

st.altair_chart(tx_chart,use_container_width=False)


#SAN ANTONIO
st.title('Bexar County (San Antonio)')

#create chloropleth map for San Antonio and surronding counties
sa_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=800,
    height=600
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Bexar', 'Medina', 'Bandera','Kendall','Comal','Guadalupe','Wilson','Atascosa'])
)

#create line chart for San Antonio and surrounding coounties
sa_line = alt.Chart(source).mark_line().encode(
    x='date',
    y='rate:Q',
    color='county',
    tooltip=['date','county','cases','population','rate']
).transform_filter(
    alt.FieldOneOfPredicate(field='county', oneOf=['Bexar', 'Medina', 'Bandera','Kendall','Comal','Guadalupe','Wilson','Atascosa'])
).properties(
    width=900,
    height=600
)


if data_view == 'Map':
    st.altair_chart(sa_chart,use_container_width=False)
elif data_view == 'Line':
    st.altair_chart(sa_line,use_container_width=False)


#AUSTIN
st.title('Travis County (Austin)')

#create chloropleth map for Austin and surrounding counties
aus_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=800,
    height=600
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Travis', 'Hays', 'Blanco','Burnet','Williamson','Lee','Bastrop','Caldwell'])
)

#create line chart for Austin and surrounding counties
aus_line = alt.Chart(source).mark_line().encode(
    x='date',
    y='rate:Q',
    color='county',
    tooltip=['date','county','cases','population','rate']
).transform_filter(
    alt.FieldOneOfPredicate(field='county', oneOf=['Travis', 'Hays', 'Blanco','Burnet','Williamson','Lee','Bastrop','Caldwell'])
).properties(
    width=900,
    height=600
)

if data_view == 'Map':
    st.altair_chart(aus_chart,use_container_width=False)
elif data_view == 'Line':
    st.altair_chart(aus_line,use_container_width=False)


#HOUSTON
st.title('Harris County (Houston)')

#create chloropleth map for Houston and surrounding counties
hou_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=800,
    height=600
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Waller', 'Montgomery', 'Harris','Liberty','Chambers','Galveston','Brazoria','Fort Bend'])
)

#create line chart for Houston and surrounding counties
hou_line = alt.Chart(source).mark_line().encode(
    x='date',
    y='rate:Q',
    color='county',
    tooltip=['date','county','cases','population','rate']
).transform_filter(
    alt.FieldOneOfPredicate(field='county', oneOf=['Waller', 'Montgomery', 'Harris','Liberty','Chambers','Galveston','Brazoria','Fort Bend'])
).properties(
    width=900,
    height=600
)

if data_view == 'Map':
    st.altair_chart(hou_chart,use_container_width=False)
elif data_view == 'Line':
    st.altair_chart(hou_line,use_container_width=False)


#DALLAS
st.title('Dallas County (Dallas)')

#create chloropleth map for Dallas and surrounding counties
dal_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'rate:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
).properties(
    width=800,
    height=600
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Dallas', 'Tarrant', 'Denton','Collin','Rockwall','Kaufman','Ellis','Johnson'])
)

#create line chart for Dallas and surrounding counties
dal_line = alt.Chart(source).mark_line().encode(
    x='date',
    y='rate:Q',
    color='county',
    tooltip=['date','county','cases','population','rate']
).transform_filter(
    alt.FieldOneOfPredicate(field='county', oneOf=['Dallas', 'Tarrant', 'Denton','Collin','Rockwall','Kaufman','Ellis','Johnson'])
).properties(
    width=900,
    height=600
)

if data_view == 'Map':
    st.altair_chart(dal_chart,use_container_width=False)
elif data_view == 'Line':
    st.altair_chart(dal_line,use_container_width=False)


### IN DEVELOPMENT >>>

#Interventions based on date - To Be Developed
#if date_slider == date(2020,3,4):
#    st.sidebar.write('Intervention measure 1, 2, and 3')
#elif date_slider == date(2020,5,7):
#    st.sidebar.write('Intervention measure 4, 5, and 6')
#elif date_slider == date(2020,7,9):
#    st.sidebar.write('Intervention measure 7, 8, and 9')

#The following code will enable automation through the progression of days and update the map accordingly. This will be added in Phase 2, with a toggle switch on the sidebar to enable users to turn it "on" or "off"

#st.write('Test')

#from datetime import timedelta, date
#import time

#def daterange(date1, date2):
#    for n in range(int ((date2 - date1).days)+1):
#        yield date1 + timedelta(n)

#start_dt = source['date'].min()
#end_dt = source['date'].max()

#chart = st.empty()
#i = 0
#progress_bar = st.sidebar.progress(i)


#for dt in daterange(start_dt, end_dt):

#    date_value = dt.strftime('%B %d, %Y')

#    tx_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
#        color=alt.condition(selection, alt.value('black'), 'rate:Q'),
#        tooltip=['[properties][NAME]:N','cases:Q','population:Q','rate:Q']
#    ).transform_lookup(
#        lookup='[properties][NAME]',
#        from_=alt.LookupData(source[source['date'] == date_value],'county',['cases','population','rate'])
#    ).properties(
#        width=700,
#        height=500
#    ).add_selection(
#        selection
#    )

#    chart.altair_chart(tx_chart,use_container_width=True)
#    time.sleep(0.5)