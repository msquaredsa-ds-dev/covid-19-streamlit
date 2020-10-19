### IMPORT PACKAGES TO BE USED ### 
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from datetime import date, timedelta

alt.data_transformers.disable_max_rows()

#setting variables which will contain geojson for county boundaries/mapping and COVID-19 case data from Texas Department of Health and Human Services
counties = alt.topo_feature('https://raw.githubusercontent.com/deldersveld/topojson/master/countries/us-states/TX-48-texas-counties.json','cb_2015_texas_county_20m')




### IMPORT DATA ###

## import weekly case data
url_weekly_cases = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/cases-weekly-processed.csv'
weekly_cases = pd.read_csv(url_weekly_cases,parse_dates=['date'])

## import cumulative case data
url_cumulative_cases = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/cases-cumulative-processed.csv'
cumulative_cases = pd.read_csv(url_cumulative_cases,parse_dates=['date'])

## import weekly death data
url_weekly_deaths = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/deaths-weekly-processed.csv'
weekly_deaths = pd.read_csv(url_weekly_deaths,parse_dates=['date'])

## import cumulative death data
url_cumulative_deaths = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/deaths-cumulative-processed.csv'
cumulative_deaths = pd.read_csv(url_cumulative_deaths,parse_dates=['date'])

## import daily case and death data from San Antonio Metropolitan Health
url_daily_cases_deaths_sa = 'https://raw.githubusercontent.com/msquaredsa-ds-dev/covid-19-streamlit/master/SAMHD_Daily_Surveillance_Data_Public.csv'
daily_sa_df = pd.read_csv(url_daily_cases_deaths_sa,parse_dates=['reporting_date'])
sa_cases_deaths_df = daily_sa_df.resample('W-Mon',label='right',closed='right',on='reporting_date').sum().reset_index()[['reporting_date','total_case_daily_change','deaths_daily_change']]




### COUNTY LISTS ###
bexar_county_list = ['Bexar', 'Medina', 'Bandera','Kendall','Comal','Guadalupe','Wilson','Atascosa']
travis_county_list = ['Travis', 'Hays', 'Blanco','Burnet','Williamson','Lee','Bastrop','Caldwell']
harris_county_list = ['Waller', 'Montgomery', 'Harris','Liberty','Chambers','Galveston','Brazoria','Fort Bend']
dallas_county_list = ['Dallas', 'Tarrant', 'Denton','Collin','Rockwall','Kaufman','Ellis','Johnson']




### CREATE WIDGETS ###

## Create widget for toggling between Incidence and Mortality
metric = st.sidebar.radio('Measure:',('Incidence','Mortality'))

## Create widget for toggling between metros
major_metro = st.sidebar.radio('Major Metro:',('San Antonio','Austin','Houston','Dallas'))

## Create date slider widget
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




### FUNCTIONS ###

## Function to create a chloropleth map using cumulative data
def cumulative_per_100k_over_time(metric, data, county_list):

    if metric == 'Incidence':
        st.write('## Cumulative Cases per 100K People Over Time')
        st.write('')
        st.write('')

        core_metric = 'cases'
    elif metric == 'Mortality':
        st.write('## Cumulative Deaths per 100K People Over Time')
        st.write('')
        st.write('')

        core_metric = 'deaths'


    selection = alt.selection_single(on='mouseover', empty='none')

    chloropleth_map = alt.Chart(counties).mark_geoshape(stroke='grey').encode(
        color=alt.condition(selection, alt.value('black'), core_metric+'-per-100K:Q'),
        tooltip=['[properties][NAME]:N',core_metric+':Q','population:Q',core_metric+'-per-100K:Q']
    ).transform_lookup(
        lookup='[properties][NAME]',
        from_=alt.LookupData(data[data['date'] == date_value],'county',[core_metric,'population',core_metric+'-per-100K'])
    ).properties(
        width=800,
        height=600
    ).add_selection(
        selection
    ).transform_filter(
        alt.FieldOneOfPredicate(field='[properties][NAME]', oneOf=county_list)
    )

    render = st.altair_chart(chloropleth_map,use_container_width=False)
    return render


## Function to create a line chart showing non-cumulative, weekly incidence or mortality data
def weekly_line_chart(metric, data, county_list):

    if metric == 'Incidence':
        st.write('## Weekly Incidence per 100K')
        st.write('')
        st.write('')

        core_metric = 'cases'
    elif metric == 'Mortality':
        st.write('## Weekly Mortality per 100K')
        st.write('')
        st.write('')

        core_metric = 'deaths'

    #create county multi-select
    county_selection = st.multiselect('Which counties do you want to study?', county_list, county_list)
    st.write('')

    line_chart = alt.Chart(data).mark_line().encode(
        x=alt.X('date',axis=alt.Axis(title='Week Starting')),
        y=alt.Y(core_metric+'-per-100K:Q',axis=alt.Axis(title=core_metric[0].upper()+core_metric[1:]+' per 100K')),
        color='county',
        tooltip=['date','county',core_metric,'population',core_metric+'-per-100K']
    ).transform_filter(
        alt.FieldOneOfPredicate(field='county', oneOf=county_selection)
    ).properties(
        width=900,
        height=600
    )

    render = st.altair_chart(line_chart,use_container_width=False)
    return render




### CREATE PAGE FOR SAN ANTONIO ###
if major_metro == 'San Antonio':


    ## Create titles ##
    st.title('Bexar County and Surrounding Counties')
    st.subheader('(Based on data from the State Dept. of Health and Human Services)')
    st.write('')
    st.write('')


    ## Create chloropleth map for San Antonio and surronding counties and render based on radio button toggle for Incidence or Mortality ##
    # Incidence
    if metric == 'Incidence':
        cumulative_per_100k_over_time(metric, cumulative_cases, bexar_county_list)

    # Mortality
    elif metric == 'Mortality':
        cumulative_per_100k_over_time(metric, cumulative_deaths, bexar_county_list)



    ### SPACING ###
    st.write('')
    st.write('')
    st.write('')
    st.write('')


    ## Create and render line chart displaying the metric (chosen based on the Incidence/Mortality toggle) per 100K on a weekly basis for Bexar and surrounding counties
    # Incidence
    if metric == 'Incidence':
        weekly_line_chart(metric, weekly_cases, bexar_county_list)

    # Mortality
    elif metric == 'Mortality':
        weekly_line_chart(metric, weekly_deaths, bexar_county_list)
        



    ### SPACING AND TITLES ###    
    st.write('')
    st.write('')
    st.title('San Antonio')
    st.subheader('(Based on data from San Antonio Metropolitan Health)')
    st.write('')
    st.write('')
    st.write('## Weekly Incidence and Mortality - San Antonio')
    st.write('')
    st.write('')


    ### CREATE DUAL AXIS CHART FOR INCIDENCE AND MORTALITY ON SA METRO HEALTH DATA
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




### CREATE PAGE FOR AUSTIN ###
elif major_metro == 'Austin':


    ## Create titles ##
    st.title('Travis County and Surrounding Counties')
    st.subheader('(Based on data from the State Dept. of Health and Human Services)')
    st.write('')
    st.write('')


    ## Create chloropleth map for Travis and surronding counties and render based on radio button toggle for Incidence or Mortality ##
    # Incidence
    if metric == 'Incidence':
        cumulative_per_100k_over_time(metric, cumulative_cases, travis_county_list)

    # Mortality
    elif metric == 'Mortality':
        cumulative_per_100k_over_time(metric, cumulative_deaths, travis_county_list)



    ### SPACING ###
    st.write('')
    st.write('')
    st.write('')
    st.write('')


    ## Create and render line chart displaying the metric (chosen based on the Incidence/Mortality toggle) per 100K on a weekly basis for Travis and surrounding counties
    # Incidence
    if metric == 'Incidence':
        weekly_line_chart(metric, weekly_cases, travis_county_list)

    # Mortality
    elif metric == 'Mortality':
        weekly_line_chart(metric, weekly_deaths, travis_county_list)

    


### CREATE PAGE FOR HOUSTON ###
elif major_metro == 'Houston':


    ## Create titles ##
    st.title('Harris County and Surrounding Counties')
    st.subheader('(Based on data from the State Dept. of Health and Human Services)')
    st.write('')
    st.write('')


    ## Create chloropleth map for Harris and surronding counties and render based on radio button toggle for Incidence or Mortality ##
    # Incidence
    if metric == 'Incidence':
        cumulative_per_100k_over_time(metric, cumulative_cases, harris_county_list)

    # Mortality
    elif metric == 'Mortality':
        cumulative_per_100k_over_time(metric, cumulative_deaths, harris_county_list)



    ### SPACING ###
    st.write('')
    st.write('')
    st.write('')
    st.write('')


    ## Create and render line chart displaying the metric (chosen based on the Incidence/Mortality toggle) per 100K on a weekly basis for Harris and surrounding counties
    # Incidence
    if metric == 'Incidence':
        weekly_line_chart(metric, weekly_cases, harris_county_list)

    # Mortality
    elif metric == 'Mortality':
        weekly_line_chart(metric, weekly_deaths, harris_county_list)




### CREATE PAGE FOR DALLAS ###
elif major_metro == 'Dallas':


    ## Create titles ##
    st.title('Dallas County and Surrounding Counties')
    st.subheader('(Based on data from the State Dept. of Health and Human Services)')
    st.write('')
    st.write('')


    ## Create chloropleth map for Dallas and surronding counties and render based on radio button toggle for Incidence or Mortality ##
    # Incidence
    if metric == 'Incidence':
        cumulative_per_100k_over_time(metric, cumulative_cases, dallas_county_list)

    # Mortality
    elif metric == 'Mortality':
        cumulative_per_100k_over_time(metric, cumulative_deaths, dallas_county_list)



    ### SPACING ###
    st.write('')
    st.write('')
    st.write('')
    st.write('')


    ## Create and render line chart displaying the metric (chosen based on the Incidence/Mortality toggle) per 100K on a weekly basis for Dallas and surrounding counties
    # Incidence
    if metric == 'Incidence':
        weekly_line_chart(metric, weekly_cases, dallas_county_list)

    # Mortality
    elif metric == 'Mortality':
        weekly_line_chart(metric, weekly_deaths, dallas_county_list)