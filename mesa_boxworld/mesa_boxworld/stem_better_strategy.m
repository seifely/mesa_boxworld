x = [5 5 6 5 5 5 5 5 5 5 4 4 5 8 8];
y = [5 5 6 5 5 11 14 13 13 13 25 22 30 37 37];
z = [1 1 1 1 1 2.2 2.8 2.6 2.6 2.6 6.5 5.5 6.0 4.6 5.4];

reactive_scores = [10.0 10.0 8.0 10.0 10.0 4.5 3.375 5.062 7.125 1.25 1.5 0.625 0.625 1.937 0.25];
deliberative_scores = [4.75 2.687 4.125 2.5 3.625 7.812 7.0 8.0 5.8125 7.562 9.937 10  9.937 9.937 9.937];


best_strat = [0 0 0 0 0 0 1 1 1 1 1 1 1 1 1];

nsIdx = best_strat == 0;
smIdx = best_strat == 1;

figure;
subplot(1,2,1);
stem3(x(nsIdx), y(nsIdx), z(nsIdx), 'Color', 'b')    % stem plot for non-smokers
hold on
stem3(x(smIdx), y(smIdx), z(smIdx), 'Color', 'r')    % stem plot for smokers
hold off

view(-60,15)
% zlim([100 140])

xlabel('Number of Obstacles')                                                      % add labels and a legend
ylabel('Total Number of Branches') 
zlabel('Mean Number of Branches per Obstacle') 
legend('Reactive', 'Deliberative', 'Location', 'NorthWest')


subplot(1,2,2);
scatter3(x,y,z,40,reactive_scores,'filled')    % draw the scatter plot
ax = gca;
% ax.XDir = 'reverse';
hold on
scatter3(x,y,z,20,deliberative_scores,'filled', 'd')
view(-60,15)
xlabel('Number of Obstacles')
ylabel('Total Number of Branches')
zlabel('Mean Number of Branches per Obstacle')
legend('Reactive', 'Deliberative', 'Location', 'NorthWest')pl

cb = colorbar;                                     % create and label the colorbar
cb.Label.String = 'Learned Average Score (/10, over 5 trials)';