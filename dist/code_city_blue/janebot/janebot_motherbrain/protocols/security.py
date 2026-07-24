"""
Security Manager - Handles authentication and payload validation for the swarm.
Ensures only authorized agents can join and that all network traffic is well-formed.
"""

import secrets
import logging
from typing import Dict, Any, Optional, Set
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ValidationSchema:
    """Defines expected types for payload fields."""
    fields: Dict[str, type]

class SecurityManager:
    """
    Manages swarm security, including token-based authentication 
    and strict payload validation to prevent adversarial injection.
    """
    
    def __init__(self):
        # In a production environment, this would be backed by a persistent store or Vault
        self._authorized_tokens: Set[str] = set()
        self._token_metadata: Dict[str, Dict[str, Any]] = {}
        logger.info("SecurityManager initialized")

    def generate_token(self, agent_id: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Generates a secure token for an agent to use during the handshake."""
        token = secrets.token_urlsafe(32)
        self._authorized_tokens.add(token)
        self._token_metadata[token] = {
            "agent_id": agent_id,
            "metadata": metadata or {},
            "issued_at": secrets.token_hex(4) # Simplified timestamp
        }
        logger.info(f"Generated join token for agent: {agent_id}")
        return token

    def validate_token(self, token: str) -> Optional[str]:
        """
        Validates a token and returns the associated agent_id if successful.
        Returns None if the token is invalid or unauthorized.
        """
        if token in self._authorized_tokens:
            agent_id = self._token_metadata[token].get("agent_id")
            logger.info(f"Token validated for agent: {agent_id}")
            return agent_id
        
        logger.warning("Unauthorized join attempt: Invalid token provided")
        return None

    def invalidate_token(self, token: str):
        """Removes a token from the authorized set."""
        self._authorized_tokens.discard(token)
        self._token_metadata.pop(token, None)

    def validate_payload(self, payload: Any, schema: Optional[ValidationSchema] = None) -> bool:
        """
        Strictly validates the payload structure and types.
        Designed to prevent 'Brown Team' crashes via malformed JSON or type mismatch.
        """
        if not isinstance(payload, dict):
            logger.error("Payload validation failed: Payload must be a dictionary")
            return False

        if schema:
            for field, expected_type in schema.fields.items():
                if field not in payload:
                    logger.error(f"Payload validation failed: Missing required field '{field}'")
                    return False
                if not isinstance(payload[field], expected_type):
                    logger.error(
                        f"Payload validation failed: Field '{field}' expected {expected_type}, "
                        f"got {type(payload[field])}"
                    )
                    return False
        
        return True

    def rotate_tokens(self):
        """Invalidates all current tokens to force a re-handshake across the swarm."""
        self._authorized_tokens.clear()
        self._token_metadata.clear()
        logger.info("All swarm join tokens rotated")
