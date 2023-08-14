from system_to_person.app_config import AppConfig
from system_to_person.routes import app

if __name__ == '__main__':
    app.run(debug=False, port=AppConfig().server_port)
