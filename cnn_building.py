# -*- coding: utf-8 -*-
"""cnn_building.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w58DSF3go_wKcqfBLIDt1PFyj1H6XrXi
"""

# Commented out IPython magic to ensure Python compatibility.
from IPython.display import display,HTML
c1,c2,f1,f2,fs1,fs2=\
'#11ff66','#6611ff','Wallpoet','Orbitron',20,10
def dhtml(string,fontcolor=c1,font=f1,fontsize=fs1):
    display(HTML("""<style>
    @import 'https://fonts.googleapis.com/css?family="""\
    +font+"""&effect=3d-float';</style>
    <h1 class='font-effect-3d-float' 
    style='font-family:"""+font+\
    """; color:"""+fontcolor+\
    """; font-size:"""+str(fontsize)+"""px;'>
#     %s</h1>"""%string))

dhtml('Code Modules, Setting, & Functions')

import warnings,imageio,urllib
import tensorflow as tf,pylab as pl
import pandas as pd,numpy as np
import tensorflow.keras.layers as tkl
import tensorflow.keras.utils as tku
import tensorflow.keras.callbacks as tkc
import tensorflow_datasets as tfds
from sklearn.metrics import \
classification_report,confusion_matrix
from IPython.core.magic import register_line_magic

warnings.filterwarnings('ignore')
pd.set_option('precision',3)
tf.keras.backend.set_floatx('float64')
fw='weights.best.hdf5'
buffer_size,batch_size=10000,64
pixels,pixels2=28,32
num_classes=10

@register_line_magic
def display_examples(pars):
    pars=pars.split()
    data,n=pars[0],int(pars[1])
    if data=='mnist': data=mnist_test
    if data=='cifar': data=cifar_test
    batch=next(iter(data.batch(n)))
    images=batch['image'].numpy()
    labels=batch['label'].numpy() 
    fig=pl.figure(figsize=(2*n//3,4.5))
    for i in range(n):
        ax=fig.add_subplot(3,n//3,i+1)
        ax.set_xticks([]); ax.set_yticks([])
        ax.imshow(np.squeeze(images[i]),
                  cmap='bone')
        ax.text(.85,.15,'{}'.format(labels[i]), 
                fontdict={'color':c1,'fontsize':30},
                horizontalalignment='center',
                verticalalignment='center', 
                transform=ax.transAxes)
    pl.show()

@register_line_magic
def display_reports(data):
    global model,fw,buffer_size,c2,f2,fs2
    model.load_weights(fw)
    if data=='mnist': data=mnist_test
    if data=='cifar': data=cifar_test
    test_results=model.evaluate(data.batch(buffer_size))
    dhtml('\ntest accuracy: {:.2f}%'\
          .format(test_results[1]*100),
          c2,f2,fs2)
    batch=next(iter(data.batch(buffer_size)))
    y_test=batch[1].numpy()
    py_test=np.argmax(
        model.predict(data.batch(buffer_size)),
                      axis=-1)
    dhtml('Classification Report',c2,f2,fs2)
    print(classification_report(y_test,py_test))
    dhtml('Confusion Matrix',c2,f2,fs2)
    print(confusion_matrix(y_test,py_test))

def cb(fw):
    early_stopping=\
    tkc.EarlyStopping(monitor='val_loss',
                      patience=10,verbose=2)
    checkpointer=\
    tkc.ModelCheckpoint(filepath=fw,
                        save_best_only=True,verbose=2)
    lr_reduction=\
    tkc.ReduceLROnPlateau(monitor='val_loss',verbose=2,
                          patience=5,factor=.75)
    return [checkpointer,early_stopping,
            lr_reduction]

def history_plot(fit_history):
    pl.figure(figsize=(10,10)); pl.subplot(211)
    keys=list(fit_history.history.keys())[0:4]
    pl.plot(fit_history.history[keys[0]],
            color=c1,label='train')
    pl.plot(fit_history.history[keys[2]],
            color=c2,label='valid')
    pl.xlabel("Epochs"); pl.ylabel("Loss")
    pl.legend(); pl.grid()
    pl.title('Loss Function')     
    pl.subplot(212)
    pl.plot(fit_history.history[keys[1]],
            color=c1,label='train')
    pl.plot(fit_history.history[keys[3]],
            color=c2,label='valid')
    pl.xlabel("Epochs"); pl.ylabel("Accuracy")    
    pl.legend(); pl.grid()
    pl.title('Accuracy'); pl.show()

dhtml('Data Processing')

mnist=tfds.builder('mnist')
mnist.download_and_prepare()
ds=mnist.as_dataset(shuffle_files=False,
            split=['train','test'])
mnist_train,mnist_test=ds[0],ds[1]

# Commented out IPython magic to ensure Python compatibility.
dhtml(mnist.info.features['image'],c2,f2,fs2)
dhtml(mnist.info.features['label'],c2,f2,fs2)
# %display_examples mnist 9

mnist_train=mnist_train.map(
    lambda item:(tf.cast(item['image'],tf.float32)/255., 
                 tf.cast(item['label'],tf.int32)))
mnist_test=mnist_test.map(
    lambda item:(tf.cast(item['image'],tf.float32)/255., 
                  tf.cast(item['label'],tf.int32)))
tf.random.set_seed(123)
mnist_train=mnist_train\
.shuffle(buffer_size=buffer_size,
         reshuffle_each_iteration=False)
mnist_valid=mnist_train.take(buffer_size).batch(batch_size)
mnist_train=mnist_train.skip(buffer_size).batch(batch_size)

cifar=tfds.builder('cifar10')
cifar.download_and_prepare()
ds=cifar.as_dataset(shuffle_files=False,
                    split=['train','test'])
cifar_train,cifar_test=ds[0],ds[1]

# Commented out IPython magic to ensure Python compatibility.
dhtml(cifar.info.features['image'],c2,f2,fs2)
dhtml(cifar.info.features['label'],c2,f2,fs2)
# %display_examples cifar 12

cifar_train=cifar_train.map(
    lambda item:(tf.cast(item['image'],tf.float32)/255., 
                 tf.cast(item['label'],tf.int32)))
cifar_test=cifar_test.map(
    lambda item:(tf.cast(item['image'],tf.float32)/255., 
                  tf.cast(item['label'],tf.int32)))
tf.random.set_seed(123)
cifar_train=cifar_train\
.shuffle(buffer_size=buffer_size,
         reshuffle_each_iteration=False)
cifar_valid=cifar_train.take(buffer_size).batch(batch_size)
cifar_train=cifar_train.skip(buffer_size).batch(batch_size)

dhtml('CNN Construction. One Channel')

model=tf.keras.Sequential()
model.add(tkl.Input((pixels,pixels,1),
                    name='input'))
model.add(tkl.Conv2D(
    filters=32,kernel_size=(7,7),
    strides=(1,1),padding='same',
    name='conv_1'))
model.add(tkl.LeakyReLU(alpha=.02,
                        name='lrelu_1'))
model.add(tf.keras.layers.MaxPool2D(
    pool_size=(2,2),name='pool_1'))
model.add(tkl.Dropout(.25,name='drop_1'))
model.add(tkl.Conv2D(
    filters=96,kernel_size=(7,7),
    strides=(1,1),padding='same',
    name='conv_2'))
model.add(tkl.LeakyReLU(alpha=.02,
                        name='lrelu_2'))
model.add(tf.keras.layers.MaxPool2D(
    pool_size=(2,2),name='pool_2'))
model.add(tkl.Dropout(.25,name='drop_2'))
model.add(tkl.Conv2D(
    filters=512,kernel_size=(7,7),
    strides=(1,1),padding='same',
    name='conv_3'))
model.add(tkl.LeakyReLU(alpha=.02,
                        name='lrelu_3'))
model.add(tf.keras.layers.MaxPool2D(
    pool_size=(2,2),name='pool_3'))
model.add(tkl.Dropout(.25,name='drop_3'))
model.compute_output_shape(
    input_shape=(batch_size,pixels,pixels,1))

model.add(tkl.GlobalMaxPooling2D(name='gmpool'))   
model.add(tkl.Dense(512,name='dense_1'))
model.add(tkl.LeakyReLU(alpha=.02,
                        name='lrelu_4'))
model.add(tkl.Dropout(.5,name='drop_4'))
model.compute_output_shape(
    input_shape=(batch_size,pixels,pixels,1))

model.add(tkl.Dense(num_classes,
                    activation='softmax',
                    name='out'))
tku.plot_model(model,show_shapes=True)

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])
history=model.fit(mnist_train,epochs=50,shuffle=True, 
                  validation_data=mnist_valid,
                  callbacks=cb(fw))

history_plot(history)

# Commented out IPython magic to ensure Python compatibility.
# %display_reports mnist

dhtml('NN Construction. Three Channels')

model=tf.keras.Sequential()
model.add(tkl.Input((pixels2,pixels2,3),
                    name='input'))
model.add(tkl.Conv2D(
    filters=32,kernel_size=(5,5),
    strides=(1,1),padding='same',
    name='conv_1'))
model.add(tkl.LeakyReLU(alpha=.02,
                        name='lrelu_1'))
model.add(tf.keras.layers.MaxPool2D(
    pool_size=(2,2),name='pool_1'))
model.add(tkl.Dropout(.25,name='drop_1'))
model.add(tkl.Conv2D(
    filters=196,kernel_size=(5,5),
    strides=(1,1),padding='same',
    name='conv_2'))
model.add(tkl.LeakyReLU(alpha=.02,
                        name='lrelu_2'))
model.add(tf.keras.layers.MaxPool2D(
    pool_size=(2,2),name='pool_2'))
model.add(tkl.Dropout(.25,name='drop_2'))
model.compute_output_shape(
    input_shape=(batch_size,pixels2,pixels2,3))

model.add(tkl.GlobalMaxPooling2D(name='gmpool'))   
model.add(tkl.Dense(1024,name='dense_1'))
model.add(tkl.LeakyReLU(alpha=.02,
                        name='lrelu_3'))
model.add(tkl.Dropout(.5,name='drop_3'))
model.compute_output_shape(
    input_shape=(batch_size,pixels2,pixels2,3))

model.add(tkl.Dense(num_classes,
                    activation='softmax',
                    name='out'))
tku.plot_model(model,show_shapes=True)

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses\
              .SparseCategoricalCrossentropy(),
              metrics=['accuracy'])
history=model.fit(cifar_train,epochs=50,shuffle=True, 
                  validation_data=cifar_valid,
                  callbacks=cb(fw))

history_plot(history)

# Commented out IPython magic to ensure Python compatibility.
# %display_reports cifar