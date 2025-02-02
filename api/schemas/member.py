from pydantic import BaseModel, constr, condate, Field, field_validator
from datetime import date

# CREATE TABLE IF NOT EXISTS member (
#     firebase_id TEXT PRIMARY KEY,
#     first_name TEXT NOT NULL,
#     last_name TEXT NOT NULL,
#     phone_number TEXT NOT NULL UNIQUE,
#     university_serial_number TEXT NOT NULL,
#     verified BOOLEAN DEFAULT FALSE,
#     seller_rating DECIMAL(3,2) DEFAULT 5.0 CHECK (seller_rating BETWEEN 1 AND 5),
#     num_seller_ratings INTEGER DEFAULT 0,
#     buyer_rating DECIMAL(3,2) DEFAULT 5.0 CHECK (buyer_rating BETWEEN 1 AND 5),
#     num_buyer_ratings INTEGER DEFAULT 0,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     UNIQUE(first_name, last_name)
# );


class MemberCreate(BaseModel):
    firebase_token_id: str
    first_name: constr(max_length=50, min_length=1)
    last_name: constr(max_length=50, min_length=1)
    university_serial_number: str = Field(
        max_length=12,
        min_length=10,
        pattern=r"^1MS\d{2}(IS|CS|EE|EC|ET|EI|ME|IM|MD|AD|AI|BT|CH|CV|CI|CY)\d{3}(-T)?$",
        examples=["1MS22IS079", "1MS23EC123", "1MS23CS101-T"],
    )
    date_of_birth: condate(lt=date.today())

    @field_validator("university_serial_number")
    def validate_usn(cls, v: str):
        current_year_last_two = date.today().year % 100
        usn_year = int(v[3:5])
        if usn_year > current_year_last_two:
            raise ValueError("USN year cannot be in the future")
        valid_branches = [
            "IS",
            "CS",
            "EE",
            "EC",
            "ET",
            "EI",
            "ME",
            "IM",
            "MD",
            "AD",
            "AI",
            "BT",
            "CH",
            "CV",
            "CI",
            "CY",
        ]
        branch_code = v[5:7]
        if branch_code not in valid_branches:
            raise ValueError(f"Invalid branch code: {branch_code}")
        return v
