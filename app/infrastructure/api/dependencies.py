from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.application.security import SECRET_KEY, ALGORITHM
from app.application.dtos.usuario_dto import TokenData
from app.domain.services.usuario_service import UsuarioService
from app.infrastructure.persistence.database import get_db
from app.infrastructure.repositories.usuario_repository_impl import UsuarioRepositoryImpl

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=int(user_id))
        except JWTError:
            raise credentials_exception

        usuario_repository = UsuarioRepositoryImpl(db)
        usuario_service = UsuarioService(usuario_repository)

        usuario = usuario_service.obtener_usuario(token_data.user_id)
        if usuario is None:
            raise credentials_exception

        return usuario
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
