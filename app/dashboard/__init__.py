from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from flask import Flask
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import logging

from app import db
from app.models import TouristArrival, TouristSource, Destination, Hotel, Booking, Occupancy, Revenue
from app.services import DataCollector

logger = logging.getLogger(__name__)

def create_dashboard(server):
    """Create the Dash dashboard application"""
    
    # Create Dash app
    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/',
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
        ],
        suppress_callback_exceptions=True
    )
    
    # Configure the app
    dash_app.config.suppress_callback_exceptions = True
    
    # Define the layout
    dash_app.layout = create_main_layout()
    
    # Register callbacks
    register_callbacks(dash_app)
    
    return dash_app

def create_main_layout():
    """Create the main dashboard layout"""
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1([
                    html.I(className="fas fa-chart-line me-3"),
                    "Sri Lanka Tourism Analytics Dashboard"
                ], className="text-center text-primary mb-4"),
                html.Hr()
            ])
        ]),
        
        # Control Panel
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Control Panel", className="card-title"),
                        dbc.Row([
                            dbc.Col([
                                html.Label("Date Range:"),
                                dcc.DatePickerRange(
                                    id='date-picker',
                                    start_date=(datetime.now() - timedelta(days=30)).date(),
                                    end_date=datetime.now().date(),
                                    display_format='DD/MM/YYYY'
                                )
                            ], width=4),
                            dbc.Col([
                                html.Label("Destination:"),
                                dcc.Dropdown(
                                    id='destination-dropdown',
                                    options=[],
                                    placeholder="Select destination",
                                    multi=True
                                )
                            ], width=4),
                            dbc.Col([
                                html.Label("Source Country:"),
                                dcc.Dropdown(
                                    id='country-dropdown',
                                    options=[],
                                    placeholder="Select country",
                                    multi=True
                                )
                            ], width=4)
                        ], className="mt-3")
                    ])
                ])
            ])
        ], className="mb-4"),
        
        # Key Metrics Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-arrivals', className="text-primary"),
                        html.P("Total Arrivals", className="text-muted")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='total-revenue', className="text-success"),
                        html.P("Total Revenue (USD)", className="text-muted")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='avg-occupancy', className="text-warning"),
                        html.P("Avg. Occupancy Rate (%)", className="text-muted")
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(id='sentiment-score', className="text-info"),
                        html.P("Sentiment Score", className="text-muted")
                    ])
                ])
            ], width=3)
        ], className="mb-4"),
        
        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Tourist Arrivals Trend"),
                    dbc.CardBody([
                        dcc.Graph(id='arrivals-trend-chart')
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Revenue Breakdown"),
                    dbc.CardBody([
                        dcc.Graph(id='revenue-breakdown-chart')
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Charts Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top Source Countries"),
                    dbc.CardBody([
                        dcc.Graph(id='source-countries-chart')
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Popular Destinations"),
                    dbc.CardBody([
                        dcc.Graph(id='destinations-chart')
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Charts Row 3
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Hotel Occupancy Trends"),
                    dbc.CardBody([
                        dcc.Graph(id='occupancy-trend-chart')
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        # Data Table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Recent Tourist Arrivals"),
                    dbc.CardBody([
                        html.Div(id='arrivals-table')
                    ])
                ])
            ])
        ]),
        
        # Hidden div for storing intermediate data
        html.Div(id='intermediate-data', style={'display': 'none'}),
        
        # Auto-refresh interval
        dcc.Interval(
            id='interval-component',
            interval=5*60*1000,  # 5 minutes
            n_intervals=0
        )
        
    ], fluid=True, className="py-4")

def register_callbacks(dash_app):
    """Register all dashboard callbacks"""
    
    @dash_app.callback(
        [Output('destination-dropdown', 'options'),
         Output('country-dropdown', 'options')],
        [Input('interval-component', 'n_intervals')]
    )
    def update_dropdown_options(n):
        """Update dropdown options"""
        try:
            # Get destinations
            destinations = Destination.query.filter_by(is_active=True).all()
            destination_options = [{'label': d.name, 'value': d.id} for d in destinations]
            
            # Get source countries
            countries = TouristSource.query.filter_by(is_active=True).all()
            country_options = [{'label': c.name, 'value': c.id} for c in countries]
            
            return destination_options, country_options
        except Exception as e:
            logger.error(f"Error updating dropdown options: {str(e)}")
            return [], []
    
    @dash_app.callback(
        [Output('total-arrivals', 'children'),
         Output('total-revenue', 'children'),
         Output('avg-occupancy', 'children'),
         Output('sentiment-score', 'children')],
        [Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date'),
         Input('destination-dropdown', 'value'),
         Input('country-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_metrics(start_date, end_date, destinations, countries, n):
        """Update key metrics"""
        try:
            # Calculate total arrivals
            arrivals_query = TouristArrival.query
            if start_date and end_date:
                arrivals_query = arrivals_query.filter(
                    TouristArrival.date >= start_date,
                    TouristArrival.date <= end_date
                )
            if destinations:
                arrivals_query = arrivals_query.filter(TouristArrival.destination_id.in_(destinations))
            if countries:
                arrivals_query = arrivals_query.filter(TouristArrival.source_country_id.in_(countries))
            
            total_arrivals = arrivals_query.with_entities(
                db.func.sum(TouristArrival.total_arrivals)
            ).scalar() or 0
            
            # Calculate total revenue
            revenue_query = Revenue.query
            if start_date and end_date:
                revenue_query = revenue_query.filter(
                    Revenue.date >= start_date,
                    Revenue.date <= end_date
                )
            if destinations:
                revenue_query = revenue_query.filter(Revenue.destination_id.in_(destinations))
            if countries:
                revenue_query = revenue_query.filter(Revenue.source_country_id.in_(countries))
            
            total_revenue = revenue_query.with_entities(
                db.func.sum(Revenue.revenue_usd)
            ).scalar() or 0
            
            # Calculate average occupancy
            occupancy_query = Occupancy.query
            if start_date and end_date:
                occupancy_query = occupancy_query.filter(
                    Occupancy.date >= start_date,
                    Occupancy.date <= end_date
                )
            
            avg_occupancy = occupancy_query.with_entities(
                db.func.avg(Occupancy.occupancy_rate)
            ).scalar() or 0
            
            # For now, use a placeholder sentiment score
            sentiment_score = "7.2/10"
            
            return (
                f"{total_arrivals:,}",
                f"${total_revenue:,.0f}",
                f"{avg_occupancy:.1f}%",
                sentiment_score
            )
            
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
            return "0", "$0", "0.0%", "N/A"
    
    @dash_app.callback(
        Output('arrivals-trend-chart', 'figure'),
        [Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date'),
         Input('destination-dropdown', 'value'),
         Input('country-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_arrivals_trend(start_date, end_date, destinations, countries, n):
        """Update arrivals trend chart"""
        try:
            query = db.session.query(
                TouristArrival.date,
                db.func.sum(TouristArrival.total_arrivals).label('total_arrivals')
            )
            
            if start_date and end_date:
                query = query.filter(
                    TouristArrival.date >= start_date,
                    TouristArrival.date <= end_date
                )
            if destinations:
                query = query.filter(TouristArrival.destination_id.in_(destinations))
            if countries:
                query = query.filter(TouristArrival.source_country_id.in_(countries))
            
            data = query.group_by(TouristArrival.date).order_by(TouristArrival.date).all()
            
            df = pd.DataFrame(data, columns=['date', 'total_arrivals'])
            
            fig = px.line(
                df, x='date', y='total_arrivals',
                title='Tourist Arrivals Trend',
                labels={'date': 'Date', 'total_arrivals': 'Total Arrivals'}
            )
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Total Arrivals",
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error updating arrivals trend: {str(e)}")
            return px.line(title='Tourist Arrivals Trend')
    
    @dash_app.callback(
        Output('revenue-breakdown-chart', 'figure'),
        [Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date'),
         Input('destination-dropdown', 'value'),
         Input('country-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_revenue_breakdown(start_date, end_date, destinations, countries, n):
        """Update revenue breakdown chart"""
        try:
            query = db.session.query(
                db.func.sum(Revenue.accommodation_revenue).label('accommodation'),
                db.func.sum(Revenue.food_beverage_revenue).label('food_beverage'),
                db.func.sum(Revenue.transportation_revenue).label('transportation'),
                db.func.sum(Revenue.entertainment_revenue).label('entertainment'),
                db.func.sum(Revenue.shopping_revenue).label('shopping'),
                db.func.sum(Revenue.other_revenue).label('other')
            )
            
            if start_date and end_date:
                query = query.filter(
                    Revenue.date >= start_date,
                    Revenue.date <= end_date
                )
            if destinations:
                query = query.filter(Revenue.destination_id.in_(destinations))
            if countries:
                query = query.filter(Revenue.source_country_id.in_(countries))
            
            result = query.first()
            
            categories = ['Accommodation', 'Food & Beverage', 'Transportation', 'Entertainment', 'Shopping', 'Other']
            values = [result.accommodation or 0, result.food_beverage or 0, result.transportation or 0,
                     result.entertainment or 0, result.shopping or 0, result.other or 0]
            
            fig = px.pie(
                values=values, names=categories,
                title='Revenue Breakdown by Category'
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            return fig
            
        except Exception as e:
            logger.error(f"Error updating revenue breakdown: {str(e)}")
            return px.pie(title='Revenue Breakdown by Category')
    
    @dash_app.callback(
        Output('source-countries-chart', 'figure'),
        [Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date'),
         Input('destination-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_source_countries(start_date, end_date, destinations, n):
        """Update source countries chart"""
        try:
            query = db.session.query(
                TouristSource.name,
                db.func.sum(TouristArrival.total_arrivals).label('total_arrivals')
            ).join(TouristArrival)
            
            if start_date and end_date:
                query = query.filter(
                    TouristArrival.date >= start_date,
                    TouristArrival.date <= end_date
                )
            if destinations:
                query = query.filter(TouristArrival.destination_id.in_(destinations))
            
            data = query.group_by(TouristSource.name).order_by(
                db.func.sum(TouristArrival.total_arrivals).desc()
            ).limit(10).all()
            
            df = pd.DataFrame(data, columns=['country', 'arrivals'])
            
            fig = px.bar(
                df, x='country', y='arrivals',
                title='Top 10 Source Countries',
                labels={'country': 'Country', 'arrivals': 'Total Arrivals'}
            )
            fig.update_layout(
                xaxis_title="Country",
                yaxis_title="Total Arrivals",
                xaxis_tickangle=-45
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error updating source countries: {str(e)}")
            return px.bar(title='Top 10 Source Countries')
    
    @dash_app.callback(
        Output('destinations-chart', 'figure'),
        [Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date'),
         Input('country-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_destinations(start_date, end_date, countries, n):
        """Update destinations chart"""
        try:
            query = db.session.query(
                Destination.name,
                db.func.sum(TouristArrival.total_arrivals).label('total_arrivals')
            ).join(TouristArrival)
            
            if start_date and end_date:
                query = query.filter(
                    TouristArrival.date >= start_date,
                    TouristArrival.date <= end_date
                )
            if countries:
                query = query.filter(TouristArrival.source_country_id.in_(countries))
            
            data = query.group_by(Destination.name).order_by(
                db.func.sum(TouristArrival.total_arrivals).desc()
            ).limit(10).all()
            
            df = pd.DataFrame(data, columns=['destination', 'arrivals'])
            
            fig = px.bar(
                df, x='destination', y='arrivals',
                title='Top 10 Popular Destinations',
                labels={'destination': 'Destination', 'arrivals': 'Total Arrivals'}
            )
            fig.update_layout(
                xaxis_title="Destination",
                yaxis_title="Total Arrivals",
                xaxis_tickangle=-45
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error updating destinations: {str(e)}")
            return px.bar(title='Top 10 Popular Destinations')
    
    @dash_app.callback(
        Output('occupancy-trend-chart', 'figure'),
        [Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date'),
         Input('interval-component', 'n_intervals')]
    )
    def update_occupancy_trend(start_date, end_date, n):
        """Update occupancy trend chart"""
        try:
            query = db.session.query(
                Occupancy.date,
                db.func.avg(Occupancy.occupancy_rate).label('avg_occupancy')
            )
            
            if start_date and end_date:
                query = query.filter(
                    Occupancy.date >= start_date,
                    Occupancy.date <= end_date
                )
            
            data = query.group_by(Occupancy.date).order_by(Occupancy.date).all()
            
            df = pd.DataFrame(data, columns=['date', 'occupancy_rate'])
            
            fig = px.line(
                df, x='date', y='occupancy_rate',
                title='Average Hotel Occupancy Rate Trend',
                labels={'date': 'Date', 'occupancy_rate': 'Occupancy Rate (%)'}
            )
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Occupancy Rate (%)",
                hovermode='x unified'
            )
            
            return fig
            
        except Exception as e:
            logger.error(f"Error updating occupancy trend: {str(e)}")
            return px.line(title='Average Hotel Occupancy Rate Trend')
    
    @dash_app.callback(
        Output('arrivals-table', 'children'),
        [Input('date-picker', 'start_date'),
         Input('date-picker', 'end_date'),
         Input('destination-dropdown', 'value'),
         Input('country-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]
    )
    def update_arrivals_table(start_date, end_date, destinations, countries, n):
        """Update arrivals table"""
        try:
            query = db.session.query(
                TouristArrival.date,
                TouristSource.name.label('source_country'),
                Destination.name.label('destination'),
                TouristArrival.total_arrivals,
                TouristArrival.purpose_of_visit
            ).join(TouristSource).join(Destination)
            
            if start_date and end_date:
                query = query.filter(
                    TouristArrival.date >= start_date,
                    TouristArrival.date <= end_date
                )
            if destinations:
                query = query.filter(TouristArrival.destination_id.in_(destinations))
            if countries:
                query = query.filter(TouristArrival.source_country_id.in_(countries))
            
            data = query.order_by(TouristArrival.date.desc()).limit(20).all()
            
            if not data:
                return html.P("No data available", className="text-muted")
            
            # Create table
            table_header = [
                html.Thead(html.Tr([
                    html.Th("Date"),
                    html.Th("Source Country"),
                    html.Th("Destination"),
                    html.Th("Arrivals"),
                    html.Th("Purpose")
                ]))
            ]
            
            table_body = [html.Tbody([
                html.Tr([
                    html.Td(str(row.date)),
                    html.Td(row.source_country),
                    html.Td(row.destination),
                    html.Td(row.total_arrivals),
                    html.Td(row.purpose_of_visit)
                ]) for row in data
            ])]
            
            return dbc.Table(table_header + table_body, bordered=True, hover=True)
            
        except Exception as e:
            logger.error(f"Error updating arrivals table: {str(e)}")
            return html.P("Error loading data", className="text-danger")

# Create blueprint for Flask
from flask import Blueprint
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    """Dashboard route"""
    return "Dashboard is running!"