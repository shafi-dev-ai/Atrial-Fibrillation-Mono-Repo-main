import sys
import os
sys.path.insert(0,os.getcwd())
from flask import Flask, request, Response, jsonify, send_file, render_template
from flask_restful import Api
from db.db import *
from server.server import ApiIsAlive, AtrialFibrillationPredictApi, AtrialFibrillationPutApi, AtrialFibrillationDeleteApi
from apispec import APISpec
from services.service import AtrialFibrillationServiceLayer
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import seaborn as sns
from ast import literal_eval
import pandas as pd
import pickle

app = Flask(__name__)
api = Api(app)

# Swagger plugin for docs
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Atrial Fibrillation Detection API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-docs/'  # URI to access UI of API Doc
})

docs = FlaskApiSpec(app)

api.add_resource(ApiIsAlive, '/health')
docs.register(ApiIsAlive)

api.add_resource(AtrialFibrillationPredictApi, '/predict_result')
docs.register(AtrialFibrillationPredictApi)


api.add_resource(AtrialFibrillationPutApi, '/update_patient_record')
docs.register(AtrialFibrillationPutApi)

api.add_resource(AtrialFibrillationDeleteApi, '/delete_patient_record')
docs.register(AtrialFibrillationDeleteApi)


@app.route('/show_vizulization', methods=['POST'])
def show_vizulization():
    srv = AtrialFibrillationServiceLayer()
    inter_section_columns = ['V6','III','age','V2','V5','V4','weight','I','sex','II','V3','V1','aVR','height','ritmi','aVF','aVL']
    data = request.data
    patient_data = literal_eval(data.decode('utf-8'))

    sub_test_data = {column: patient_data[column] for column in inter_section_columns}
    test_df = pd.DataFrame(sub_test_data,index=[0])
    test_df['sex'] = test_df['sex'].apply(lambda x : 0 if x=='male' else 1)
    X_test = test_df.drop(columns='ritmi')
    y_test = test_df['ritmi']

        # load model
    modelfile = open(rf'weights/17_feature_random_model.pkl','rb')
    model = pickle.load(modelfile)

        # do inference
    y_pred_prob = list(model.predict_proba(X_test)[0])

    df = pd.DataFrame({'Probability': y_pred_prob})
    df.index = ['Normal (SR)', 'Atrial Fibrillation (AF)', 'All other arrhythmia (VA)']

    # Create the bar chart
    fig,ax=plt.subplots(figsize=(6,6))
    sns.barplot(x=df.index, y='Probability', data=df)
    canvas=FigureCanvas(fig)
    img = io.BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    InitDB()
    app.run(port=5000, debug=False)
