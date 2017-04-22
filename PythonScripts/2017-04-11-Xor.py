##XOR truth table
#   0 | 1
#0: 0   1     
#1: 1   0

import tensorflow as tf

#Create input/feature tensors
x = tf.placeholder(tf.float32, shape=[4, 2], name="x-input")
y = tf.placeholder(tf.float32, shape=[4, 1], name="expected-outputs")


#initliase weights
#[2,2] -> 2 nodes, 2 input weights each
#-1, 1 -> random values between -1 and 1
weights1 = tf.Variable(tf.random_uniform([2,2], -1, 1), name="weights_layer1")
weights2 = tf.Variable(tf.random_uniform([2,1], -1, 1), name="weights_layer2")


#biases for layers 1 and 2
bias1 = tf.Variable(tf.zeros([2]), name="bias_layer1")
bias2 = tf.Variable(tf.zeros([1]), name="bias_layer2")


layer1Sigmoid = tf.sigmoid(tf.matmul(x, weights1) + bias1)
#( sigmoid output ) add biases
outputSigmoid = tf.sigmoid(tf.matmul(layer1Sigmoid, weights2) + bias2)

############## end of forward architecture declaration

#ignore this
cost = tf.reduce_mean(((y * tf.log(outputSigmoid)) + 
                       ((1 - y) * tf.log(1.0 - outputSigmoid))) * -1)

learning_rate = 0.01
train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

############## end of training architecture declaration

#Training data
XOR_X = [[0,0],
         [0,1],
         [1,0],
         [1,1]]
XOR_Y = [[0], #[ 0.01426198]
         [1], #[ 0.9833445 ]
         [1], #[ 0.98336637]
         [0]] #[ 0.02638073]]

##################


init = tf.global_variables_initializer()
sess = tf.Session()


sess.run(init)

writer = tf.summary.FileWriter("./logs/xorlogs", sess.graph)
writer.close()


epochs = 100000
for epoch in range(epochs):
    sess.run(train_step, feed_dict={x: XOR_X, y: XOR_Y})
    if( epoch % 1000 == 0 ):
        print("Epoch", epoch)
        print("predication", sess.run(outputSigmoid, feed_dict={x: XOR_X, y: XOR_Y}))
        print("weights layer 1:", sess.run(weights1))
        print("bias 1:", sess.run(bias1))
        print("Loss", sess.run(cost, feed_dict={x: XOR_X, y: XOR_Y}))
    

    
    






















