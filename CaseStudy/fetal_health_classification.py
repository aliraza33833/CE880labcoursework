# -*- coding: utf-8 -*-
"""fetal-health-classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fiHrJrRv8k-AlnQGPdA0vcxsJZvrx_dP
"""

# upload fetal.csv file here in content directory.
!ls
!pwd

"""# <h1 style='background:#F7B2B0; border:0; color:black'><center>FETAL HEALTH</center></h1> 
 

 
Cardiotocography (CTG) is used during pregnancy to monitor fetal heart rate and uterine contractions. It is monitor fetal well-being and allows early detection of fetal distress. 

 CTG interpretation helps in determining if the pregnancy is high or low risk.  An abnormal CTG may indicate the need for further investigations and potential intervention.

In this project, I will create a model to classify the outcome of Cardiotocogram test to ensure the well being of the fetus.

# **<span style="color:#F7B2B0;">TABLE OF CONTENTS</span>**

**IMPORTING LIBRARIES**

**LOADING DATA**

**DATA PREPROCESSING**

**DATA ANALYSIS**

**MODEL BUILDING**

**CONCLUSIONS**

 # **<span style="color:#F7B2B0;">IMPORTING LIBRARIES</span>**
"""

# Cell:1
# Importing Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_score, recall_score, confusion_matrix, classification_report, accuracy_score, f1_score
from sklearn import metrics
from sklearn.metrics import roc_curve, auc, roc_auc_score

import statsmodels.api as sm
import tensorflow as tf
from tensorflow import keras
np.random.seed(0)

"""# **<span style="color:#F7B2B0;">LOADING DATA</span>**"""

# Cell:2
data = pd.read_csv("./fetal_health.csv")
data.head()

# Cell:3
data.info()

# Cell:4
data.describe().T

"""**On This Dataset**
**Cardiotocograms (CTGs)** are a simple and cost accessible option to assess fetal health, allowing healthcare professionals to take action in order to prevent child and maternal mortality. The equipment itself works by sending ultrasound pulses and reading its response, thus shedding light on fetal heart rate (FHR), fetal movements, uterine contractions and more.

This dataset contains 2126 records of features extracted from Cardiotocogram exams, which were then classified by expert obstetrician into 3 classes:

1. Normal
1. Suspect
1. Pathological

**Features**

* **'baseline value'** FHR baseline (beats per minute)
* **'accelerations'** Number of accelerations per second
* **'fetal_movement'** Number of fetal movements per second
* **'uterine_contractions'** Number of uterine contractions per second
* **'light_decelerations'** Number of light decelerations per second
* **'severe_decelerations'** Number of severe decelerations per second
* **'prolongued_decelerations'** Number of prolonged decelerations per second
* **'abnormal_short_term_variability'** Percentage of time with abnormal short term variability
* **'mean_value_of_short_term_variability'** Mean value of short term variability
* **'percentage_of_time_with_abnormal_long_term_variability'** Percentage of time with abnormal long term variability
* **'mean_value_of_long_term_variability'** Mean value of long term variability 
* **'histogram_width'** Width of FHR histogram
* **'histogram_min' Minimum** (low frequency) of FHR histogram
* **'histogram_max' Maximum** (high frequency) of FHR histogram
* **'histogram_number_of_peaks'** Number of histogram peaks
* **'histogram_number_of_zeroes'** Number of histogram zeros
* **'histogram_mode'** Histogram mode
* **'histogram_mean'** Histogram mean
* **'histogram_median'** Histogram median
* **'histogram_variance'** Histogram variance
* **'histogram_tendency'** Histogram tendency

* **Target**
* **'fetal_health'** Tagged as 1 (Normal), 2 (Suspect) and 3 (Pathological)

# **<span style="color:#F7B2B0;">EXPLORATORY DATA ANALYSIS (EDA)</span>**

**The analysis consist of:**
* Feature exploration
* Null values removal
* Feature normaliztion/ standardization
* Feature engineering
* Feature selection
"""

# Cell:5
# Visually Check regression of each data column on the class (fetal_heath)

y = data['fetal_health']
x1 = data[['baseline value', 'accelerations', 'fetal_movement', 'uterine_contractions','light_decelerations', 'severe_decelerations', 'prolongued_decelerations',
          'abnormal_short_term_variability', 'mean_value_of_short_term_variability', 'percentage_of_time_with_abnormal_long_term_variability',
          'mean_value_of_long_term_variability', 'histogram_width', 'histogram_min', 'histogram_max', 'histogram_number_of_peaks', 'histogram_number_of_zeroes',
          'histogram_mode', 'histogram_mean', 'histogram_median', 'histogram_variance', 'histogram_tendency']]

# plt.scatter(x1, y)
# plt.xlabel('baseline value', fontsize=20)
# plt.ylabel('fetal_health', fontsize=20)
# plt.show()

"""Using Stats model API to run reression analysis on each feature with target to know which features are important and have most effect on the target classification."""

# Cell:6
#check regression of each feature on target class
x = sm.add_constant(x1)
results = sm.OLS(y, x).fit()
results.summary()

"""All the features having P-Value less than 0.05 can be considered as important and the rest columns can be dropped.

"""

important_features = ['baseline value', 'accelerations', 'uterine_contractions', 'severe_decelerations', 'prolongued_decelerations', 'abnormal_short_term_variability', 'mean_value_of_long_term_variability', 'histogram_min', 'histogram_max'
'histogram_mode', 'histogram_median', 'histogram_variance', 'histogram_tendency']

"""# **<span style="color:#F7B2B0;">MODEL SELECTION AND BUILDING</span>**
In this section we will:
* Set up features(X) and target(Y)
* Scale the features
* Split training and test sets 
* Model selection
* Hyperparameter tuning
"""

# Cell:7
#assigning values to features as X and target as y
X=data.drop(["fetal_health",'accelerations', 'fetal_movement', 'light_decelerations', 'mean_value_of_short_term_variability',
             'histogram_width', 'histogram_number_of_peaks', 'histogram_number_of_zeroes', 'histogram_mean'],axis=1)
y=data["fetal_health"]

#Set up a standard scaler for the features
col_names = list(X.columns)
s_scaler = preprocessing.StandardScaler()
X_df= s_scaler.fit_transform(X)
X_df = pd.DataFrame(X_df, columns=col_names)   
X_df.describe().T
X_df.head()

# Cell:8
#looking at the scaled features
shades =["#f7b2b0","#c98ea6","#8f7198","#50587f", "#003f5c"]
plt.figure(figsize=(20,10))
sns.boxenplot(data = X_df,palette = shades)
plt.xticks(rotation=90)
plt.show()

# Cell:9
#spliting test and training sets
X_train, X_test, y_train,y_test = train_test_split(X_df,y,test_size=0.15,random_state=42)

# Cell:10
#A quick model selection process
#pipelines of models( it is short was to fit and pred)
pipeline_lr=Pipeline([('lr_classifier',LogisticRegression(random_state=10))])

pipeline_dt=Pipeline([ ('dt_classifier',DecisionTreeClassifier(random_state=42))])

pipeline_rf=Pipeline([('rf_classifier',RandomForestClassifier())])

pipeline_svc=Pipeline([('sv_classifier',SVC())])

pipeline_knn=Pipeline([('knn_classifier',KNeighborsClassifier(n_neighbors=10,p=4,metric='euclidean'))])


# List of all the pipelines
pipelines = [pipeline_lr, pipeline_dt, pipeline_rf, pipeline_svc, pipeline_knn]

# Dictionary of pipelines and classifier types for ease of reference
pipe_dict = {0: 'Logistic Regression', 1: 'Decision Tree', 2: 'RandomForest', 3: "SVC", 4: 'KNN'}


# Fit the pipelines
for pipe in pipelines:
    pipe.fit(X_train, y_train)

#cross validation on accuracy 
cv_results_accuracy = []
for i, model in enumerate(pipelines):
    cv_score = cross_val_score(model, X_train,y_train, cv=10 )
    cv_results_accuracy.append(cv_score)
    print("%s: %f " % (pipe_dict[i], cv_score.mean()))

#taking look at the test set
pred_rfc = pipeline_rf.predict(X_test)
accuracy = accuracy_score(y_test, pred_rfc)
print("Random forest TEST Accuracy:", accuracy)

pred_rfc = pipeline_lr.predict(X_test)
accuracy = accuracy_score(y_test, pred_rfc)
print("Logistic Regression TEST Accuracy:", accuracy)



# Cell:11
# Artificial neural network

X_train_nn, X_test_nn, y_train_nn, y_test_nn = train_test_split(X, y, test_size=0.15)

ss = StandardScaler()
X_train_scaled = ss.fit_transform(X_train_nn)
X_test_scaled = ss.transform(X_test_nn)


# OneHotEncoding Target Variable
y_train_encoded = pd.get_dummies(y_train_nn)
y_test_encoded = pd.get_dummies(y_test_nn)

# Code from https://www.kaggle.com/fatihdeniz/ann-fetal-health-classification
ann_classifier = keras.Sequential([
    # Input Layer
    keras.layers.Dense(20, input_shape=X_train_scaled[0].shape, activation="relu", kernel_initializer="HeNormal"),
    
    # Hidden Layer 1
    keras.layers.Dense(40,activation="relu"),
    keras.layers.Dense(80,activation="relu"),
    keras.layers.Dropout(0.3),
    
    # Hidden Layer 2
    keras.layers.Dense(160,activation="relu"),
    keras.layers.Dense(320,activation="relu"),
    keras.layers.Dropout(0.3),
    
    # Hidden Layer 3
    keras.layers.Dense(640,activation="relu"),
    keras.layers.Dense(3, activation="softmax")
])

ann_classifier.summary()


ann_classifier.compile(loss="categorical_crossentropy", metrics="accuracy", optimizer="rmsprop")

history = ann_classifier.fit(X_train_scaled, y_train_encoded, validation_data=(X_test_scaled, y_test_encoded), epochs=50)

y_pred_prob = ann_classifier.predict(X_test_scaled)
y_pred_prob

y_pred = []

for i in y_pred_prob:
    y_pred.append(np.argmax(i) + 1)
    
y_pred = np.array(y_pred)
y_pred

ann_accuracy = accuracy_score(y_pred, y_test_nn)
print("ANN Accuracy :", ann_accuracy)





"""**<span style="color:#003f5c;"> If you liked this Notebook, please do upvote.</span>**

**<span style="color:#003f5c;"> If you have any suggestions or questions, I am all ears!</span>**

**<span style="color:#003f5c;">Best Wishes!</span>**

<a id="5"></a> 
# <h1 style='background:#f7b2b0; border:0; color:black'><center>END</center></h1> 
"""