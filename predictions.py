import numpy as np
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense

myData = loadtxt('data.csv', delimiter=",")
x = myData[:, 0:5]
y = myData[:, 5]

model = Sequential()
model.add(Dense(4, input_dim=5, activation="relu"))
model.add(Dense(2, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x, y, epochs=100, batch_size=150, shuffle=True)

_, accuracy = model.evaluate(x, y)
print("Accuracy: ", accuracy)

predict = model.predict(x)
classes = np.argmax(predict, axis=1)
# for i in range(5):
#     print(x[i].tolist(), "predicts", predict[i], "ACTUAL :", y[i])

#
dataset = loadtxt('realApplicant.csv', delimiter=",")
ds = dataset[:, 0:5]
predict = model.predict(ds)
classes = np.argmax(predict, axis=1)
for i in range(5):
    print(ds[i].tolist(), "predicts", predict[i])
