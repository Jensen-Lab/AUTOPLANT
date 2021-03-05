%% --- Script for transfer learning GoogLeNet to detect glandular trichomes --- %% 
%% --- Magnus Paludan, 2021 --- %% 
%% --- DTU Physics --- %% 



%% Make network
clc 
clear all
close all

%Transfer learning on GoogLeNet 
net = googlenet; 
lgraph = layerGraph(net);

newLayers1 = [fullyConnectedLayer(2,'name','newfc')]; 
newLayers2 = [softmaxLayer('name','newsoftmax')]; 
newLayers3 = [classificationLayer('name','newclassification')];

%Replace classification layers (1000 outputs) with new classification
%layers (2 outputs)
lgraph = replaceLayer(lgraph,'loss3-classifier',newLayers1);
lgraph = replaceLayer(lgraph,'prob',newLayers2); 
lgraph = replaceLayer(lgraph,'output',newLayers3); 

%% Import training data 
folder = cd; 
folder_training_data = fullfile(folder,'../generate_training_data/training_data'); 

imds = imageDatastore(folder_training_data,'IncludeSubfolders',true,'LabelSource','foldernames');
[imdsTrain,imdsValidation] = splitEachLabel(imds,0.7,'randomized');

augimdsTrain = augmentedImageDatastore([224 224],imdsTrain);
augimdsValidation = augmentedImageDatastore([224 224],imdsValidation);

%% Train network
options = trainingOptions('sgdm', ...
    'ExecutionEnvironment','auto',...
    'MiniBatchSize',10, ...
    'MaxEpochs',4, ...
    'Shuffle','every-epoch', ...
    'InitialLearnRate',1e-4, ...
    'ValidationData',augimdsValidation, ...
    'ValidationFrequency',10, ...
    'Verbose',false, ...
    'Plots','training-progress');

neuralNet = trainNetwork(augimdsTrain,lgraph,options);
save neuralNet