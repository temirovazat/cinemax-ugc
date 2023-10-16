import logging
from http import HTTPStatus
from typing import Dict
from uuid import UUID, uuid4

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError

from core.config import CONFIG

security = HTTPBearer(auto_error=not CONFIG.fastapi.debug)


class AuthService:
    """Service class for user authentication."""

    def __init__(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Upon class initialization, it accepts an HTTP request header with a JWT token.

        Args:
            credentials: HTTP authorization header with a token
        """
        if credentials:
            self.token = credentials.credentials
        else:
            self.token = jwt.encode({'user_id': str(uuid4())}, key=CONFIG.fastapi.secret_key, algorithm='HS256')

    @property
    def user_id(self) -> UUID:
        """Property with the user ID from the token claims.

        Raises:
            HTTPException: Identification error

        Returns:
            UUID: Unique user identifier
        """
        claims = self.decode_token()
        if not (user_id := claims.get('user_id')):
            logging.critical('Problem with user identification: No user ID in the token!')
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return user_id

    def decode_token(self) -> Dict:
        """Decode the JWT token.

        Raises:
            HTTPException: Authorization error

        Returns:
            Dict: Token content
        """
        try:
            payload = jwt.decode(self.token, key=CONFIG.fastapi.secret_key, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
        except Exception as exc:
            logging.error('Problem with user authentication: {exc}!'.format(exc=exc))
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return payload
