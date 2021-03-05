%% --- Script for generating training data for glandular trichome detection CNN --- %% 
%% --- Magnus Paludan, 2021 --- %% 
%% --- DTU Physics --- %% 

clc
clear all
close all


addpath('full_res_image/'); % Path to full resolution image folder 
posPath = 'training_data/positive/'; % Path to (empty) positive crop folder 
negPath = 'training_data/negative/'; % Path to (empty) negative crop folder
load('full_res_labels.mat'); % File with manually labelled gland coordinates on full-res images. 
XTrain = []; 
YTrain = [];
for genImage = 1:300 % Loop for generating 224x224 crops from the full-res images. 
%genImage
randNr = randi(length(A)); % Picks a gland coordinate pair in a random full-res image. 
imId = A(1,randNr);
thisx = A(2,randNr);
thisy = A(3,randNr); 
fileId = char("image"+string(imId)+".png");

image = imread(fileId);
allIds = [A(1,:) == imId];
allX = A(2,allIds);
allY = A(3,allIds);

for j=1:length(allX)
    thisx = allX(j); % Gland coordinates 
    thisy = allY(j);
    
    off_x = randi([0 20]); % Random off-sets for crops 
    off_y = randi([0 20]);
    sign_x = randi([0 1]); 
    sign_y = randi([0 1]); 
    if sign_x == 0 
        sign_x = -1; 
    end
    if sign_y == 0 
        sign_y = -1; 
    end
    off_x = off_x * sign_x; 
    off_y = off_y * sign_y; 
    imSize = 224;
    if thisx-imSize/2+off_x > 0 && thisx-imSize/2+off_x+imSize < 4096
        if thisy-imSize/2+off_y > 0 && thisy-imSize/2+off_y+imSize < 2160
            J = imcrop(image,[thisx-imSize/2+off_x thisy-imSize/2+off_y imSize-1 imSize-1]); % Crop and save 
            imwrite(J,char(string(posPath)+string(genImage)+"no"+string(j)+".png"));
        end
    end
    
end

count = 0;
xarr = [];
yarr = [];
for j=1:length(allX)
   for k=1:imSize
     xarr(end+1) = allX(j)+k; % Maps all regions of full-res image containing glands 
     xarr(end+1) = allX(j)-k;
     yarr(end+1) = allY(j)+k;
     yarr(end+1) = allY(j)-k;
   end
end
time0 = tic;
patience = 2;
while count < 20 && toc(time0)<patience % Generates negative ("no-gland") images
    [n,m,dim] = size(image);
    rand_x = randi(m);
    rand_y = randi(n);
    if ismember(rand_x,xarr)==0 && ismember(rand_y,yarr)==0
        if rand_x > 0 && rand_x+imSize < 4096
            if rand_y > 0 && rand_y+imSize < 2160
                backIm = imcrop(image,[rand_x rand_y imSize-1 imSize-1]);
                count = count + 1; 
                imwrite(backIm,char(string(negPath)+string(genImage)+"no"+string(count)+".png")); % crop and save 
            end
        end
    end
    
end


end