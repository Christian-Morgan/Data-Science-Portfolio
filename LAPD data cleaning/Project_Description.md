# Project Description
## Objective
In this project, we seek to comprehensively clean the dataset provided by the LAPD regarding crimes that have occurred between 2020 up to the present year. Given the size of the dataset, we limit our focus to only assault-related crimes.
## Dataset
The dataset can be downloaded here: [Crime Data from 2020 to Present](https://catalog.data.gov/dataset/crime-data-from-2020-to-present).

According to the website:

> "This dataset reflects incidents of crime in the City of Los Angeles dating back to 2020. This data is transcribed from original crime reports that are typed on paper and therefore there may be some inaccuracies within the data."
## Data Cleaning and Preprocessing Steps
In our analysis, we observe that there are indeed many inaccuracies, particularly in the victim age and victim descent columns. We replace these inaccuracies with NaN values and then impute them using the K-Nearest Neighbors imputation algorithm in scikit-learn.

The victim sex column contained `X` labels, signifying that the gender of the individual was unknown. We replaced all missing values with NaN, then used label encoding to replace each `M` and `F` label with `1` and `0`, respectively. To ensure that the `Victim Sex` column is in one-hot encoding format, we created two separate gender columns while ensuring that all NaN values stay in place.

Finally, as an exercise, we replace every label in the `Premis Desc` (premise description) column with either `public_property` or `private_property` and apply one-hot encoding.
