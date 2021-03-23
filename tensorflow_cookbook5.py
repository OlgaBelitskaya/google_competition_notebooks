# -*- coding: utf-8 -*-
"""tensorflow_cookbook5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tqBIS9Vl3tog3QTl54JqPI-7crf-R0Lh
"""

from IPython.display import display,HTML,clear_output,Image
from IPython.core.magic import register_line_magic
#Sequential (Single-Hue,Multi-Hue),Diverging, Cyclical cmaps: 
#Reds,Sinebow,Rainbow,Turbo,Warm,Cool,Plasma,Spectral,etc.
@register_line_magic
def cmap_header(params):
    params=params.split('|'); string=params[0]
    if len(params)==1: 
        font_size='30'; font_family='Akronim'; cmap='Sinebow'
    elif  len(params)==2: 
        font_size=params[1]
        font_family='Akronim'; cmap='Sinebow'
    elif  len(params)==3: 
        font_size=params[1]; font_family=params[2]
        cmap='Sinebow'
    else: 
        font_size=params[1]; font_family=params[2]; cmap=params[3]
    html_str="""
    <head><script src='https://d3js.org/d3.v6.min.js'></script>
    </head><style>@import 'https://fonts.googleapis.com/css?family="""+\
    font_family+"""&effect=3d'; #colorized {font-family:"""+font_family+\
    """; color:white; padding-left:10px; font-size:"""+font_size+\
    """px;}</style><h1 id='colorized' class='font-effect-3d'>"""+\
    string+"""</h1><script>
    var tc=setInterval(function(){
        var now=new Date().getTime();
        var iddoc=document.getElementById('colorized');
        iddoc.style.color=d3.interpolate"""+cmap+\
    """(now%(30000)/30000);},1)</script>"""
    display(HTML(html_str))

# Commented out IPython magic to ensure Python compatibility.
# %cmap_header Code Modules & Functions

import warnings; warnings.filterwarnings('ignore')
import os,urllib,tensorflow_hub as hub
import numpy as np,tensorflow as tf,pylab as pl
import PIL.Image,time,imageio
from IPython.core.magic import register_line_magic
file_path='https://olgabelitskaya.gitlab.io/data/'
tfhub_path='https://tfhub.dev/google/magenta/'+\
           'arbitrary-image-stylization-v1-256/2'
os.environ['TFHUB_MODEL_LOAD_FORMAT']='COMPRESSED'

def get_file(file_name,folder_name,file_path=file_path):
    print(file_path+folder_name+file_name)
    input_file=urllib.request.urlopen(
        file_path+folder_name+file_name)
    output_file=open(file_name,'wb'); 
    output_file.write(input_file.read())
    output_file.close(); input_file.close()
def load_img(path_to_img,max_dim=512):
    img=tf.io.read_file(path_to_img)
    img=tf.image.decode_image(img,channels=3)
    img=tf.image.convert_image_dtype(img,tf.float32)
    shape=tf.cast(tf.shape(img)[:-1],tf.float32)
    long_dim=max(shape); scale=max_dim/long_dim
    new_shape=tf.cast(shape*scale,tf.int32)
    img=tf.image.resize(img,new_shape)
    return img[tf.newaxis,:]
def tensor2img(tensor,rot=True):
    if rot: tensor=tf.image.rot90(tensor)
    tensor=tensor*255
    tensor=np.array(tensor,dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0]==1
        tensor=tensor[0]
    return PIL.Image.fromarray(tensor)

def display_images(original_img,style_img,rot=True):
    if rot: original_img=tf.image.rot90(original_img) 
    fig=pl.figure(figsize=(10,5))
    ax=fig.add_subplot(121)
    str1='Shape of the original image: %s'
    pl.title(str1%str(original_img.shape),fontsize=int(8))
    ax.imshow(np.squeeze(original_img))
    ax=fig.add_subplot(122)
    str2='Shape of the style image: %s'
    pl.title(str2%str(style_img.shape),fontsize=int(8))
    ax.imshow(np.squeeze(style_img))
    pl.tight_layout(); pl.show()
def item_stats(item):
    for name,output in item:
        print(name)
        print('  shape: ',output.numpy().shape)
        print('  min: ',output.numpy().min())
        print('  max: ',output.numpy().max())
        print('  mean: ',output.numpy().mean())
        print(30*'-')

# Commented out IPython magic to ensure Python compatibility.
# %cmap_header Image Data

original,style='00_01_001.png','01_00_001.png'
original_folder,style_folder='humans/','paintings/'
for f in [[original,original_folder],[style,style_folder]]: 
    get_file(f[0],f[1])
original_img=load_img(original)
style_img=load_img(style)
display_images(original_img,style_img)

hub_model=hub.load(tfhub_path)
stylized_img=hub_model(
    tf.constant(original_img),
    tf.image.rot90(tf.constant(style_img)))[0]
tensor2img(stylized_img)

original,style='00_01_001.png','01_05_002.png'
original_folder,style_folder='humans/','paintings/'
for f in [[original,original_folder],[style,style_folder]]: 
    get_file(f[0],f[1])
original_img=load_img(original)
#for i in range(3): original_img=tf.image.rot90(original_img)
style_img=load_img(style)
display_images(original_img,style_img)

hub_model=hub.load(tfhub_path)
stylized_img=hub_model(
    tf.constant(original_img),tf.constant(style_img))[0]
tensor2img(stylized_img)

original,style='00_01_001.png','00_02_001.png'
original_folder,style_folder='humans/','paintings/'
for f in [[original,original_folder],[style,style_folder]]: 
    get_file(f[0],f[1])
original_img=load_img(original)
style_img=load_img(style)
display_images(original_img,style_img)

hub_model=hub.load(tfhub_path)
stylized_img=hub_model(
    tf.constant(original_img),
    tf.image.rot90(tf.constant(style_img)))[0]
tensor2img(stylized_img)

original,style='00_01_001.png','00_03_001.png'
original_folder,style_folder='humans/','paintings/'
for f in [[original,original_folder],[style,style_folder]]: 
    get_file(f[0],f[1])
original_img=load_img(original)
style_img=load_img(style)
display_images(original_img,style_img)

hub_model=hub.load(tfhub_path)
stylized_img=hub_model(
    tf.constant(original_img),
    tf.image.rot90(tf.constant(style_img)))[0]
tensor2img(stylized_img)

# Commented out IPython magic to ensure Python compatibility.
# %cmap_header Keras Applications

vgg19=tf.keras.applications.VGG19(
    include_top=False,weights='imagenet')
layers=[]
for layer in vgg19.layers:
    layers+=[layer.name]
for i in range(5): print(layers[5*i:5*(i+1)])
original_layers=['block5_conv2'] 
style_layers=['block1_conv1','block2_conv1',
              'block3_conv1','block4_conv1','block5_conv1']
num_original_layers=len(original_layers)
num_style_layers=len(style_layers)

def vgg_layers(layer_names):
    vgg19=tf.keras.applications.VGG19(
        include_top=False,weights='imagenet')
    vgg19.trainable=False
    outputs=[vgg19.get_layer(name).output 
             for name in layer_names]
    model=tf.keras.Model([vgg19.input],outputs)
    return model

# Commented out IPython magic to ensure Python compatibility.
# %cmap_header Style Extracting

original,style='00_01_001.png','03_06_001.png'
original_folder,style_folder='humans/','paintings/'
for f in [[original,original_folder],[style,style_folder]]: 
    get_file(f[0],f[1])
original_img=load_img(original)
style_img=load_img(style)
display_images(original_img,style_img)
style_extractor=vgg_layers(style_layers)
style_outputs=style_extractor(style_img*255)
item_stats(zip(style_layers,style_outputs))

def gram_matrix(input_tensor):
    result=tf.linalg.einsum(
        'bijc,bijd->bcd',input_tensor,input_tensor)
    input_shape=tf.shape(input_tensor)
    num_locations=tf.cast(
        input_shape[1]*input_shape[2],tf.float32)
    return result/(num_locations)

class StyleOriginalModel(tf.keras.models.Model):
    def __init__(self,style_layers,original_layers):
        super(StyleOriginalModel,self).__init__()
        self.vgg=vgg_layers(style_layers+original_layers)
        self.style_layers=style_layers
        self.original_layers=original_layers
        self.num_style_layers=len(style_layers)
        self.vgg.trainable=False
    def call(self,inputs):
        inputs=inputs*255.0
        preprocessed_input=\
        tf.keras.applications.vgg19.preprocess_input(inputs)
        outputs=self.vgg(preprocessed_input)
        style_outputs,original_outputs=\
        (outputs[:self.num_style_layers],
         outputs[self.num_style_layers:])
        style_outputs=[gram_matrix(style_output)
                       for style_output in style_outputs]
        original_dict={original_name:value for original_name,value 
                       in zip(self.original_layers,original_outputs)}
        style_dict={style_name:value for style_name,value
                    in zip(self.style_layers,style_outputs)}
        return {'original':original_dict,'style':style_dict}

extractor=StyleOriginalModel(style_layers,original_layers)
results=extractor(tf.constant(original_img))
print('Styles:')
item_stats(sorted(results['style'].items()))
print('Originals:')
item_stats(sorted(results['original'].items()))

# Commented out IPython magic to ensure Python compatibility.
# %cmap_header Gradient Descent Steps

style_targets=extractor(tf.image.rot90(style_img))['style']
original_targets=extractor(original_img)['original']
optimizer=tf.optimizers.Adam(
    learning_rate=.01,beta_1=.99,epsilon=.1)
style_weight=.02; original_weight=10**3
img=tf.Variable(original_img)

def clip01(img):
  return tf.clip_by_value(
      img,clip_value_min=0.,clip_value_max=1.)

def style_original_loss(outputs):
    style_outputs=outputs['style']
    original_outputs=outputs['original']
    style_loss=tf.add_n(
        [tf.reduce_mean((style_outputs[name]-style_targets[name])**2) 
         for name in style_outputs.keys()])
    style_loss*=style_weight/num_style_layers
    original_loss=tf.add_n(
        [tf.reduce_mean((original_outputs[name]-original_targets[name])**2) 
         for name in original_outputs.keys()])
    original_loss*=original_weight/num_original_layers
    loss=style_loss+original_loss
    return loss

@tf.function()
def train_step(img,optimizer=optimizer):
  with tf.GradientTape() as tape:
    outputs=extractor(img)
    loss=style_original_loss(outputs)
  gradient=tape.gradient(loss,img)
  optimizer.apply_gradients([(gradient,img)])
  img.assign(clip01(img))

for i in range(5):
    train_step(img)
tensor2img(img)

start=time.time()
epochs=30; steps_per_epoch=100
step=0
for n in range(epochs):
    for m in range(steps_per_epoch):
        step+=1
        train_step(img)
        print('-',end='')
    clear_output(wait=True)
    display(tensor2img(img))
    print('Train step: {}'.format(step))
end=time.time()
print('Total time: {:.1f}'.format(end-start))

# Commented out IPython magic to ensure Python compatibility.
# %cmap_header Total Variation Loss

def highpass_xy(img):
    x_var=img[:,:,1:,:]-img[:,:,:-1,:]
    y_var=img[:,1:,:,:]-img[:,:-1,:,:]
    return x_var,y_var

rot=True
if rot: rot_img=tf.image.rot90(original_img)
x_deltas,y_deltas=highpass_xy(rot_img)
pl.figure(figsize=(10,8))
pl.subplot(2,4,1)
pl.imshow(tf.squeeze(clip01(2*y_deltas+.5)))
pl.title('Horizontal Deltas | Original')
pl.subplot(2,4,2)
pl.imshow(tf.squeeze(clip01(2*x_deltas+.5)))
pl.title('Vertical Deltas | Original')
x_deltas,y_deltas=highpass_xy(rot_img)
pl.subplot(2,4,3)
pl.imshow(tf.squeeze(clip01(2*y_deltas+.5)))
pl.title('Horizontal Deltas | Styled')
pl.subplot(2,4,4)
pl.imshow(tf.squeeze(clip01(2*x_deltas+.5)))
pl.title('Vertical Deltas | Styled')
sobel=tf.image.sobel_edges(rot_img)
pl.subplot(2,4,5)
pl.imshow(tf.squeeze(clip01(sobel[...,0]/4+.5)))
pl.title('Horizontal Sobel-edges')
pl.subplot(2,4,6)
pl.imshow(tf.squeeze(clip01(sobel[...,1]/4+.5)))
pl.title('Vertical Sobel-edges');

def total_variation_loss(img):
    x_deltas,y_deltas=highpass_xy(img)
    return tf.reduce_sum(tf.abs(x_deltas))+\
           tf.reduce_sum(tf.abs(y_deltas))

total_variation_loss(img).numpy(),\
tf.image.total_variation(img).numpy()

# Commented out IPython magic to ensure Python compatibility.
# %cmap_header Train Steps with Total Variation Loss

total_variation_weight=10
img=tf.Variable(original_img)
@tf.function()
def train_step(img,total_variation_weight=total_variation_weight):
    with tf.GradientTape() as tape:
        outputs=extractor(img)
        loss=style_original_loss(outputs)
        loss+=total_variation_weight*tf.image.total_variation(img)
    gradient=tape.gradient(loss,img)
    optimizer.apply_gradients([(gradient,img)])
    img.assign(clip01(img))

start=time.time()
epochs=100; steps_per_epoch=100
step=0; imgs=[]
for n in range(epochs):
    for m in range(steps_per_epoch):
        step+=1
        train_step(img)
        print('-',end='')
    clear_output(wait=True)
    display(tensor2img(img))
    if rot: 
        imgs.append(np.squeeze(tf.image.rot90(img).numpy()))
    else: 
        imgs.append(np.squeeze(img.numpy()))
    print('Train step: {}'.format(step))
end=time.time()
imgs=np.array(imgs)
print('Total time: {:.1f}'.format(end-start))

file_name='pic.gif'
imgs=np.array(imgs*255,dtype=np.uint8)
imageio.mimsave(file_name,imgs)
Image(open('pic.gif','rb').read())