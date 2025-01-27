from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date, datetime


class UserInit(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=50, examples=["John"])
    last_name: str = Field(min_length=1, max_length=50, example=["Doe"])
    uni_serial_number: str = Field(
        max_length=10,
        min_length=10,
        pattern=r"^1MS\d{2}(IS|CS|EE|EC|ET|EI|ME|IM|MD|AD|AI|BT|CH|CV|CI|CY)\d{3}(?:-T)$",
        examples=["1MS22IS079", "1MS23EC123"],
    )
    ph_no: str = Field(
        min_length=10, max_length=10, pattern=r"^[0-9]{10}$", example=["8123456709"]
    )
    date_of_birth: date

    @field_validator("uni_serial_number")
    def validate_usn(cls, v: str):
        current_year_last_two = datetime.now().year % 100
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


# used for verification during login and signup
class UserVerify(BaseModel):
    email: EmailStr
    otp: str = Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
        examples=["123456"],
    )
