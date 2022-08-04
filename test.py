import datetime

from jose import jwt

expire = datetime.datetime(2100, 12, 20, 0, 0)
data = {
    "id": 1,
    "type":"access"
}
to_encode = data.copy()
to_encode.update({"exp": expire})
encoded_jwt = jwt.encode(
    to_encode, 'daee617f159dbcfd2707b3819a57f79d2896558033dc97a58409256598dcb1bf', algorithm='HS256'
)
print(encoded_jwt)
