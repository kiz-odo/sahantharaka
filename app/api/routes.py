from flask import jsonify, request
from app.api import api_bp
from app import db
from app.models import TouristArrival, TouristSource, Destination, Hotel, Booking, Occupancy, Revenue
from app.services import DataCollector
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Sri Lanka Tourism Analytics API'
    })

@api_bp.route('/tourist-arrivals', methods=['GET'])
def get_tourist_arrivals():
    """Get tourist arrival data"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        destination_id = request.args.get('destination_id')
        source_country_id = request.args.get('source_country_id')
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = TouristArrival.query
        
        if start_date:
            query = query.filter(TouristArrival.date >= start_date)
        if end_date:
            query = query.filter(TouristArrival.date <= end_date)
        if destination_id:
            query = query.filter(TouristArrival.destination_id == destination_id)
        if source_country_id:
            query = query.filter(TouristArrival.source_country_id == source_country_id)
        
        # Execute query
        arrivals = query.order_by(TouristArrival.date.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [arrival.to_dict() for arrival in arrivals],
            'count': len(arrivals)
        })
        
    except Exception as e:
        logger.error(f"Error getting tourist arrivals: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/revenue', methods=['GET'])
def get_revenue():
    """Get revenue data"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        destination_id = request.args.get('destination_id')
        source_country_id = request.args.get('source_country_id')
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = Revenue.query
        
        if start_date:
            query = query.filter(Revenue.date >= start_date)
        if end_date:
            query = query.filter(Revenue.date <= end_date)
        if destination_id:
            query = query.filter(Revenue.destination_id == destination_id)
        if source_country_id:
            query = query.filter(Revenue.source_country_id == source_country_id)
        
        # Execute query
        revenue_data = query.order_by(Revenue.date.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [revenue.to_dict() for revenue in revenue_data],
            'count': len(revenue_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting revenue data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/hotels', methods=['GET'])
def get_hotels():
    """Get hotel data"""
    try:
        # Get query parameters
        destination_id = request.args.get('destination_id')
        category = request.args.get('category')
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = Hotel.query.filter_by(is_active=True)
        
        if destination_id:
            query = query.filter(Hotel.destination_id == destination_id)
        if category:
            query = query.filter(Hotel.category == category)
        
        # Execute query
        hotels = query.limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [hotel.to_dict() for hotel in hotels],
            'count': len(hotels)
        })
        
    except Exception as e:
        logger.error(f"Error getting hotel data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/occupancy', methods=['GET'])
def get_occupancy():
    """Get occupancy data"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        hotel_id = request.args.get('hotel_id')
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = Occupancy.query
        
        if start_date:
            query = query.filter(Occupancy.date >= start_date)
        if end_date:
            query = query.filter(Occupancy.date <= end_date)
        if hotel_id:
            query = query.filter(Occupancy.hotel_id == hotel_id)
        
        # Execute query
        occupancy_data = query.order_by(Occupancy.date.desc()).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [occupancy.to_dict() for occupancy in occupancy_data],
            'count': len(occupancy_data)
        })
        
    except Exception as e:
        logger.error(f"Error getting occupancy data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/destinations', methods=['GET'])
def get_destinations():
    """Get destination data"""
    try:
        # Get query parameters
        category = request.args.get('category')
        province = request.args.get('province')
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = Destination.query.filter_by(is_active=True)
        
        if category:
            query = query.filter(Destination.category == category)
        if province:
            query = query.filter(Destination.province == province)
        
        # Execute query
        destinations = query.limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [destination.to_dict() for destination in destinations],
            'count': len(destinations)
        })
        
    except Exception as e:
        logger.error(f"Error getting destination data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/source-countries', methods=['GET'])
def get_source_countries():
    """Get source country data"""
    try:
        # Get query parameters
        region = request.args.get('region')
        limit = request.args.get('limit', 100, type=int)
        
        # Build query
        query = TouristSource.query.filter_by(is_active=True)
        
        if region:
            query = query.filter(TouristSource.region == region)
        
        # Execute query
        countries = query.limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [country.to_dict() for country in countries],
            'count': len(countries)
        })
        
    except Exception as e:
        logger.error(f"Error getting source country data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary"""
    try:
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Calculate summary statistics
        arrivals_query = TouristArrival.query
        revenue_query = Revenue.query
        occupancy_query = Occupancy.query
        
        if start_date:
            arrivals_query = arrivals_query.filter(TouristArrival.date >= start_date)
            revenue_query = revenue_query.filter(Revenue.date >= start_date)
            occupancy_query = occupancy_query.filter(Occupancy.date >= start_date)
        
        if end_date:
            arrivals_query = arrivals_query.filter(TouristArrival.date <= end_date)
            revenue_query = revenue_query.filter(Revenue.date <= end_date)
            occupancy_query = occupancy_query.filter(Occupancy.date <= end_date)
        
        # Get totals
        total_arrivals = arrivals_query.with_entities(
            db.func.sum(TouristArrival.total_arrivals)
        ).scalar() or 0
        
        total_revenue = revenue_query.with_entities(
            db.func.sum(Revenue.revenue_usd)
        ).scalar() or 0
        
        avg_occupancy = occupancy_query.with_entities(
            db.func.avg(Occupancy.occupancy_rate)
        ).scalar() or 0
        
        # Get top destinations
        top_destinations = db.session.query(
            Destination.name,
            db.func.sum(TouristArrival.total_arrivals).label('total_arrivals')
        ).join(TouristArrival).group_by(Destination.name).order_by(
            db.func.sum(TouristArrival.total_arrivals).desc()
        ).limit(5).all()
        
        # Get top source countries
        top_countries = db.session.query(
            TouristSource.name,
            db.func.sum(TouristArrival.total_arrivals).label('total_arrivals')
        ).join(TouristArrival).group_by(TouristSource.name).order_by(
            db.func.sum(TouristArrival.total_arrivals).desc()
        ).limit(5).all()
        
        return jsonify({
            'success': True,
            'data': {
                'total_arrivals': total_arrivals,
                'total_revenue_usd': total_revenue,
                'average_occupancy_rate': avg_occupancy,
                'top_destinations': [
                    {'name': d.name, 'arrivals': d.total_arrivals} 
                    for d in top_destinations
                ],
                'top_source_countries': [
                    {'name': c.name, 'arrivals': c.total_arrivals} 
                    for c in top_countries
                ]
            }
        })
        
    except Exception as e:
        logger.error(f"Error getting analytics summary: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api_bp.route('/data/collect', methods=['POST'])
def collect_data():
    """Trigger data collection"""
    try:
        data_type = request.json.get('data_type', 'all')
        start_date = request.json.get('start_date')
        end_date = request.json.get('end_date')
        
        collector = DataCollector()
        
        if data_type == 'arrivals':
            count = collector.collect_tourist_arrivals(start_date, end_date)
        elif data_type == 'hotels':
            count = collector.collect_hotel_data()
        elif data_type == 'revenue':
            count = collector.collect_revenue_data(start_date, end_date)
        elif data_type == 'weather':
            count = collector.collect_weather_data()
        else:  # all
            count = (
                collector.collect_tourist_arrivals(start_date, end_date) +
                collector.collect_hotel_data() +
                collector.collect_revenue_data(start_date, end_date) +
                collector.collect_weather_data()
            )
        
        return jsonify({
            'success': True,
            'message': f'Collected {count} records',
            'data_type': data_type
        })
        
    except Exception as e:
        logger.error(f"Error collecting data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500