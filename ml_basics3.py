# -*- coding: utf-8 -*-
"""ml_basics3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1djAv8JBVP8TMuXidwU7J-bFn-U92McL2

## Modules & Functions
"""

import warnings; warnings.filterwarnings('ignore')
import numpy as np,pylab as pl,pandas as pd
import sys,h5py,urllib,zipfile
import tensorflow as tf
import tensorflow_hub as th
from sklearn.model_selection import train_test_split
fpath='https://olgabelitskaya.github.io/'

def prepro(x_train,y_train,x_test,y_test,n_class):
    n=int(len(x_test)/2)
    x_train=x_train.astype('float32')/255
    x_test=x_test.astype('float32')/255
    y_train=y_train.astype('int32')
    y_test=y_test.astype('int32')    
    x_valid,y_valid=x_test[:n],y_test[:n]
    x_test,y_test=x_test[n:],y_test[n:]
    cy_train=tf.keras.utils.to_categorical(y_train,n_class) 
    cy_valid=tf.keras.utils.to_categorical(y_valid,n_class)
    cy_test=tf.keras.utils.to_categorical(y_test,n_class)
    df=pd.DataFrame([[x_train.shape,x_valid.shape,x_test.shape],
                     [y_train.shape,y_valid.shape,y_test.shape],
                     [cy_train.shape,cy_valid.shape,cy_test.shape]],
                    columns=['train','valid','test'],
                    index=['images','labels','encoded labels'])
    display(df)
    return [[x_train,x_valid,x_test],
            [y_train,y_valid,y_test],
            [cy_train,cy_valid,cy_test]]
def display_10img(X,y,s):
    fig,ax=pl.subplots(figsize=(10,3),nrows=2,ncols=5,
                       sharex=True,sharey=True)
    ax=ax.flatten()
    for i in range(10):
        ax[i].imshow(X[i].reshape(s,s,3),cmap=pl.cm.Pastel1)
        ax[i].set_title(y[i])
    ax[0].set_xticks([]); ax[0].set_yticks([])
    pl.tight_layout()
def display_resize(x_train,x_valid,x_test,
                   y_valid,cy_valid,pixels):
    x_train=tf.image.resize(x_train,[pixels,pixels])
    x_valid=tf.image.resize(x_valid,[pixels,pixels])
    x_test=tf.image.resize(x_test,[pixels,pixels])
    img=x_valid[1]
    lbl='one example of resized images \nlabel: '+\
     str(y_valid[1][0])+'=>'+str(cy_valid[1])+\
     '\nshape: '+str(img.shape)
    pl.imshow(img); pl.title(lbl)
    return [x_train,x_valid,x_test]
def cb(fw):
    early_stopping=tf.keras.callbacks\
    .EarlyStopping(monitor='val_loss',patience=20,verbose=2)
    checkpointer=tf.keras.callbacks\
    .ModelCheckpoint(filepath=fw,save_best_only=True,verbose=2)
    lr_reduction=tf.keras.callbacks\
    .ReduceLROnPlateau(monitor='val_loss',verbose=2,
                       patience=5,factor=.8)
    return [checkpointer,early_stopping,lr_reduction]

"""## Data"""

(x_train1,y_train1),(x_test1,y_test1)=\
tf.keras.datasets.cifar10.load_data()
[[x_train1,x_valid1,x_test1],
 [y_train1,y_valid1,y_test1],
 [cy_train1,cy_valid1,cy_test1]]=\
prepro(x_train1,y_train1,x_test1,y_test1,10)
display_10img(x_test1,y_test1,32)

zf='LetterColorImages_123.h5.zip'
input_file=urllib.request.urlopen(fpath+zf)
output_file=open(zf,'wb'); 
output_file.write(input_file.read())
output_file.close(); input_file.close()
zipf=zipfile.ZipFile(zf,'r')
zipf.extractall(''); zipf.close()
f=h5py.File(zf[:-4],'r')
keys=list(f.keys()); print(keys)
images=np.array(f[keys[1]])
labels=np.array(f[keys[2]]).reshape(-1,1)-1
x_train2,x_test2,y_train2,y_test2=\
train_test_split(images,labels,test_size=.2,random_state=1)
del images,labels
[[x_train2,x_valid2,x_test2],
 [y_train2,y_valid2,y_test2],
 [cy_train2,cy_valid2,cy_test2]]=\
prepro(x_train2,y_train2,x_test2,y_test2,33)
display_10img(x_test2,y_test2,32)

"""## MLP Building & Training"""

def cat_accuracy(predictions,labels):
    return (100.0*np.sum(np.argmax(predictions,1)==\
           np.argmax(labels,1))/predictions.shape[0])
def mlp(x,weights,biases):
    layer1=tf.add(tf.matmul(x,weights['W1']),biases['b1'])
    layer2=tf.add(tf.matmul(layer1,weights['W2']),biases['b2'])
    return tf.matmul(layer2,weights['out'])+biases['out']

def nn_train(x_train,cy_train,x_test,cy_test,
             lr,epochs,hidden1,hidden2,batch_size,
             display_step,n_inputs,n_classes):
    graph=tf.Graph()
    with graph.as_default():
        weights={'W1':tf.Variable(\
        tf.compat.v1.random_normal([n_inputs,hidden1])),
        'W2':tf.Variable(\
        tf.compat.v1.random_normal([hidden1,hidden2])),
        'out':tf.Variable(\
        tf.compat.v1.random_normal([hidden2,n_classes]))}
        biases={'b1':tf.Variable(\
        tf.compat.v1.random_normal([hidden1])),
        'b2':tf.Variable(\
        tf.compat.v1.random_normal([hidden2])),
        'out':tf.Variable(\
        tf.compat.v1.random_normal([n_classes]))}
        X=tf.compat.v1.placeholder("float32",[None,n_inputs])
        y=tf.compat.v1.placeholder("int32",[None,n_classes])
        vX=tf.constant(x_test.reshape(-1,n_inputs))
        logits=mlp(X,weights,biases)
        vlogits=mlp(vX,weights,biases)
        loss=tf.reduce_mean(\
        tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=y))
        optimizer=tf.compat.v1.train.AdamOptimizer(learning_rate=lr)
        train_opt=optimizer.minimize(loss)
        train_predictions=tf.nn.softmax(logits)
        test_predictions=tf.nn.softmax(vlogits)
    with tf.compat.v1.Session(graph=graph) as sess:
        tf.compat.v1.global_variables_initializer().run()
        for epoch in range(epochs):
            avg_loss=0.; avg_acc=0.
            total_batch=int(x_train.shape[0]/batch_size)
            for i in range(total_batch):
                offset=(i*batch_size)%(x_train.shape[0]-batch_size)
                batch_X=x_train.reshape(-1,32*32*3)[offset:(offset+batch_size)]
                batch_y=cy_train[offset:(offset+batch_size)]
                _,l,batch_py=\
                sess.run([train_opt,loss,train_predictions],
                         feed_dict={X:batch_X,y:batch_y})
                avg_loss+=l/total_batch
                avg_acc+=cat_accuracy(batch_py,batch_y)/total_batch
            if epoch%display_step==0:
                print("Epoch: %04d"%(epoch+1),
                      "loss={:.9f}".format(avg_loss),
                      "accuracy={:.3f}".format(avg_acc))
        print("Test accuracy: %.3f%%"%\
        cat_accuracy(test_predictions.eval(),cy_test))

lr=.001; epochs=15
hidden1=512; hidden2=256
batch_size=128; display_step=1 
n_inputs=32*32*3; n_classes=10
tf.compat.v1.reset_default_graph()
nn_train(x_train1,cy_train1,x_test1,cy_test1,
         lr,epochs,hidden1,hidden2,batch_size,
         display_step,n_inputs,n_classes)

lr=.001; epochs=100; hidden1=512; hidden2=256
batch_size=128; display_step=5; 
n_inputs=32*32*3; n_classes=33
tf.compat.v1.reset_default_graph()
nn_train(x_train2,cy_train2,x_test2,cy_test2,
         lr,epochs,hidden1,hidden2,batch_size,
         display_step,n_inputs,n_classes)

"""## CNN Building & Training"""

lr=.001; epochs=200; 
batch_size=128; display_step=5 
img_size=32; n_classes=10
save_model_path='./img_class'

def cnn(x,n_classes,conv1,conv2,dense1):
    W1=tf.Variable(tf.compat.v1\
         .truncated_normal([2,2,x.shape[3],conv1],stddev=.04))
    b1=tf.Variable(tf.compat.v1\
         .constant(.04,shape=[conv1]))
    x=tf.nn.conv2d(x,W1,strides=[1,5,5,1],padding='SAME')
    x=tf.nn.relu(x+b1)
    x=tf.nn.max_pool(x,ksize=[1,2,2,1], 
                     strides=[1,2,2,1],padding='SAME')
    x=tf.nn.dropout(x,.2)
    W2=tf.Variable(tf.compat.v1\
         .truncated_normal([2,2,x.shape[3],conv2],stddev=.04))
    b2=tf.Variable(tf.compat.v1\
         .constant(.04,shape=[conv2]))
    x=tf.nn.conv2d(x,W2,strides=[1,2,2,1],padding='SAME')
    x=tf.nn.relu(x+b2)
    x=tf.nn.max_pool(x,ksize=[1,2,2,1], 
                     strides=[1,2,2,1],padding='SAME')
    x=tf.nn.dropout(x,.2)
    x=tf.reshape(x,[-1,x.shape[1]*x.shape[2]*x.shape[3]])
    W3=tf.Variable(tf.compat.v1.\
    truncated_normal([x.shape[1],dense1],stddev=.04))
    b3=tf.Variable(tf.compat.v1.truncated_normal([dense1],stddev=.04))
    x=tf.nn.relu(tf.add(tf.matmul(x,W3),b3)) 
    W=tf.Variable(tf.compat.v1.\
    truncated_normal([x.shape[1],n_classes],stddev=.04))
    b=tf.Variable(tf.compat.v1.truncated_normal([n_classes],stddev=.04))
    x=tf.add(tf.matmul(x,W),b)
    return x

tf.compat.v1.reset_default_graph()
graph=tf.Graph()
with graph.as_default():
    X=tf.compat.v1.\
    placeholder("float32",[None,img_size,img_size,3],name='x')
    y=tf.compat.v1.placeholder("int32",[None,n_classes],name='y')
    logits=cnn(X,n_classes,32,196,1024)
    logits=tf.compat.v1.identity(logits,name='logits')
    loss=tf.reduce_mean(\
    tf.nn.softmax_cross_entropy_with_logits(logits=logits,labels=y))
    optimizer=tf.compat.v1.train.AdamOptimizer(learning_rate=lr)
    train_opt=optimizer.minimize(loss)
    train_predictions=tf.nn.softmax(logits)
    correct_predictions=tf.equal(tf.argmax(train_predictions,1),
                                 tf.argmax(y,1))
    accuracy=tf.reduce_mean(tf.cast(correct_predictions,tf.float32),
                            name='accuracy')

with tf.compat.v1.Session(graph=graph) as sess:
    tf.compat.v1.global_variables_initializer().run()
    for epoch in range(epochs):
        avg_loss=0.; avg_acc=0.
        total_batch=int(x_train1.shape[0]/batch_size)
        for i in range(total_batch):
            offset=(i*batch_size)%(x_train1.shape[0]-batch_size)
            batch_X=x_train1[offset:(offset+batch_size)]
            batch_y=cy_train1[offset:(offset+batch_size)]
            _,l,_,_,acc=sess.run([train_opt,loss,train_predictions,
                                  correct_predictions,accuracy],
                                  feed_dict={X:batch_X,y:batch_y})
            avg_loss+=l/total_batch
            avg_acc+=acc/total_batch
        if epoch%display_step==0:
            print("Epoch: %04d"%(epoch+1),
                  "loss={:.9f}".format(avg_loss),
                  "accuracy={:.3f}".format(avg_acc))
    saver=tf.compat.v1.train.Saver()
    save_path=saver.save(sess,save_model_path)

loaded_graph=tf.Graph()
with tf.compat.v1.Session(graph=loaded_graph) as sess:
    loader=tf.compat.v1.train.import_meta_graph(save_model_path+'.meta')
    loader.restore(sess,save_model_path)
    loaded_X=loaded_graph.get_tensor_by_name('x:0')
    loaded_y=loaded_graph.get_tensor_by_name('y:0')
    loaded_logits=loaded_graph.get_tensor_by_name('logits:0')
    loaded_acc=loaded_graph.get_tensor_by_name('accuracy:0')
    loss=tf.reduce_mean(\
    tf.nn.softmax_cross_entropy_with_logits(logits=loaded_logits,
                                            labels=loaded_y))
    avg_loss=0.; avg_acc=0.
    total_batch=int(x_valid1.shape[0]/batch_size)
    for i in range(total_batch):
        offset=(i*batch_size)%(x_valid1.shape[0]-batch_size)
        batch_X=x_valid1[offset:(offset+batch_size)]
        batch_y=cy_valid1[offset:(offset+batch_size)]
        l,acc=sess.run([loss,loaded_acc],
                     feed_dict={loaded_X:batch_X,
                                loaded_y:batch_y})
        avg_loss+=l/total_batch
        avg_acc+=acc/total_batch
    print("test loss={:.9f}".format(avg_loss),
          "test accuracy={:.3f}".format(avg_acc))

"""## Comparing with Keras Applications"""

def premodel(pix,den,mh,lbl):
    model=tf.keras.Sequential([
        tf.keras.layers.Input((pix,pix,3),
                              name='input'),
        th.KerasLayer(mh,trainable=True),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(den,activation='relu'),
        tf.keras.layers.Dropout(rate=.5),
        tf.keras.layers.Dense(lbl,activation='softmax')])
    model.compile(optimizer='adam',metrics=['accuracy'],
                  loss='categorical_crossentropy')
    display(model.summary())
    return model

[handle_base,pixels]=["mobilenet_v2_050_96",96]
mhandle="https://tfhub.dev/google/imagenet/{}/feature_vector/4"\
.format(handle_base)
fw='weights.best.hdf5'

[x_train1,x_valid1,x_test1]=\
display_resize(x_train1,x_valid1,x_test1,
               y_valid1,cy_valid1,pixels)

model=premodel(pixels,512,mhandle,10)
history=model.fit(x=x_train1,y=cy_train1,batch_size=64,
                  epochs=10,callbacks=cb(fw),
                  validation_data=(x_valid1,cy_valid1))

model.load_weights(fw)
model.evaluate(x_test1,cy_test1)

del x_train1,x_valid1,x_test1,\
y_train1,y_valid1,y_test1,\
cy_train1,cy_valid1,cy_test1

[x_train2,x_valid2,x_test2]=\
display_resize(x_train2,x_valid2,x_test2,
               y_valid2,cy_valid2,pixels)

model=premodel(pixels,512,mhandle,33)
history=model.fit(x=x_train2,y=cy_train2,batch_size=64,
                  epochs=100,callbacks=cb(fw),
                  validation_data=(x_valid2,cy_valid2))

model.load_weights(fw)
model.evaluate(x_test2,cy_test2)