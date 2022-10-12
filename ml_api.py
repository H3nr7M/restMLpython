
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json


app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):
    
    Glucose : int
    BloodPressure : int
    Insulin : int
    BMI : float
        
# loading the saved model
diabetes_model = pickle.load(open('trained_model.sav', 'rb'))
# Api root or home endpoint
@app.get('/')
def read_home():
    """
     Home endpoint which can be used to test the availability of the application.
     """
    return {'message': 'System is healthy'}

@app.post('/diabetes_prediction')
def diabetes_predd(input_parameters : model_input):
    
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    
    glu = input_dictionary['Glucose']
    bp = input_dictionary['BloodPressure']
    insulin = input_dictionary['Insulin']
    bmi = input_dictionary['BMI']
    
    
    input_list = [glu, bp, insulin, bmi]
    
    prediction = diabetes_model.predict([input_list])
    return "No diabetic" if prediction == 0 else "diabetic"
    # if (prediction[0] == 0):
    #     return 'The person is not diabetic'
    # else:
    #     return 'The person is diabetic'
    
    



