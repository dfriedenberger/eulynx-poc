from flask import Flask, render_template , request  , jsonify                                              
import logging




class WebPage:

    def __init__(self,name,handler):
        self.name = name
        self.handler = handler
        self.app = Flask(__name__, template_folder='htdocs',static_folder='htdocs',static_url_path = "/")

        @self.app.route("/")
        def index():
            return render_template('index.html')

        @self.app.route("/api/v1/train",methods=['POST'])
        def train():
            self.handler('train',request.json)
            return jsonify({"status" : "OK"})

    def run(self):
        logging.info("Thread %s: starting", self.name)
        self.app.run()
        logging.info("Thread %s: finishing", self.name)