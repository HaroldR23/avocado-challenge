from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.src.routes.tasks import tasks_router
from controllers.src.routes.health import health_router
from controllers.src.exceptions.handler_exceptions import register_exception_handler

def create_app() -> FastAPI:
	app = FastAPI()
	app.add_middleware(
			CORSMiddleware,
			allow_origins=["*"],
			allow_credentials=False,
			allow_methods=["*"],
			allow_headers=["*"],
		)
	app.include_router(tasks_router)
	app.include_router(health_router)
	register_exception_handler(app)

	return app
