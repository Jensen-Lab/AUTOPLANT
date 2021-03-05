%% --- Script for testing gland detection CNN --- %% 
%% --- Magnus Paludan, 2021 --- %% 
%% --- DTU Physics --- %% 

clc
clear all
close all

addpath('../train_neural_network/');
addpath('../generate_training_data/full_res_image/'); 

%% load neural network
load neuralNet

%% load image 
imageNo = 25; 
image = imread(char("image"+string(imageNo)+".png")); 

imSize = 224; 
stepNet = 2; 
sens = 0.95; 
heatSize = 150; 
netWork = neuralNet; 

%% pass image through network 
[xGlands, yGlands] = passThruNet(sens,image,heatSize,stepNet,netWork,imSize); 

figure(1)
imshow(image)
hold on
plot(xGlands, yGlands, 'ro')





function [xGlands, yGlands] = passThruNet(sens,image,heatSize, step, netWork,imSize)
[r c rgb] = size(image); 
xpos = [];
ypos = [];
xGlands = []; 
yGlands = []; 
heatMap = zeros(r,c); 
val = 0; 

for i=1:imSize/step:c 
    disp("Evaluating network progress: "+string(i/c*100)+" %."); 
    
    for j=1:imSize/step:r 
        if i+imSize-1<=c && j+imSize-1 <= r 
            rect = [i j imSize-1 imSize-1]; 
            J = imcrop(image,rect);
            [prediction,score] = classify(netWork, J); 
            if score(2) > sens 
                heatMap(j:j+heatSize, i:i+heatSize) = heatMap(j:j+heatSize,i:i+heatSize)+50; 
            end
        end
    end
end

[feats,num] = bwlabel(heatMap,4); 
fppropData = regionprops(feats,heatMap,'all');
centroids = cat(1,fppropData.Centroid); 
if ~isempty(centroids) 
    xGlands = centroids(:,1); 
    yGlands = centroids(:,2);
end
end



















