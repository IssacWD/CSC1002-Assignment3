# CSC-1002 Assignment3: Handwritten Digit Recognition 

## 1. Scopes and Goals
#### 1) Goals
In this assignment, a programme is to be designed and developed using one of the popular classification algorithms called kNN (k-Nearest Neighbors) to programmatically predict handwritten digits in its digitized format. 

#### 2) Scopes
**a.** 2 KNN models should be constructed for prediction.
**b.** Training data, testing data, and digits to be predicted should be based on the files given, namely, 'digit-training.txt', 'digit-testing.txt', and 'digit-predict.txt'.
**c.** Training information, testing information, and prediction result should be printed for each KNN models.


## 2. Programming Solution
#### 1) Modules Import
For this assignment, modules imported are as follows:
```Python
import math
import time
import re
from random import sample
from collections import Counter
from functools import reduce
```

#### 2) Functions Design
To implement KNN models, 10 functions are defined as follows.
**a.** `vectorSubtract(v, w)`, `sumOfSquares(v)`, `distance(v, w)`
These three functions are for implementing vector operations. The first two of them are defined for the sake of constructing the third one, which can be used to calculate the distance between vectors.

**b.** `readData(filename)`
This function is to read the data from the text files and put them into dictionary. Firstly, a dictionary with 10 keys 0-9 will be created and their values are empty lists: `data = {x:[] for x in range(10)}`. Then for every digitized image read in the text files, the image's 32\*32 matrix will be converted to a 1\*1024 vector consisting of 1s and 0s and put into the list with the corresponding key which is identical to the number represented by the image: `data[n].append(vector)`.

**c.** `predictModel1(vector, data, k)`
This function represents the first KNN model used in this programme. The parameter `vector` represents the vector to be predicted. And `data` stands for the training data for predictions, which be a dictionary. `k` is the number of nearest vectors required to be chosen for voting. Firstly, the vectors in the dictionary will be taken out and put into a list:
```Python
vector_set = reduce(lambda x, y: x+y, list(data.values()))
```
Then the list of vectors will be sorted by their distances to the vector that is to be predicted, before k vectors in the list is chosen:
```Python
k_vectors = sorted(vector_set, key=lambda x: distance(x, vector))[:k]
```
After this, the digits represented by the vectors in this list will be also found out and put in another list:
```Python
digits = [digit for digit, vectors in data.items() for v in k_vectors if v in vectors]
```
Finally, the mode of the digits will be return as the prediction result:
```Python
return Counter(digits).most_common(1)[0][0]
```

**d.** `predictModel2(vector, data, k)`
This function represents the second model used in this programme. The parameters required to be input are consistent with model 1, and the process of prediction is similar, except one step which compressed the training data:
```Python
compressed_data = {i:sample(data[i], 47) for i in range(10)}
```
Since 943 image samples, of 10 digits, are read, the average number of samples for each digit is around 94. Hence 50% of them, indicating 47 vectors, for each digit are chosen randomly to represent the training data and thus the predicting accuracy may varies among tries. After this, the `compressed_data` will be used as the training data in model 1 and go through the similar process. 

**e.** `trainingInfo(training_data, total_samples=0)`, `testingInfo(training_data, testing_data, k, model)`, `predictInfo(training_data, predict_data, k, model)`
These three functions are defined to print the training, testing, and prediction information in fixed format required in the examples.

**f.** `main(k, model)`
This is the main function to process the whole programme in accordance with specified k and model required.

#### 3) Startup Design
```Python
if __name__ == '__main__':
    k = int(input("Please input an integer k (0<k<10):"))
    main(k, predictModel1)
    main(k, predictModel2)
```
At the beginning, the programme will prompt the user to input k (the range for k is just for reference). And the programme will print the three streams of information for both model 1 and model 2.

## 3) Limitations and Enhancements
#### 1) Model Choosing
Before choosing these two models for prediction, models with OR-vector method and AND-vector method have been tested in trials, however, abandoned due to the low accuracy rate of around 20%. Though, these two methods are still potential in compressing data set of vectors. A sophisticated model combining these two methods, random-sampling, and some other methods should be considered.

#### 2) Mode of the k Sample Digits
When the digits of the k vectors chosen have been put into a list, finding the mode of them seems simple. However, the models will automatically choose the first one of those digits appearing for the same frequency.:
```Python
return Counter(digits).most_common(1)[0][0]
```
This feature may dramatically reduce the accuracy when some the programme is not pretty sure about some digits. So other algorithm for determining the correct one from digits with same frequency should be developed.

#### 3) Input verification
For simplification, this programme merely prompt the user to input an integer k without verifying process to check if the input is valid. To strengthen the programme, this verification should be detailed until it is robust enough to refuse invalid input.

