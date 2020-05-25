'''
Process anomaly detection using word2vec modelling and one class classification algorithms
'''

import os
import time
import numpy as np
import pandas as pd
from multiprocessing import cpu_count
from sklearn import metrics
from gensim.models import Word2Vec
from sklearn.svm import SVC
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingClassifier
from sklearn.exceptions import ConvergenceWarning
from warnings import simplefilter
from sys import warnoptions

if not warnoptions:
    simplefilter("ignore", ConvergenceWarning)
    os.environ["PYTHONWARNINGS"] = "ignore" # Also affect subprocesses

n_workers = cpu_count()

def read_log(path, log):
    '''
    Reads event log and preprocess it
    '''
    df_raw = pd.read_csv(f'{path}/{log}')
    df_raw['event_processed'] = df_raw['activity_name'].str.replace(' ', '-')
    labels = [1 if x == 'normal' else -1 for x in df_raw['label']]
    df_raw['label'] = labels
    df_proc = df_raw[['case_id', 'event_processed', 'label']]
    del df_raw
    return df_proc

def cases_y_list(df):
    '''
    Creates a list of cases for model training
    '''
    cases, y = [], []
    for group in df.groupby('case_id'):
        events = list(group[1].event_processed)
        cases.append([''.join(x) for x in events])
        y.append(list(group[1].label)[0])

    return cases, y

def create_models(cases, size, window, min_count):
    '''
    Creates a word2vec model
    '''
    model = Word2Vec(
                size=size,
                window=window,
                min_count=min_count,
                workers=n_workers)
    model.build_vocab(cases)
    model.train(cases, total_examples=len(cases), epochs=10)

    return model

def average_feature_vector(cases, model):
    '''
    Computes average feature vector for each trace
    '''
    vectors = []
    for case in cases:
        case_vector = []
        for token in case:
            try:
                case_vector.append(model.wv[token])
            except KeyError:
                pass
        vectors.append(np.array(case_vector).mean(axis=0))

    return vectors

def compute_metrics(y_true, y_pred):
    '''
    Computes performance metrics
    '''
    acc = metrics.accuracy_score(y_true, y_pred)
    f1 = metrics.f1_score(y_true, y_pred)
    precision = metrics.precision_score(y_true, y_pred)
    recall = metrics.recall_score(y_true, y_pred)

    return acc, f1, precision, recall

scl = StandardScaler()
path = 'sample_data'
for log in os.listdir(path):
    log_name = log.split('.csv')[0]
    start_time_log = time.time()

    # reads event log
    df = read_log(path, log)

    # process cases and labels
    cases, y = cases_y_list(df)
    del df

    for size_param in [50, 100, 150, 200, 250, 300, 400, 500, 750, 1000]:
        for window_param in [1, 3, 5, 10]:
            # generate model
            model = create_models(cases, size_param, window_param, 1)

            # calculating the average feature vector for each sentence (trace)
            vectors = average_feature_vector(cases, model)
            # normalization
            vectors = scl.fit_transform(vectors)

            X_train, X_test, y_train, y_test = train_test_split(vectors, y, test_size=0.3, random_state=1)
            X_train = np.array(X_train)
            positive_mask = np.array(y_train) == 1

            for neighbors_param in [1, 10, 25, 50, 100, 250]:
                for contamination_param in [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 'auto']:
                    start_time = time.time()
                    lof = LocalOutlierFactor(n_neighbors=neighbors_param, contamination=contamination_param, novelty=True, n_jobs=n_workers)
                    lof.fit(X_train[positive_mask])
                    y_pred = lof.predict(X_test)
                    acc, fscore, precision, recall = compute_metrics(y_test, y_pred)
                    elapsed_time = time.time() - start_time
                    print(log_name, 'LOF', size_param, window_param, neighbors_param, contamination_param, acc, fscore, precision, recall, elapsed_time)

            for c_param in [0.1, 1, 10, 100, 1000, 10000, 100000]:
                for kernel_param in ['poly', 'rbf', 'sigmoid']:
                    for gamma_param in ['scale', 'auto']:
                        n_estimators = 10
                        start_time = time.time()
                        svm = BaggingClassifier(base_estimator=SVC(kernel=kernel_param, C=c_param, gamma=gamma_param, max_iter=1000000), max_samples=1.0 / n_estimators, n_estimators=n_estimators, n_jobs=n_workers)
                        svm.fit(X_train, y_train)
                        y_pred = svm.predict(X_test)
                        acc, fscore, precision, recall = compute_metrics(y_test, y_pred)
                        elapsed_time = time.time() - start_time
                        print(log_name, 'SVM', size_param, window_param, c_param, kernel_param, gamma_param, acc, fscore, precision, recall, elapsed_time)

            for nu_param in [0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4]:
                for kernel_param in ['poly', 'rbf', 'sigmoid']:
                    for gamma_param in ['scale', 'auto']:
                        start_time = time.time()
                        ocsvm = OneClassSVM(nu=nu_param, kernel=kernel_param, gamma=gamma_param, max_iter=1000000)
                        ocsvm.fit(X_train[positive_mask])
                        y_pred = ocsvm.predict(X_test)
                        acc, fscore, precision, recall = compute_metrics(y_test, y_pred)
                        elapsed_time = time.time() - start_time
                        print(log_name, 'OCSVM', size_param, window_param, nu_param, kernel_param, gamma_param, acc, fscore, precision, recall, elapsed_time)

    elapsed_time_log = time.time() - start_time_log
    print('Finished log', log_name, 'with', elapsed_time_log, 'seconds')
    print()
