VERIFICATION_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verify Your Email</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="background: linear-gradient(to right, #4CAF50, #45a049); padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">Verify Your Email</h1>
  </div>
  <div style="background-color: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <p>Hello,</p>
    <p>Thank you for signing up! Your verification code is:</p>
    <div style="text-align: center; margin: 30px 0;">
      <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #4CAF50;">{verificationCode}</span>
    </div>
    <p>Enter this code on the verification page to complete your registration.</p>
    <p>This code will expire in 5 minutes for security reasons.</p>
    <p>If you didn't create an account with us, please ignore this email.</p>
    <p>Best regards,<br>Your App Team</p>
  </div>
  <div style="text-align: center; margin-top: 20px; color: #888; font-size: 0.8em;">
    <p>This is an automated message, please do not reply to this email.</p>
  </div>
</body>
</html>
"""

# WELCOME_EMAIL_TEMPLATE = """
# <html>
# <body>
#     <p>Welcome, <strong>{userName}</strong>! We're glad to have you onboard.</p>
# </body>
# </html>
# """

WELCOME_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome Aboard!</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="background: linear-gradient(to right, #4CAF50, #45a049); padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">Welcome to LeafyLabs</h1>
  </div>
  <div style="background-color: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <p>Hi <strong>{userName}</strong>,</p>
    <p>Welcome and thank you for joining us!</p>
    <p>We're excited to have you on board. Get ready to explore and enjoy everything our platform has to offer.</p>
    <p>If you have any questions or need help getting started, feel free to reach out to our support team at any time.</p>
    <p>We’re here to help you every step of the way.</p>
    <p>Best regards,<br>Your App Team</p>
  </div>
  <div style="text-align: center; margin-top: 20px; color: #888; font-size: 0.8em;">
    <p>This is an automated message, please do not reply to this email.</p>
  </div>
</body>
</html>
"""

PASSWORD_RESET_REQUEST_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>…</head>
<body style="…">
  <div>…</div>
  <div style="background-color: #f9f9f9; padding: 20px; …">
    <p>Hello,</p>
    <p>We received a request to reset your password. Klik tombol di bawah untuk mengganti password Anda:</p>
    <div style="text-align: center; margin: 30px 0;">
      <a href="{resetLink}"
         style="display: inline-block; padding: 12px 24px; background: #e67e22;
                color: white; text-decoration: none; border-radius: 4px;
                font-weight: bold;">
        Reset Password
      </a>
    </div>
    <p>Jika tombol di atas tidak berfungsi, salin URL ini ke browser Anda:</p>
    <p style="word-break: break-all;"><small>{resetLink}</small></p>
    <p>This link will expire in 15 minutes.</p>
    <p>If you didn’t request a password reset, just ignore this email.</p>
    <p>Best regards,<br>Your App Team</p>
  </div>
  <div style="…">…</div>
</body>
</html>
"""


# PASSWORD_RESET_REQUEST_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Password Reset Request</title>
# </head>
# <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
#   <div style="background: linear-gradient(to right, #f39c12, #e67e22); padding: 20px; text-align: center;">
#     <h1 style="color: white; margin: 0;">Reset Your Password</h1>
#   </div>
#   <div style="background-color: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
#     <p>Hello,</p>
#     <p>We received a request to reset your password. Use the code below to proceed:</p>
#     <div style="text-align: center; margin: 30px 0;">
#       <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #e67e22;">{resetCode}</span>
#     </div>
#     <p>This code will expire in 15 minutes for security reasons.</p>
#     <p>If you didn’t request a password reset, please ignore this message or contact our support team.</p>
#     <p>Best regards,<br>Your App Team</p>
#   </div>
#   <div style="text-align: center; margin-top: 20px; color: #888; font-size: 0.8em;">
#     <p>This is an automated message, please do not reply to this email.</p>
#   </div>
# </body>
# </html>
# """


PASSWORD_RESET_SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Password Successfully Reset</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="background: linear-gradient(to right, #2c3e50, #34495e); padding: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">Password Reset Successful</h1>
  </div>
  <div style="background-color: #f9f9f9; padding: 20px; border-radius: 0 0 5px 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
    <p>Hello {userName},</p>
    <p>Your password has been successfully updated.</p>
    <p>If you did not perform this action, we strongly recommend you contact our support team immediately to secure your account.</p>
    <p>Best regards,<br>Your App Team</p>
  </div>
  <div style="text-align: center; margin-top: 20px; color: #888; font-size: 0.8em;">
    <p>This is an automated message, please do not reply to this email.</p>
  </div>
</body>
</html>
"""
