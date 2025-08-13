"""
Security Manager Component

Implements multi-factor authentication (MFA) and security features for the tourism chatbot.
Supports TOTP, SMS, email, and biometric authentication methods.
"""

import logging
import secrets
import hashlib
import time
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

try:
    import pyotp
    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False
    logging.warning("PyOTP not available, TOTP authentication disabled")

try:
    import qrcode
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False
    logging.warning("QRCode not available, QR code generation disabled")

logger = logging.getLogger(__name__)


class MFAMethod(Enum):
    """Supported MFA methods."""
    TOTP = "totp"
    SMS = "sms"
    EMAIL = "email"
    BIOMETRIC = "biometric"
    BACKUP_CODES = "backup_codes"


class SecurityLevel(Enum):
    """Security levels for different user types."""
    LOW = "low"           # Tourist users
    MEDIUM = "medium"     # Guide users
    HIGH = "high"         # Admin users
    CRITICAL = "critical" # System administrators


@dataclass
class MFASetup:
    """MFA setup information for a user."""
    user_id: str
    method: MFAMethod
    secret: Optional[str] = None
    qr_code_url: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    backup_codes: List[str] = None
    is_active: bool = False
    created_at: datetime = None
    last_used: Optional[datetime] = None


@dataclass
class SecurityEvent:
    """Security event log entry."""
    event_id: str
    user_id: str
    event_type: str
    description: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = None
    severity: str = "info"


class SecurityManager:
    """
    Comprehensive security manager for the tourism chatbot.
    Implements MFA, session management, and security monitoring.
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the security manager.
        
        Args:
            config: Configuration dictionary for security settings
        """
        self.config = config or {}
        
        # Security settings
        self.max_failed_attempts = self.config.get('max_failed_attempts', 5)
        self.lockout_duration = self.config.get('lockout_duration', 1800)  # 30 minutes
        self.session_timeout = self.config.get('session_timeout', 3600)    # 1 hour
        self.mfa_required_for_admin = self.config.get('mfa_required_for_admin', True)
        
        # User security data
        self.user_mfa_setups = {}
        self.user_security_status = {}
        self.failed_attempts = {}
        self.locked_users = {}
        self.security_events = []
        
        # MFA method configurations
        self.mfa_methods = {
            MFAMethod.TOTP: {
                'name': 'Time-based One-Time Password',
                'security_level': SecurityLevel.HIGH,
                'user_experience': 'Good',
                'implementation_effort': 'Medium',
                'cost': 'Low'
            },
            MFAMethod.SMS: {
                'name': 'SMS Verification',
                'security_level': SecurityLevel.MEDIUM,
                'user_experience': 'Excellent',
                'implementation_effort': 'Low',
                'cost': 'Medium'
            },
            MFAMethod.EMAIL: {
                'name': 'Email Verification',
                'security_level': SecurityLevel.MEDIUM,
                'user_experience': 'Good',
                'implementation_effort': 'Low',
                'cost': 'Low'
            },
            MFAMethod.BIOMETRIC: {
                'name': 'Biometric Authentication',
                'security_level': SecurityLevel.HIGH,
                'user_experience': 'Excellent',
                'implementation_effort': 'High',
                'cost': 'Medium'
            },
            MFAMethod.BACKUP_CODES: {
                'name': 'Backup Codes',
                'security_level': SecurityLevel.MEDIUM,
                'user_experience': 'Good',
                'implementation_effort': 'Low',
                'cost': 'Low'
            }
        }
        
        logger.info("Security Manager initialized successfully")
    
    def setup_mfa(self, user_id: str, method: MFAMethod, 
                  additional_data: Dict = None) -> Dict:
        """
        Setup MFA for a user.
        
        Args:
            user_id: Unique user identifier
            method: MFA method to setup
            additional_data: Additional data needed for the method
            
        Returns:
            Dictionary containing setup information
        """
        try:
            if method not in self.mfa_methods:
                raise ValueError(f"Unsupported MFA method: {method}")
            
            # Create MFA setup
            mfa_setup = MFASetup(
                user_id=user_id,
                method=method,
                created_at=datetime.now()
            )
            
            if method == MFAMethod.TOTP:
                setup_info = self._setup_totp(user_id, mfa_setup)
            elif method == MFAMethod.SMS:
                setup_info = self._setup_sms(user_id, mfa_setup, additional_data)
            elif method == MFAMethod.EMAIL:
                setup_info = self._setup_email(user_id, mfa_setup, additional_data)
            elif method == MFAMethod.BIOMETRIC:
                setup_info = self._setup_biometric(user_id, mfa_setup, additional_data)
            elif method == MFAMethod.BACKUP_CODES:
                setup_info = self._setup_backup_codes(user_id, mfa_setup)
            else:
                raise ValueError(f"Unsupported MFA method: {method}")
            
            # Store MFA setup
            if user_id not in self.user_mfa_setups:
                self.user_mfa_setups[user_id] = []
            
            self.user_mfa_setups[user_id].append(mfa_setup)
            
            # Log security event
            self._log_security_event(
                user_id=user_id,
                event_type="mfa_setup",
                description=f"MFA setup initiated for method: {method.value}",
                severity="info"
            )
            
            return setup_info
            
        except Exception as e:
            logger.error(f"Error setting up MFA for user {user_id}: {str(e)}")
            raise SecurityException(f"MFA setup failed: {str(e)}")
    
    def _setup_totp(self, user_id: str, mfa_setup: MFASetup) -> Dict:
        """Setup TOTP authentication."""
        if not PYOTP_AVAILABLE:
            raise SecurityException("TOTP library not available")
        
        try:
            # Generate secret key
            secret = pyotp.random_base32()
            
            # Create TOTP object
            totp = pyotp.TOTP(secret)
            
            # Generate QR code URL for easy setup
            qr_code_url = totp.provisioning_uri(
                name=user_id,
                issuer_name="Sri Lanka Tourism Chatbot"
            )
            
            # Update MFA setup
            mfa_setup.secret = secret
            mfa_setup.qr_code_url = qr_code_url
            
            # Generate backup codes
            backup_codes = self._generate_backup_codes()
            mfa_setup.backup_codes = backup_codes
            
            return {
                'method': 'totp',
                'secret': secret,
                'qr_code_url': qr_code_url,
                'backup_codes': backup_codes,
                'setup_instructions': self._get_totp_setup_instructions()
            }
            
        except Exception as e:
            logger.error(f"TOTP setup error: {str(e)}")
            raise SecurityException("TOTP setup failed")
    
    def _setup_sms(self, user_id: str, mfa_setup: MFASetup, 
                   additional_data: Dict) -> Dict:
        """Setup SMS authentication."""
        try:
            phone_number = additional_data.get('phone_number')
            if not phone_number:
                raise ValueError("Phone number required for SMS MFA")
            
            # Validate phone number format
            if not self._validate_phone_number(phone_number):
                raise ValueError("Invalid phone number format")
            
            # Update MFA setup
            mfa_setup.phone_number = phone_number
            
            # Send verification code
            verification_code = self._generate_verification_code()
            self._send_sms(phone_number, verification_code)
            
            # Store verification code temporarily
            self._store_verification_code(user_id, verification_code)
            
            return {
                'method': 'sms',
                'phone_number': phone_number,
                'verification_sent': True,
                'setup_instructions': self._get_sms_setup_instructions()
            }
            
        except Exception as e:
            logger.error(f"SMS setup error: {str(e)}")
            raise SecurityException("SMS setup failed")
    
    def _setup_email(self, user_id: str, mfa_setup: MFASetup, 
                    additional_data: Dict) -> Dict:
        """Setup email authentication."""
        try:
            email = additional_data.get('email')
            if not email:
                raise ValueError("Email required for email MFA")
            
            # Validate email format
            if not self._validate_email(email):
                raise ValueError("Invalid email format")
            
            # Update MFA setup
            mfa_setup.email = email
            
            # Send verification code
            verification_code = self._generate_verification_code()
            self._send_email(email, verification_code)
            
            # Store verification code temporarily
            self._store_verification_code(user_id, verification_code)
            
            return {
                'method': 'email',
                'email': email,
                'verification_sent': True,
                'setup_instructions': self._get_email_setup_instructions()
            }
            
        except Exception as e:
            logger.error(f"Email setup error: {str(e)}")
            raise SecurityException("Email setup failed")
    
    def _setup_biometric(self, user_id: str, mfa_setup: MFASetup, 
                         additional_data: Dict) -> Dict:
        """Setup biometric authentication."""
        try:
            # This is a placeholder for biometric setup
            # In production, integrate with actual biometric hardware/software
            
            return {
                'method': 'biometric',
                'setup_instructions': self._get_biometric_setup_instructions(),
                'status': 'pending_hardware_verification'
            }
            
        except Exception as e:
            logger.error(f"Biometric setup error: {str(e)}")
            raise SecurityException("Biometric setup failed")
    
    def _setup_backup_codes(self, user_id: str, mfa_setup: MFASetup) -> Dict:
        """Setup backup codes."""
        try:
            backup_codes = self._generate_backup_codes()
            mfa_setup.backup_codes = backup_codes
            
            return {
                'method': 'backup_codes',
                'backup_codes': backup_codes,
                'setup_instructions': self._get_backup_codes_instructions()
            }
            
        except Exception as e:
            logger.error(f"Backup codes setup error: {str(e)}")
            raise SecurityException("Backup codes setup failed")
    
    def verify_mfa(self, user_id: str, method: MFAMethod, 
                   code: str, additional_data: Dict = None) -> bool:
        """
        Verify MFA code for a user.
        
        Args:
            user_id: Unique user identifier
            method: MFA method to verify
            code: Verification code
            additional_data: Additional data for verification
            
        Returns:
            True if verification successful, False otherwise
        """
        try:
            # Check if user is locked
            if self._is_user_locked(user_id):
                logger.warning(f"User {user_id} is locked, MFA verification blocked")
                return False
            
            # Get user's MFA setup
            mfa_setup = self._get_user_mfa_setup(user_id, method)
            if not mfa_setup:
                logger.warning(f"No MFA setup found for user {user_id} with method {method}")
                return False
            
            # Verify based on method
            if method == MFAMethod.TOTP:
                is_valid = self._verify_totp_code(mfa_setup, code)
            elif method == MFAMethod.SMS:
                is_valid = self._verify_sms_code(user_id, code)
            elif method == MFAMethod.EMAIL:
                is_valid = self._verify_email_code(user_id, code)
            elif method == MFAMethod.BIOMETRIC:
                is_valid = self._verify_biometric(mfa_setup, additional_data)
            elif method == MFAMethod.BACKUP_CODES:
                is_valid = self._verify_backup_code(mfa_setup, code)
            else:
                logger.error(f"Unsupported MFA method for verification: {method}")
                return False
            
            if is_valid:
                # Update last used timestamp
                mfa_setup.last_used = datetime.now()
                
                # Reset failed attempts
                self._reset_failed_attempts(user_id)
                
                # Log successful verification
                self._log_security_event(
                    user_id=user_id,
                    event_type="mfa_verification_success",
                    description=f"Successful MFA verification using {method.value}",
                    severity="info"
                )
                
                return True
            else:
                # Increment failed attempts
                self._increment_failed_attempts(user_id)
                
                # Log failed verification
                self._log_security_event(
                    user_id=user_id,
                    event_type="mfa_verification_failed",
                    description=f"Failed MFA verification using {method.value}",
                    severity="warning"
                )
                
                return False
                
        except Exception as e:
            logger.error(f"Error verifying MFA for user {user_id}: {str(e)}")
            return False
    
    def _verify_totp_code(self, mfa_setup: MFASetup, code: str) -> bool:
        """Verify TOTP code."""
        try:
            if not mfa_setup.secret:
                return False
            
            totp = pyotp.TOTP(mfa_setup.secret)
            
            # Verify code with tolerance for time drift
            return totp.verify(code, valid_window=1)
            
        except Exception as e:
            logger.error(f"TOTP verification error: {str(e)}")
            return False
    
    def _verify_sms_code(self, user_id: str, code: str) -> bool:
        """Verify SMS verification code."""
        try:
            stored_code = self._get_verification_code(user_id)
            if not stored_code:
                return False
            
            if code == stored_code:
                # Clear verification code after successful use
                self._clear_verification_code(user_id)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"SMS verification error: {str(e)}")
            return False
    
    def _verify_email_code(self, user_id: str, code: str) -> bool:
        """Verify email verification code."""
        try:
            stored_code = self._get_verification_code(user_id)
            if not stored_code:
                return False
            
            if code == stored_code:
                # Clear verification code after successful use
                self._clear_verification_code(user_id)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Email verification error: {str(e)}")
            return False
    
    def _verify_biometric(self, mfa_setup: MFASetup, additional_data: Dict) -> bool:
        """Verify biometric authentication."""
        try:
            # This is a placeholder for biometric verification
            # In production, integrate with actual biometric verification
            
            biometric_data = additional_data.get('biometric_data')
            if not biometric_data:
                return False
            
            # Placeholder verification logic
            return True
            
        except Exception as e:
            logger.error(f"Biometric verification error: {str(e)}")
            return False
    
    def _verify_backup_code(self, mfa_setup: MFASetup, code: str) -> bool:
        """Verify backup code."""
        try:
            if not mfa_setup.backup_codes:
                return False
            
            if code in mfa_setup.backup_codes:
                # Remove used backup code
                mfa_setup.backup_codes.remove(code)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Backup code verification error: {str(e)}")
            return False
    
    def _generate_verification_code(self) -> str:
        """Generate a 6-digit verification code."""
        return str(secrets.randbelow(1000000)).zfill(6)
    
    def _generate_backup_codes(self, count: int = 10) -> List[str]:
        """Generate backup codes for account recovery."""
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()
            codes.append(f"{code[:4]}-{code[4:8]}")
        return codes
    
    def _validate_phone_number(self, phone_number: str) -> bool:
        """Validate phone number format."""
        # Basic validation - in production, use a proper phone number library
        import re
        pattern = r'^\+?1?\d{9,15}$'
        return bool(re.match(pattern, phone_number))
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _send_sms(self, phone_number: str, code: str):
        """Send SMS with verification code."""
        # Placeholder for SMS sending
        # In production, integrate with SMS service provider
        logger.info(f"SMS verification code {code} sent to {phone_number}")
    
    def _send_email(self, email: str, code: str):
        """Send email with verification code."""
        # Placeholder for email sending
        # In production, integrate with email service provider
        logger.info(f"Email verification code {code} sent to {email}")
    
    def _store_verification_code(self, user_id: str, code: str):
        """Store verification code temporarily."""
        # In production, use secure storage with expiration
        if user_id not in self._verification_codes:
            self._verification_codes = {}
        self._verification_codes[user_id] = {
            'code': code,
            'expires_at': datetime.now() + timedelta(minutes=10)
        }
    
    def _get_verification_code(self, user_id: str) -> Optional[str]:
        """Get stored verification code."""
        if user_id in self._verification_codes:
            code_data = self._verification_codes[user_id]
            if datetime.now() < code_data['expires_at']:
                return code_data['code']
            else:
                # Code expired, remove it
                del self._verification_codes[user_id]
        return None
    
    def _clear_verification_code(self, user_id: str):
        """Clear verification code after use."""
        if user_id in self._verification_codes:
            del self._verification_codes[user_id]
    
    def _get_user_mfa_setup(self, user_id: str, method: MFAMethod) -> Optional[MFASetup]:
        """Get user's MFA setup for a specific method."""
        if user_id in self.user_mfa_setups:
            for setup in self.user_mfa_setups[user_id]:
                if setup.method == method and setup.is_active:
                    return setup
        return None
    
    def _increment_failed_attempts(self, user_id: str):
        """Increment failed authentication attempts."""
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = 0
        
        self.failed_attempts[user_id] += 1
        
        # Check if user should be locked
        if self.failed_attempts[user_id] >= self.max_failed_attempts:
            self._lock_user(user_id)
    
    def _reset_failed_attempts(self, user_id: str):
        """Reset failed authentication attempts."""
        if user_id in self.failed_attempts:
            del self.failed_attempts[user_id]
    
    def _lock_user(self, user_id: str):
        """Lock user account due to too many failed attempts."""
        self.locked_users[user_id] = datetime.now()
        
        # Log security event
        self._log_security_event(
            user_id=user_id,
            event_type="user_locked",
            description="User account locked due to multiple failed MFA attempts",
            severity="warning"
        )
    
    def _is_user_locked(self, user_id: str) -> bool:
        """Check if user account is locked."""
        if user_id in self.locked_users:
            lock_time = self.locked_users[user_id]
            if datetime.now() - lock_time < timedelta(seconds=self.lockout_duration):
                return True
            else:
                # Lock expired, remove it
                del self.locked_users[user_id]
        return False
    
    def _log_security_event(self, user_id: str, event_type: str, 
                           description: str, severity: str = "info",
                           ip_address: str = None, user_agent: str = None):
        """Log security event."""
        event = SecurityEvent(
            event_id=secrets.token_hex(16),
            user_id=user_id,
            event_type=event_type,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now(),
            severity=severity
        )
        
        self.security_events.append(event)
        
        # Keep only last 1000 events
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]
    
    def get_user_mfa_status(self, user_id: str) -> Dict:
        """Get user's MFA status."""
        try:
            if user_id not in self.user_mfa_setups:
                return {'mfa_enabled': False, 'methods': []}
            
            methods = []
            for setup in self.user_mfa_setups[user_id]:
                if setup.is_active:
                    methods.append({
                        'method': setup.method.value,
                        'name': self.mfa_methods[setup.method]['name'],
                        'security_level': setup.method.value,
                        'last_used': setup.last_used.isoformat() if setup.last_used else None
                    })
            
            return {
                'mfa_enabled': len(methods) > 0,
                'methods': methods,
                'total_methods': len(methods)
            }
            
        except Exception as e:
            logger.error(f"Error getting MFA status for user {user_id}: {str(e)}")
            return {'mfa_enabled': False, 'methods': [], 'error': str(e)}
    
    def get_security_events(self, user_id: str = None, 
                           event_type: str = None, 
                           limit: int = 100) -> List[Dict]:
        """Get security events with optional filtering."""
        try:
            events = self.security_events
            
            if user_id:
                events = [e for e in events if e.user_id == user_id]
            
            if event_type:
                events = [e for e in events if e.event_type == event_type]
            
            # Sort by timestamp (newest first)
            events.sort(key=lambda x: x.timestamp, reverse=True)
            
            # Limit results
            events = events[:limit]
            
            return [
                {
                    'event_id': e.event_id,
                    'user_id': e.user_id,
                    'event_type': e.event_type,
                    'description': e.description,
                    'ip_address': e.ip_address,
                    'user_agent': e.user_agent,
                    'timestamp': e.timestamp.isoformat(),
                    'severity': e.severity
                }
                for e in events
            ]
            
        except Exception as e:
            logger.error(f"Error getting security events: {str(e)}")
            return []
    
    def get_security_stats(self) -> Dict:
        """Get security statistics."""
        try:
            total_users = len(self.user_mfa_setups)
            users_with_mfa = sum(1 for setups in self.user_mfa_setups.values() 
                               if any(s.is_active for s in setups))
            
            total_events = len(self.security_events)
            recent_events = len([e for e in self.security_events 
                               if e.timestamp > datetime.now() - timedelta(hours=24)])
            
            locked_users = len(self.locked_users)
            
            return {
                'total_users': total_users,
                'users_with_mfa': users_with_mfa,
                'mfa_adoption_rate': (users_with_mfa / total_users * 100) if total_users > 0 else 0,
                'total_security_events': total_events,
                'recent_security_events_24h': recent_events,
                'locked_users': locked_users,
                'security_status': 'healthy' if locked_users < total_users * 0.1 else 'warning'
            }
            
        except Exception as e:
            logger.error(f"Error getting security stats: {str(e)}")
            return {'error': str(e)}
    
    def _get_totp_setup_instructions(self) -> str:
        """Get TOTP setup instructions."""
        return """
        To setup TOTP authentication:
        1. Install an authenticator app (Google Authenticator, Authy, etc.)
        2. Scan the QR code with your authenticator app
        3. Enter the 6-digit code from your app to verify
        4. Save your backup codes in a secure location
        """
    
    def _get_sms_setup_instructions(self) -> str:
        """Get SMS setup instructions."""
        return """
        To setup SMS authentication:
        1. Enter your phone number
        2. Check your phone for the verification code
        3. Enter the 6-digit code to verify
        4. SMS authentication will be enabled
        """
    
    def _get_email_setup_instructions(self) -> str:
        """Get email setup instructions."""
        return """
        To setup email authentication:
        1. Enter your email address
        2. Check your email for the verification code
        3. Enter the 6-digit code to verify
        4. Email authentication will be enabled
        """
    
    def _get_biometric_setup_instructions(self) -> str:
        """Get biometric setup instructions."""
        return """
        To setup biometric authentication:
        1. Ensure your device supports biometric authentication
        2. Follow the device-specific setup process
        3. Complete biometric enrollment
        4. Biometric authentication will be enabled
        """
    
    def _get_backup_codes_instructions(self) -> str:
        """Get backup codes instructions."""
        return """
        Backup codes are generated for account recovery:
        1. Save these codes in a secure location
        2. Each code can only be used once
        3. Use these codes if you lose access to other MFA methods
        4. Generate new codes if you run out
        """


class SecurityException(Exception):
    """Custom exception for security-related errors."""
    pass


# Initialize verification codes storage
_verification_codes = {}