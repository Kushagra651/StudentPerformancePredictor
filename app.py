# from flask import Flask,request,render_template
# import numpy as np
# import pandas as pd

# from sklearn.preprocessing import StandardScaler
# from src.pipeline.predict_pipeline import CustomData,PredictPipeline

# application=Flask(__name__)

# app=application

# ## Route for a home page

# @app.route('/')
# def index():
#     return render_template('index.html') 

# @app.route('/predictdata',methods=['GET','POST'])
# def predict_datapoint():
#     if request.method=='GET':
#         return render_template('home.html')
#     else:
#         data=CustomData(
#             gender=request.form.get('gender'),
#             race_ethnicity=request.form.get('ethnicity'),
#             parental_level_of_education=request.form.get('parental_level_of_education'),
#             lunch=request.form.get('lunch'),
#             test_preparation_course=request.form.get('test_preparation_course'),
#             reading_score=float(request.form.get('writing_score')),
#             writing_score=float(request.form.get('reading_score'))

#         )
#         pred_df=data.get_data_as_data_frame()
#         print(pred_df)
#         print("Before Prediction")

#         predict_pipeline=PredictPipeline()
#         print("Mid Prediction")
#         results=predict_pipeline.predict(pred_df)
#         print("after Prediction")
#         return render_template('home.html',results=results[0])
    

# if __name__=="__main__":
#     app.run(host="0.0.0.0")   
import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import sys

# Placeholder for the PredictPipeline and CustomData classes
# In a real project, these would be imported from your src directory.
# We define them here to make the app a single, runnable file.

# A simple class to simulate your utils.py load_object function
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()
        
class CustomData:
    def __init__(self, gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course, reading_score, writing_score):
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }
            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
            st.error(f"Error creating DataFrame: {e}")
            st.stop()

class PredictPipeline:
    def __init__(self):
        # We assume the artifacts folder is in the same directory as the Streamlit app
        artifacts_path = os.path.join(os.path.dirname(__file__), 'artifacts')
        self.model_path = os.path.join(artifacts_path, "model.pkl")
        self.preprocessor_path = os.path.join(artifacts_path, 'proprocessor.pkl')

    def predict(self, features):
        try:
            model = load_object(file_path=self.model_path)
            preprocessor = load_object(file_path=self.preprocessor_path)
            
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        except Exception as e:
            st.error(f"Prediction failed. Make sure 'artifacts' folder with 'model.pkl' and 'preprocessor.pkl' exists in the same directory as this script.")
            st.stop()

# --- STREAMLIT APP LAYOUT AND LOGIC ---

# Main Title and Welcome Message
st.set_page_config(page_title="Student Exam Performance Indicator", layout="centered")
st.title("Student Exam Performance Indicator")
st.write("Welcome to the Student Exam Performance Prediction App. Please enter the student's details below to predict their final math score.")

# --- Prediction Form ---
with st.container():
    st.header("Student Exam Performance Prediction")
    
    # Using st.columns for a more organized, two-column layout
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("Gender", ["Select your Gender", "male", "female"])
        ethnicity = st.selectbox("Race or Ethnicity", ["Select Ethnicity", "group A", "group B", "group C", "group D", "group E"])
        parental_level_of_education = st.selectbox("Parental Level of Education", ["Select Parent Education", "associate's degree", "bachelor's degree", "high school", "master's degree", "some college", "some high school"])
        lunch = st.selectbox("Lunch Type", ["Select Lunch Type", "free/reduced", "standard"])

    with col2:
        test_preparation_course = st.selectbox("Test Preparation Course", ["Select Test_course", "none", "completed"])
        reading_score = st.number_input("Reading Score out of 100", min_value=0, max_value=100)
        writing_score = st.number_input("Writing Score out of 100", min_value=0, max_value=100)
        
    # Predict button
    if st.button("Predict your Math Score"):
        if "Select" in [gender, ethnicity, parental_level_of_education, lunch, test_preparation_course]:
            st.warning("Please fill out all the fields.")
        else:
            try:
                # Create CustomData object
                data = CustomData(
                    gender=gender,
                    race_ethnicity=ethnicity,
                    parental_level_of_education=parental_level_of_education,
                    lunch=lunch,
                    test_preparation_course=test_preparation_course,
                    reading_score=reading_score,
                    writing_score=writing_score
                )
                
                # Get data as a DataFrame
                pred_df = data.get_data_as_data_frame()
                
                # Run the prediction pipeline
                predict_pipeline = PredictPipeline()
                results = predict_pipeline.predict(pred_df)
                
                # Display the result
                st.success(f"The predicted Math Score is: {results[0]:.2f}")
                
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")