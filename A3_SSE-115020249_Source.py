import math
import time
import re
from random import sample
from collections import Counter
from functools import reduce

def vectorSubtract(v, w):
    return tuple([v_i - w_i for v_i, w_i in zip(v,w)])

def sumOfSquares(v):
    return sum(v_i * v_i for v_i in v)

def distance(v, w):
    s = vectorSubtract(v,w)
    return math.sqrt(sumOfSquares(s))

def readData(filename):
    data = {x:[] for x in range(10)}
    f = open(filename, 'r')
    while True:
        seq = f.read(1059)
        if seq == '':
            f.close()
            break
        n = int(seq[1057])
        vector = tuple([int(i) for i in re.sub('\n', '', seq[:-4])])
        data[n].append(vector)
    return data

def predictModel1(vector, data, k):
    vector_set = reduce(lambda x, y: x+y, list(data.values()))
    k_vectors = sorted(vector_set, key=lambda x: distance(x, vector))[:k]
    digits = [digit for digit, vectors in data.items() for v in k_vectors if v in vectors]
    return Counter(digits).most_common(1)[0][0]

def predictModel2(vector, data, k):
    compressed_data = {i:sample(data[i], 47) for i in range(10)}
    vector_set = reduce(lambda x, y: x+y, list(compressed_data.values()))
    k_vectors = sorted(vector_set, key=lambda x: distance(x, vector))[:k]
    digits = [digit for digit, vectors in data.items() for v in k_vectors if v in vectors]
    return Counter(digits).most_common(1)[0][0]

def trainingInfo(training_data, total_samples=0):
    print("Beginning of Training @ {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print('-'*40 + '\n' + "Training Info".center(40) + '\n' + '-'*40)
    for i in range(10):
        total_samples += len(training_data[i])
        print("{0} = {1:3}".format(i, len(training_data[i])).rjust(21))
    print('-'*40 + '\n' + '  Total Samples = ' + str(total_samples) + '\n' + '-'*40)

def testingInfo(training_data, testing_data, k, model):
    print("Testing Info".center(40) + '\n' + '-'*40)
    total_correct, total_num = 0, 0
    for i in range(10):
        correct, incorrect = 0, 0
        for vector in testing_data[i]:
            if model(vector, training_data, k) == i:
                correct += 1
            else:
                incorrect += 1
        p = round(correct / (correct + incorrect) * 100)
        total_correct += correct
        total_num += len(testing_data[i])
        print("{0} = {1:3}, {2:3}, {3:3}%".format(i, correct, incorrect, p).rjust(32))
    t_p = round(total_correct / total_num * 100, 2)
    print('-'*40 + '\n' + "Accuracy = ".rjust(18) + '{}%'.format(t_p))
    print("Correct/Total = ".rjust(18) + "{0}/{1}".format(total_correct, total_num))
    print('-'*40 + '\n' + "End of Training @ {}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

def predictInfo(training_data, predict_data, k, model):
    print("Prediction loading......")
    for vector in predict_data[0]:
        print(model(vector, training_data, k))
    print("Prediction completes." + '\n')

def main(k, model):
    training_data = readData('digit-training.txt')
    testing_data = readData('digit-testing.txt')
    predict_data = readData('digit-predict.txt')
    trainingInfo(training_data)
    testingInfo(training_data, testing_data, k, model)
    predictInfo(training_data, predict_data, k, model)

if __name__ == '__main__':
    k = int(input("Please input an integer k (0<k<10):"))
    main(k, predictModel1)
    main(k, predictModel2)






