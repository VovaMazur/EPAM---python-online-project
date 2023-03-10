from manifestapp import create_app
from flask import has_app_context

if __name__ == "__main__":
    application = create_app()
    application.run()