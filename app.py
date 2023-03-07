import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

# load the dataset
data = pd.read_csv('Sales.csv')

# extract the year from the 'Order Date' column
data['Year'] = pd.to_datetime(data['Order Date']).dt.year

# create a Dash application instance
app = dash.Dash(__name__)

# define the layout of the dashboard
app.layout = html.Div(children=[
    html.H1(children='Sales Dashboard'),
    
    # dropdown menu to select year
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': str(year), 'value': year} for year in data['Year'].unique()],
        value=data['Year'].max(),
        clearable=False
    ),
    
    # sales overview chart
    dcc.Graph(
        id='sales-by-region-and-category',
        style={'height': '500px'},
    ),
    
    # product performance chart
    dcc.Graph(
        id='top-selling-products',
        style={'height': '500px'},
    ),
])

# update the sales overview chart based on the selected year
@app.callback(
    dash.dependencies.Output('sales-by-region-and-category', 'figure'),
    dash.dependencies.Input('year-dropdown', 'value')
)
def update_sales_by_region_and_category(year):
    sales_by_region_category = data[data['Year'] == year].groupby(['Region', 'Product Category'])['Sales'].sum().reset_index()
    fig = go.Figure(
        data=[go.Bar(
            x=sales_by_region_category[sales_by_region_category['Product Category'] == i]['Region'],
            y=sales_by_region_category[sales_by_region_category['Product Category'] == i]['Sales'],
            name=i
        ) for i in sales_by_region_category['Product Category'].unique()],
        layout=go.Layout(
            title=f'Total Sales Revenue by Region and Product Category ({year})',
            xaxis_title='Region',
            yaxis_title='Total Sales Revenue'
        )
    )
    return fig

# update the top-selling products chart based on the selected year
@app.callback(
    dash.dependencies.Output('top-selling-products', 'figure'),
    dash.dependencies.Input('year-dropdown', 'value')
)
def update_top_selling_products(year):
    top_selling_products = data[data['Year'] == year].groupby('Product Category')['Sales'].agg(['sum', 'count']).reset_index().sort_values(by='sum', ascending=False)[:10]
    fig = go.Figure(
        data=[
            go.Bar(
                x=top_selling_products['Product Category'],
                y=top_selling_products['sum'],
                name='Revenue'
            ),
            go.Bar(
                x=top_selling_products['Product Category'],
                y=top_selling_products['count'],
                name='Quantity Sold'
            )
        ],
        layout=go.Layout(
            title=f'Top-selling Products ({year})',
            xaxis_title='Product Category',
            yaxis_title='Revenue / Quantity Sold',
            barmode='group'
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
