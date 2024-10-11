# Project Description
## Objective
In this project, we predict, using machine learning, whether a person will have a sleep disorder using features such as age, gender, stress level, etc.
## Preprocessing
The `Sleep Disorder` column contains three unique entries: Sleep Apnea, Insomnia, and NaN. We replace the NaN values with No_Sleep_Disorder and combine the other two labels into Sleep_Disorder. We also remove duplicate columns and those irrelevant to our model.

For the `Blood Pressure` column, we categorize each reading into one of four groups: Normal BP, Elevated BP, Type 1 Hypertension, and Type 2 Hypertension. Then, we apply one-hot encoding to this column as well as the `Gender` column to prepare the data for our model.


## Summary and Results
Using logistic regression, we are able to predict with 80.77% accuracy. We used grid search to find the best hyperparameters for our model. Since our dataset is small, we used stratified K-fold cross validation
to see how well it performs in general.
