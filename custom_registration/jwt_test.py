import jwt

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyNzAyMjk4LCJpYXQiOjE3MDI3MDE5OTgsImp0aSI6IjM1ZGJjNTcyZWE0ZDQwNjA4MmIzZjZhMjMyZWFjYzQ1IiwidXNlcl9pZCI6Mjl9.7e8oclmf3phfITaRXmCElp-xFN-QvHfQkbr9_J4YlKw"

try:
    decoded_token = jwt.decode(token, algorithms=["HS256"], verify=False)
    print(decoded_token)
except jwt.ExpiredSignatureError:
    print("Token has expired.")
except jwt.InvalidTokenError:
    print("Invalid token.")
