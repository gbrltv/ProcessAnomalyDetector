# Business Process Anomaly Detector

> Detection of anomalous business process traces in a scarcity of labels scenario. For that, it uses the word2vec encoding in combination with one-class classification algorithms

[![GitHub issues](https://img.shields.io/github/issues/gbrltv/ProcessAnomalyDetector)](https://github.com/gbrltv/ProcessAnomalyDetector/issues)
[![GitHub forks](https://img.shields.io/github/forks/gbrltv/ProcessAnomalyDetector)](https://github.com/gbrltv/ProcessAnomalyDetector/network)
[![GitHub stars](https://img.shields.io/github/stars/gbrltv/ProcessAnomalyDetector)](https://github.com/gbrltv/ProcessAnomalyDetector/stargazers)
[![GitHub license](https://img.shields.io/github/license/gbrltv/ProcessAnomalyDetector)](https://github.com/gbrltv/ProcessAnomalyDetector/blob/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/url?style=social)](https://twitter.com/intent/tweet?text=Using+Business%20Process+Anomaly+Detector:&url=https://github.com/gbrltv/ProcessAnomalyDetector)

---

## Table of Contents

- [Event Log Stats](#event_log_statistics)
- [Experimental Setup](#experimental_setup)

---

## Event Log Statistics

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

---

## Experimental Setup

> Collection of combined hyperparametes values

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
