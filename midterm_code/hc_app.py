# load packages and necessary datasets
import pandas as pd

df = pd.read_csv('/Users/bradyengelke/MSBA/spring/ELP/minority_tracts.csv')
df_snap = pd.read_csv('/Users/bradyengelke/MSBA/spring/ELP/snap_tracts.csv')
df_hdi = pd.read_csv('/Users/bradyengelke/MSBA/spring/ELP/hdi_avg.csv')
df_low_hdi_race = pd.read_csv('/Users/bradyengelke/MSBA/spring/ELP/low_hdi_race.csv')
df_high_hdi_race = pd.read_csv('/Users/bradyengelke/MSBA/spring/ELP/high_hdi_race.csv')

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# begin dashboard content
app.layout = html.Div(children=[
    # create title and subtitles for first graphic
    html.H1(children='Hennepin County Dashboard', style={'color': 'blue'}),
    
    html.H2(children='Do minority dominant neighborhoods have a disproportionate school enrollment rate?'),
    
    html.Div(children='''
        Cypher Query: MATCH (d:District)-[:EDUCATES]->(t:Tract) WHERE t.black_perc > 30 
        RETURN t.name AS tract, t.black_perc AS prop_black, t.k_12_enrolled_perc AS perc_enrolled_k_12, d.avg_ACT AS avg_ACT 
                             ORDER BY t.black_perc DESC LIMIT 25
    ''', style={'color': 'red', 'fontSize': 18}),
    # create first graphic
        dcc.Graph(
        id='graph1',
        figure={
            'data': [
                {'x': df['race'], 'y': df['k_12_enrollment'], 'type': 'bar', 'name': 'SF'}
            ],
            'layout': dict(
                title = 'Tracts that Are Majority White Have a Higher k-12 Enrollment Rate',
                yaxis = {'title': '% of kids enrolled in k-12'},
                xaxis = {'title': 'Top 25 Tracts in terms % of Population White & Black'} 
            )
        }
    ),
    # create subtitle for second graphic
    html.H2(children='What is the avg act score of the districts that educate these tracts?'),
        # create second graphic
        dcc.Graph(
        id='graph2',
        figure={
            'data': [
                {'x': df['race'], 'y': df['avg_ACT'], 'type': 'bar', 'name': 'SF'},
            ],
            'layout': dict(
                title = 'Tracts that Are Majority White Have Higher District ACT Scores',
                yaxis = {'title': 'Avg ACT Score'},
                xaxis = {'title': 'Top 25 Tracts in terms % of Population White & Black'} 
            )
        }
    ),
    # create subtitles for third graphic
    html.H2(children='For tracts with high SNAP enrollment rate vs low SNAP enrollment, what is the percentage of the population that attends undergrad?'),
    
    html.Div(children='''
        Cypher Query: MATCH (t:Tract) WHERE t.households_on_SNAP_perc > 25 
    RETURN t.name AS tract, t.households_on_SNAP_perc AS households_on_snap_perc, t.college_undergrad_perc AS undergrad_perc 
                             ORDER BY t.households_on_SNAP_perc DESC
    ''', style={'color': 'red', 'fontSize': 18}),
    # create third graphic
        dcc.Graph(
        id='graph3',
        figure={
            'data': [
                {'x': df_snap['snap_enrollment'], 'y': df_snap['undergrad_perc'], 'type': 'bar', 'name': 'SF'}
            ],
            'layout': dict(
                title = 'Tracts with High Snap Enrollment Go to Undergrad More?',
                yaxis = {'title': '% of Pop who Attend Undergrad'},
                xaxis = {'title': 'Snap Enrollment Rate Bucket'} 
            )
        }
    ),
    # create subtitles for fourht graphic
    html.H2(children='What is the HDI of tracts across Hennepin County?'),
    
    
    html.Div(children='''
        Cypher Query: MATCH (c:County)-[:SERVES]->(t:Tract) WHERE c.name = 'hennepin' 
        RETURN c.life_expectancy AS life_expectancy, t.college_undergrad_perc AS undergrad_perc, t.k_12_enrolled_perc AS k_12_enrollment, 
        t.income_median AS income_median, t.white_perc AS white_perc, t.black_perc AS black_perc, t.asian_perc AS asian_perc, 
        t.other_ethnicity_perc AS other_perc, t.name AS tract
    ''', style={'color': 'red', 'fontSize': 18}),
    # create fourth graphic
        dcc.Graph(
        id='graph4',
        figure={
            'data': [
                {'x': df_hdi['hdi_level'], 'y': df_hdi['hdi'], 'type': 'bar', 'name': 'SF'}
            ],
            'layout': dict(
                yaxis = {'title': 'HDI'},
                xaxis = {'title': 'HDI Bucket (low = bottom 25%, middle = 50%, high = top 25%)'} 
            )
        }
    ),
    # create subtitle for fifth graphic
    html.H2(children='What is the racial distribution of tracts with lowest HDI vs highest HDI?'),
        # create fifth graphic
        dcc.Graph(
        id='graph5',
        figure={
            'data': [
                {'x': df_low_hdi_race['race'], 'y': df_low_hdi_race['perc_of_pop'], 'type': 'bar', 'name': 'Bottom 25% HDI'},
                {'x': df_high_hdi_race['race'], 'y': df_high_hdi_race['perc_of_pop'], 'type': 'bar', 'name': 'Top 25% HDI'}
            ],
            'layout': dict(
                title = 'Tracts that Are Majority White Have Higher HDI Ratings',
                yaxis = {'title': '% of Population'},
                xaxis = {'title': 'Race'} 
            )
        }
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
