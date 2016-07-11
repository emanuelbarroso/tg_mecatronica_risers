A = [-0.08792257388842735 -3.838890836751964
 3.8388908366434844 -0.08792257389554865];

B = [148.68871004880776,2.946650299830884]';

C = [-0.0007538198029195632 0.03291341240176541];

D = [-0.2746289805914115];

sys = ss(A, B, C, D);
opt = stepDataOptions;opt.InputOffset = 0;
opt.StepAmplitude = 0.3;
t = (0:0.01:50)';
y = step(sys, t, opt);fig = figure;
hold on;
plot(t,y,'k-');
xlabel('Time (s)'), ylabel('Position (m)');
title('Sistema original N = 200, simulacao reduzida para ordem 4');
print('SimulationReduceN200', '-dpng', '-r300');
close(fig);
