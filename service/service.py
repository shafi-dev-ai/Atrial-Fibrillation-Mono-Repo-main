from marshmallow import ValidationError
from db.db import *
from services.validate_schema import BaseSchema
import json
import pandas as pd
from bson import ObjectId
import pickle
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

class AtrialFibrillationServiceLayer:
    def __init__(self):
        # collection we are using
        self.col_AF = DB['AtrialFibrillationCollection']
        self.col_Person = DB['PersonCollection']
        # database column we need
        self.inter_section_columns = ['V6','III','age','V2','V5','V4','weight','I','sex','II','V3','V1','aVR','height','ritmi','aVF','aVL']
        self.person_columns = ["name", "age", "height", "weight", "sex"]

    def Create_Schema(self, patient_schema):
        schema = BaseSchema()
        try:
            result = schema.load(patient_schema)
        except ValidationError as err:
             return json.dumps(err.messages)

        try:
            person_col = {column: patient_schema[column] for column in self.person_columns}
            if person_col['sex'] == 0:
                person_col['sex'] = 'male'
            else:
                person_col['sex'] = 'female'

            res = self.col_AF.insert_one(patient_schema)
            self.col_Person.insert_one(person_col)
            return res.inserted_id
        except ValidationError as err:
            return "cannot insert patient schema"


    def Get_Prediction(self, patient_schema):

        sub_test_data = {column: patient_schema[column] for column in self.inter_section_columns}
        test_df = pd.DataFrame(sub_test_data,index=[0])
        test_df['sex'] = test_df['sex'].apply(lambda x : 0 if x=='male' else 1)
        X_test = test_df.drop(columns='ritmi')
        y_test = test_df['ritmi']

        # load model
        modelfile = open(rf'weights/17_feature_random_model.pkl','rb')
        model = pickle.load(modelfile)

        # do inference
        y_pred_prob = list(model.predict_proba(X_test)[0])

        prediction_string=f'{round(y_pred_prob[0],2)*100}% Normal (SR), {round(y_pred_prob[1],2)*100}% Atrial Fibrillation (AF), {round(y_pred_prob[2],2)*100}% All other arrhythmia (VA)'

        try:
            return prediction_string
        except Exception as e:
            return {'model_prediction':None}

    def Update_Record(self, patient_schema):
        res_af =self.col_AF.find_one({}, {"name": patient_schema['name']})
        res_pa =self.col_Person.find_one({}, {"name": patient_schema['name']})
        new_values_af =  { "height":patient_schema['height'],
                              "weight":patient_schema['weight'], "ritmi": patient_schema['ritmi'],
                              "aVF":patient_schema["aVF"], "aVL": patient_schema['aVL'],
                              "aVR":patient_schema['aVR'], "I": patient_schema['I'], "II": patient_schema['II'],
                              "III": patient_schema['III'], "V1": patient_schema['V1'],
                              "V2":patient_schema['V2'], "V3": patient_schema['V3'],"V4": patient_schema['V4'],
                              "V5":patient_schema['V5'], "V6": patient_schema['V6']}

        new_values_per =  {"height":patient_schema['height'],
                            "weight":patient_schema['weight']}
        try:
            self.col_AF.update_one({"_id":res_af.get('_id')}, {"$set": new_values_af})
            self.col_Person.update_one({"_id":res_pa.get('_id')},  {"$set": new_values_per})
            return True
        except ValidationError as err:
            print(err)
            return False

    def Delete_Record(self, patient_schema):
        res_af =self.col_AF.find_one({}, {"name": patient_schema['name']})
        res_pa =self.col_Person.find_one({}, {"name": patient_schema['name']})
        try:
            self.col_AF.delete_one({"_id":res_af.get('_id')})
            self.col_Person.delete_one({"_id":res_pa.get('_id')})
            return True
        except ValidationError as err:
            print(err)
            return False
