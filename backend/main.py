from controllers.src.create_app import create_app
from scripts.create_default_user import create_default_user
import uvicorn

app = create_app()
create_default_user()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
