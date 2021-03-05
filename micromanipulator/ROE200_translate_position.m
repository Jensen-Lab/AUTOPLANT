%% -- Micromanipulator script (position, translation) for use with Sutter Instruments ROE-200 -- %%
%% -- Magnus Paludan, 2021 -- %% 
%% -- DTU Physics -- %% 
clc
clear all
close all


%% Initialize micromanipulator
COMport = 'COMX'; %Replace X with open COM-port (see Device Manager on WIN pcs).
obj = serial(COMport,'BaudRate',128000,'Terminator','CR','DataBits',8,'DataTerminalReady','on','FlowControl','none','RequestToSend','on','StopBits',1,'TimeOut',100,'Tag','SutterMP');
fopen(obj);

%% Ask for position 
xyz = position(obj); % 
x = xyz(1); %x position is the first entry in xyz, y is second, z is third. 

%% Translate 
% Define new position as array with [x_position, y_position, z_position] in microns; 
xyz_new = [2000, 3000, 4000]; % Like this. 
translate(obj,xyz_new); 

%Go back to the initial position
translate(obj,xyz); 

%% Close serial connection 
fclose(obj); 


% Function for position
function xyz = position(obj)
disp('Running position.m')

fprintf(obj,'C') %Ask for position. 
c = fread(obj,14,'uint8'); %Get 14 bytes of data in uint8 format. 
c = c(2:13);  %We dont want byte 1 (manipulator no.) and 14 (CR). 
c2 = typecast(uint8(c),'int32');
xyz = c2./16;

c = 0; 
c2 = 0;

end

% Function for translation
function translate(obj,xyz)
disp('Running translate.m')

    xyz = xyz(:);
    xyz_steps = xyz.*16;

    xyz_move = typecast(int32(xyz_steps),'uint8');

    xyz_move_str = [uint8(77); xyz_move; uint8(13)]; 
    fwrite(obj, xyz_move_str, 'uint8')
    pause(0.1)
    fread(obj,1,'uint8');
end



