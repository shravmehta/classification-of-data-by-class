import csv
import neuralNet

x = neuralNet.NeuralNetwork([45,60,45], None, None) 

print("Training...")

training_data = []

with open('tender_scores.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if(len(row)):
            temp = []
            for feature in row:
                temp.append(float(feature))
            training_data.append(temp)

x.simulate(training_data, training_data, 0.001)

print("Saving...")

x.save('neural_network.csv')