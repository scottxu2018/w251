# w251_finalproject

# Commands used on VM to start docker image / etc
 docker run --rm --runtime=nvidia -it -p 8888:8888 -v /root:/root w251/hw06:x86-64
# Commands used to download s3fs object storage
# This command pulls from the edible bucket into a folder root/train2
s3cmd sync s3://edible train2

# This python script takes the flattened image file names and saves them in the correct
# Folder structure so that the training file works properly
import os, sys, glob
from shutil import copyfile

filepath = 'train'
files = os.listdir(filepath)
x = 0
for file in files:
    folder = ' '.join(file.split('/')[-1].split('_')[:-1])
    folder = folder.lstrip(' ').rstrip(' ')
    if not os.direxists(filepath + '/' + folder):
        os.mkdir(filepath + '/' + folder)
    copyfile(file, filepath + '/' + folder + '/' + str(x) + '.jpg')


# Training
86% after 100 setting

```
def build_finetune_model(base_model, dropout, fc_layers, num_classes):
    for layer in base_model.layers:
        layer.trainable = True

    x = base_model.output
    x = Flatten()(x)
    for fc in fc_layers:
        # Can look here if adding different types of layers has an effect
        # Also explore differences in changing activation function
        # Can also iterate on droupout amount
        x = Dense(fc, activation='relu')(x) 
        x = Dropout(dropout)(x)

    # New softmax layer
    predictions = Dense(num_classes, activation='softmax')(x) 
    
    finetune_model = Model(inputs=base_model.input, outputs=predictions)

    return finetune_model

# Can change the model architecture here
FC_LAYERS = [128,32]
dropout = 0.3
```

# Two options to save model after training for now
1) Frozen the graph and save as pb file
example file https://drive.google.com/drive/folders/1mwGs2R9QrS15nyakswxPtOzmiYW0t2Cn
2) Convert h5 to ckpt
example file https://drive.google.com/drive/folders/1CvKaJvVOvIX0Hx1aMZQAUS48j6Tbvxig

# TX2 deployment

Docker cmd: docker run --privileged --rm -p 8888:8888 -d tensorrtlab05

Went through https://docs.nvidia.com/deeplearning/frameworks/tf-trt-user-guide/index.html

This is the last issue https://github.com/keras-team/keras/issues/11032 i went through. It seems unsolved.

The batch norm layer creates some issues when reloading.
In frozen graph, error shows 
ValueError: Input 0 of node bn_conv1/cond/ReadVariableOp/Switch was passed float from bn_conv1/gamma:0 incompatible with expected resource.

In checkpoint, error shows: 
ValueError: Tensor name 'bn_conv1/cond/ReadVariableOp/Switch:1' is invalid.

So we might need get back to tensorflow not keras to train the model in order to deploy properly on TX2 as the vanilla resnet model.