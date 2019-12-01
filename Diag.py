import numpy as np
import tensorflow as tf
import random

# 读取特征数据文件
def readdata(filename):
    data = []
    f = open(filename, 'r')
    line = f.readline()
    num = 0
    while line:
        buf = list(map(float, line.split()))
        data.append(buf)
        line = f.readline()
        num = num + 1
    f.close()
    data = np.array(data)  #读取的数据存储在二维数组中
    return data

# 读取label文件
def readlabel(filename):
    label = []
    f = open(filename, 'r')
    line = f.readline()
    num = 0
    while line:
        buf = list(map(float, line.split()))
        label.append(buf)
        num = num + 1
        line = f.readline()
    f.close()
    label = np.array(label)  #读取的数据存储在二维数组中
    return label

# 读取预测数据文件
def readresult(filename):
    result = []
    f = open(filename, 'r')
    line = f.readline()
    while line:
        buf = list(map(int, line.split()))
        result.append(buf[0])
        line = f.readline()
    f.close()
    result = np.array(result)   #读取的数据存储在二维数组中
    return result

# 主要函数，训练模型，生成预测结果并保存
def train():
    # 读取文件数据
    traindata = readdata("traindata.txt")
    verifdata = readdata("verifdata.txt")
    trainlabel = readlabel("trainlabel.txt")
    veriflabel = readlabel("veriflabel.txt")
    testdata = readdata("testdata.txt")
    veriflabel =veriflabel-1      # 将1、2数据变为0、1数据
    lr = tf.Variable(0.11, dtype=tf.float32)
    index = [i for i in range(len(traindata))]  # 将读入的数据顺序打乱
    random.shuffle(index)
    traindata = traindata[index]
    trainlabel = trainlabel[index]-1  # 将1、2数据变为0、1数据

    x_train = tf.placeholder(tf.float32,[None,13],name='x_train-input')
    y_train = tf.placeholder(tf.float32, [None,1],name='y_train-input')
    keep_prob = tf.placeholder(tf.float32)  # 网络随机去除线路——网络简单，我没有用

    # 三层网络
    W1 = tf.Variable(tf.truncated_normal([13,100]),name='weight1')
    b1 = tf.Variable(tf.zeros([100]),name='bias1')
    L1 = tf.sigmoid(tf.matmul(x_train,W1)+b1)

    # W2 = tf.Variable(tf.truncated_normal([100,50]),name='weight2')
    # b2 = tf.Variable(tf.zeros([50]),name='bias2')
    # L2 = tf.sigmoid(tf.matmul(L1,W2)+b2)

    W2 = tf.Variable(tf.truncated_normal([100,1]),name='weight2')
    b2 = tf.Variable(tf.zeros([1]),name='bias2')
    logits = tf.sigmoid(tf.matmul(L1,W2)+b2)

    # 预测值小于0.5为0，大于0.5为1
    one = tf.ones_like(logits)
    zero = tf.zeros_like(logits)
    prediction = tf.where(logits < 0.5, x=zero, y=one)
    #loss=tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_train,logits=logits))
    loss = tf.reduce_mean(tf.square(y_train-logits))
    train_step = tf.train.AdamOptimizer(lr).minimize(loss)

    # 使用Tensorboard监测
    with tf.name_scope('summary'):
        tf.summary.scalar('loss', loss)
        mean1 = tf.reduce_mean(logits)
        tf.summary.scalar('logits', mean1)
        mean2 = tf.reduce_mean(y_train)
        tf.summary.scalar('y_train', mean2)
        mean3 = tf.reduce_mean(W1)
        tf.summary.scalar('W1', mean3)
        mean4 = tf.reduce_mean(b1)
        tf.summary.scalar('b1', mean4)
        mean5 = tf.reduce_mean(prediction)
        tf.summary.scalar('prediction', mean5)
    merged = tf.summary.merge_all()

    # 计算准确率
    correct_prediction = tf.equal(y_train,prediction)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

    # run
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        sess.run(tf.local_variables_initializer())
        writer = tf.summary.FileWriter('logs/',sess.graph)
        for epoch in range(1000):
            sess.run(tf.assign(lr, 0.11* (0.999 ** epoch)))
            summary,_= sess.run([merged,train_step], feed_dict={x_train:traindata, y_train:trainlabel})
            writer.add_summary(summary, epoch)
            acc_train = sess.run(accuracy,feed_dict={x_train:traindata,y_train:trainlabel})
            acc_verif = sess.run(accuracy, feed_dict={x_train:verifdata, y_train:veriflabel})
            print ("Iter"+str(epoch)+", Trainset Accuracy= "+ str(acc_train)+", Verifset Accuracy= "+ str(acc_verif))
        if acc_train >= 0.9:# and acc_verif >= 0.9:
            result = sess.run(prediction,feed_dict={x_train:testdata})
            print("result:"+str(result.astype(int)+1))
            # 保存结果
            f = open('result.txt', 'w')
            for i in range(len(result)):
                f.write(str(result[i][0].astype(int)+1)+"\n")
            f.close

# 多结果投票获得最终结果
def ensembel(n):
    result = np.zeros((n,90), dtype=np.int)
    final=[]
    for i in range(n):
        result[i]=readresult("result"+str(i)+".txt")
    print(result)
    for i in range(90):
        nums=[]
        for j in range(n):
            nums.append(result[j][i])
        counts = np.bincount(nums)
        final.append(np.argmax(counts))
    print (final)
    f = open('finalresult.txt', 'w')
    for i in range(len(final)):
        f.write(str(final[i].astype(int)) + "\n")
    f.close

# 主函数
if __name__ == "__main__" :
    train()
    ensembel(5)  # 五个结果投票