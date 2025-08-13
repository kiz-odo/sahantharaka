"""
Speech Handler Component

Provides speech-to-text and text-to-speech capabilities for the multilingual
tourism chatbot, supporting Sinhala, Tamil, and English.
"""

import logging
import tempfile
import os
from typing import Dict, List, Optional, Tuple, BinaryIO
from pathlib import Path
import json

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    logging.warning("SpeechRecognition not available, speech-to-text disabled")

try:
    from gtts import gTTS
    from gtts.lang import tts_langs
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    logging.warning("gTTS not available, text-to-speech disabled")

try:
    from pydub import AudioSegment
    from pydub.playback import play
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    logging.warning("pydub not available, audio playback disabled")

logger = logging.getLogger(__name__)


class SpeechHandler:
    """
    Handles speech-to-text and text-to-speech operations for multiple languages.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the speech handler.
        
        Args:
            config: Configuration dictionary for speech settings
        """
        self.config = config or {}
        self.supported_languages = {
            'en': 'en',
            'si': 'si',  # Sinhala
            'ta': 'ta'   # Tamil
        }
        
        # Initialize speech recognition
        self.recognizer = None
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self._configure_recognizer()
        
        # Audio settings
        self.audio_format = self.config.get('audio_format', 'mp3')
        self.audio_quality = self.config.get('audio_quality', 'high')
        self.temp_dir = Path(tempfile.gettempdir()) / 'sri_lanka_chatbot'
        self.temp_dir.mkdir(exist_ok=True)
        
        logger.info("Speech Handler initialized successfully")
    
    def _configure_recognizer(self):
        """Configure speech recognition settings."""
        if self.recognizer:
            # Adjust for ambient noise
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Language-specific configurations
            self.recognizer.phrase_threshold = 0.3
            self.recognizer.non_speaking_duration = 0.5
    
    def speech_to_text(self, audio_data: BinaryIO, language: str = 'en') -> Dict:
        """
        Convert speech audio to text.
        
        Args:
            audio_data: Audio file or data
            language: Expected language code
            
        Returns:
            Dictionary containing transcription and metadata
        """
        try:
            if not SPEECH_RECOGNITION_AVAILABLE:
                return {
                    'success': False,
                    'error': 'Speech recognition not available',
                    'transcription': None
                }
            
            # Convert language code to recognizer format
            recognizer_lang = self._get_recognizer_language(language)
            
            # Perform speech recognition
            with sr.AudioFile(audio_data) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.record(source)
                
                # Try multiple recognition methods
                transcription = self._recognize_speech(audio, recognizer_lang)
                
                if transcription:
                    return {
                        'success': True,
                        'transcription': transcription,
                        'language': language,
                        'confidence': 0.8,  # Placeholder confidence
                        'method': 'speech_recognition'
                    }
                else:
                    return {
                        'success': False,
                        'error': 'Could not transcribe audio',
                        'transcription': None
                    }
                    
        except Exception as e:
            logger.error(f"Error in speech-to-text: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'transcription': None
            }
    
    def _recognize_speech(self, audio, language: str) -> Optional[str]:
        """
        Attempt speech recognition using multiple methods.
        
        Args:
            audio: Audio data from recognizer
            language: Language code for recognition
            
        Returns:
            Transcribed text or None
        """
        # Method 1: Google Speech Recognition
        try:
            transcription = self.recognizer.recognize_google(
                audio, 
                language=language,
                show_all=False
            )
            if transcription:
                return transcription
        except sr.UnknownValueError:
            logger.debug("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.warning(f"Google Speech Recognition service error: {e}")
        
        # Method 2: Sphinx (offline, English only)
        if language == 'en':
            try:
                transcription = self.recognizer.recognize_sphinx(audio)
                if transcription:
                    return transcription
            except sr.UnknownValueError:
                logger.debug("Sphinx could not understand audio")
            except Exception as e:
                logger.debug(f"Sphinx recognition error: {e}")
        
        # Method 3: Try with different language variants
        if language == 'si':
            # Try with broader Sinhala recognition
            try:
                transcription = self.recognizer.recognize_google(
                    audio, 
                    language='si-LK',
                    show_all=False
                )
                if transcription:
                    return transcription
            except:
                pass
        
        elif language == 'ta':
            # Try with broader Tamil recognition
            try:
                transcription = self.recognizer.recognize_google(
                    audio, 
                    language='ta-IN',
                    show_all=False
                )
                if transcription:
                    return transcription
            except:
                pass
        
        return None
    
    def text_to_speech(self, text: str, language: str = 'en', 
                       save_to_file: bool = False) -> Dict:
        """
        Convert text to speech audio.
        
        Args:
            text: Text to convert to speech
            language: Language code for speech synthesis
            save_to_file: Whether to save audio to file
            
        Returns:
            Dictionary containing audio data and metadata
        """
        try:
            if not GTTS_AVAILABLE:
                return {
                    'success': False,
                    'error': 'Text-to-speech not available',
                    'audio_file': None
                }
            
            # Get language code for TTS
            tts_lang = self._get_tts_language(language)
            
            # Create TTS object
            tts = gTTS(text=text, lang=tts_lang, slow=False)
            
            if save_to_file:
                # Save to temporary file
                audio_file = self._save_audio_file(tts, text, language)
                return {
                    'success': True,
                    'audio_file': str(audio_file),
                    'language': language,
                    'text_length': len(text),
                    'method': 'gtts'
                }
            else:
                # Return audio data directly
                audio_data = self._get_audio_data(tts)
                return {
                    'success': True,
                    'audio_data': audio_data,
                    'language': language,
                    'text_length': len(text),
                    'method': 'gtts'
                }
                
        except Exception as e:
            logger.error(f"Error in text-to-speech: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'audio_file': None
            }
    
    def _get_tts_language(self, language: str) -> str:
        """
        Get the appropriate TTS language code.
        
        Args:
            language: Language code from chatbot
            
        Returns:
            TTS language code
        """
        # Map chatbot language codes to TTS language codes
        tts_language_map = {
            'en': 'en',
            'si': 'si',  # Sinhala
            'ta': 'ta'   # Tamil
        }
        
        return tts_language_map.get(language, 'en')
    
    def _save_audio_file(self, tts: gTTS, text: str, language: str) -> Path:
        """
        Save TTS audio to a temporary file.
        
        Args:
            tts: gTTS object
            text: Original text
            language: Language code
            
        Returns:
            Path to saved audio file
        """
        # Create filename based on content hash
        import hashlib
        text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        filename = f"speech_{language}_{text_hash}.{self.audio_format}"
        filepath = self.temp_dir / filename
        
        # Save audio file
        tts.save(str(filepath))
        
        logger.debug(f"Audio saved to: {filepath}")
        return filepath
    
    def _get_audio_data(self, tts: gTTS) -> bytes:
        """
        Get audio data directly from TTS object.
        
        Args:
            tts: gTTS object
            
        Returns:
            Audio data as bytes
        """
        # Create temporary file and read data
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            tts.save(temp_file.name)
            temp_file.seek(0)
            audio_data = temp_file.read()
        
        # Clean up temporary file
        os.unlink(temp_file.name)
        
        return audio_data
    
    def play_audio(self, audio_file: str) -> bool:
        """
        Play audio file using system audio player.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            True if playback successful, False otherwise
        """
        try:
            if not PYDUB_AVAILABLE:
                # Fallback to system command
                return self._play_audio_system(audio_file)
            
            # Load and play audio using pydub
            audio = AudioSegment.from_file(audio_file)
            play(audio)
            return True
            
        except Exception as e:
            logger.error(f"Error playing audio: {str(e)}")
            # Try system fallback
            return self._play_audio_system(audio_file)
    
    def _play_audio_system(self, audio_file: str) -> bool:
        """
        Play audio using system commands.
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            True if playback successful, False otherwise
        """
        try:
            import subprocess
            import platform
            
            system = platform.system()
            
            if system == "Darwin":  # macOS
                subprocess.run(["afplay", audio_file], check=True)
            elif system == "Linux":
                subprocess.run(["aplay", audio_file], check=True)
            elif system == "Windows":
                subprocess.run(["start", audio_file], shell=True, check=True)
            else:
                logger.warning(f"Unknown system: {system}, cannot play audio")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"System audio playback failed: {str(e)}")
            return False
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get dictionary of supported languages for speech."""
        return self.supported_languages.copy()
    
    def is_speech_available(self) -> bool:
        """Check if speech recognition is available."""
        return SPEECH_RECOGNITION_AVAILABLE
    
    def is_tts_available(self) -> bool:
        """Check if text-to-speech is available."""
        return GTTS_AVAILABLE
    
    def is_audio_playback_available(self) -> bool:
        """Check if audio playback is available."""
        return PYDUB_AVAILABLE or True  # System playback always available
    
    def get_audio_formats(self) -> List[str]:
        """Get list of supported audio formats."""
        return ['mp3', 'wav', 'ogg']
    
    def cleanup_temp_files(self):
        """Clean up temporary audio files."""
        try:
            for file_path in self.temp_dir.glob("speech_*"):
                file_path.unlink()
                logger.debug(f"Cleaned up temporary file: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up temp files: {str(e)}")
    
    def get_speech_stats(self) -> Dict:
        """Get statistics about speech processing capabilities."""
        return {
            'speech_recognition': SPEECH_RECOGNITION_AVAILABLE,
            'text_to_speech': GTTS_AVAILABLE,
            'audio_playback': PYDUB_AVAILABLE,
            'supported_languages': list(self.supported_languages.keys()),
            'audio_formats': self.get_audio_formats(),
            'temp_directory': str(self.temp_dir),
            'config': self.config
        }
    
    def _get_recognizer_language(self, language: str) -> str:
        """
        Get the appropriate language code for speech recognition.
        
        Args:
            language: Language code from chatbot
            
        Returns:
            Recognizer language code
        """
        # Map chatbot language codes to recognizer language codes
        recognizer_language_map = {
            'en': 'en-US',
            'si': 'si-LK',  # Sinhala (Sri Lanka)
            'ta': 'ta-IN'   # Tamil (India)
        }
        
        return recognizer_language_map.get(language, 'en-US')
    
    def process_voice_message(self, audio_file: str, expected_language: str = 'en') -> Dict:
        """
        Process a voice message: convert to text and return response.
        
        Args:
            audio_file: Path to audio file
            expected_language: Expected language of the message
            
        Returns:
            Dictionary containing transcription and processing results
        """
        try:
            # Open audio file for processing
            with open(audio_file, 'rb') as audio_data:
                # Convert speech to text
                stt_result = self.speech_to_text(audio_data, expected_language)
                
                if stt_result['success']:
                    return {
                        'success': True,
                        'transcription': stt_result['transcription'],
                        'language': stt_result['language'],
                        'confidence': stt_result['confidence'],
                        'audio_file': audio_file,
                        'processing_method': 'speech_to_text'
                    }
                else:
                    return {
                        'success': False,
                        'error': stt_result['error'],
                        'audio_file': audio_file,
                        'processing_method': 'speech_to_text'
                    }
                    
        except Exception as e:
            logger.error(f"Error processing voice message: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'audio_file': audio_file,
                'processing_method': 'voice_processing'
            }
    
    def create_voice_response(self, text: str, language: str, 
                             save_to_file: bool = True) -> Dict:
        """
        Create a voice response from text.
        
        Args:
            text: Text to convert to speech
            language: Language for speech synthesis
            save_to_file: Whether to save to file
            
        Returns:
            Dictionary containing voice response data
        """
        # Convert text to speech
        tts_result = self.text_to_speech(text, language, save_to_file)
        
        if tts_result['success']:
            return {
                'success': True,
                'text': text,
                'language': language,
                'audio_file': tts_result.get('audio_file'),
                'audio_data': tts_result.get('audio_data'),
                'text_length': len(text),
                'processing_method': 'text_to_speech'
            }
        else:
            return {
                'success': False,
                'error': tts_result['error'],
                'text': text,
                'language': language,
                'processing_method': 'text_to_speech'
            }