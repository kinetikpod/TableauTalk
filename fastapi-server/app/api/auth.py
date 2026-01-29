# from asyncpg import Connection
# from fastapi import Depends, Request, status, HTTPException
# from app.auth.schemas.user import UserOut
# from app.auth.services.auth import AuthService
# # from app.infra.postgres.repository import UserRepository
# from app.auth.repositories.user import UserRepository
# from app.infra.email.mailjet import EmailService
# from collections.abc import AsyncGenerator
# import jwt
# from app.core.config import settings
# # from infra.postgres.pool import db
# from app.infra.postgres.deps import get_db_conn


# # --------------------------------
# # User Repository
# # --------------------------------
# async def get_user_repo(
#     conn: Connection = Depends(get_db_conn),
# ) -> AsyncGenerator[UserRepository, None]:
#     yield UserRepository(conn)


# # --------------------------
# # Email service dependency
# # --------------------------
# def get_email_service() -> EmailService:
#     # singleton/simple instantiation
#     return EmailService()


# # -------------------------
# # Auth service dependency
# # -------------------------
# def get_auth_service(
#     user_repo: UserRepository = Depends(get_user_repo),
#     email_svc: EmailService = Depends(get_email_service),
# ) -> AuthService:
#     return AuthService(user_repo, email_svc)


# # -------------------------------------------
# #  Check current user in request for session
# # -------------------------------------------
# async def get_current_user(
#     request: Request,
#     conn: Connection = Depends(get_db_conn),
# ) -> UserOut:
#     # 1. Ambil token dari cookie
#     token = request.cookies.get("access_token")
#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated",
#         )

#     # 2. Decode & verifikasi JWT
#     try:
#         payload = jwt.decode(
#             token,
#             settings.SECRET_KEY,
#             algorithms=[settings.JWT_ALGORITHM],
#         )
#         user_id = int(payload.get("sub"))
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Token expired",
#         )
#     except jwt.InvalidTokenError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid token",
#         )

#     # 3. Query user lewat repository
#     repo = UserRepository(conn)
#     auth_user = await repo.get_by_id(user_id)
#     if not auth_user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found",
#         )

#     if not auth_user["is_active"]:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Access denied. Email verification required.",
#         )

#     user_dict = dict(auth_user)
#     return UserOut(**user_dict)


