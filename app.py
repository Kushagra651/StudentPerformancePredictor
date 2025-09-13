import streamlit as st
import pandas as pd
import numpy as np
import os
import pickle
import altair as alt

# --- Helper Functions ---

def load_object(file_path):
    """Load a pickle object safely."""
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()

# --- Data Classes ---

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
            st.error("Prediction failed. Ensure 'artifacts/model.pkl' and 'artifacts/proprocessor.pkl' exist.")
            st.stop()

# --- STREAMLIT APP LAYOUT ---

st.set_page_config(page_title="Student Exam Performance Indicator", layout="centered")
st.title("Student Exam Performance Indicator")
st.write("Enter student details below to predict the final math score.")

with st.container():
    st.header("Student Exam Performance Prediction")
    col1, col2 = st.columns(2)
    
    with col1:
        gender = st.selectbox("Gender", ["Select your Gender", "male", "female"])
        ethnicity = st.selectbox("Race or Ethnicity", ["Select Ethnicity", "group A", "group B", "group C", "group D", "group E"])
        parental_level_of_education = st.selectbox(
            "Parental Level of Education",
            ["Select Parent Education", "associate's degree", "bachelor's degree", "high school", "master's degree", "some college", "some high school"]
        )
        lunch = st.selectbox("Lunch Type", ["Select Lunch Type", "free/reduced", "standard"])

    with col2:
        test_preparation_course = st.selectbox("Test Preparation Course", ["Select Test_course", "none", "completed"])
        reading_score = st.number_input("Reading Score out of 100", min_value=0, max_value=100)
        writing_score = st.number_input("Writing Score out of 100", min_value=0, max_value=100)
        
    if st.button("Predict your Score"):
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
                
                # Convert to DataFrame
                pred_df = data.get_data_as_data_frame()
                
                # Run the prediction pipeline
                predict_pipeline = PredictPipeline()
                results = predict_pipeline.predict(pred_df)
                
                # Display numeric result
                st.success(f"The predicted Math Score is: {results[0]:.2f}")
                
                # --- Visualization with Altair ---
                chart_data = pd.DataFrame({
                    'Category': ['Predicted Score', 'Max Score'],
                    'Score': [results[0], 100]
                })
                
                chart = alt.Chart(chart_data).mark_bar(color='orange').encode(
                    x='Category',
                    y='Score'
                ).properties(
                    title='Predicted Score vs Maximum Score'
                )
                
                st.altair_chart(chart, use_container_width=True)
                
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")

# --- Embed DagsHub Pipeline ---

st.header("ML Pipeline DAG")
dag_image_path = r"C:\Users\ASUS\Desktop\gujju_home_ml_project\image_pipeline.jpg"

# Display the image
st.image(dag_image_path, caption="DVC Pipeline DAG", use_container_width=True)
