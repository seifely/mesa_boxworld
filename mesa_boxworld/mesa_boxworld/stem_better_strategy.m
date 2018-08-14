x = [5 5 6 5 5 5 5 5 5 5 4 4 5 8 8];
y = [5 5 6 5 5 11 14 13 13 13 25 22 30 37 37];
z = [1 1 1 1 1 2.2 2.8 2.6 2.6 2.6 6.5 5.5 6.0 4.6 5.4];

reactive_scores = [10.0 10.0 8.0 10.0 10.0 4.5 3.375 5.062 7.125 1.25 1.5 0.625 0.625 1.937 0.25];
deliberative_scores = [4.75 2.687 4.125 2.5 3.625 7.812 7.0 8.0 5.8125 7.562 9.937 10  9.937 9.937 9.937];


best_strat_k3 = [0 0 0 0 0 0 1 1 1 1 1 1 1 1 1];

nsIdx = best_strat_k3 == 0;
smIdx = best_strat_k3 == 1;

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
legend('Reactive', 'Deliberative', 'Location', 'NorthWest')

cb = colorbar;                                     % create and label the colorbar
cb.Label.String = 'Learned Average Score (/10, over 5 trials)';

%% Graph to Show Test Judgements at k=3

x = [5 5 6 5 5 5 5 5 5 5 4 4 5 8 8, 13 10 15 2 6 4 35 5 10 8 3 3 7 4 5];
y = [5 5 6 5 5 11 14 13 13 13 25 22 30 37 37, 27 32 45 12 9 5 42 11 33 17 33 6 14 8 15];
z = [1 1 1 1 1 2.2 2.8 2.6 2.6 2.6 6.5 5.5 6.0 4.6 5.4, 2.7 3.2 2.75 6 1.28 1.25 1.2 2.2 3.3 2.125 11 2 2.14 2 3];

best_strat_k3 = [0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 2 2 2 2 3 3 2 2 2 2 2 3 3 2 2];

nsIdx = best_strat_k3 == 0;
smIdx = best_strat_k3 == 1;
pmIdx = best_strat_k3 == 2;
dmIdx = best_strat_k3 == 3;

figure;
% subplot(1,2,1);
stem3(x(nsIdx), y(nsIdx), z(nsIdx), 'Color', 'b')    % stem plot for non-smokers
hold on
stem3(x(smIdx), y(smIdx), z(smIdx), 'Color', 'r')    % stem plot for smokers
stem3(x(pmIdx), y(pmIdx), z(pmIdx), 'Color', 'g')
stem3(x(dmIdx), y(dmIdx), z(dmIdx), 'Color', 'm') 
hold off

view(-60,15)
% zlim([100 140])

xlabel('Number of Obstacles')                                                      % add labels and a legend
ylabel('Total Number of Branches') 
zlabel('Mean Number of Branches per Obstacle') 
legend('Reactive', 'Deliberative', 'New Deliberative', 'New Reactive', 'Location', 'NorthWest')

%% Graph for Difference in K

y = [1 2];
x = [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15];
k_1 = [2 2 2 1 1 1 2 2 2 2 2 1 2 2 2];
k_3 = [2 2 2 2 1 1 2 2 2 2 2 1 1 2 2];
k_5 = [2 2 2 2 1 1 2 2 2 2 2 1 2 1 2];

figure;
stem(x, k_1, 'r')
hold on
stem(x, k_3, 'b')
stem(x, k_5, 'g')
legend('k=1', 'k=3', 'k=5')

%% Graph for k decision error 

x = [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15];
reactive = [1.3 0.3 1.3 4.6 7.6 8.3 6.6 7.3 1 2.6 0.3 10 5 3 4];
deliberative = [8.6 7.3 10 2 1.6 2 10 3.6 6.67 10 8.3 2 4 3 4.3];

z = [0 1 2];
knn_choice = [2 2 2 2 1 1 2 2 2 2 2 1 2 2 2];
correct_choice = [2 2 2 1 1 1 2 1 2 2 2 1 1 0 2];

figure;
yyaxis left
stem(x, reactive, 'm');
hold on
stem(x, deliberative, 'k');
legend('Reactive', 'Deliberative', 'KNN Strategy Choice', 'Best Strategy')
xlabel('Test Map Number')
hold off 

yyaxis right
scatter(x,knn_choice, 'b');
hold on
scatter(x, correct_choice, 'r');

%%
x = [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15];
Y = [1.3, 8.6
     0.3, 8.1
     1.3, 10
     4.6, 2
     7.6, 1.6
     8.3, 2
     6.6, 10
     7.3, 3.6
     1, 6.67
     2.6, 10
     0.3, 8.3
     10, 2
     5, 4
     3, 3
     4, 4.3];
 
knn_choice = [2 2 2 2 1 1 2 2 2 2 2 1 2 2 2];
correct_choice = [2 2 2 1 1 1 2 1 2 2 2 1 1 0 2];
 
figure;
bar(Y)
xlabel('Test Map Number')
yyaxis right
plot(x,knn_choice, 'b');
hold on
plot(x, correct_choice, 'r');
legend('Reactive', 'Deliberative', 'KNN Strategy Choice', 'Best Strategy')

%% Solely KNN Error

x = [1 2 3 4 5 6 7 8 9 10 11 12 13 14 15];
knn_choice = [2 2 2 2 1 1 2 2 2 2 2 1 2 2 2];
correct_choice = [2 2 2 1 1 1 2 1 2 2 2 1 1 1.5 2];

figure;
scatter(x, correct_choice, 'r')
hold on
scatter(x, knn_choice, 'b')
legend('Best Strategy By Average', 'KNN Strategy Choice')

%% Surface Plot

% x = [5 5 6 5 5 5 5 5 5 5 4 4 5 8 8, 13 10 15 2 6 4 35 5 10 8 3 3 7 4 5];
% y = [5 5 6 5 5 11 14 13 13 13 25 22 30 37 37, 27 32 45 12 9 5 42 11 33 17 33 6 14 8 15];
% z = [1 1 1 1 1 2.2 2.8 2.6 2.6 2.6 6.5 5.5 6.0 4.6 5.4, 2.7 3.2 2.75 6 1.28 1.25 1.2 2.2 3.3 2.125 11 2 2.14 2 3];
% 
% best_strat_k3 = [0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 2 2 2 2 3 3 2 2 2 2 2 3 3 2 2];
% 
% nsIdx = best_strat_k3 == 0;
% smIdx = best_strat_k3 == 1;
% pmIdx = best_strat_k3 == 2;
% dmIdx = best_strat_k3 == 3;
% 
% figure;
% % subplot(1,2,1);
% surf(x(nsIdx), y(nsIdx), z(nsIdx), 'Color', 'b')    % stem plot for non-smokers
% hold on
% surf(x(smIdx), y(smIdx), z(smIdx), 'Color', 'r')    % stem plot for smokers
% surf(x(pmIdx), y(pmIdx), z(pmIdx), 'Color', 'g')
% surf(x(dmIdx), y(dmIdx), z(dmIdx), 'Color', 'm') 
% hold off
% 
% view(-60,15)
% % zlim([100 140])
% 
% xlabel('Number of Obstacles')                                                      % add labels and a legend
% ylabel('Total Number of Branches') 
% zlabel('Mean Number of Branches per Obstacle') 
% legend('Reactive', 'Deliberative', 'New Deliberative', 'New Reactive', 'Location', 'NorthWest')

