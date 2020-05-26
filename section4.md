Results and Discussions {#rd}
=======================

This section presents the results obtained from several complementary
perspectives. The goal is to explore each perspective and evaluate its
impact on the overall performance. Regarding the experiment
configuration, we refer to Table [tab:tuning]. To follow the open
science principles, we made the experiments available[^1], while event
logs can be obtained as stated in the procedure of Section [el].

Word2vec descriptive performance {#res:w2v}
--------------------------------

The initial experiment aims at evaluating how representational learning
influences the results. Regarding word2vec hyperparameters, we explored
the number of dimensions and window size, which are reportedly the most
impacting hyperparameters. The implementation used the *gensim* package
for Python[^2] and all other hyperparameters were set to standard
values. Figure [fig:w2vvector] and [fig:w2vwindow] show the accuracy
values obtained.

According to Figure [fig:w2vvector], the impact of different vector
sizes on the performance is minimal. For this task, we ranged values
from 50 to 1000. In other domains, the number of dimensions highly
affects the representational capacity of word2vec. A low number usually
diminish encoding quality. But traditional NLP tasks perform over a set
of texts containing large quantities of unique words. In business
processes, the set of unique activities (which we consider as words) is
of several orders of magnitude less than words in standard text corpora.
Moreover, the contexts that surround business process activities are
less heterogeneous. The same phenomenon is revealed in Figure
[fig:w2vwindow], where various window sizes are compared. The window
size controls how much of the context surrounding each word is selected
as a target of the learning procedure. We expect longer windows to drive
richer characterization of activities but our experimental results show
that it does not impact performances.

The main lesson learned for these experiments is the robustness of
word2vec in representing the context of business activities. It can be
adopted without the need of searching for optimal hyperparametrization.
Hence, in BPM applications, smaller vector and window sizes are advised
as they consume less computational resources without losing
representational capacity.

<span>.5</span> ![Vector](figures/word2vecVectorSize.pdf "fig:")
[fig:w2vvector]

<span>.5</span> ![Window](figures/word2vecWindowSize.pdf "fig:")
[fig:w2vwindow]

[fig:w2v]

Figure [fig:w2vdim] further demonstrates the effectiveness of word2vec
embeddings. We applied this technique to the `small-0.3-2` event log
using $200$ dimensions and a window size of $1$. Then, using the t-SNE
dimensionality reduction technique (with standard hyperparameters from
Scikit-learn package[^3]), the number of dimensions was reduced to two.
We can see how word2vec distributes the normal and anomalous classes in
the feature space. Word2vec correctly interprets the activities contexts
placing anomalous behaviour apart from normal. Moreover, anomalous
instances are usually near normal ones because they are a slight
variation of them, according to the injecting procedure we followed.

![`small-0.3-2` trace distribution. The experiment used word2vec to
model the business process behaviour. Then, the t-SNE dimensionality
reduction technique was applied for visualisation. It is notable how
anomalous and normal behaviour is quite separated in the feature
space](figures/small-0.3-2.pdf "fig:") [fig:w2vdim]

Time analysis
-------------

We compared a total of 40 different word2vec configurations with several
setups of LOF, OCSVM, and SVM. It is possible to observe that small
vector sizes, i.e., less than 200 features, affect the execution time
with small window sizes. Configurations of this kind demand more time
due to more frequent sliding over the samples, as seen in figures
[fig:loftime], [fig:ocsvmtime] and [fig:svmtime]. When dealing with more
than 250 features, time consumption is independent of window sizes,
drastically reducing the number of outliers in the results.

<span>0.5</span> ![LOF and
word2vec](figures/Timeword2vecWindowSize_LOF.pdf "fig:") [fig:loftime]

<span>0.5</span> ![OCSVM and
word2vec](figures/Timeword2vecWindowSize_OCSVM.pdf "fig:")
[fig:ocsvmtime]

<span>0.5</span> ![SVM and
word2vec](figures/Timeword2vecWindowSize_SVM.pdf "fig:") [fig:svmtime]

<span>0.5</span> ![Running time
distribution](figures/TimeComparison.pdf "fig:") [fig:fdptime]

SVM shows a slightly superior time performance, followed by LOF and
OCSVM. However, the average time difference is less than one second, as
observed in the running time distribution of Figure [fig:fdptime]. The
size of the vector has, indeed, the most prominent impact on execution
time. We compared the time of classification algorithms according to the
Friedman and Nemenyi test @demvsar2006statistical. Using $\tau = 0.05$
and critical distance of 0.53, it was possible to observe a
significantly different performance of SVM (1.37, ranked 1st), the
fastest algorithm. LOF (2.13, ranked 2nd) and OCSVM (2.50, ranked 3rd)
were not significantly different.

Considering the results of Section [res:w2v], we then suggest the
adoption of small vector sizes, particularly 50 dimensions, which
provide fast processing and stability for most event logs with
competitive predictive performance.

Hyperparameter selection
------------------------

This experimentation focused on the tuning of hyperparameters, as
described in Section [sec:tuning], to improve performances and support
fair comparisons among the methods.

Regarding the SVM method, the best hyperparameter to deal with all event
logs was $c=$1000 and $gamma$ as $scale$ using a $polynomial$ kernel.
This method was the most volatile to hyperparameter selection, e.g.,
some configurations of $c$ using $sigmoid$ kernel reduced drastically
the F-score, as shown in Figures [fig:svm~p~loy], [fig:svm~r~bf] and
[fig:svm~s~ig]. For OCSVM, the $nu$ hyperparameter has impacted the most
on performance. Small $nu$ values (best $nu=$0.01) results in better
predictive outcomes independent of $gamma$ or $kernel$. Figures
[fig:ocsvm1], [fig:ocsvm2] and [fig:ocsvm3] expose the F-score
performance with different OCSVM hyperparameter combinations. Finally
LOF, similarly to SVM, demands a combination of hyperparameters to
achieve the optimal performance. Also, the $auto$ value for the
$contamination$ parameter obtained an average good performance. For $k$
(*number of neighbours*), smaller values (1, 10, 25 and 50) were the
best. Using high $contamination$ (value of $0.4$) we obtained the worst
LOF performances, as visible in Figure [fig:lofhyper].

<span>0.5</span> ![SVM with poly
kernel](figures/Performance_Hyper_poly_SVM.pdf "fig:") [fig:svm~p~loy]

<span>0.5</span> ![SVM with rbf
kernel](figures/Performance_Hyper_rbf_SVM.pdf "fig:") [fig:svm~r~bf]

<span>0.5</span> ![SVM with sigmoid
kernel](figures/Performance_Hyper_sigmoid_SVM.pdf "fig:") [fig:svm~s~ig]

<span>0.5</span> ![OCSVM with poly
kernel](figures/Performance_Hyper_poly_OCSVM.pdf "fig:") [fig:ocsvm1]

<span>0.5</span> ![OCSVM with sigmoid
kernel](figures/Performance_Hyper_sigmoid_OCSVM.pdf "fig:") [fig:ocsvm2]

<span>0.5</span> ![OCSVM with rbf
kernel](figures/Performance_Hyper_rbf_OCSVM.pdf "fig:") [fig:ocsvm3]

<span>1</span> ![LOF](figures/Performance_Hyper_LOF.pdf "fig:")
[fig:lofhyper]

Classification performance
--------------------------

Figure [fig:best~s~core] shows a boxplot of the best F-scores for each
algorithm. LOF’s entire first quartile is above 0.95 while its median is
0.96. The median F-scores for OCSVM and SVM were 0.87 and 0.9,
respectively. Therefore, LOF outperforms both SVM and OCSVM. Though SVM
uses anomalous instances to learn the business process behaviour, its
performance is not the best. This result is valuable as LOF does not
even need anomalous examples to induce its model, making it easier to
prepare an event log for this method. That is, supervised methods do not
necessarily imply better performance. Moreover, even OCSVM use, which
has a slightly lower performance than SVM, can be preferred in scenarios
with a scarcity of labels.

![Best algorithms setup F-score](figures/Best_Fscore.pdf "fig:")
[fig:best~s~core]

Figure [fig:tunedAlgorithms] compares the performances over individual
event logs. As corroborated by the previous analysis, LOF outperforms
the other two algorithms in almost all event logs. This trend is even
more explicit in synthetic event logs, where LOF reaches F-scores of
over 0.95. In most datasets, SVM is better than OCSVM by a low margin,
however it required a longer tuning process for its hyperparameters.

Real-life event logs have a lower F-score when compared to synthetics.
The main reason is that BPIC event logs naturally contain not labelled
anomalies, which incorrectly represent normal behaviour. Furthermore,
results also show high recall scores for real-life logs, meaning that
the approaches do detect these anomalies, but have their precision
scores punished due to wrong labels. Using the same event logs, Nolle et
al. @NOLLE2019101458 also observed this phenomenon.

F-score comparison among the classification algorithms, according to the
Friedman and Nemenyi test using $\tau = 0.05$, showed significantly
different performances @demvsar2006statistical. The critical distance of
0.53 attested the superiority of LOF (1.11, ranked 1st), followed by SVM
(2.00, ranked 2nd) and OCSVM (2.89, ranked 3rd).

![image](figures/BPIC_chart.png)
![image](figures/GiganticHuge_chart.png)
![image](figures/LargeMedium_chart.png) ![F-score per event logs dataset
grouped by size and behaviour](figures/P2pSmallLarge_chart.png "fig:")
[fig:tunedAlgorithms]

Performances by anomaly
-----------------------

As there are six anomaly types, we further conducted an experiment to
analyse their differences. For this, we created six additional event
logs using the `medium-0.3-1` behaviour. For each anomaly type, we
created an event log with 30% of anomalies using only the respective
type. Figure [fig:anomalies] reports the results of the algorithms for
each anomaly. The first important note is that having only one type of
anomaly in the log makes the anomaly identification easier. This happens
because having a log with various anomalies makes its behaviour more
complex and less predictable. Given that, LOF reached F-scores of 1 in
five out of the six datasets, and SVM obtained the same performance in
three datasets. Therefore, this is a direct result of having only one
anomaly in each log.

The *attribute* anomalies are the most difficult of being detected by
the algorithms. Hence, as our approach uses the control-flow perspective
to model process behaviour, this type of anomaly becomes more
challenging to detect.

Regarding the other anomaly types, LOF can detect anomalous instances as
they all affect the control-flow aspect, which is well inferred by
word2vec. SVM presented good results for *insert*, *rework* and *skip*
anomalies. These anomalies are easier to detect due to a higher impact
on activities’ contexts. For instance, *skip* makes traces missing a
required activity execution. Then, when analysing a trace with a skipped
activity, word2vec modeling is sensible enough to detect that the trace
context is different from normal behaviour. For *early* and *late*
anomalies, the effect on the context is more subtle because the
activities are still in the trace even if in wrong positions. Therefore,
this shows the importance of having an OCC classification on top of
word2vec as it relies on normal samples, counterbalancing this issue.
This is seen by the exceptional performance reached by LOF.

![Comparing the F-score of each classification method using event log
`medium-0.3-1`](figures/AnomalyFscore.pdf "fig:") [fig:anomalies]

[^1]: <https://github.com/gbrltv/ProcessAnomalyDetector>

[^2]: <https://radimrehurek.com/gensim/models/word2vec.html>

[^3]: <https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html>
