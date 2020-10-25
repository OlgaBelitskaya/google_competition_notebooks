# -*- coding: utf-8 -*-
"""style_transfer_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xXFADlgQ1YQmXODto1Fa6Nb-lNzqY8-b

# Style Transfer 3
Perfect and complete explanation - [Artistic Style Transfer by Naoki Shibuya](https://github.com/naokishibuya/deep-learning/blob/master/python/artistic_style_transfer.ipynb)
## Libraries
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import warnings; warnings.filterwarnings('ignore')
import urllib,cv2
from PIL import Image
import numpy as np,tensorflow as tf,pylab as pl,keras as ks
from tqdm import tqdm
fpath='https://olgabelitskaya.github.io/'
style_layers=['block1_conv1','block2_conv1','block3_conv1',
              'block4_conv1','block5_conv1']

#from google.colab import files
#uploaded=files.upload()

#!ls

#for k,v in uploaded.items():
#    open(k,'wb').write(v)

"""## Displaying Vertical Images"""

def display_images(original,style,fpath=fpath):
    input_file=urllib.request.urlopen(fpath+original)
    output_file=open(original,'wb'); 
    output_file.write(input_file.read())
    output_file.close(); input_file.close()
    input_file=urllib.request.urlopen(fpath+style)
    output_file=open(style,'wb'); 
    output_file.write(input_file.read())
    output_file.close(); input_file.close()
    original_img=cv2.imread(original)
    style_img=cv2.imread(style)    
    pl.figure(1,figsize=(12,4))
    pl.subplot(121)
    pl.title("Shape of the original image: %s"%str(original_img.shape))
    pl.imshow(cv2.cvtColor(original_img,cv2.COLOR_BGR2RGB))
    pl.subplot(122)
    pl.title("Shape of the style image: %s"%str(style_img.shape))
    pl.imshow(cv2.cvtColor(style_img,cv2.COLOR_BGR2RGB)); pl.show()

display_images('HMRM.png','pattern02.png')

"""## Preprocessing"""

def rr_img(image,angle,width,height):
    [h,w]=image.shape[:2]; x,y=w//2,h//2
    M=cv2.getRotationMatrix2D((x,y),-angle,1.)
    cos,sin=np.abs(M[0,0]),np.abs(M[0,1])
    nw,nh=int((h*sin)+(w*cos)),int((h*cos)+(w*sin))
    M[0,2]+=(nw/2)-x; M[1,2]+=(nh/2)-y
    img=cv2.warpAffine(image,M,(nw,nh))
    return cv2.resize(img,(width,height)).astype('float32')

picture01=cv2.imread('HMRM.png').astype('float32')
pattern01=cv2.imread('pattern02.png').astype('float32')
picture01=rr_img(picture01,90,500,400)
pattern01=rr_img(pattern01,0,500,400)
picture01.shape,pattern01.shape

picture01[1]

def preprocess(img):
    img=img.copy(); img=np.expand_dims(img,axis=0) 
    return ks.applications.vgg16.preprocess_input(img)
def deprocess(img):
    img=img.copy()[0]                        
    img[:,:,0]+=103.939; img[:,:,1]+=116.779; img[:,:,2]+=123.68             
    img=img[:,:,::-1]              
    img=np.clip(img,0,255)         
    return img.astype('uint8')

def inputs(original_img,style_img):
    original_input=tf.constant(preprocess(original_img))
    style_input=tf.constant(preprocess(style_img))
    generated_input=tf.placeholder(tf.float32,original_input.shape)
    return original_input,style_input,generated_input

original_input,style_input,generated_input=\
inputs(picture01,pattern01)
input_tensor=tf.concat([original_input,style_input,
                        generated_input],axis=0)
input_tensor.shape

"""## VGG16 Usage"""

vgg16_model=ks.applications.vgg16.\
VGG16(input_tensor=input_tensor,include_top=False)
vgg16_layer_dict={layer.name:layer for layer in vgg16_model.layers}
vgg16_model.summary()

def calculate_original_loss(layer_dict,original_layer_names):
    loss=0
    for name in original_layer_names:
        layer=layer_dict[name]
        original_features=layer.output[0,:,:,:]  
        generated_features=layer.output[2,:,:,:] 
        loss+=ks.backend.sum(ks.backend.square(generated_features-original_features))
    return loss/len(original_layer_names)
def gram_matrix(x):    
    features=ks.backend.batch_flatten(ks.backend.permute_dimensions(x,(2,0,1))) 
    gram=ks.backend.dot(features,ks.backend.transpose(features))
    return gram
def get_style_loss(style_features,generated_features,size):
    S=gram_matrix(style_features)
    G=gram_matrix(generated_features)
    channels=3
    return ks.backend.sum(ks.backend.square(S-G))/(4.*(channels**2)*(size**2))
def calculate_style_loss(layer_dict,style_layer_names,size):
    loss=0
    for name in style_layer_names:
        layer=layer_dict[name]
        style_features=layer.output[1,:,:,:] 
        generated_features=layer.output[2,:,:,:] 
        loss+=get_style_loss(style_features,generated_features,size) 
    return loss/len(style_layer_names)
def calculate_variation_loss(x):
    row_diff=ks.backend.square(x[:,:-1,:-1,:]-x[:,1:,:-1,:])
    col_diff=ks.backend.square(x[:,:-1,:-1,:]-x[:,:-1,1:,:])
    return ks.backend.sum(ks.backend.pow(row_diff+col_diff,1.25))

original_loss=calculate_original_loss(vgg16_layer_dict,['block5_conv2'])
style_loss=calculate_style_loss(vgg16_layer_dict,style_layers, 
                                pattern01.shape[0]*pattern01.shape[1])
variation_loss=calculate_variation_loss(generated_input)

"""## Generated Images"""

loss=.7*original_loss+1.*style_loss+.1*variation_loss    
gradients=ks.backend.gradients(loss,generated_input)[0]
calculate=ks.backend.function([generated_input],[loss,gradients])
generated_data=preprocess(picture01) 
for i in tqdm(range(20)):
    _,gradients_value=calculate([generated_data])
    generated_data-=gradients_value*.001

loss=.7*original_loss+1.*style_loss+.1*variation_loss    
gradients=ks.backend.gradients(loss,generated_input)[0]
calculate=ks.backend.function([generated_input],[loss,gradients])
generated_data2=preprocess(picture01) 
for i in tqdm(range(200)):
    _,gradients_value=calculate([generated_data2])
    generated_data2-=gradients_value*.001

#numpy.save('generated_data.npy',generated_data)
#numpy.save('generated_data2.npy',generated_data2)

# generated_data=numpy.load('generated_data.npy')
# generated_data2=numpy.load('generated_data2.npy')

generated_image01=deprocess(generated_data)
generated_image02=deprocess(generated_data2)
generated_image01=rr_img(generated_image01,270,400,500)/255
generated_image02=rr_img(generated_image02,270,400,500)/255
pl.figure(1,figsize=(16,8))
pl.subplot(121)
pl.title("Loss function: 0.7*original_loss+1.0*style_loss+0.1*variation_loss; 20 steps")
pl.imshow(cv2.cvtColor(generated_image01,cv2.COLOR_BGR2RGB))
pl.subplot(122)
pl.title("Loss function: 0.7*original_loss+1.0*style_loss+0.1*variation_loss; 200 steps")
pl.imshow(cv2.cvtColor(generated_image02,cv2.COLOR_BGR2RGB))
pl.show()

"""## Displaying Horizontal Images"""

display_images('BH.png','pattern02.png')

"""## Generated Images"""

picture01=cv2.imread('BH.png').astype('float32')
pattern01=cv2.imread('pattern02.png').astype('float32')
picture01=cv2.resize(picture01,
                     (pattern01.shape[1],
                      pattern01.shape[0])).astype('float32')
original_input,style_input,generated_input=\
inputs(picture01,pattern01)
input_tensor=tf.concat([original_input,style_input,
                        generated_input],axis=0)
input_tensor.shape

picture01[1]

vgg16_model=ks.applications.vgg16.\
VGG16(input_tensor=input_tensor,include_top=False)
vgg16_layer_dict={layer.name:layer for layer in vgg16_model.layers}
original_loss=calculate_original_loss(vgg16_layer_dict,['block5_conv2'])
style_loss=calculate_style_loss(vgg16_layer_dict,style_layers, 
                                pattern01.shape[0]*pattern01.shape[1])
variation_loss=calculate_variation_loss(generated_input)

loss=.5*original_loss+1.*style_loss+.1*variation_loss    
gradients=ks.backend.gradients(loss,generated_input)[0]
calculate=ks.backend.function([generated_input],[loss,gradients])
generated_data=preprocess(picture01) 
for i in tqdm(range(70)):
    _,gradients_value=calculate([generated_data])
    generated_data-=gradients_value*.001

loss=.5*original_loss+1.*style_loss+.1*variation_loss    
gradients=ks.backend.gradients(loss,generated_input)[0]
calculate=ks.backend.function([generated_input],[loss,gradients])
generated_data2=preprocess(picture01) 
for i in tqdm(range(7000)):
    _,gradients_value=calculate([generated_data2])
    generated_data2-=gradients_value*.001

generated_image01=deprocess(generated_data)
generated_image02=deprocess(generated_data2)
pl.figure(1,figsize=(16,8))
pl.subplot(121)
pl.title("Loss function: 0.5*original_loss+1.0*style_loss+0.1*variation_loss; 70 steps")
pl.imshow(cv2.cvtColor(generated_image01,cv2.COLOR_BGR2RGB))
pl.subplot(122)
pl.title("Loss function: 0.5*original_loss+1.0*style_loss+0.1*variation_loss; 7000 steps")
pl.imshow(cv2.cvtColor(generated_image02,cv2.COLOR_BGR2RGB))
pl.show()