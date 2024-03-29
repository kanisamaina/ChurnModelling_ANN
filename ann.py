#Importing the libraries
import numpy as np
import pandas as pd
import tensorflow as tf

#Part 1-Data Preprocessing

#Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')
X = dataset.iloc[:, 3:-1].values
Y = dataset.iloc[:,-1].values

#Encoding categorical data
#Label Encoding the "gender" column 
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
X[:, 2] = le.fit_transform(X[:,2])
#One Hot Encoding the "Geography" column
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers = [('encoder',OneHotEncoder(),[1])],remainder='passthrough')
X = np.array(ct.fit_transform(X))

#Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test = train_test_split(X,Y, test_size = 0.2,random_state = 0)

#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)


#Part 2-Building the ANN

#Initialising the ANN
ann = tf.keras.models.Sequential()
#Adding the input layer and the first hidden layer
ann.add(tf.keras.layers.Dense(units=6,activation = 'relu'))
#Adding the second hidden layer
ann.add(tf.keras.layers.Dense(units=6,activation = 'relu'))
#Adding the output layer
ann.add(tf.keras.layers.Dense(units=1,activation = 'sigmoid'))


#Part 3-Training the ANN

#Compiling the ANN
ann.compile(optimizer = 'adam',loss = 'binary_crossentropy',metrics = ['accuracy'])
#Training the ANN on the Training set
ann.fit(X_train,Y_train,batch_size = 32, epochs = 100)


#Part 4-Making the predictions and evaluatin the model

#predicting the result of a single observation(
#Geography:France,
#Credit Score:600,
#Gender:Male,
#Age:40 years old,
#Tenure:3 years,
#Balance:$60000,
#Number of Products:2,
#Does this customer have a credit card?Yes,
#Is this customer an Active Member:Yes,
#Estimated Salary:$50000,
#So,should we say goodbye to the customer?)
print(ann.predict(sc.transform([[1, 0, 0, 600, 1, 40, 3, 60000, 2, 1, 1, 50000]])) > 0.5)
#Predicting the Test set results
y_pred = ann.predict(X_test)
y_pred = (y_pred > 0.5)
print(np.concatenate((y_pred.reshape(len(y_pred),1),Y_test.reshape(len(Y_test),1)),1))
#Making the Confusion Matrix
from sklearn.metrics import confusion_matrix,accuracy_score
cm = confusion_matrix(Y_test, y_pred)
print(cm)
accuracy_score(Y_test, y_pred)