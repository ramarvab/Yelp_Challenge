"""
=======================================
Receiver Operating Characteristic (ROC)
=======================================

Example of Receiver Operating Characteristic (ROC) metric to evaluate
classifier output quality.

ROC curves typically feature true positive rate on the Y axis, and false
positive rate on the X axis. This means that the top left corner of the plot is
the "ideal" point - a false positive rate of zero, and a true positive rate of
one. This is not very realistic, but it does mean that a larger area under the
curve (AUC) is usually better.

The "steepness" of ROC curves is also important, since it is ideal to maximize
the true positive rate while minimizing the false positive rate.

Multiclass settings
-------------------

ROC curves are typically used in binary classification to study the output of
a classifier. In order to extend ROC curve and ROC area to multi-class
or multi-label classification, it is necessary to binarize the output. One ROC
curve can be drawn per label, but one can also draw a ROC curve by considering
each element of the label indicator matrix as a binary prediction
(micro-averaging).

Another evaluation measure for multi-class classification is
macro-averaging, which gives equal weight to the classification of each
label.

.. note::

    See also :func:`sklearn.metrics.roc_auc_score`,
             :ref:`example_model_selection_plot_roc_crossval.py`.

"""
print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from scipy import interp

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB 
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn import cross_validation
from sklearn import metrics
from sklearn.linear_model import SGDClassifier

import pickle
from pprint import pprint
from time import time
import sys

with open("/Users/huzefa/Workspace/College-Fall-2015/Search/Dataset/Task2/Onlyreviews.fv") as f:
    global XAll
    XAll= pickle.load(f)
with open("/Users/huzefa/Workspace/College-Fall-2015/Search/Dataset/Task2/Onlyreviews.target2") as f:
    global yAll 
    yAll= pickle.load(f)
with open("/Users/huzefa/Workspace/College-Fall-2015/Search/Dataset/Task2/Onlyreviews.mlb") as f:
    mlb = pickle.load(f)

n_classes = yAll.shape[1]

# shuffle and split training and test sets
xTrain, xTest, yTrain, yTest = train_test_split(XAll, yAll, test_size=.4,
                                                    random_state=0)

# Learn to predict each class against the other
print "Training Classifier"
#svcClassifier = OneVsRestClassifier(LinearSVC()).fit(xTrain, yTrain)
sgdClassifier = OneVsRestClassifier(SGDClassifier()).fit(xTrain, yTrain)
#print "Training classifier took : "+str(time()- classifierTime)
with open("/Users/huzefa/Workspace/College-Fall-2015/Search/Dataset/Task2.1/sgd60BinaryROC.classifier", 'w') as f:
    pickle.dump(sgdClassifier, f)
print "Classifier dumped on disk"    
print "Predicting ... "
y_score = sgdClassifier.fit(xTrain, yTrain).decision_function(xTest)

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(yTest[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(yTest.ravel(), y_score.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])


##############################################################################
# Plot of a ROC curve for a specific class 0 and 1
plt.figure()
plt.plot(fpr[0], tpr[0], label='ROC curve Class 0(area = %0.2f)' % roc_auc[0])
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()

plt.figure()
plt.plot(fpr[0], tpr[0], label='ROC curve Class 1(area = %0.2f)' % roc_auc[0])
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()

##############################################################################
# Plot ROC curves for the multiclass problem

# Compute macro-average ROC curve and ROC area

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()

plt.plot(fpr["macro"], tpr["macro"],
         label='Average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         linewidth=2)

for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'
                                   ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve for helpfulness of a review')
plt.legend(loc="lower right")
plt.show()