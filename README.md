# Autoplant
Neural networks and robotic microneedles enable autonomous extraction of plant metabolites

Hansol Bae, Magnus Paludan, Jan Knoblauch and Kaare H. Jensen*
Department of Physics, Technical University of Denmark, DK-2800 Kgs. Lyngby
E-mail for correspondence: khjensen@fysik.dtu.dk


This repository contains scripts for
1. controlling a Sutter Instruments ROE-200 micromanipulator ("micromanipulator/") 
2. generating training data for a CNN for glandular trichome detection on micrographs ("generate_training_data/") 
3. training (transfer learning) GoogLeNet for glandular trichome detection on micrographs ("train_neural_network/") 
4. testing the network on micrographs ("test_neural_network/") 


To generate training data, train the network, and test the network follow these steps: 
Steps 1-4 may be skipped, as the network is already trained (network weights in train_neural_network/neuralNet.mat). 

Generating training data (MAY BE SKIPPED): 
1. make folder "training_data" in "generate_training_data". 
2. make folders "negative" and "positive" in "generate_training_data/training_data" 
3. run the MATLAB code "generate_training_data/generate_training_data.m"

Training (transfer learning) GoogLeNet CNN (MAY BE SKIPPED): 
4. run the MATLAB code "train_neural_network/train_network.m" 

Test the neural network: 
5. run the MATLAB code test_neural_network/test_network.m 
6. on line 16 the variable "imageNo" may be changed to any image index in "generate_training_data/full_res_images/". Alternatively, a full-path to a micrograph may be inserted in line 17. 








