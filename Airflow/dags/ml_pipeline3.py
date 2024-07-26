from airflow.models import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import pandas as pd
import os
from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, precision_score, log_loss
import numpy as np
import pickle
from sklearn import metrics


def prepare_data():
    print("---- Inside prepare_data component ----")
    df = pd.read_csv("https://raw.githubusercontent.com/TripathiAshutosh/dataset/main/iris.csv")
    df = df.dropna()
    df.to_csv('final_df.csv', index=False)

def train_test_split_func():
    print("---- Inside train_test_split component ----")
    final_data = pd.read_csv('final_df.csv')
    target_column = 'class'
    X = final_data.loc[:, final_data.columns != target_column]
    y = final_data.loc[:, final_data.columns == target_column]

    X_train, X_test, y_train, y_test = tts(X, y, test_size=0.2, random_state=42)

    np.save('X_train.npy', X_train)
    np.save('X_test.npy', X_test)
    np.save('y_train.npy', y_train)
    np.save('y_test.npy', y_test)

    print("\n---- X_train  ----")
    print(X_train)

    print("\n---- X_test  ----")
    print(X_test)

    print("\n---- y_train  ----")
    print(y_train)

    print("\n---- y_test  ----")
    print(y_test)

def training_basic_classifier():
    print("---- Inside training_basic_classifier component ----")
    X_train = np.load('X_train.npy', allow_pickle=True)
    y_train = np.load('y_train.npy', allow_pickle=True)

    classifier = LogisticRegression(max_iter=500)
    classifier.fit(X_train, y_train)

    with open('model.pkl', 'wb') as f:
        pickle.dump(classifier, f)

    print("\n Logistic regression classifier is trained on iris data and saved to PV location /model.pkl ----")    

def predict_on_test_data():
    print("---- Inside predict_on_test_data component ----")
    with open('model.pkl', 'rb') as f:
        Logistic_reg_model = pickle.load(f)
    X_test = np.load('X_test.npy', allow_pickle=True)
    y_pred = Logistic_reg_model.predict(X_test)
    np.save('y_pred.npy', y_pred)

    print("\n---- Predicted classes ---")
    print(y_pred)

def predict_prob_on_test_data():
    print("---- Inside predict_prob_on_test_data component ----")
    with open('model.pkl', 'rb') as f:
        Logistic_reg_model = pickle.load(f)
    X_test = np.load('X_test.npy', allow_pickle=True)
    y_pred_prob = Logistic_reg_model.predict(X_test)
    np.save('y_pred_prob.npy', y_pred_prob)

    print("\n---- Predicted Probabilities ---")
    print(y_pred_prob)

def get_metrics():
    print("--- Inside get_metrics component ---")
    y_test = np.load('y_test.npy', allow_pickle=True)
    y_pred = np.load('y_pred.npy', allow_pickle=True)
    y_pred_prob = np.load('y_pred_prob.npy', allow_pickle=True)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='micro')
    recall = recall_score(y_test, y_pred_prob, average='micro')
    entropy = log_loss(y_test, y_pred_prob)

    print(metrics.classification_report(y_test, y_pred))

    print("\n Model Metrics:", {'accuracy': round(acc, 2), 'precision': round(prec,2), 'recall': round(recall, 2)})

with DAG(
    dag_id='ml_pipeline_demo',
    schedule_interval='@daily',
    start_date=datetime(2024, 7, 26),
    catchup=False
) as dag:

    task_prepare_data = PythonOperator(
        task_id='prepare_data',
        python_callable=prepare_data,
    )

    task_train_test_split = PythonOperator(
        task_id='train_test_split',
        python_callable=train_test_split_func,
    )

    task_training_basic_classifier = PythonOperator(
        task_id='training_basic_classifier',  # Ensure this task_id is unique
        python_callable=training_basic_classifier,
    )    

    task_predict_on_test_data = PythonOperator(
        task_id='predict_on_test_data',
        python_callable=predict_on_test_data,
    )

    task_predict_prob_on_test_data = PythonOperator(
        task_id='predict_prob_on_test_data',
        python_callable=predict_prob_on_test_data,
    )    

    task_get_metrics = PythonOperator(
        task_id='get_metrics',
        python_callable=get_metrics
    )  

    task_prepare_data >> task_train_test_split >> task_training_basic_classifier >> \
        task_predict_on_test_data >> task_predict_prob_on_test_data >> task_get_metrics
