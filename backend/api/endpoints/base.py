from fastapi import APIRouter

# i am going to continue this file tomorrow


class BaseRouter:
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

        def setup_routes(self):
            """
            TODO: you are supposed to inherit this class wherever
            you are defining the routes for each, Model
            """
            raise NotImplementedError(
                "subclass must implement setup_routes in base_router"
            )
