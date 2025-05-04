import tkinter as tk
from tkinter import messagebox
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value

def format_data_for_vertex(data):
    instances = []
    for item in data:
        instance = {
            "age": item.get("age", ""),
            "blood_glucose_level": item.get("blood_glucose_level", ""),
            "bmi": item.get("bmi", ""),
            "gender": item.get("gender", ""),
            "HbA1c_level": item.get("HbA1c_level", ""),
            "heart_disease": item.get("heart_disease", ""),
            "hypertension": item.get("hypertension", ""),
            "smoking_history": item.get("smoking_history", "")
        }
        instances.append(instance)
    return instances

def predict_tabular_classification_sample(project, endpoint_id, data, location="us-central1", api_endpoint="us-central1-aiplatform.googleapis.com"):
    try:
        # Format the data
        formatted_instances = format_data_for_vertex(data)

        # Initialize client options
        client_options = {"api_endpoint": api_endpoint}
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

        # Convert each instance to protobuf format
        instances = [json_format.ParseDict(instance, Value()) for instance in formatted_instances]
        parameters_dict = {}
        parameters = json_format.ParseDict(parameters_dict, Value())

        # Define endpoint path
        endpoint = client.endpoint_path(project=project, location=location, endpoint=endpoint_id)

        # Make the prediction request
        response = client.predict(endpoint=endpoint, instances=instances, parameters=parameters)

        # Extract prediction
        predictions = [dict(prediction) for prediction in response.predictions]
        return predictions
    except Exception as e:
        messagebox.showerror("Error", f"Prediction failed: {str(e)}")
        return None

# Create the GUI
def create_gui():
    def submit_data():
        # Collect user input
        data = [{
            "age": entry_age.get(),
            "blood_glucose_level": entry_bgl.get(),
            "bmi": entry_bmi.get(),
            "gender": entry_gender.get(),
            "HbA1c_level": entry_hba1c.get(),
            "heart_disease": entry_hd.get(),
            "hypertension": entry_ht.get(),
            "smoking_history": entry_smoke.get()
        }]

        # Make prediction
        project = "stone-citizen-441700-c2"
        endpoint_id = "8826475827018334208"
        predictions = predict_tabular_classification_sample(project, endpoint_id, data)

        # Show results
        if predictions:
            result_text.set(f"Prediction: {predictions}")
        else:
            result_text.set("Prediction failed.")

    # Initialize the GUI window
    root = tk.Tk()
    root.title("Diabetes Prediction")

    # Input fields
    tk.Label(root, text="Age:").grid(row=0, column=0)
    entry_age = tk.Entry(root)
    entry_age.grid(row=0, column=1)

    tk.Label(root, text="Blood Glucose Level:").grid(row=1, column=0)
    entry_bgl = tk.Entry(root)
    entry_bgl.grid(row=1, column=1)

    tk.Label(root, text="BMI:").grid(row=2, column=0)
    entry_bmi = tk.Entry(root)
    entry_bmi.grid(row=2, column=1)

    tk.Label(root, text="Gender:").grid(row=3, column=0)
    entry_gender = tk.Entry(root)
    entry_gender.grid(row=3, column=1)

    tk.Label(root, text="HbA1c Level:").grid(row=4, column=0)
    entry_hba1c = tk.Entry(root)
    entry_hba1c.grid(row=4, column=1)

    tk.Label(root, text="Heart Disease (0 or 1):").grid(row=5, column=0)
    entry_hd = tk.Entry(root)
    entry_hd.grid(row=5, column=1)

    tk.Label(root, text="Hypertension (0 or 1):").grid(row=6, column=0)
    entry_ht = tk.Entry(root)
    entry_ht.grid(row=6, column=1)

    tk.Label(root, text="Smoking History:").grid(row=7, column=0)
    entry_smoke = tk.Entry(root)
    entry_smoke.grid(row=7, column=1)

    # Button to submit data
    tk.Button(root, text="Predict", command=submit_data).grid(row=8, column=0, columnspan=2)

    # Result display
    result_text = tk.StringVar()
    tk.Label(root, textvariable=result_text, fg="blue").grid(row=9, column=0, columnspan=2)

    # Start the GUI loop
    root.mainloop()

# Run the GUI
create_gui()
