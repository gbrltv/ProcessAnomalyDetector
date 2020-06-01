# Business Process Anomaly Detector

> Detection of anomalous business process traces in a scarcity of labels scenario. For that, it uses the word2vec encoding in combination with one-class classification algorithms

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/gbrltv/ProcessAnomalyDetector/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/gbrltv/ProcessAnomalyDetector)](https://github.com/gbrltv/ProcessAnomalyDetector/issues)
[![GitHub forks](https://img.shields.io/github/forks/gbrltv/ProcessAnomalyDetector)](https://github.com/gbrltv/ProcessAnomalyDetector/network)
[![GitHub stars](https://img.shields.io/github/stars/gbrltv/ProcessAnomalyDetector)](https://github.com/gbrltv/ProcessAnomalyDetector/stargazers)
[![GitHub license](https://img.shields.io/github/license/gbrltv/ProcessAnomalyDetector)](https://github.com/gbrltv/ProcessAnomalyDetector/blob/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url?style=social)](https://twitter.com/intent/tweet?text=Using+Business%20Process+Anomaly+Detector:&url=https://github.com/gbrltv/ProcessAnomalyDetector)


## Table of Contents

- [Installation](#installation)
- [Event Log Stats](#event-log-statistics)
- [Experimental Setup](#experimental-setup)
- [Data Analysis](#data-analysis)
- [Contributors](#contributors)

## Installation

### Clone

Clone this repo to your local machine using

```shell
git clone https://github.com/gbrltv/ProcessAnomalyDetector.git
```

### Experiments

Simulate the experiments described here

```shell
python process_anomaly.py
```

## Event Log Statistics

Event logs were generated following the procedure proposed at https://github.com/tnolle/binet. The PLG2 tool was used to create six random process models with varying complexities, such as, the number of activities, breadth and width. Moreover, a procurement process model (P2P) and the real event logs from BPIC challenges were added (https://www.tf-pm.org/resources/logs). The process models were implemented as likelihood graphs, which were then simulated. Finally, six different types of anomalies were injected in the event logs. These anomalies represent complex behaviors that might affect a process execution. All event logs have a 30% rate of anomalous instances, which can be identified by the label attribute in the logs. Log statistics are reported in the following table.

<div id="tab:stats">

| Name     | \#Logs | \#Activities | \#Cases   | \#Events | \#Attributes | \#Attribute values |
| :------- | :----- | :----------- | :-------- | :------- | :----------- | :----------------- |
| P2P      | 4      | 27           | 5k        | 48k-53k  | 1-4          | 13-386             |
| Small    | 4      | 41           | 5k        | 53k-57k  | 1-4          | 13-360             |
| Medium   | 4      | 65           | 5k        | 39k-42k  | 1-4          | 13-398             |
| Large    | 4      | 85           | 5k        | 61k-68k  | 1-4          | 13-398             |
| Huge     | 4      | 109          | 5k        | 47k-53k  | 1-4          | 13-420             |
| Gigantic | 4      | 154-157      | 5k        | 38k-42k  | 1-4          | 13-409             |
| Wide     | 4      | 68-69        | 5k        | 39k-42k  | 1-4          | 13-382             |
| BPIC12   | 1      | 73           | 13k       | 290k     | 0            | 0                  |
| BPIC13   | 3      | 11-27        | 0.8k-7.5k | 4k-81k   | 2-4          | 23-1.8k            |
| BPIC15   | 5      | 422-486      | 0.8k-1.4k | 46k-62k  | 2-3          | 23-481             |
| BPIC17   | 1      | 53           | 31k       | 1.2M     | 1            | 299                |

</div>


## Experimental Setup

The main idea behind the encoding is to read activities as words and traces as sentences. This perspective allow us to model process instances using the word2vec algorithm. With that, we are capable of evaluating activities context and further identify anomalous executions. For the experiments, we used three algorithms: Support Vector Machines (SVM), One-Class Support Vector Machines (OCSVM) and Local Outlier Factor (LOF). SVM is a traditional machine learning algorithm used in many tasks, and as a supervised technique, it requires knowledge of the instances for the training phase. OCSVM is a one-class version of SVM, meaning that it only need positive classes for training (in our case, normal process executions). The same applied for LOF, an algorithm that detects outliers given a set of vectors using local point density. The implementation used the scikit-learn Python library (https://github.com/scikit-learn/scikit-learn). The following table lists the hyperparameters configurations. We performed a hyperparameter tuning following the grid search technique.

<div id="tab:tuning">

|       Method        | Hyperparameter  | Values                                                                               |
| :-----------------: | :-------------: | :----------------------------------------------------------------------------------- |
|         SVM         |       *c*       | <span>\[</span>0.1, 1, 10, 100, 1000, 10000, 100000<span>\]</span>                   |
|         SVM         |    *kernel*     | <span>\[</span>polynomial, rbf, sigmoid<span>\]</span>                               |
|         SVM         |     *gamma*     | <span>\[</span>auto, scale<span>\]</span>                                            |
|        OCSVM        |      *nu*       | <span>\[</span>0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4<span>\]</span>       |
|        OCSVM        |    *kernel*     | <span>\[</span>polynomial, rbf, sigmoid<span>\]</span>                               |
|        OCSVM        |     *gamma*     | <span>\[</span>auto, scale<span>\]</span>                                            |
|         LOF         |       *k*       | <span>\[</span>1, 10, 25, 50, 100, 250<span>\]</span>                                |
|         LOF         | *contamination* | <span>\[</span>0.01, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, auto<span>\]</span> |

</div>

> Collection of combined hyperparametes values

## Data Analysis

### Trace distribution

![small-0.3-2 Trace Distribution](/figures/small-0.3-2.jpeg)

<div style="text-align: justify;">

*small-0.3-2* trace distribution further demonstrates the effectiveness of word2vec embeddings. We applied this technique to the *small-0.3-2* event log using 200 dimensions and a window size of 1. Then, using the t-SNE dimensionality reduction technique (with standard hyperparameters from [scikit-learn package](https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html "t-SNE Scikit Documentation"), the number of dimensions was reduced to two. We can see how word2vec distributes the normal and anomalous classes in the feature space. Word2vec correctly interprets the activities contexts placing anomalous behaviour apart from normal. Moreover, anomalous instances are usually near normal ones because they are a slight variation of them, according to the injecting procedure we followed.

</div>

### Classification performance

![Overall classification performance using the F-score metric](/figures/classification_performance.jpeg)

<div style="text-align: justify;">

As the figure above shows, LOF outperforms the other two algorithms with some margin, with its entire first quartile above 0.95. This result even more interesting when considering that LOF only needs normal examples in the training process. On the other hand, SVM, which uses anomalous examples in the training phase, has a lower performance because of the noise during the model induction. In conclusion, traditional supervised methods do not necessarily have better performance than one-class classification algorithms. 

</div>

## Contributors

- [Gabriel Marques Tavares](https://www.researchgate.net/profile/Gabriel_Tavares6), PhD candidate at Università degli Studi di Milano
- [Paolo Ceravolo](https://www.unimi.it/en/ugov/person/paolo-ceravolo), Associate Professor at Università degli Studi di Milano
- [Sylvio Barbon Junior](http://www.barbon.com.br/), Associate Professor at State University of Londrina
