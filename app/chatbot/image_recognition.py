"""
Image Recognition Component

Provides image recognition capabilities for identifying Sri Lankan landmarks,
tourist attractions, and cultural elements from uploaded images.
"""

import logging
import os
import tempfile
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import json
import hashlib
from datetime import datetime

try:
    import cv2
    import numpy as np
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False
    logging.warning("OpenCV not available, image recognition disabled")

try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow not available, advanced image recognition disabled")

try:
    from PIL import Image, ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL not available, image processing disabled")

logger = logging.getLogger(__name__)


class ImageRecognitionHandler:
    """
    Handles image recognition for Sri Lankan landmarks and tourist attractions.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the image recognition handler.
        
        Args:
            config: Configuration dictionary for image recognition settings
        """
        self.config = config or {}
        self.supported_formats = ['jpg', 'jpeg', 'png', 'bmp', 'tiff']
        self.max_file_size = self.config.get('max_file_size', 10 * 1024 * 1024)  # 10MB
        
        # Initialize image processing
        self.temp_dir = Path(tempfile.gettempdir()) / 'sri_lanka_chatbot_images'
        self.temp_dir.mkdir(exist_ok=True)
        
        # Landmark database
        self.landmarks = self._initialize_landmarks()
        
        # Feature extraction models
        self.feature_extractor = None
        if TENSORFLOW_AVAILABLE:
            self._initialize_feature_extractor()
        
        logger.info("Image Recognition Handler initialized successfully")
    
    def _initialize_landmarks(self) -> Dict:
        """Initialize the database of Sri Lankan landmarks."""
        return {
            'sigiriya': {
                'name': 'Sigiriya',
                'name_si': 'සීගිරිය',
                'name_ta': 'சிகிரியா',
                'description': 'Ancient palace and fortress complex',
                'description_si': 'පුරාණ රාජ මාලිගාවක් සහ බලකොටුවක්',
                'description_ta': 'பழைய அரண்மனை மற்றும் கோட்டை வளாகம்',
                'location': 'Central Province',
                'coordinates': (7.9570, 80.7603),
                'features': ['rock fortress', 'palace', 'frescoes', 'lion gate', 'water gardens'],
                'image_patterns': ['rock formation', 'ancient architecture', 'fortress walls'],
                'confidence_threshold': 0.7
            },
            'kandy_temple': {
                'name': 'Temple of the Sacred Tooth Relic',
                'name_si': 'ශ්‍රී දන්ත ධාතුන් වහන්සේගේ දේවාලය',
                'name_ta': 'தந்தம் கோவில்',
                'description': 'Sacred Buddhist temple housing the tooth relic',
                'description_si': 'ශ්‍රී දන්ත ධාතුන් වහන්සේගේ දේවාලය',
                'description_ta': 'தந்தம் கோவில்',
                'location': 'Kandy, Central Province',
                'coordinates': (7.2935, 80.6384),
                'features': ['buddhist temple', 'golden roof', 'traditional architecture', 'sacred relic'],
                'image_patterns': ['temple architecture', 'buddhist symbols', 'golden decorations'],
                'confidence_threshold': 0.75
            },
            'galle_fort': {
                'name': 'Galle Fort',
                'name_si': 'ගාල්ල කොටුව',
                'name_ta': 'காலி கோட்டை',
                'description': 'UNESCO World Heritage colonial fort',
                'description_si': 'යුනෙස්කෝ ලෝක උරුම තොටුපළ',
                'description_ta': 'யுனெஸ்கோ உலக பாரம்பரிய கோட்டை',
                'location': 'Galle, Southern Province',
                'coordinates': (6.0535, 80.2210),
                'features': ['colonial fort', 'dutch architecture', 'coastal fortification', 'lighthouse'],
                'image_patterns': ['fort walls', 'colonial buildings', 'coastal views', 'lighthouse'],
                'confidence_threshold': 0.8
            },
            'polonnaruwa': {
                'name': 'Polonnaruwa Ancient City',
                'name_si': 'පොළොන්නරුව පුරාණ නගරය',
                'name_ta': 'பொலன்னறுவை பழைய நகரம்',
                'description': 'Ancient capital with well-preserved ruins',
                'description_si': 'හොඳින් සංරක්ෂිත නටබුන් සහිත පුරාණ අගනුවර',
                'description_ta': 'நன்கு பாதுகாக்கப்பட்ட சிதிலங்களுடன் பழைய தலைநகரம்',
                'location': 'North Central Province',
                'coordinates': (7.9403, 81.0189),
                'features': ['ancient ruins', 'buddhist temples', 'archaeological site', 'stone carvings'],
                'image_patterns': ['stone ruins', 'ancient temples', 'archaeological remains'],
                'confidence_threshold': 0.7
            },
            'anuradhapura': {
                'name': 'Anuradhapura Sacred City',
                'name_si': 'අනුරාධපුර පූජනීය නගරය',
                'name_ta': 'அனுராதபுர புனித நகரம்',
                'description': 'Ancient Buddhist capital with sacred sites',
                'description_si': 'පූජනීය ස්ථාන සහිත පුරාණ බෞද්ධ අගනුවර',
                'description_ta': 'புனித இடங்களுடன் பழைய புத்த தலைநகரம்',
                'location': 'North Central Province',
                'coordinates': (8.3354, 80.3884),
                'features': ['sacred bo tree', 'ancient stupas', 'buddhist monasteries', 'sacred ponds'],
                'image_patterns': ['buddhist stupas', 'sacred trees', 'ancient monasteries'],
                'confidence_threshold': 0.75
            },
            'ella_rock': {
                'name': 'Ella Rock',
                'name_si': 'එල්ලා ගල',
                'name_ta': 'எல்லா பாறை',
                'description': 'Scenic mountain viewpoint and hiking destination',
                'description_si': 'සුන්දර කඳු දර්ශන සහ හයිකිං ගමනාන්තය',
                'description_ta': 'அழகான மலை காட்சி மற்றும் ஹைக்கிங் இடம்',
                'location': 'Ella, Uva Province',
                'coordinates': (6.8667, 81.0500),
                'features': ['mountain viewpoint', 'hiking trail', 'tea plantations', 'scenic views'],
                'image_patterns': ['mountain peaks', 'tea estates', 'hiking trails', 'scenic landscapes'],
                'confidence_threshold': 0.7
            },
            'mirissa_beach': {
                'name': 'Mirissa Beach',
                'name_si': 'මිරිස්ස වෙරළ',
                'name_ta': 'மிரிசா கடற்கரை',
                'description': 'Beautiful beach known for whale watching',
                'description_si': 'තල්මසුන් නැරඹීමට ප්‍රසිද්ධ සුන්දර වෙරළ',
                'description_ta': 'திமிங்கலங்களைப் பார்க்க பிரபலமான அழகான கடற்கரை',
                'location': 'Mirissa, Southern Province',
                'coordinates': (5.9435, 80.4584),
                'features': ['sandy beach', 'coconut palms', 'ocean views', 'whale watching'],
                'image_patterns': ['beach scenes', 'ocean views', 'coconut trees', 'coastal landscapes'],
                'confidence_threshold': 0.8
            }
        }
    
    def _initialize_feature_extractor(self):
        """Initialize the feature extraction model."""
        try:
            # Use a pre-trained model for feature extraction
            # In a production environment, you would load a custom-trained model
            if TENSORFLOW_AVAILABLE:
                # Placeholder for model initialization
                # self.feature_extractor = tf.keras.applications.ResNet50(
                #     include_top=False, 
                #     weights='imagenet'
                # )
                pass
        except Exception as e:
            logger.error(f"Error initializing feature extractor: {str(e)}")
    
    def process_image(self, image_file: str, language: str = 'en') -> Dict:
        """
        Process an uploaded image to identify landmarks.
        
        Args:
            image_file: Path to the image file
            language: Language for response ('en', 'si', 'ta')
            
        Returns:
            Dictionary containing recognition results
        """
        try:
            # Validate image file
            validation_result = self._validate_image(image_file)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['error'],
                    'landmarks': []
                }
            
            # Load and preprocess image
            image = self._load_image(image_file)
            if image is None:
                return {
                    'success': False,
                    'error': 'Could not load image',
                    'landmarks': []
                }
            
            # Extract features and analyze
            features = self._extract_features(image)
            analysis_result = self._analyze_image(features, image)
            
            # Get landmark matches
            landmarks = self._identify_landmarks(analysis_result, language)
            
            return {
                'success': True,
                'landmarks': landmarks,
                'image_analysis': analysis_result,
                'language': language,
                'processing_method': 'image_recognition'
            }
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'landmarks': []
            }
    
    def _validate_image(self, image_file: str) -> Dict:
        """
        Validate the uploaded image file.
        
        Args:
            image_file: Path to the image file
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Check if file exists
            if not os.path.exists(image_file):
                return {'valid': False, 'error': 'Image file not found'}
            
            # Check file size
            file_size = os.path.getsize(image_file)
            if file_size > self.max_file_size:
                return {
                    'valid': False, 
                    'error': f'File size too large. Maximum allowed: {self.max_file_size / (1024*1024):.1f}MB'
                }
            
            # Check file extension
            file_ext = Path(image_file).suffix.lower().lstrip('.')
            if file_ext not in self.supported_formats:
                return {
                    'valid': False, 
                    'error': f'Unsupported file format. Supported: {", ".join(self.supported_formats)}'
                }
            
            return {'valid': True, 'error': None}
            
        except Exception as e:
            return {'valid': False, 'error': f'Validation error: {str(e)}'}
    
    def _load_image(self, image_file: str) -> Optional[np.ndarray]:
        """
        Load and preprocess the image.
        
        Args:
            image_file: Path to the image file
            
        Returns:
            Preprocessed image array or None
        """
        try:
            if not OPENCV_AVAILABLE:
                return None
            
            # Load image using OpenCV
            image = cv2.imread(image_file)
            if image is None:
                return None
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize for processing (maintain aspect ratio)
            height, width = image.shape[:2]
            max_dim = 800
            if max(height, width) > max_dim:
                scale = max_dim / max(height, width)
                new_width = int(width * scale)
                new_height = int(height * scale)
                image = cv2.resize(image, (new_width, new_height))
            
            return image
            
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            return None
    
    def _extract_features(self, image: np.ndarray) -> Dict:
        """
        Extract features from the image for analysis.
        
        Args:
            image: Preprocessed image array
            
        Returns:
            Dictionary containing extracted features
        """
        features = {
            'basic_info': {},
            'color_analysis': {},
            'texture_features': {},
            'edge_features': {},
            'shape_features': {}
        }
        
        try:
            if image is None:
                return features
            
            # Basic image information
            height, width = image.shape[:2]
            features['basic_info'] = {
                'dimensions': (width, height),
                'aspect_ratio': width / height if height > 0 else 0,
                'total_pixels': width * height
            }
            
            # Color analysis
            features['color_analysis'] = self._analyze_colors(image)
            
            # Texture features
            features['texture_features'] = self._analyze_texture(image)
            
            # Edge features
            features['edge_features'] = self._analyze_edges(image)
            
            # Shape features
            features['shape_features'] = self._analyze_shapes(image)
            
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
        
        return features
    
    def _analyze_colors(self, image: np.ndarray) -> Dict:
        """Analyze color characteristics of the image."""
        try:
            # Convert to different color spaces
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Color statistics
            color_stats = {
                'dominant_colors': self._get_dominant_colors(image),
                'brightness': np.mean(gray),
                'contrast': np.std(gray),
                'saturation': np.mean(hsv[:, :, 1]),
                'hue_distribution': self._analyze_hue_distribution(hsv)
            }
            
            return color_stats
            
        except Exception as e:
            logger.error(f"Error analyzing colors: {str(e)}")
            return {}
    
    def _get_dominant_colors(self, image: np.ndarray, num_colors: int = 5) -> List:
        """Extract dominant colors from the image."""
        try:
            # Reshape image to 2D array of pixels
            pixels = image.reshape(-1, 3)
            
            # Use k-means to find dominant colors
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=num_colors, random_state=42)
            kmeans.fit(pixels)
            
            # Get cluster centers (dominant colors)
            dominant_colors = kmeans.cluster_centers_.astype(int)
            
            return dominant_colors.tolist()
            
        except ImportError:
            # Fallback: simple color analysis
            return self._simple_color_analysis(image)
        except Exception as e:
            logger.error(f"Error getting dominant colors: {str(e)}")
            return []
    
    def _simple_color_analysis(self, image: np.ndarray) -> List:
        """Simple color analysis fallback."""
        try:
            # Sample colors from different regions
            height, width = image.shape[:2]
            sample_points = [
                image[height//4, width//4],
                image[height//4, 3*width//4],
                image[3*height//4, width//4],
                image[3*height//4, 3*width//4],
                image[height//2, width//2]
            ]
            
            return [color.tolist() for color in sample_points]
            
        except Exception as e:
            logger.error(f"Error in simple color analysis: {str(e)}")
            return []
    
    def _analyze_hue_distribution(self, hsv_image: np.ndarray) -> Dict:
        """Analyze the distribution of hues in the image."""
        try:
            hue = hsv_image[:, :, 0]
            
            # Create hue histogram
            hist, bins = np.histogram(hue, bins=18, range=(0, 180))
            
            # Find dominant hue ranges
            dominant_hues = []
            for i, count in enumerate(hist):
                if count > np.mean(hist) + np.std(hist):
                    hue_range = (bins[i], bins[i+1])
                    dominant_hues.append({
                        'range': hue_range,
                        'count': int(count),
                        'percentage': float(count / np.sum(hist) * 100)
                    })
            
            return {
                'histogram': hist.tolist(),
                'dominant_hues': dominant_hues,
                'mean_hue': float(np.mean(hue)),
                'hue_variance': float(np.var(hue))
            }
            
        except Exception as e:
            logger.error(f"Error analyzing hue distribution: {str(e)}")
            return {}
    
    def _analyze_texture(self, image: np.ndarray) -> Dict:
        """Analyze texture characteristics of the image."""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Calculate texture features using GLCM-like approach
            texture_features = {
                'smoothness': self._calculate_smoothness(gray),
                'uniformity': self._calculate_uniformity(gray),
                'entropy': self._calculate_entropy(gray),
                'contrast': self._calculate_contrast(gray)
            }
            
            return texture_features
            
        except Exception as e:
            logger.error(f"Error analyzing texture: {str(e)}")
            return {}
    
    def _calculate_smoothness(self, gray_image: np.ndarray) -> float:
        """Calculate image smoothness."""
        try:
            # Apply Laplacian filter to detect edges
            laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
            variance = np.var(laplacian)
            smoothness = 1 / (1 + variance)
            return float(smoothness)
        except:
            return 0.0
    
    def _calculate_uniformity(self, gray_image: np.ndarray) -> float:
        """Calculate image uniformity."""
        try:
            hist, _ = np.histogram(gray_image, bins=256, range=(0, 256))
            hist = hist / np.sum(hist)
            uniformity = np.sum(hist ** 2)
            return float(uniformity)
        except:
            return 0.0
    
    def _calculate_entropy(self, gray_image: np.ndarray) -> float:
        """Calculate image entropy."""
        try:
            hist, _ = np.histogram(gray_image, bins=256, range=(0, 256))
            hist = hist / np.sum(hist)
            hist = hist[hist > 0]  # Remove zero probabilities
            entropy = -np.sum(hist * np.log2(hist))
            return float(entropy)
        except:
            return 0.0
    
    def _calculate_contrast(self, gray_image: np.ndarray) -> float:
        """Calculate image contrast."""
        try:
            return float(np.std(gray_image))
        except:
            return 0.0
    
    def _analyze_edges(self, image: np.ndarray) -> Dict:
        """Analyze edge characteristics of the image."""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Edge detection
            edges = cv2.Canny(gray, 50, 150)
            
            edge_features = {
                'edge_density': np.sum(edges > 0) / edges.size,
                'edge_direction': self._analyze_edge_direction(edges),
                'edge_strength': np.mean(edges[edges > 0]) if np.any(edges > 0) else 0
            }
            
            return edge_features
            
        except Exception as e:
            logger.error(f"Error analyzing edges: {str(e)}")
            return {}
    
    def _analyze_edge_direction(self, edges: np.ndarray) -> Dict:
        """Analyze the direction of edges in the image."""
        try:
            # Use Sobel operators to get gradients
            sobelx = cv2.Sobel(edges, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(edges, cv2.CV_64F, 0, 1, ksize=3)
            
            # Calculate gradient magnitude and direction
            magnitude = np.sqrt(sobelx**2 + sobely**2)
            direction = np.arctan2(sobely, sobelx)
            
            # Convert to degrees
            direction_deg = np.degrees(direction)
            
            # Analyze direction distribution
            hist, bins = np.histogram(direction_deg, bins=8, range=(-180, 180))
            
            return {
                'direction_histogram': hist.tolist(),
                'dominant_direction': float(direction_deg[np.argmax(magnitude)]),
                'direction_variance': float(np.var(direction_deg))
            }
            
        except Exception as e:
            logger.error(f"Error analyzing edge direction: {str(e)}")
            return {}
    
    def _analyze_shapes(self, image: np.ndarray) -> Dict:
        """Analyze shape characteristics of the image."""
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Find contours
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            shape_features = {
                'contour_count': len(contours),
                'largest_contour_area': 0,
                'average_contour_area': 0,
                'shape_complexity': 0
            }
            
            if contours:
                areas = [cv2.contourArea(contour) for contour in contours]
                shape_features['largest_contour_area'] = max(areas)
                shape_features['average_contour_area'] = np.mean(areas)
                
                # Calculate shape complexity (perimeter/area ratio)
                perimeters = [cv2.arcLength(contour, True) for contour in contours]
                complexity = [p / (a + 1e-6) for p, a in zip(perimeters, areas)]
                shape_features['shape_complexity'] = np.mean(complexity)
            
            return shape_features
            
        except Exception as e:
            logger.error(f"Error analyzing shapes: {str(e)}")
            return {}
    
    def _analyze_image(self, features: Dict, image: np.ndarray) -> Dict:
        """
        Analyze the image based on extracted features.
        
        Args:
            features: Extracted image features
            image: Original image array
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {
            'image_type': 'unknown',
            'landscape_type': 'unknown',
            'architectural_elements': [],
            'natural_elements': [],
            'cultural_indicators': [],
            'confidence': 0.0
        }
        
        try:
            # Determine image type based on features
            if features.get('edge_features', {}).get('edge_density', 0) > 0.1:
                analysis['image_type'] = 'structured'
                if features.get('shape_features', {}).get('contour_count', 0) > 10:
                    analysis['architectural_elements'].append('buildings')
                    analysis['architectural_elements'].append('structures')
            else:
                analysis['image_type'] = 'natural'
                analysis['natural_elements'].append('landscape')
                analysis['natural_elements'].append('nature')
            
            # Analyze color patterns for cultural indicators
            color_analysis = features.get('color_analysis', {})
            if color_analysis.get('dominant_colors'):
                # Check for traditional colors (gold, red, white)
                for color in color_analysis['dominant_colors']:
                    if self._is_traditional_color(color):
                        analysis['cultural_indicators'].append('traditional_colors')
                        break
            
            # Analyze texture for material identification
            texture = features.get('texture_features', {})
            if texture.get('smoothness', 0) > 0.7:
                analysis['architectural_elements'].append('smooth_surfaces')
            elif texture.get('roughness', 0) > 0.7:
                analysis['natural_elements'].append('rough_surfaces')
            
            # Calculate overall confidence
            analysis['confidence'] = self._calculate_analysis_confidence(features)
            
        except Exception as e:
            logger.error(f"Error analyzing image: {str(e)}")
        
        return analysis
    
    def _is_traditional_color(self, color: List[int]) -> bool:
        """Check if a color is traditionally associated with Sri Lankan culture."""
        r, g, b = color
        
        # Check for gold/yellow tones
        if r > 200 and g > 150 and b < 100:
            return True
        
        # Check for red tones (common in temples)
        if r > 150 and g < 100 and b < 100:
            return True
        
        # Check for white tones
        if r > 200 and g > 200 and b > 200:
            return True
        
        return False
    
    def _calculate_analysis_confidence(self, features: Dict) -> float:
        """Calculate confidence score for image analysis."""
        try:
            confidence = 0.0
            
            # Feature completeness
            if features.get('basic_info'):
                confidence += 0.2
            if features.get('color_analysis'):
                confidence += 0.2
            if features.get('texture_features'):
                confidence += 0.2
            if features.get('edge_features'):
                confidence += 0.2
            if features.get('shape_features'):
                confidence += 0.2
            
            # Quality indicators
            if features.get('basic_info', {}).get('total_pixels', 0) > 100000:
                confidence += 0.1
            
            if features.get('color_analysis', {}).get('contrast', 0) > 30:
                confidence += 0.1
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.0
    
    def _identify_landmarks(self, analysis: Dict, language: str = 'en') -> List[Dict]:
        """
        Identify landmarks based on image analysis.
        
        Args:
            analysis: Image analysis results
            language: Language for response
            
        Returns:
            List of identified landmarks with confidence scores
        """
        landmarks = []
        
        try:
            for landmark_id, landmark_info in self.landmarks.items():
                confidence = self._calculate_landmark_confidence(analysis, landmark_info)
                
                if confidence >= landmark_info['confidence_threshold']:
                    landmark_result = {
                        'id': landmark_id,
                        'name': landmark_info[f'name_{language}'] if f'name_{language}' in landmark_info else landmark_info['name'],
                        'description': landmark_info[f'description_{language}'] if f'description_{language}' in landmark_info else landmark_info['description'],
                        'location': landmark_info['location'],
                        'coordinates': landmark_info['coordinates'],
                        'confidence': confidence,
                        'features_matched': self._get_matched_features(analysis, landmark_info)
                    }
                    landmarks.append(landmark_result)
            
            # Sort by confidence (highest first)
            landmarks.sort(key=lambda x: x['confidence'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error identifying landmarks: {str(e)}")
        
        return landmarks
    
    def _calculate_landmark_confidence(self, analysis: Dict, landmark_info: Dict) -> float:
        """Calculate confidence score for a specific landmark."""
        try:
            confidence = 0.0
            
            # Check image type compatibility
            if analysis.get('image_type') == 'structured' and 'architectural' in landmark_info['features']:
                confidence += 0.3
            elif analysis.get('image_type') == 'natural' and 'natural' in landmark_info['features']:
                confidence += 0.3
            
            # Check for architectural elements
            architectural_elements = analysis.get('architectural_elements', [])
            if any(elem in landmark_info['image_patterns'] for elem in architectural_elements):
                confidence += 0.2
            
            # Check for natural elements
            natural_elements = analysis.get('natural_elements', [])
            if any(elem in landmark_info['image_patterns'] for elem in natural_elements):
                confidence += 0.2
            
            # Check cultural indicators
            cultural_indicators = analysis.get('cultural_indicators', [])
            if cultural_indicators:
                confidence += 0.1
            
            # Base confidence from analysis
            confidence += analysis.get('confidence', 0.0) * 0.2
            
            return min(confidence, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating landmark confidence: {str(e)}")
            return 0.0
    
    def _get_matched_features(self, analysis: Dict, landmark_info: Dict) -> List[str]:
        """Get list of features that matched between analysis and landmark."""
        matched_features = []
        
        try:
            # Check architectural elements
            architectural_elements = analysis.get('architectural_elements', [])
            for elem in architectural_elements:
                if elem in landmark_info['image_patterns']:
                    matched_features.append(elem)
            
            # Check natural elements
            natural_elements = analysis.get('natural_elements', [])
            for elem in natural_elements:
                if elem in landmark_info['image_patterns']:
                    matched_features.append(elem)
            
            # Check cultural indicators
            cultural_indicators = analysis.get('cultural_indicators', [])
            for indicator in cultural_indicators:
                if indicator in landmark_info['image_patterns']:
                    matched_features.append(indicator)
                    
        except Exception as e:
            logger.error(f"Error getting matched features: {str(e)}")
        
        return matched_features
    
    def get_supported_landmarks(self, language: str = 'en') -> List[Dict]:
        """Get list of supported landmarks in specified language."""
        landmarks = []
        
        for landmark_id, landmark_info in self.landmarks.items():
            landmark_data = {
                'id': landmark_id,
                'name': landmark_info[f'name_{language}'] if f'name_{language}' in landmark_info else landmark_info['name'],
                'description': landmark_info[f'description_{language}'] if f'description_{language}' in landmark_info else landmark_info['description'],
                'location': landmark_info['location'],
                'coordinates': landmark_info['coordinates']
            }
            landmarks.append(landmark_data)
        
        return landmarks
    
    def get_landmark_info(self, landmark_id: str, language: str = 'en') -> Optional[Dict]:
        """Get detailed information about a specific landmark."""
        if landmark_id in self.landmarks:
            landmark_info = self.landmarks[landmark_id]
            return {
                'id': landmark_id,
                'name': landmark_info[f'name_{language}'] if f'name_{language}' in landmark_info else landmark_info['name'],
                'description': landmark_info[f'description_{language}'] if f'description_{language}' in landmark_info else landmark_info['description'],
                'location': landmark_info['location'],
                'coordinates': landmark_info['coordinates'],
                'features': landmark_info['features'],
                'image_patterns': landmark_info['image_patterns']
            }
        return None
    
    def cleanup_temp_files(self):
        """Clean up temporary image files."""
        try:
            for file_path in self.temp_dir.glob("*"):
                file_path.unlink()
                logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {str(e)}")
    
    def get_recognition_stats(self) -> Dict:
        """Get statistics about image recognition capabilities."""
        return {
            'opencv_available': OPENCV_AVAILABLE,
            'tensorflow_available': TENSORFLOW_AVAILABLE,
            'pil_available': PIL_AVAILABLE,
            'supported_formats': self.supported_formats,
            'max_file_size': self.max_file_size,
            'landmarks_count': len(self.landmarks),
            'temp_directory': str(self.temp_dir)
        }