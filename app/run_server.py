# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
	# load the pre-trained model
	global model
	with open(model_path, 'rb') as f:
		model = dill.load(f)
	print(model)

modelpath = r'C:\Users\aermo\Desktop\ML_Bussines\materials9\app\app\models\RandomForest.dill'
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
	return """Welcome to fraudelent prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}
	dt = strftime("[%Y-%b-%d %H:%M:%S]")
	# ensure an image was properly uploaded to our endpoint
	if flask.request.method == "POST":
		Geography, Gender, Tenure, HasCrCard, IsActiveMember, CreditScore, Age, Balance, NumOfProducts, EstimatedSalary = "", "", "", "", "", "", "", "", "", ""
		request_json = flask.request.get_json()
		if request_json["Geography"]:
			Geography = request_json['Geography']

		if request_json["Gender"]:
			Gender = request_json['Gender']

		if request_json["Tenure"]:
			Tenure = request_json['Tenure']

		if request_json["HasCrCard"]:
			HasCrCard = request_json['HasCrCard']

		if request_json["IsActiveMember"]:
			IsActiveMember = request_json['IsActiveMember']

		if request_json["CreditScore"]:
			CreditScore = request_json['CreditScore']

		if request_json["Age"]:
			Age = request_json['Age']

		if request_json["Balance"]:
			Balance = request_json['Balance']

		if request_json["NumOfProducts"]:
			NumOfProducts = request_json['NumOfProducts']

		if request_json["EstimatedSalary"]:
			EstimatedSalary = request_json['EstimatedSalary']

		logger.info(f'{dt} Data: Geography={Geography}, Gender={Gender}, Tenure={Tenure}, HasCrCard={HasCrCard}, IsActiveMember={IsActiveMember}, CreditScore={CreditScore}, Age={Age}, Balance={Balance}, NumOfProducts={NumOfProducts}, EstimatedSalary={EstimatedSalary}')
		try:
			preds = model.predict_proba(pd.DataFrame({"Geography": [Geography],
												  "Gender": [Gender],
												  "Tenure": [Tenure],
												  "HasCrCard": [HasCrCard],
												  "IsActiveMember": [IsActiveMember],
												  "CreditScore": [CreditScore],
												  "Age": [Age],
												  "Balance": [Balance],
												  "NumOfProducts": [NumOfProducts],
												  "EstimatedSalary": [EstimatedSalary],}))
		except AttributeError as e:
			logger.warning(f'{dt} Exception: {str(e)}')
			data['predictions'] = str(e)
			data['success'] = False
			return flask.jsonify(data)

		data["predictions"] = preds[:, 1][0]
		# indicate that the request was a success
		data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading the model and Flask starting server..."
		"please wait until server has fully started"))
	port = int(os.environ.get('PORT', 8180))
	app.run(host='0.0.0.0', debug=True, port=port)
