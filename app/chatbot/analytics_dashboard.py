"""
Advanced Analytics Dashboard Component

Provides comprehensive analytics and insights into chatbot performance,
user behavior, conversation patterns, and business intelligence for Phase 3.
"""

import logging
import json
import pandas as pd
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import seaborn as sns

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logging.warning("Plotly not available, advanced visualizations disabled")

logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of analytics metrics."""
    CONVERSATION = "conversation"
    USER_ENGAGEMENT = "user_engagement"
    PERFORMANCE = "performance"
    CONTENT = "content"
    LANGUAGE = "language"
    RECOMMENDATION = "recommendation"


class TimeGranularity(Enum):
    """Time granularity for analytics."""
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


@dataclass
class AnalyticsMetric:
    """Structure for analytics metrics."""
    name: str
    value: float
    unit: str
    change: float  # Percentage change from previous period
    trend: str  # 'up', 'down', 'stable'
    timestamp: datetime
    metadata: Dict[str, Any]


@dataclass
class ConversationInsight:
    """Structure for conversation insights."""
    total_conversations: int
    average_duration: float
    completion_rate: float
    user_satisfaction: float
    common_topics: List[Tuple[str, int]]
    peak_hours: List[Tuple[int, int]]
    language_distribution: Dict[str, int]
    intent_success_rate: Dict[str, float]


class AdvancedAnalyticsDashboard:
    """
    Advanced analytics dashboard providing deep insights into chatbot performance,
    user behavior, and business intelligence.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the analytics dashboard.
        
        Args:
            config: Configuration dictionary for analytics settings
        """
        self.config = config or {}
        self.metrics_history = defaultdict(list)
        self.conversation_data = []
        self.user_behavior_data = []
        self.performance_data = []
        
        # Analytics settings
        self.retention_days = self.config.get('retention_days', 90)
        self.update_frequency = self.config.get('update_frequency', 3600)  # seconds
        self.last_update = datetime.now()
        
        # Data aggregation
        self.hourly_stats = defaultdict(lambda: defaultdict(int))
        self.daily_stats = defaultdict(lambda: defaultdict(int))
        self.weekly_stats = defaultdict(lambda: defaultdict(int))
        
        logger.info("Advanced Analytics Dashboard initialized successfully")
    
    def record_conversation(self, conversation_data: Dict[str, Any]):
        """
        Record conversation data for analysis.
        
        Args:
            conversation_data: Dictionary containing conversation information
        """
        try:
            # Add timestamp if not present
            if 'timestamp' not in conversation_data:
                conversation_data['timestamp'] = datetime.now()
            
            # Store conversation data
            self.conversation_data.append(conversation_data)
            
            # Update aggregated statistics
            self._update_aggregated_stats(conversation_data)
            
            # Clean old data
            self._cleanup_old_data()
            
        except Exception as e:
            logger.error(f"Error recording conversation: {str(e)}")
    
    def record_user_behavior(self, user_id: str, behavior_type: str, data: Dict[str, Any]):
        """
        Record user behavior data for analysis.
        
        Args:
            user_id: User identifier
            behavior_type: Type of behavior (click, search, recommendation_view, etc.)
            data: Additional behavior data
        """
        try:
            behavior_record = {
                'user_id': user_id,
                'behavior_type': behavior_type,
                'data': data,
                'timestamp': datetime.now()
            }
            
            self.user_behavior_data.append(behavior_record)
            
        except Exception as e:
            logger.error(f"Error recording user behavior: {str(e)}")
    
    def record_performance_metric(self, metric_name: str, value: float, metadata: Dict[str, Any] = None):
        """
        Record performance metrics for analysis.
        
        Args:
            metric_name: Name of the performance metric
            value: Metric value
            metadata: Additional metadata about the metric
        """
        try:
            metric_record = {
                'name': metric_name,
                'value': value,
                'metadata': metadata or {},
                'timestamp': datetime.now()
            }
            
            self.performance_data.append(metric_record)
            
            # Store in metrics history
            self.metrics_history[metric_name].append(metric_record)
            
        except Exception as e:
            logger.error(f"Error recording performance metric: {str(e)}")
    
    def get_conversation_insights(self, time_window: timedelta = timedelta(days=30)) -> ConversationInsight:
        """
        Get comprehensive insights about conversations.
        
        Args:
            time_window: Time window for analysis
            
        Returns:
            ConversationInsight object with detailed analytics
        """
        try:
            cutoff_time = datetime.now() - time_window
            recent_conversations = [
                conv for conv in self.conversation_data
                if conv['timestamp'] > cutoff_time
            ]
            
            if not recent_conversations:
                return ConversationInsight(
                    total_conversations=0,
                    average_duration=0.0,
                    completion_rate=0.0,
                    user_satisfaction=0.0,
                    common_topics=[],
                    peak_hours=[],
                    language_distribution={},
                    intent_success_rate={}
                )
            
            # Calculate basic metrics
            total_conversations = len(recent_conversations)
            
            # Average duration
            durations = [conv.get('duration', 0) for conv in recent_conversations]
            average_duration = np.mean(durations) if durations else 0.0
            
            # Completion rate
            completed = sum(1 for conv in recent_conversations if conv.get('completed', False))
            completion_rate = (completed / total_conversations * 100) if total_conversations > 0 else 0.0
            
            # User satisfaction
            satisfaction_scores = [conv.get('satisfaction_score', 0) for conv in recent_conversations]
            user_satisfaction = np.mean(satisfaction_scores) if satisfaction_scores else 0.0
            
            # Common topics
            topics = [conv.get('topic', 'unknown') for conv in recent_conversations]
            topic_counts = Counter(topics)
            common_topics = topic_counts.most_common(10)
            
            # Peak hours
            hour_counts = defaultdict(int)
            for conv in recent_conversations:
                hour = conv['timestamp'].hour
                hour_counts[hour] += 1
            
            peak_hours = sorted(hour_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Language distribution
            languages = [conv.get('language', 'en') for conv in recent_conversations]
            language_distribution = dict(Counter(languages))
            
            # Intent success rate
            intent_success = defaultdict(lambda: {'success': 0, 'total': 0})
            for conv in recent_conversations:
                intent = conv.get('intent', 'unknown')
                success = conv.get('intent_success', False)
                intent_success[intent]['total'] += 1
                if success:
                    intent_success[intent]['success'] += 1
            
            intent_success_rate = {}
            for intent, counts in intent_success.items():
                if counts['total'] > 0:
                    success_rate = (counts['success'] / counts['total']) * 100
                    intent_success_rate[intent] = success_rate
            
            return ConversationInsight(
                total_conversations=total_conversations,
                average_duration=average_duration,
                completion_rate=completion_rate,
                user_satisfaction=user_satisfaction,
                common_topics=common_topics,
                peak_hours=peak_hours,
                language_distribution=language_distribution,
                intent_success_rate=intent_success_rate
            )
            
        except Exception as e:
            logger.error(f"Error getting conversation insights: {str(e)}")
            return ConversationInsight(
                total_conversations=0,
                average_duration=0.0,
                completion_rate=0.0,
                user_satisfaction=0.0,
                common_topics=[],
                peak_hours=[],
                language_distribution={},
                intent_success_rate={}
            )
    
    def get_user_engagement_metrics(self, time_window: timedelta = timedelta(days=30)) -> Dict[str, Any]:
        """
        Get user engagement metrics and trends.
        
        Args:
            time_window: Time window for analysis
            
        Returns:
            Dictionary containing engagement metrics
        """
        try:
            cutoff_time = datetime.now() - time_window
            recent_behavior = [
                behavior for behavior in self.user_behavior_data
                if behavior['timestamp'] > cutoff_time
            ]
            
            if not recent_behavior:
                return {}
            
            # Unique users
            unique_users = set(behavior['user_id'] for behavior in recent_behavior)
            total_users = len(unique_users)
            
            # Behavior frequency
            behavior_counts = Counter(behavior['behavior_type'] for behavior in recent_behavior)
            
            # User activity patterns
            user_activity = defaultdict(int)
            for behavior in recent_behavior:
                user_activity[behavior['user_id']] += 1
            
            # Engagement levels
            engagement_levels = {
                'high': sum(1 for count in user_activity.values() if count >= 10),
                'medium': sum(1 for count in user_activity.values() if 3 <= count < 10),
                'low': sum(1 for count in user_activity.values() if count < 3)
            }
            
            # Session duration (if available)
            session_durations = []
            for behavior in recent_behavior:
                if 'session_duration' in behavior['data']:
                    session_durations.append(behavior['data']['session_duration'])
            
            avg_session_duration = np.mean(session_durations) if session_durations else 0.0
            
            # Return on engagement
            return_visits = sum(1 for behavior in recent_behavior if behavior['behavior_type'] == 'return_visit')
            return_rate = (return_visits / total_users * 100) if total_users > 0 else 0.0
            
            return {
                'total_users': total_users,
                'active_users': len([u for u, count in user_activity.items() if count > 0]),
                'behavior_frequency': dict(behavior_counts),
                'engagement_levels': engagement_levels,
                'average_session_duration': avg_session_duration,
                'return_rate': return_rate,
                'user_activity_distribution': dict(user_activity)
            }
            
        except Exception as e:
            logger.error(f"Error getting user engagement metrics: {str(e)}")
            return {}
    
    def get_performance_metrics(self, metric_name: str = None, 
                               time_window: timedelta = timedelta(days=30)) -> List[AnalyticsMetric]:
        """
        Get performance metrics with trend analysis.
        
        Args:
            metric_name: Specific metric to retrieve (None for all)
            time_window: Time window for analysis
            
        Returns:
            List of AnalyticsMetric objects
        """
        try:
            cutoff_time = datetime.now() - time_window
            metrics_to_analyze = [metric_name] if metric_name else list(self.metrics_history.keys())
            
            analytics_metrics = []
            
            for metric in metrics_to_analyze:
                if metric not in self.metrics_history:
                    continue
                
                metric_data = self.metrics_history[metric]
                recent_metrics = [m for m in metric_data if m['timestamp'] > cutoff_time]
                
                if not recent_metrics:
                    continue
                
                # Current value
                current_value = recent_metrics[-1]['value']
                
                # Previous period value
                previous_period_start = cutoff_time - time_window
                previous_metrics = [m for m in metric_data if previous_period_start < m['timestamp'] <= cutoff_time]
                
                if previous_metrics:
                    previous_value = np.mean([m['value'] for m in previous_metrics])
                    change = ((current_value - previous_value) / previous_value * 100) if previous_value != 0 else 0.0
                else:
                    change = 0.0
                
                # Determine trend
                if change > 5:
                    trend = 'up'
                elif change < -5:
                    trend = 'down'
                else:
                    trend = 'stable'
                
                # Calculate unit based on metric type
                unit = self._get_metric_unit(metric)
                
                analytics_metric = AnalyticsMetric(
                    name=metric,
                    value=current_value,
                    unit=unit,
                    change=change,
                    trend=trend,
                    timestamp=datetime.now(),
                    metadata={'data_points': len(recent_metrics)}
                )
                
                analytics_metrics.append(analytics_metric)
            
            return analytics_metrics
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {str(e)}")
            return []
    
    def get_language_analytics(self, time_window: timedelta = timedelta(days=30)) -> Dict[str, Any]:
        """
        Get analytics specific to language usage and performance.
        
        Args:
            time_window: Time window for analysis
            
        Returns:
            Dictionary containing language analytics
        """
        try:
            cutoff_time = datetime.now() - time_window
            recent_conversations = [
                conv for conv in self.conversation_data
                if conv['timestamp'] > cutoff_time
            ]
            
            if not recent_conversations:
                return {}
            
            # Language distribution
            languages = [conv.get('language', 'en') for conv in recent_conversations]
            language_counts = Counter(languages)
            
            # Language performance metrics
            language_metrics = {}
            for language in set(languages):
                lang_conversations = [conv for conv in recent_conversations if conv.get('language') == language]
                
                if lang_conversations:
                    # Success rate
                    success_count = sum(1 for conv in lang_conversations if conv.get('intent_success', False))
                    success_rate = (success_count / len(lang_conversations)) * 100
                    
                    # Average satisfaction
                    satisfaction_scores = [conv.get('satisfaction_score', 0) for conv in lang_conversations]
                    avg_satisfaction = np.mean(satisfaction_scores) if satisfaction_scores else 0.0
                    
                    # Average duration
                    durations = [conv.get('duration', 0) for conv in lang_conversations]
                    avg_duration = np.mean(durations) if durations else 0.0
                    
                    language_metrics[language] = {
                        'conversation_count': len(lang_conversations),
                        'success_rate': success_rate,
                        'average_satisfaction': avg_satisfaction,
                        'average_duration': avg_duration
                    }
            
            return {
                'language_distribution': dict(language_counts),
                'language_performance': language_metrics,
                'total_conversations': len(recent_conversations)
            }
            
        except Exception as e:
            logger.error(f"Error getting language analytics: {str(e)}")
            return {}
    
    def get_recommendation_analytics(self, time_window: timedelta = timedelta(days=30)) -> Dict[str, Any]:
        """
        Get analytics specific to recommendation performance.
        
        Args:
            time_window: Time window for analysis
            
        Returns:
            Dictionary containing recommendation analytics
        """
        try:
            cutoff_time = datetime.now() - time_window
            recent_behavior = [
                behavior for behavior in self.user_behavior_data
                if behavior['timestamp'] > cutoff_time and behavior['behavior_type'] == 'recommendation_view'
            ]
            
            if not recent_behavior:
                return {}
            
            # Recommendation types
            rec_types = [behavior['data'].get('type', 'unknown') for behavior in recent_behavior]
            type_counts = Counter(rec_types)
            
            # Click-through rates
            clicks = [behavior for behavior in recent_behavior if behavior['data'].get('clicked', False)]
            ctr = (len(clicks) / len(recent_behavior)) * 100 if recent_behavior else 0.0
            
            # User preferences
            user_preferences = []
            for behavior in recent_behavior:
                prefs = behavior['data'].get('user_preferences', [])
                user_preferences.extend(prefs)
            
            preference_counts = Counter(user_preferences)
            
            # Location-based performance
            locations = [behavior['data'].get('location', 'unknown') for behavior in recent_behavior]
            location_counts = Counter(locations)
            
            return {
                'total_recommendations': len(recent_behavior),
                'recommendation_types': dict(type_counts),
                'click_through_rate': ctr,
                'user_preferences': dict(preference_counts),
                'location_performance': dict(location_counts),
                'engagement_rate': ctr
            }
            
        except Exception as e:
            logger.error(f"Error getting recommendation analytics: {str(e)}")
            return {}
    
    def generate_insights_report(self, time_window: timedelta = timedelta(days=30)) -> Dict[str, Any]:
        """
        Generate comprehensive insights report.
        
        Args:
            time_window: Time window for analysis
            
        Returns:
            Dictionary containing comprehensive insights
        """
        try:
            report = {
                'generated_at': datetime.now().isoformat(),
                'time_window': str(time_window),
                'conversation_insights': self.get_conversation_insights(time_window),
                'user_engagement': self.get_user_engagement_metrics(time_window),
                'performance_metrics': self.get_performance_metrics(time_window),
                'language_analytics': self.get_language_analytics(time_window),
                'recommendation_analytics': self.get_recommendation_analytics(time_window),
                'key_findings': self._generate_key_findings(time_window),
                'recommendations': self._generate_recommendations(time_window)
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating insights report: {str(e)}")
            return {'error': str(e)}
    
    def _update_aggregated_stats(self, conversation_data: Dict[str, Any]):
        """Update aggregated statistics with new conversation data."""
        try:
            timestamp = conversation_data['timestamp']
            
            # Hourly stats
            hour_key = timestamp.strftime('%Y-%m-%d %H:00')
            self.hourly_stats[hour_key]['total_conversations'] += 1
            self.hourly_stats[hour_key]['languages'][conversation_data.get('language', 'en')] += 1
            
            # Daily stats
            day_key = timestamp.strftime('%Y-%m-%d')
            self.daily_stats[day_key]['total_conversations'] += 1
            self.daily_stats[day_key]['unique_users'].add(conversation_data.get('user_id', 'unknown'))
            
            # Weekly stats
            week_key = timestamp.strftime('%Y-W%U')
            self.weekly_stats[week_key]['total_conversations'] += 1
            
        except Exception as e:
            logger.error(f"Error updating aggregated stats: {str(e)}")
    
    def _cleanup_old_data(self):
        """Clean up old data based on retention policy."""
        try:
            cutoff_time = datetime.now() - timedelta(days=self.retention_days)
            
            # Clean conversation data
            self.conversation_data = [
                conv for conv in self.conversation_data
                if conv['timestamp'] > cutoff_time
            ]
            
            # Clean user behavior data
            self.user_behavior_data = [
                behavior for behavior in self.user_behavior_data
                if behavior['timestamp'] > cutoff_time
            ]
            
            # Clean performance data
            self.performance_data = [
                metric for metric in self.performance_data
                if metric['timestamp'] > cutoff_time
            ]
            
            # Clean metrics history
            for metric_name in list(self.metrics_history.keys()):
                self.metrics_history[metric_name] = [
                    metric for metric in self.metrics_history[metric_name]
                    if metric['timestamp'] > cutoff_time
                ]
                
                # Remove empty metric histories
                if not self.metrics_history[metric_name]:
                    del self.metrics_history[metric_name]
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {str(e)}")
    
    def _get_metric_unit(self, metric_name: str) -> str:
        """Get appropriate unit for a metric."""
        unit_mapping = {
            'response_time': 'ms',
            'accuracy': '%',
            'user_satisfaction': '/5',
            'conversation_count': 'conversations',
            'user_count': 'users',
            'error_rate': '%'
        }
        
        return unit_mapping.get(metric_name, 'units')
    
    def _generate_key_findings(self, time_window: timedelta) -> List[str]:
        """Generate key findings from analytics data."""
        try:
            findings = []
            
            # Get conversation insights
            conv_insights = self.get_conversation_insights(time_window)
            
            if conv_insights.total_conversations > 0:
                # Peak usage time
                if conv_insights.peak_hours:
                    peak_hour, count = conv_insights.peak_hours[0]
                    findings.append(f"Peak conversation time is {peak_hour}:00 with {count} conversations")
                
                # Language distribution
                if conv_insights.language_distribution:
                    top_language = max(conv_insights.language_distribution.items(), key=lambda x: x[1])
                    findings.append(f"Most popular language is {top_language[0]} ({top_language[1]} conversations)")
                
                # Satisfaction
                if conv_insights.user_satisfaction > 4.0:
                    findings.append("User satisfaction is high (above 4.0/5.0)")
                elif conv_insights.user_satisfaction < 3.0:
                    findings.append("User satisfaction needs improvement (below 3.0/5.0)")
            
            # Get performance metrics
            perf_metrics = self.get_performance_metrics(time_window=time_window)
            for metric in perf_metrics:
                if metric.trend == 'up' and metric.change > 10:
                    findings.append(f"{metric.name} is improving significantly (+{metric.change:.1f}%)")
                elif metric.trend == 'down' and metric.change < -10:
                    findings.append(f"{metric.name} needs attention (-{metric.change:.1f}%)")
            
            return findings[:5]  # Limit to top 5 findings
            
        except Exception as e:
            logger.error(f"Error generating key findings: {str(e)}")
            return []
    
    def _generate_recommendations(self, time_window: timedelta) -> List[str]:
        """Generate actionable recommendations based on analytics."""
        try:
            recommendations = []
            
            # Get conversation insights
            conv_insights = self.get_conversation_insights(time_window)
            
            if conv_insights.total_conversations > 0:
                # Completion rate
                if conv_insights.completion_rate < 70:
                    recommendations.append("Improve conversation completion rate by optimizing conversation flow")
                
                # Satisfaction
                if conv_insights.user_satisfaction < 3.5:
                    recommendations.append("Focus on improving user satisfaction through better responses and features")
                
                # Intent success
                low_success_intents = [
                    intent for intent, rate in conv_insights.intent_success_rate.items()
                    if rate < 80
                ]
                if low_success_intents:
                    recommendations.append(f"Improve intent recognition for: {', '.join(low_success_intents[:3])}")
            
            # Get user engagement
            engagement = self.get_user_engagement_metrics(time_window)
            if engagement:
                if engagement.get('return_rate', 0) < 30:
                    recommendations.append("Increase user return rate through better engagement strategies")
                
                if engagement.get('average_session_duration', 0) < 300:  # 5 minutes
                    recommendations.append("Extend user session duration with more engaging content")
            
            return recommendations[:5]  # Limit to top 5 recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return []
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get overall dashboard statistics."""
        return {
            'total_conversations': len(self.conversation_data),
            'total_users': len(set(behavior['user_id'] for behavior in self.user_behavior_data)),
            'total_metrics': len(self.performance_data),
            'data_retention_days': self.retention_days,
            'last_update': self.last_update.isoformat(),
            'metrics_tracked': list(self.metrics_history.keys())
        }