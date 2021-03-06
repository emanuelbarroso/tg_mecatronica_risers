function [xhatOut, yhatOut] = KALMAN(u,meas)
% This Embedded MATLAB Function implements a very simple Kalman filter.
%
% It implements a Kalman filter for estimating both the state and output
% of a linear, discrete-time, time-invariant, system given by the following
% state-space equations:
%
% x(k) = 0.914 x(k-1) + 0.25 u(k) + w(k)
% y(k) = 0.344 x(k-1) + v(k)
%
% where w(k) has a variance of 0.01 and v(k) has a variance of 0.1.

% Author: Phil Goddard (phil@goddardconsulting.ca)
% Date: Q2, 2011.

% Define storage for the variables that need to persist
% between time periods.
persistent P xhat A B C Q R
if isempty(P)
% First time through the code so do some initialization
   xhat = [0;0;0;0];
   P = zeros(4,4);
   A = [0.993175847266250,0.0997676389875316,
       0.00447446153612418,0.000154491807255262;
       -0.266442692060039,0.989506934720158,
       0.0794137333776907,0.00441443534842949;
       -7.61331011046535,-0.371277877313592,
       0.407916221277208,0.0776985503560236;
       -134.001998512554,-9.45851595845769,
       -10.6078657460473,0.377727256243161];

   B = [0.674742463375352;3.50238796155364;
       -32.6963528822316;-364.795682866366];

   C = [1,0,0,0];

   Q = 0.01^2*eye(4);
   R = 0.4^2;
end
% Propagate the state estimate and covariance matrix:
xhat = A*xhat + B*u;
P = A*P*A' + Q;
% Calculate the Kalman gain
K = P*C'/(C*P*C' + R);
% Calculate the measurement residual
resid = meas- C*xhat;
% Update the state and error covariance estimate
xhat = xhat + K*resid;
P = (eye(size(K,1))-K*C)*P;
% Post the results
xhatOut = xhat;
yhatOut = xhat(1);
