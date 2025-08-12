from drf_yasg import openapi

# Common fields
address_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, example="Toshkent shahar, Chilonzor tumani, Bunyodkor ko'chasi 1-uy"),
        "lat": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=41.311081),
        "long": openapi.Schema(type=openapi.TYPE_NUMBER, format="float", example=69.240562),
    }
)

user_basic_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=123),
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Aliyev Vali Karimovich"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
    }
)

# /api/v1/accounts/edit/ PUT
edit_put_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Aliyev Vali Karimovich"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "address": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
    },
    required=["full_name", "phone_number", "address"]
)

edit_put_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Aliyev Vali Karimovich"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "profile_photo": openapi.Schema(type=openapi.TYPE_STRING, example="https://admin.77.uz/media/profiles/user_photo.jpg"),
        "address": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
    }
)

# /api/v1/accounts/edit/ PATCH
edit_patch_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Aliyev Vali Karimovich"),
    }
)

edit_patch_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Aliyev Vali Karimovich / Алиев Вали Каримович"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "profile_photo": openapi.Schema(type=openapi.TYPE_STRING, example="https://admin.77.uz/media/profiles/user_photo.jpg"),
        "address": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
    }
)

# /api/v1/accounts/login/
login_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, example="mySecurePassword123"),
    },
    required=["phone_number", "password"]
)

login_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(type=openapi.TYPE_STRING, example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.example"),
        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.example"),
        "user": user_basic_schema
    }
)

# /api/v1/accounts/me/
me_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=123),
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Aliyev Vali Karimovich"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "profile_photo": openapi.Schema(type=openapi.TYPE_STRING, example="https://admin.77.uz/media/profiles/user_photo.jpg"),
        "address": address_schema
    }
)

# /api/v1/accounts/register/
register_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Aliyev Vali Karimovich"),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, example="mySecurePassword123"),
        "password_confirm": openapi.Schema(type=openapi.TYPE_STRING, example="mySecurePassword123"),
    },
    required=["full_name", "phone_number", "password", "password_confirm"]
)

register_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(type=openapi.TYPE_STRING, example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.example"),
        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.example"),
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=123),
                "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Aliyev Vali Karimovich / Алиев Вали Каримович"),
                "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998901234567"),
                "profile_photo": openapi.Schema(type=openapi.TYPE_STRING, example="https://admin.77.uz/media/profiles/user_photo.jpg"),
                "address": address_schema,
                "created_at": openapi.Schema(type=openapi.TYPE_STRING, format="date-time", example="2024-01-01T00:00:00Z")
            }
        )
    }
)

# /api/v1/accounts/seller/registration/
seller_registration_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Karimov Akmal Rustamovich"),
        "project_name": openapi.Schema(type=openapi.TYPE_STRING, example="TechnoMart Online Do'koni"),
        "category": openapi.Schema(type=openapi.TYPE_INTEGER, example=7),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998971234567"),
        "address": address_schema
    },
    required=["full_name", "project_name", "category", "phone_number", "address"]
)

seller_registration_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=4321),
        "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Karimov Akmal Rustamovich"),
        "project_name": openapi.Schema(type=openapi.TYPE_STRING, example="TechnoMart Online Do'koni"),
        "category_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=7),
        "phone_number": openapi.Schema(type=openapi.TYPE_STRING, example="+998971234567"),
        "address": openapi.Schema(type=openapi.TYPE_STRING, example="Toshkent shahar, Mirobod tumani, Amir Temur ko'chasi 15-uy"),
        "status": openapi.Schema(type=openapi.TYPE_STRING, example="pending")
    }
)

# /api/v1/accounts/token/refresh/
token_refresh_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.example")
    },
    required=["refresh_token"]
)

token_refresh_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "access_token": openapi.Schema(type=openapi.TYPE_STRING, example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.newAccessToken.example")
    }
)

# /api/v1/accounts/token/verify/
token_verify_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "token": openapi.Schema(type=openapi.TYPE_STRING, example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.example")
    },
    required=["token"]
)

token_verify_response = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "valid": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
        "user_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=123)
    }
)
