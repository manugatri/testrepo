# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                {'label': 'All Sites', 'value': 'ALL'},
                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                ],
                                placeholder='All Sites',
                                style={'font-size': 20},
                                searchable=True,
                                ),
                                html.Br(),

                                # TASK 2: Añadir un gráfico circular para mostrar el recuento total de lanzamientos con éxito de todos los sitios.
                                # Si se ha seleccionado un punto de lanzamiento específico, se muestra el recuento de éxitos y fracasos del punto.
                    
                                html.Div([dcc.Graph(id='success-pie-chart', className='pastel', style={'display':'flex'}),]),

                                html.Br(),



                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    marks={0: '0',
                                    100: '100Kg',
                                    500: '500Kg',
                                    1500: '1500Kg',
                                    2500: '2500Kg',
                                    5000: '5000Kg',
                                    6500: '6500Kg',
                                    10000: '10000Kg'},
                                    value=[1000, 10000]),

                                # TASK 4: Añadir un gráfico de dispersión para mostrar la correlación entre la carga útil y el éxito del lanzamiento.
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])





# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(##### ACTUALIZA EL GRAFICO DE CIRULO
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class']== 1]
        filtered_df = filtered_df.groupby("Launch Site")['class'].count()
        fig=px.pie(filtered_df, values='class',
            names=filtered_df.index,
            title='Total de Lanzamientos completados por Sitios de Lanzamientos')
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df = filtered_df.groupby('class').size().reset_index(name='total')
        fig = px.pie(filtered_df, values='total',names='class', title=f"Total de lanzamientos {entered_site}")

        return fig

get_pie_chart('ALL')


# TASK 4:
# Añadir una función de callback para `site-dropdown` y `payload-slider` como entradas, `success-payload-scatter-chart` como salida.
@app.callback(### ACTUALIZA EL GRAFICO DE DISPERSION #######
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_slider):
    # ASIGNAION DE FILTRO DEL MENU DESLIZANTE
    filtered_df = spacex_df[spacex_df["Payload Mass (kg)"].between(payload_slider[0], payload_slider[1])]
    #filtered_df= spacex_df
    if entered_site == 'ALL':
        fig=px.scatter(filtered_df,
            y="class",
            x="Payload Mass (kg)",
            color="Booster Version Category",
            title="Lanzamientos realizados desde todos los Launch Site")
        return fig

    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig= px.scatter(filtered_df,
                        x="Payload Mass (kg)",
                        y='class',
                        color='Booster Version Category',
                        symbol='Booster Version Category',
                        title=f"Total de lanzamientos realizados desde Launch Site {entered_site}"
                        )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()

