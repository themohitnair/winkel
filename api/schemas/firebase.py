from pydantic import BaseModel


class FirebaseUserData(BaseModel):
    uid: str
    phone: str


class FirebaseAdminCredentials(BaseModel):
    type: str
    project_id: str
    private_key: str
    client_email: str
    token_uri: str
