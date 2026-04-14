%%## ECE5110 Spring 2026
%%## UnitTest Cubic Splines
addpath ("./src/");
clear

%%
clear;
clc;
X = [1 2 3 4]';
Y = [4 10 12 0]';

% Solve the system of equations Ax = B (just to cross check)

[solution, err] = function_splines(X,Y);

%%
disp("DONE");