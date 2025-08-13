"""
Advanced Voice Assistant Component

Provides continuous voice conversation, emotion detection, voice biometrics,
and advanced voice processing capabilities for Phase 3 of the chatbot.
"""

import logging
import asyncio
import threading
import queue
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import numpy as np
from datetime import datetime, timedelta

try:
    import pyaudio
    import wave
    import librosa
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    logging.warning("PyAudio not available, advanced voice features disabled")

try:
    from scipy import signal
    from scipy.stats import entropy
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logging.warning("SciPy not available, advanced audio processing disabled")

logger = logging.getLogger(__name__)


class VoiceState(Enum):
    """Voice assistant states."""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"
    ERROR = "error"


class EmotionType(Enum):
    """Detected emotion types."""
    HAPPY = "happy"
    EXCITED = "excited"
    CALM = "calm"
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    NEUTRAL = "neutral"


@dataclass
class VoiceCommand:
    """Voice command structure."""
    text: str
    confidence: float
    language: str
    emotion: EmotionType
    timestamp: datetime
    audio_features: Dict[str, Any]
    user_id: Optional[str] = None


@dataclass
class VoiceResponse:
    """Voice response structure."""
    text: str
    audio_file: Optional[str]
    emotion: EmotionType
    should_listen: bool
    priority: int = 1


class AdvancedVoiceAssistant:
    """
    Advanced voice assistant with continuous listening, emotion detection,
    and intelligent conversation management.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the advanced voice assistant.
        
        Args:
            config: Configuration dictionary for voice settings
        """
        self.config = config or {}
        self.state = VoiceState.IDLE
        self.is_listening = False
        self.audio_queue = queue.Queue()
        self.response_queue = queue.Queue()
        
        # Audio settings
        self.sample_rate = self.config.get('sample_rate', 16000)
        self.chunk_size = self.config.get('chunk_size', 1024)
        self.channels = self.config.get('channels', 1)
        self.format = pyaudio.paFloat32
        
        # Voice processing
        self.voice_activity_detector = VoiceActivityDetector()
        self.emotion_detector = EmotionDetector()
        self.voice_biometrics = VoiceBiometrics()
        
        # Conversation management
        self.conversation_history = []
        self.user_profiles = {}
        self.active_conversations = {}
        
        # Callbacks
        self.on_command_detected: Optional[Callable] = None
        self.on_emotion_changed: Optional[Callable] = None
        self.on_user_identified: Optional[Callable] = None
        
        # Threading
        self.audio_thread = None
        self.processing_thread = None
        self.stop_event = threading.Event()
        
        logger.info("Advanced Voice Assistant initialized successfully")
    
    def start_listening(self, user_id: str = None) -> bool:
        """
        Start continuous voice listening.
        
        Args:
            user_id: Optional user ID for personalized experience
            
        Returns:
            True if started successfully, False otherwise
        """
        if self.is_listening:
            logger.warning("Voice assistant is already listening")
            return False
        
        if not PYAUDIO_AVAILABLE:
            logger.error("PyAudio not available for voice listening")
            return False
        
        try:
            self.is_listening = True
            self.state = VoiceState.LISTENING
            self.stop_event.clear()
            
            # Start audio capture thread
            self.audio_thread = threading.Thread(
                target=self._audio_capture_loop,
                args=(user_id,),
                daemon=True
            )
            self.audio_thread.start()
            
            # Start processing thread
            self.processing_thread = threading.Thread(
                target=self._processing_loop,
                daemon=True
            )
            self.processing_thread.start()
            
            logger.info("Voice assistant started listening")
            return True
            
        except Exception as e:
            logger.error(f"Error starting voice assistant: {str(e)}")
            self.is_listening = False
            self.state = VoiceState.ERROR
            return False
    
    def stop_listening(self):
        """Stop voice listening and processing."""
        if not self.is_listening:
            return
        
        self.is_listening = False
        self.stop_event.set()
        self.state = VoiceState.IDLE
        
        # Wait for threads to finish
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join(timeout=2)
        
        if self.processing_thread and self.processing_thread.is_alive():
            self.processing_thread.join(timeout=2)
        
        logger.info("Voice assistant stopped listening")
    
    def _audio_capture_loop(self, user_id: str = None):
        """Main audio capture loop."""
        try:
            audio = pyaudio.PyAudio()
            stream = audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            logger.info("Audio stream opened successfully")
            
            while self.is_listening and not self.stop_event.is_set():
                try:
                    # Read audio data
                    audio_data = stream.read(self.chunk_size, exception_on_overflow=False)
                    
                    # Convert to numpy array
                    audio_array = np.frombuffer(audio_data, dtype=np.float32)
                    
                    # Check for voice activity
                    if self.voice_activity_detector.detect_voice(audio_array):
                        # Capture voice segment
                        voice_segment = self._capture_voice_segment(stream, audio_array)
                        
                        if voice_segment is not None:
                            # Add to processing queue
                            self.audio_queue.put((voice_segment, user_id))
                    
                    time.sleep(0.01)  # Small delay to prevent CPU overload
                    
                except Exception as e:
                    logger.error(f"Error in audio capture: {str(e)}")
                    break
            
            # Cleanup
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
        except Exception as e:
            logger.error(f"Error in audio capture loop: {str(e)}")
            self.state = VoiceState.ERROR
    
    def _capture_voice_segment(self, stream, initial_chunk: np.ndarray) -> Optional[np.ndarray]:
        """Capture a complete voice segment."""
        try:
            voice_chunks = [initial_chunk]
            silence_frames = 0
            max_silence_frames = int(0.5 * self.sample_rate / self.chunk_size)  # 0.5 seconds
            
            while silence_frames < max_silence_frames:
                try:
                    audio_data = stream.read(self.chunk_size, exception_on_overflow=False)
                    audio_array = np.frombuffer(audio_data, dtype=np.float32)
                    
                    if self.voice_activity_detector.detect_voice(audio_array):
                        voice_chunks.append(audio_array)
                        silence_frames = 0
                    else:
                        silence_frames += 1
                    
                except Exception:
                    break
            
            if len(voice_chunks) > 1:
                return np.concatenate(voice_chunks)
            
            return None
            
        except Exception as e:
            logger.error(f"Error capturing voice segment: {str(e)}")
            return None
    
    def _processing_loop(self):
        """Main audio processing loop."""
        while self.is_listening and not self.stop_event.is_set():
            try:
                # Get audio data from queue
                try:
                    voice_segment, user_id = self.audio_queue.get(timeout=1.0)
                except queue.Empty:
                    continue
                
                self.state = VoiceState.PROCESSING
                
                # Process voice segment
                voice_command = self._process_voice_segment(voice_segment, user_id)
                
                if voice_command:
                    # Add to conversation history
                    self.conversation_history.append(voice_command)
                    
                    # Trigger callback if set
                    if self.on_command_detected:
                        self.on_command_detected(voice_command)
                    
                    # Generate response
                    response = self._generate_voice_response(voice_command)
                    
                    if response:
                        self.response_queue.put(response)
                
                self.state = VoiceState.LISTENING
                
            except Exception as e:
                logger.error(f"Error in processing loop: {str(e)}")
                self.state = VoiceState.ERROR
    
    def _process_voice_segment(self, voice_segment: np.ndarray, user_id: str = None) -> Optional[VoiceCommand]:
        """Process a voice segment and extract command information."""
        try:
            # Extract audio features
            audio_features = self._extract_audio_features(voice_segment)
            
            # Detect emotion
            emotion = self.emotion_detector.detect_emotion(audio_features)
            
            # Identify user (if not already identified)
            if user_id is None:
                user_id = self.voice_biometrics.identify_user(audio_features)
            
            # Convert speech to text (placeholder - integrate with your STT)
            text = self._speech_to_text(voice_segment)
            
            if text:
                return VoiceCommand(
                    text=text,
                    confidence=audio_features.get('confidence', 0.8),
                    language=audio_features.get('detected_language', 'en'),
                    emotion=emotion,
                    timestamp=datetime.now(),
                    audio_features=audio_features,
                    user_id=user_id
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing voice segment: {str(e)}")
            return None
    
    def _extract_audio_features(self, audio_data: np.ndarray) -> Dict[str, Any]:
        """Extract comprehensive audio features for analysis."""
        try:
            features = {}
            
            # Basic features
            features['duration'] = len(audio_data) / self.sample_rate
            features['rms_energy'] = np.sqrt(np.mean(audio_data**2))
            features['zero_crossing_rate'] = np.sum(np.diff(np.sign(audio_data))) / len(audio_data)
            
            # Spectral features
            if SCIPY_AVAILABLE:
                # Mel-frequency cepstral coefficients (MFCC)
                mfcc = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=13)
                features['mfcc_mean'] = np.mean(mfcc, axis=1).tolist()
                features['mfcc_std'] = np.std(mfcc, axis=1).tolist()
                
                # Spectral features
                spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=self.sample_rate)[0]
                features['spectral_centroid_mean'] = float(np.mean(spectral_centroids))
                features['spectral_centroid_std'] = float(np.std(spectral_centroids))
                
                # Pitch features
                pitches, magnitudes = librosa.piptrack(y=audio_data, sr=self.sample_rate)
                features['pitch_mean'] = float(np.mean(pitches[magnitudes > 0.1]))
                features['pitch_std'] = float(np.std(pitches[magnitudes > 0.1]))
            
            # Voice quality features
            features['confidence'] = self._calculate_voice_confidence(audio_data)
            features['detected_language'] = self._detect_language_from_audio(audio_data)
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting audio features: {str(e)}")
            return {'confidence': 0.5, 'detected_language': 'en'}
    
    def _calculate_voice_confidence(self, audio_data: np.ndarray) -> float:
        """Calculate confidence score for voice quality."""
        try:
            # Simple confidence calculation based on signal quality
            rms = np.sqrt(np.mean(audio_data**2))
            zero_crossings = np.sum(np.diff(np.sign(audio_data))) / len(audio_data)
            
            # Normalize and combine metrics
            rms_score = min(rms * 10, 1.0)  # RMS should be reasonable
            zc_score = 1.0 - abs(zero_crossings - 0.1)  # Zero crossings should be moderate
            
            confidence = (rms_score + zc_score) / 2
            return max(0.0, min(1.0, confidence))
            
        except Exception:
            return 0.5
    
    def _detect_language_from_audio(self, audio_data: np.ndarray) -> str:
        """Detect language from audio characteristics (simplified)."""
        try:
            # This is a simplified language detection
            # In production, use proper language detection models
            
            # Extract pitch and rhythm characteristics
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=self.sample_rate)
            pitch_mean = np.mean(pitches[magnitudes > 0.1])
            
            # Simple heuristics based on pitch characteristics
            if pitch_mean > 200:  # Higher pitch
                return 'si'  # Sinhala tends to have higher pitch
            elif pitch_mean > 150:
                return 'ta'  # Tamil
            else:
                return 'en'  # English
            
        except Exception:
            return 'en'
    
    def _speech_to_text(self, audio_data: np.ndarray) -> str:
        """Convert speech to text (placeholder implementation)."""
        try:
            # This is a placeholder - integrate with your actual STT service
            # For now, return a sample response based on audio characteristics
            
            duration = len(audio_data) / self.sample_rate
            
            if duration < 1.0:
                return "Hello"
            elif duration < 2.0:
                return "How can I help you?"
            else:
                return "Tell me more about your question"
            
        except Exception as e:
            logger.error(f"Error in speech to text: {str(e)}")
            return ""
    
    def _generate_voice_response(self, voice_command: VoiceCommand) -> Optional[VoiceResponse]:
        """Generate appropriate voice response based on command."""
        try:
            # Analyze command and generate response
            response_text = self._analyze_command_and_respond(voice_command)
            
            if response_text:
                return VoiceResponse(
                    text=response_text,
                    audio_file=None,  # Will be generated by TTS
                    emotion=voice_command.emotion,
                    should_listen=True,
                    priority=1
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating voice response: {str(e)}")
            return None
    
    def _analyze_command_and_respond(self, voice_command: VoiceCommand) -> str:
        """Analyze voice command and generate appropriate response."""
        try:
            text = voice_command.text.lower()
            
            # Simple response logic - integrate with your main chatbot
            if 'hello' in text or 'hi' in text:
                return "Hello! Welcome to Sri Lanka. How can I help you today?"
            elif 'weather' in text:
                return "I'd be happy to tell you about the weather. Which city are you interested in?"
            elif 'sigiriya' in text or 'sigiriya' in text:
                return "Sigiriya is a magnificent ancient palace and fortress. Would you like to know about visiting times or directions?"
            elif 'help' in text:
                return "I can help you with attractions, weather, directions, and cultural information. What would you like to know?"
            else:
                return "I heard you say something about " + text + ". Could you please repeat that more clearly?"
            
        except Exception as e:
            logger.error(f"Error analyzing command: {str(e)}")
            return "I'm sorry, I didn't understand that. Could you please repeat?"
    
    def get_conversation_history(self, user_id: str = None, limit: int = 10) -> List[VoiceCommand]:
        """Get conversation history for a user."""
        if user_id:
            return [cmd for cmd in self.conversation_history if cmd.user_id == user_id][-limit:]
        return self.conversation_history[-limit:]
    
    def get_user_emotion_trend(self, user_id: str, time_window: timedelta = timedelta(hours=1)) -> Dict[EmotionType, int]:
        """Get emotion trend for a user over time."""
        try:
            cutoff_time = datetime.now() - time_window
            recent_commands = [
                cmd for cmd in self.conversation_history
                if cmd.user_id == user_id and cmd.timestamp > cutoff_time
            ]
            
            emotion_counts = {}
            for emotion in EmotionType:
                emotion_counts[emotion] = sum(1 for cmd in recent_commands if cmd.emotion == emotion)
            
            return emotion_counts
            
        except Exception as e:
            logger.error(f"Error getting emotion trend: {str(e)}")
            return {}
    
    def set_callbacks(self, on_command_detected: Callable = None, 
                      on_emotion_changed: Callable = None,
                      on_user_identified: Callable = None):
        """Set callback functions for various events."""
        self.on_command_detected = on_command_detected
        self.on_emotion_changed = on_emotion_changed
        self.on_user_identified = on_user_identified
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the voice assistant."""
        return {
            'state': self.state.value,
            'is_listening': self.is_listening,
            'conversation_count': len(self.conversation_history),
            'active_users': len(set(cmd.user_id for cmd in self.conversation_history if cmd.user_id)),
            'audio_queue_size': self.audio_queue.qsize(),
            'response_queue_size': self.response_queue.qsize()
        }


class VoiceActivityDetector:
    """Detects voice activity in audio streams."""
    
    def __init__(self):
        self.energy_threshold = 0.01
        self.silence_threshold = 0.005
        self.min_voice_duration = 0.1  # seconds
    
    def detect_voice(self, audio_chunk: np.ndarray) -> bool:
        """Detect if audio chunk contains voice activity."""
        try:
            energy = np.sqrt(np.mean(audio_chunk**2))
            return energy > self.energy_threshold
        except Exception:
            return False


class EmotionDetector:
    """Detects emotions from voice characteristics."""
    
    def __init__(self):
        self.emotion_models = self._initialize_emotion_models()
    
    def detect_emotion(self, audio_features: Dict[str, Any]) -> EmotionType:
        """Detect emotion from audio features."""
        try:
            # Simple emotion detection based on audio characteristics
            # In production, use trained ML models
            
            pitch_mean = audio_features.get('pitch_mean', 150)
            rms_energy = audio_features.get('rms_energy', 0.1)
            spectral_centroid = audio_features.get('spectral_centroid_mean', 1000)
            
            # Emotion classification logic
            if rms_energy > 0.2 and pitch_mean > 200:
                return EmotionType.EXCITED
            elif rms_energy > 0.15 and spectral_centroid > 1500:
                return EmotionType.HAPPY
            elif rms_energy < 0.05:
                return EmotionType.CALM
            elif pitch_mean < 100:
                return EmotionType.FRUSTRATED
            else:
                return EmotionType.NEUTRAL
                
        except Exception:
            return EmotionType.NEUTRAL
    
    def _initialize_emotion_models(self) -> Dict[str, Any]:
        """Initialize emotion detection models (placeholder)."""
        return {}


class VoiceBiometrics:
    """Handles voice-based user identification."""
    
    def __init__(self):
        self.user_voice_profiles = {}
    
    def identify_user(self, audio_features: Dict[str, Any]) -> Optional[str]:
        """Identify user from voice characteristics."""
        try:
            # Simple user identification based on pitch characteristics
            # In production, use proper voice biometrics
            
            pitch_mean = audio_features.get('pitch_mean', 150)
            
            # Match with existing profiles
            for user_id, profile in self.user_voice_profiles.items():
                if abs(profile['pitch_mean'] - pitch_mean) < 20:
                    return user_id
            
            # Create new profile if no match
            user_id = f"user_{len(self.user_voice_profiles) + 1}"
            self.user_voice_profiles[user_id] = {
                'pitch_mean': pitch_mean,
                'created_at': datetime.now()
            }
            
            return user_id
            
        except Exception:
            return None
    
    def update_user_profile(self, user_id: str, audio_features: Dict[str, Any]):
        """Update user voice profile."""
        try:
            if user_id in self.user_voice_profiles:
                profile = self.user_voice_profiles[user_id]
                profile['pitch_mean'] = (profile['pitch_mean'] + audio_features.get('pitch_mean', 150)) / 2
                profile['updated_at'] = datetime.now()
        except Exception as e:
            logger.error(f"Error updating user profile: {str(e)}")