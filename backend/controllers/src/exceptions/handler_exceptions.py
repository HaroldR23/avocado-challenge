from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from http import HTTPStatus

from use_cases.src.exceptions.user_exceptions import UserNotFoundError
from use_cases.src.exceptions.task_exceptions import EmptyTaskTitleError, TaskNotFoundError
from use_cases.src.exceptions.comment_exceptions import EmptyCommentError
from domain.src.ports.repositories import RepositoryException

def register_exception_handler(app: FastAPI):

	@app.exception_handler(UserNotFoundError)
	def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
		return JSONResponse(
			status_code=HTTPStatus.NOT_FOUND,
			content={"detail": exc.message, "user_id": exc.user_id}
		)

	@app.exception_handler(EmptyTaskTitleError)
	def empty_task_title_exception_handler(request: Request, exc: EmptyTaskTitleError):
		return JSONResponse(
			status_code=HTTPStatus.BAD_REQUEST,
			content={"detail": exc.message}
		)

	@app.exception_handler(RepositoryException)
	def repository_exception_handler(request: Request, exc: RepositoryException):
		return JSONResponse(
			status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
			content={"detail": exc.message}
		)

	@app.exception_handler(TaskNotFoundError)
	def task_not_found_exception_handler(request: Request, exc: TaskNotFoundError):
		return JSONResponse(
			status_code=HTTPStatus.NOT_FOUND,
			content={"detail": exc.message, "task_id": exc.task_id}
		)

	@app.exception_handler(EmptyCommentError)
	def empty_comment_exception_handler(request: Request, exc: EmptyCommentError):
		return JSONResponse(
			status_code=HTTPStatus.BAD_REQUEST,
			content={"detail": exc.message}
		)
