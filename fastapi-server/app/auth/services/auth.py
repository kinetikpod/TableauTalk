from datetime import datetime, timedelta, timezone
import secrets
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    set_auth_cookie,
)
from fastapi import BackgroundTasks, HTTPException, status, Response
from app.infra.email.mailjet import EmailService
from app.core.config import settings
from app.auth.schemas.auth import MessageResponse
from app.auth.schemas.user import UserOut
from app.auth.repositories.user import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository, email_svc: EmailService):
        self.user_repo = user_repo
        self.email_svc = email_svc

    # =======================================================
    # Registrasi user baru
    async def signup(
        self, *, name: str, email: str, password: str, tasks: BackgroundTasks
    ) -> MessageResponse:
        # 1. Pastikan email belum digunakan
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email sudah terdaftar",
            )

        # 2. Hash password sebelum disimpan
        hashed = hash_password(password)

        # 3. Simpan data user ke database
        user_id = await self.user_repo.create_user(name, email, hashed)

        # 4. Buat token verifikasi email

        # code or OTP
        token_otp = f"{secrets.randbelow(10**6):06d}"
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.EMAIL_VERIFICATION_TOKEN_TTL_MINUTES
        )

        await self.user_repo.save_verification_token(user_id, token_otp, expires_at)

        # 5. Kirim email verifikasi secara async di background
        tasks.add_task(self.email_svc.send_verification_email, email, token_otp)

        # 6. kirim akses token via cookie

        return MessageResponse(
            message="Signup berhasil. Silakan verifikasi email Anda."
        )

    # =======================================================
    # Verifikasi token email
    async def verify_email_token(
        self, token: str, tasks: BackgroundTasks, response: Response
    ) -> UserOut:
        # 1. Ambil informasi token dari database
        record = await self.user_repo.get_user_by_verification_token(token)
        if not record:
            raise HTTPException(status_code=400, detail="Token tidak valid")

        # 2. Cek apakah token sudah kedaluwarsa
        if record["expires_at"] < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Token telah kedaluwarsa")

        # 3. Aktifkan user
        await self.user_repo.activate_user(record["user_id"])

        # 4. Hapus token dari database demi keamanan
        await self.user_repo.delete_verification_token(token)

        # 5. Kirim email selamat datang secara async di background
        tasks.add_task(
            self.email_svc.send_welcome_email, record["email"], record["name"]
        )

        # record["is_active"] = True  # di database udah true,di memori belum
        access_token = create_access_token(record["user_id"])
        set_auth_cookie(response, access_token)

        return UserOut(
            id=record["user_id"],
            name=record["name"],
            email=record["email"],
            is_active=True,
        )

    # =======================================================
    # Login
    async def signin(self, email: str, password: str, response: Response) -> UserOut:
        user = await self.user_repo.get_by_email(email)

        if not user or not user["is_active"]:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not verify_password(password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(user["id"])
        set_auth_cookie(response, access_token)

        return UserOut(
            id=user["id"],
            name=user["name"],
            email=user["email"],
            is_active=user["is_active"],
        )

    # =======================================================
    # Permintaan reset password
    async def request_password_reset(
        self, email: str, tasks: BackgroundTasks
    ) -> MessageResponse:
        user = await self.user_repo.get_by_email(email)

        # Token dan email dikirim hanya jika user terdaftar
        if user:
            reset_token = secrets.token_urlsafe(32)
            expires_at = datetime.now(timezone.utc) + timedelta(
                minutes=settings.EMAIL_VERIFICATION_TOKEN_TTL_MINUTES
            )
            await self.user_repo.save_password_reset_token(
                user["id"], reset_token, expires_at
            )

            reset_link = f"{settings.CLIENT_URL}/reset-password/{reset_token}"

            tasks.add_task(self.email_svc.send_password_reset_email, email, reset_link)

        # Pesan tetap sama untuk menjaga keamanan (gak terlalu eksplisit)
        return MessageResponse(
            message="If the account is registered, you will receive a password reset email."
        )

    # =======================================================
    # Proses reset password
    async def reset_password(
        self, token: str, new_password: str, tasks: BackgroundTasks
    ) -> MessageResponse:
        # 1. Validasi token reset password
        record = await self.user_repo.get_user_by_password_reset_token(token)
        if not record or record["expires_at"] < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=400, detail="Invalid or expired reset link."
            )

        # 2. Hash password baru
        hashed = hash_password(new_password)

        # 3. Update password di database
        await self.user_repo.update_user_password(record["user_id"], hashed)

        # 4. Hapus token reset dari database
        await self.user_repo.delete_password_reset_token(token)

        # 5. Kirim email konfirmasi bahwa reset password berhasil
        tasks.add_task(
            self.email_svc.send_reset_success_email, record["email"], record["name"]
        )

        return MessageResponse(message="Password has been successfully reset")
