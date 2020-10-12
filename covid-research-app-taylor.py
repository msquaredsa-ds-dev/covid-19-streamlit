#import packges to be used 
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import date, timedelta

alt.data_transformers.disable_max_rows()

#setting variables which will contain geojson for county boundaries/mapping and COVID-19 case data from Texas Department of Health and Human Services
counties = alt.topo_feature('https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/TX-48-texas-counties.json','cb_2015_texas_county_20m')

#import weekly case data
url_weekly_cases = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/cases-weekly-processed.csv'
weekly_cases = pd.read_csv(url_weekly_cases,parse_dates=['date'])

#import cumulative case data
url_cumulative_cases = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/cases-cumulative-processed.csv'
cumulative_cases = pd.read_csv(url_cumulative_cases,parse_dates=['date'])

#import weekly death data
url_weekly_deaths = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/deaths-weekly-processed.csv'
weekly_deaths = pd.read_csv(url_weekly_deaths,parse_dates=['date'])

#import cumulative death data
url_cumulative_deaths = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/deaths-cumulative-processed.csv'
cumulative_deaths = pd.read_csv(url_cumulative_deaths,parse_dates=['date'])

metric = st.sidebar.radio('Measure:',('Incidence','Mortality'))

#Create date slider widget
if metric == 'Incidence':
    min_date = weekly_cases['date'].min()
    max_date = weekly_cases['date'].max()

    date_slider = st.sidebar.slider('Date',min_value=min_date.date(),max_value=max_date.date(),step=timedelta(days=7))
    date_value = date_slider.strftime('%B %d, %Y')
elif metric == 'Mortality':
    min_date = weekly_deaths['date'].min()
    max_date = weekly_deaths['date'].max()

    date_slider = st.sidebar.slider('Date',min_value=min_date.date(),max_value=max_date.date(),step=timedelta(days=7))
    date_value = date_slider.strftime('%B %d, %Y')

selection = alt.selection_single(on='mouseover', empty='none')

#SAN ANTONIO
st.title('Bexar County and Surrounding Counties')
st.subheader('(Based on data from the State Dept. of Health and Human Services)')
st.write('')
st.write('')

#create chloropleth map for San Antonio and surronding counties - Incidence
incidence_sa_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'cases-per-100K:Q'),
    tooltip=['[properties][NAME]:N','cases:Q','population:Q','cases-per-100K:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(cumulative_cases[cumulative_cases['date'] == date_value],'county',['cases','population','cases-per-100K'])
).properties(
    width=800,
    height=600
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Bexar', 'Medina', 'Bandera','Kendall','Comal','Guadalupe','Wilson','Atascosa'])
)

#create chloropleth map for San Antonio and surronding counties - Mortality
mortality_sa_chart = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
    color=alt.condition(selection, alt.value('black'), 'deaths-per-100K:Q'),
    tooltip=['[properties][NAME]:N','deaths:Q','population:Q','deaths-per-100K:Q']
).transform_lookup(
    lookup='[properties][NAME]',
    from_=alt.LookupData(cumulative_deaths[cumulative_deaths['date'] == date_value],'county',['deaths','population','deaths-per-100K'])
).properties(
    width=800,
    height=600
).add_selection(
    selection
).transform_filter(
    alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=['Bexar', 'Medina', 'Bandera','Kendall','Comal','Guadalupe','Wilson','Atascosa'])
)

if metric == 'Incidence':
    st.write('## Cumulative Cases per 100K People Over Time')
    st.write('')
    st.write('')
    st.altair_chart(incidence_sa_chart,use_container_width=False)
elif metric == 'Mortality':
    st.write('## Cumulative Deaths per 100K People Over Time')
    st.write('')
    st.write('')
    st.altair_chart(mortality_sa_chart,use_container_width=False)

st.write('')
st.write('')
st.write('')
st.write('')



if metric == 'Incidence':
    st.write('## Weekly Incidence per 100K')
    st.write('')
    st.write('')

    #create county multi-select
    county_selection = st.multiselect('Which counties do you want to study?',['Bexar', 'Medina', 'Bandera', 'Kendall','Comal','Guadalupe','Wilson','Atascosa'],['Bexar', 'Medina', 'Bandera', 'Kendall','Comal','Guadalupe','Wilson','Atascosa'])
    st.write('')

    #create line chart for San Antonio and surrounding counties - Incidence
    incidence_sa_line = alt.Chart(weekly_cases).mark_line().encode(
        x=alt.X('date',axis=alt.Axis(title='Week Starting')),
        y=alt.Y('cases-per-100K:Q',axis=alt.Axis(title='Cases per 100K')),
        color='county',
        tooltip=['date','county','cases','population','cases-per-100K']
    ).transform_filter(
        alt.FieldOneOfPredicate(field='county', oneOf=county_selection)
    ).properties(
        width=900,
        height=600
    )

    #render chart
    st.altair_chart(incidence_sa_line,use_container_width=False)

elif metric == 'Mortality':
    st.write('## Weekly Mortality per 100K')
    st.write('')
    st.write('')

    #create county multi-select
    county_selection = st.multiselect('Which counties do you want to study?',['Bexar', 'Medina', 'Bandera', 'Kendall','Comal','Guadalupe','Wilson','Atascosa'],['Bexar', 'Medina', 'Bandera', 'Kendall','Comal','Guadalupe','Wilson','Atascosa'])
    st.write('')

    #create line chart for San Antonio and surrounding counties - Mortality
    mortality_sa_line = alt.Chart(weekly_deaths).mark_line().encode(
        x=alt.X('date',axis=alt.Axis(title='Week Starting')),
        y=alt.Y('deaths-per-100K:Q',axis=alt.Axis(title='Deaths per 100K')),
        color='county',
        tooltip=['date','county','deaths','population','deaths-per-100K']
    ).transform_filter(
        alt.FieldOneOfPredicate(field='county', oneOf=county_selection)
    ).properties(
        width=900,
        height=600
    )

    #render chart
    st.altair_chart(mortality_sa_line,use_container_width=False)

st.write('')
st.write('')
st.title('San Antonio')
st.subheader('(Based on data from San Antonio Metropolitan Health)')
st.write('')
st.write('')
st.write('## Weekly Incidence and Mortality - San Antonio')
st.write('')
st.write('')


#create
url_daily_cases_deaths_sa = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/SAMHD_Daily_Surveillance_Data_Public.csv'
daily_sa_df = pd.read_csv(url_daily_cases_deaths_sa,parse_dates=['reporting_date'])
sa_cases_deaths_df = daily_sa_df.resample('W-Mon',label='right',closed='right',on='reporting_date').sum().reset_index()[['reporting_date','total_case_daily_change','deaths_daily_change']]

base = alt.Chart(sa_cases_deaths_df).encode(
    alt.X('reporting_date',axis=alt.Axis(title='Reporting Date'))
)

sa_deaths_line = base.mark_line(color='#FF2D00').encode(
    y=alt.Y('deaths_daily_change', axis=alt.Axis(title='Weekly Deaths',titleColor='#FF2D00'))
).properties(
    height=600,
    width=900
)

sa_cases_line = base.mark_line(color='#000000').encode(
    y=alt.Y('total_case_daily_change', axis=alt.Axis(title='Weekly Cases',titleColor='#000000'))
).properties(
    height=600,
    width=900
)

cases_deaths_sa_layer_chart = alt.layer(sa_cases_line,sa_deaths_line).resolve_scale(y='independent').encode(tooltip=['reporting_date','total_case_daily_change','deaths_daily_change'])

st.altair_chart(cases_deaths_sa_layer_chart,use_container_width=False)
