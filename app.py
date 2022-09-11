
from flask import Flask, Blueprint, jsonify,render_template
from flask_cors import CORS

from simple_app.endpoints import project_api_routes



def create_app():
#name the appa nd initialize flask app
    web_app = Flask(__name__,template_folder='templates')  
    CORS(web_app)
   

    api_blueprint = Blueprint('api_blueprint', __name__)
    api_blueprint = project_api_routes(api_blueprint)

    web_app.register_blueprint(api_blueprint, url_prefix='/api')    

    return web_app


app = create_app()
#code to run the program
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)#to automatically deploy the changes and for development set it true
                                      #production set it as false