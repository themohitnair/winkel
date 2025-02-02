import firebase_admin
from firebase_admin import auth, credentials
import os
from dotenv import load_dotenv
import logging
from schemas.firebase import FirebaseUserData, FirebaseAdminCredentials
from typing import Optional

load_dotenv()


class FirebaseAuth:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not firebase_admin._apps:
            firebase_creds = FirebaseAdminCredentials(
                type="service_account",
                project_id=os.getenv("FIREBASE_PROJECT_ID"),
                private_key=os.getenv("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
                client_email=os.getenv("FIREBASE_CLIENT_EMAIL"),
                token_uri=os.getenv("FIREBASE_TOKEN_URI"),
            )
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)

    def verify_token(self, id_token: str) -> Optional[FirebaseUserData]:
        try:
            decoded_token = auth.verify_id_token(id_token)
            return FirebaseUserData(
                uid=decoded_token.get("uid"),
                phone_number=decoded_token.get("phone_number"),
            )
        except Exception as e:
            self.logger.info(
                f"An error occurred while verifying the Firebase ID Token: {e}"
            )
            raise

    def get_user_by_uid(self, uid: str) -> Optional[FirebaseUserData]:
        try:
            user = auth.get_user(uid)
            return FirebaseUserData(uid=user.uid, phone_number=user.phone_number)
        except Exception as e:
            self.logger.info(
                f"An error occurred while fetching the user data from Firebase: {e}"
            )
            raise
