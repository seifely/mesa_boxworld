%% MB-P Informal Tests

map = [1 2 3];

map_one_basic = [6 5 6 4 3];
mob_switch = [3 2 3 9 2];

map_two_basic = [7 7 6 8 7];
mtb_switch = [2 2 3 2 1];

map_three_basic = [10 10 10 9 10];
mthb_switch = [9 9 9 9 9];

av_1 = mean(map_one_basic);
av_1_s = mean(mob_switch);
av_2 = mean(map_two_basic);
av_2_s = mean(mtb_switch);
av_3 = mean(map_three_basic);
av_3_s = mean(mthb_switch);

sd_1 = std(map_one_basic);
sd_1_s = std(mob_switch);
sd_2 = std(map_two_basic);
sd_2_s = std(mtb_switch);
sd_3 = std(map_three_basic);
sd_3_s = std(mthb_switch);


standard_performance_average = [av_1 av_2 av_3];
standard_switch_average = [av_1_s av_2_s av_3_s];

standard_perf_sd = [sd_1 sd_2 sd_3];
standard_switch_sd = [sd_1_s sd_2_s sd_3_s];

% % Test Versions

ver_1_score_map_1 = [4 2 3 4 2 4]; av_1_sc_1 = mean(ver_1_score_map_1); sd_1_sc_1 = std(ver_1_score_map_1);
ver_1_switch_map_1 = [5 9 1 1 8 4]; av_1_sw_1 = mean(ver_1_switch_map_1); sd_1_sw_1 = std(ver_1_switch_map_1);

ver_2_score_map_1 = [3 3 4 2 4 3]; av_2_sc_1 = mean(ver_2_score_map_1); sd_2_sc_1 = std(ver_2_score_map_1);
ver_2_switch_map_1 = [12 1 1 9 1 2]; av_2_sw_1 = mean(ver_2_switch_map_1); sd_2_sw_1 = std(ver_2_switch_map_1);

ver_3_score_map_1 = [7 7 8 2 4]; av_3_sc_1 = mean(ver_3_score_map_1); sd_3_sc_1 = std(ver_3_score_map_1); % test 14 with new build, without end switching
ver_3_switch_map_1 = [3 2 2 9 8]; av_3_sw_1 = mean(ver_3_switch_map_1); sd_3_sw_1 = std(ver_3_switch_map_1);

ver_4_score_map_1 = [2 2 6 2 3]; av_4_sc_1 = mean(ver_4_score_map_1); sd_4_sc_1 = std(ver_4_score_map_1);
ver_4_switch_map_1 = [10 10 9 14 13]; av_4_sw_1 = mean(ver_4_switch_map_1); sd_4_sw_1 = std(ver_4_switch_map_1);

 % 

ver_1_score_map_2 = [9 5 7 7 5];  av_1_sc_2 = mean(ver_1_score_map_2); sd_1_sc_2 = std(ver_1_score_map_2); % these need redoing or rewriting,  2 from end and 2 from original
ver_1_switch_map_2 = [12 19 16 6 15]; av_1_sw_2 = mean(ver_1_switch_map_2); sd_1_sw_2 = std(ver_1_switch_map_2);

ver_2_score_map_2 = [7 7 7 6 8]; av_2_sc_2 = mean(ver_2_score_map_2); sd_2_sc_2 = std(ver_2_score_map_2);
ver_2_switch_map_2 = [6 9 15 9 8 10]; av_2_sw_2 = mean(ver_2_switch_map_2); sd_2_sw_2 = std(ver_2_switch_map_2);

ver_3_score_map_2 = [2 2 2 3 2]; av_3_sc_2 = mean(ver_3_score_map_2); sd_3_sc_2 = std(ver_3_score_map_2);
ver_3_switch_map_2 = [1 1 1 1 1]; av_3_sw_2 = mean(ver_3_switch_map_2); sd_3_sw_2 = std(ver_3_switch_map_2);

ver_4_score_map_2 = [3 3 2 2 1]; av_4_sc_2 = mean(ver_4_score_map_2); sd_4_sc_2 = std(ver_4_score_map_2);
ver_4_switch_map_2 = [4 4 1 2 2]; av_4_sw_2 = mean(ver_4_switch_map_2); sd_4_sw_2 = std(ver_4_switch_map_2);

%

ver_1_score_map_3 = [3 9 7 7 6];  av_1_sc_3 = mean(ver_1_score_map_3); sd_1_sc_3 = std(ver_1_score_map_3);
ver_1_switch_map_3 = [56 9 9 9 9]; av_1_sw_3 = mean(ver_1_switch_map_3); sd_1_sw_3 = std(ver_1_switch_map_3);

ver_2_score_map_3 = [3 4 4 9 6]; av_2_sc_3 = mean(ver_1_score_map_3); sd_2_sc_3 = std(ver_2_score_map_3);
ver_2_switch_map_3 = [51 48 57 9 9]; av_2_sw_3 = mean(ver_2_switch_map_3); sd_2_sw_3 = std(ver_2_switch_map_3);

ver_3_score_map_3 = [2 7 3 4 3]; av_3_sc_3 = mean(ver_3_score_map_3); sd_3_sc_3 = std(ver_3_score_map_3);
ver_3_switch_map_3 = [30 9 22 23 26]; av_3_sw_3 = mean(ver_3_switch_map_3); sd_3_sw_3 = std(ver_3_switch_map_3);

ver_4_score_map_3 = [7 6 10 7 6]; av_4_sc_3 = mean(ver_4_score_map_3); sd_4_sc_3 = std(ver_4_score_map_3);
ver_4_switch_map_3 = [9 9 9 9 9]; av_4_sw_3 = mean(ver_4_switch_map_3); sd_4_sw_3 = std(ver_4_switch_map_3);

% Test Data Collected

ver_1_score = [av_1_sc_1 av_1_sc_2 av_1_sc_3];
ver_1_switch = [av_1_sw_1 av_1_sw_2 av_1_sw_3];

ver_1_sd_score = [sd_1_sc_1 sd_1_sc_2 sd_1_sc_3];
ver_1_sd_switch = [sd_1_sw_1 sd_1_sw_2 sd_1_sw_3];

ver_2_score = [av_2_sc_1 av_2_sc_2 av_2_sc_3];
ver_2_switch = [av_2_sw_1 av_2_sw_2 av_2_sw_3];

ver_2_sd_score = [sd_2_sc_1 sd_2_sc_2 sd_2_sc_3];
ver_2_sd_switch = [sd_2_sw_1 sd_2_sw_2 sd_2_sw_3];

ver_3_score = [av_3_sc_1 av_3_sc_2 av_3_sc_3];
ver_3_switch = [av_3_sw_1 av_3_sw_2 av_3_sw_3];

ver_3_sd_score = [sd_3_sc_1 sd_3_sc_2 sd_3_sc_3];
ver_3_sd_switch = [sd_3_sw_1 sd_3_sw_2 sd_3_sw_3];

ver_4_score = [av_4_sc_1 av_4_sc_2 av_4_sc_3];
ver_4_switch = [av_4_sw_1 av_4_sw_2 av_4_sw_3];

ver_4_sd_score = [sd_4_sc_1 sd_4_sc_2 sd_4_sc_3];
ver_4_sd_switch = [sd_4_sw_1 sd_4_sw_2 sd_4_sw_3];

% % Plots
% 
x = map;
% figure;
% subplot(1,2,1);
% plot(x, standard_performance_average)
% hold on
% plot(x, ver_1_score)
% plot(x, ver_2_score)
% plot(x, ver_3_score)
% plot(x, ver_4_score)
% 
% subplot(1,2,2);
% plot(x, standard_switch_average)
% hold on
% plot(x, ver_1_switch)
% plot(x, ver_2_switch)
% plot(x, ver_3_switch)
% plot(x, ver_4_switch)

%

map_one = [standard_performance_average(1) ver_1_score(1) ver_2_score(1) ver_3_score(1) ver_4_score(1)];
map_two = [standard_performance_average(2) ver_1_score(2) ver_2_score(2) ver_3_score(2) ver_4_score(2)];
map_three = [standard_performance_average(3) ver_1_score(3) ver_2_score(3) ver_3_score(3) ver_4_score(3)];

map_one_switch = [standard_switch_average(1) ver_1_switch(1) ver_2_switch(1) ver_3_switch(1) ver_4_switch(1)];
map_two_switch = [standard_switch_average(2) ver_1_switch(2) ver_2_switch(2) ver_3_switch(2) ver_4_switch(2)];
map_three_switch = [standard_switch_average(3) ver_1_switch(3) ver_2_switch(3) ver_3_switch(3) ver_4_switch(3)];

map_one_sd = [standard_perf_sd(1) ver_1_sd_score(1) ver_2_sd_score(1) ver_3_sd_score(1) ver_4_sd_score(1)];
map_two_sd = [standard_perf_sd(2) ver_1_sd_score(2) ver_2_sd_score(2) ver_3_sd_score(2) ver_4_sd_score(2)];
map_three_sd = [standard_perf_sd(3) ver_1_sd_score(3) ver_2_sd_score(3) ver_3_sd_score(3) ver_4_sd_score(3)];

% map_one_sd_switch = [standard_switch_sd(1) ver_1_sd_switch(1) ver_2_sd_switch(1) ver_3_sd_switch(1) ver_4_sd_switch (1)];
% map_two_sd_switch = [standard_switch_sd(2) ver_1_sd_switch(2) ver_2_sd_switch(2) ver_3_sd_switch(2) ver_4_sd_switch (2)];
% map_three_sd_switch = [standard_switch_sd(3) ver_1_sd_switch(3) ver_2_sd_switch(3) ver_3_sd_switch(3) ver_4_sd_switch (3)];

map_one_sd_switch = [0.7071 3.3862 4.8854 3.4205 2.1679];
map_two_sd_switch = [1.3038 4.9295 3.0166 0 1.3416];
map_three_sd_switch = [0.4472 21.0190 23.7739 7.9057 0];

% figure;
% % subplot(1,2,1);
% % Y = [standard_performance_average
% %      ver_1_score
% %      ver_2_score
% %      ver_3_score
% %      ver_4_score];
% Y = [map_one
%      map_two
%      map_three];
% bar(Y)
% legend('Non-Stressed Switcher', 'Stressed Switcher V.1', 'Stressed Switcher V.2', 'Stressed Switcher V.3', 'Stressed Switcher V.4')
% hold on
% errorbar(map_one, map_one_sd)
% errorbar(map_two, map_two_sd)
% errorbar(map_three, map_three_sd)
% hold off
% grid
% 
% % subplot(1,2,2);
% figure;
% Y = [map_one_switch
%      map_two_switch
%      map_three_switch];
% bar(Y)
% legend('Non-Stressed Switcher', 'Stressed Switcher V.1', 'Stressed Switcher V.2', 'Stressed Switcher V.3', 'Stressed Switcher V.4')
% hold on
% errorbar(map_one_switch, map_one_sd_switch)
% errorbar(map_two_switch, map_two_sd_switch)
% errorbar(map_three_switch, map_three_sd_switch)
% hold off
% grid

% Trying to get the error bars on the bars...
% ------------------------ Score Data ----------------------------

% Data to be plotted as a bar graph
model_series = [map_one; map_two; map_three];

%Data to be plotted as the error bars
model_error = [map_one_sd; map_two_sd; map_three_sd];

% Creating axes and the bar graph
ax = axes;
h = bar(model_series,'BarWidth',1);

% Set color for each bar face
% h(1).FaceColor = 'blue';
% h(2).FaceColor = 'yellow';

% Properties of the bar graph as required
ax.YGrid = 'on';
ax.GridLineStyle = '-';
xticks(ax,[1 2 3]);

% Naming each of the bar groups
xticklabels(ax,{ 'Test-14', 'Test-7', 'Test-9'});

% X and Y labels
xlabel ('Map Number');
ylabel ('Average Score (/10)');

% Creating a legend and placing it outside the bar plot
lg = legend('Non-Stressed Switcher','Stressed Switcher V.1','Stressed Switcher V.2','Stressed Switcher V.3','Stressed Switcher V.4','AutoUpdate','off');
lg.Location = 'EastOutside';
lg.Orientation = 'Vertical'; 
hold on;

% Finding the number of groups and the number of bars in each group
ngroups = size(model_series, 1);
nbars = size(model_series, 2);

% Calculating the width for each bar group
groupwidth = min(0.8, nbars/(nbars + 1.5));

% Set the position of each error bar in the centre of the main bar
% Based on barweb.m by Bolu Ajiboye from MATLAB File Exchange
for i = 1:nbars
    % Calculate center of each bar
    x = (1:ngroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*nbars);
    errorbar(x, model_series(:,i), model_error(:,i), 'k', 'linestyle', 'none');
end

% ------------------------ Switch Data ----------------------------
figure;
% Data to be plotted as a bar graph
model_series = [map_one_switch; map_two_switch; map_three_switch];

%Data to be plotted as the error bars
model_error = [map_one_sd_switch; map_two_sd_switch; map_three_sd_switch];

% Creating axes and the bar graph
ax = axes;
h = bar(model_series,'BarWidth',1);

% Set color for each bar face
% h(1).FaceColor = 'blue';
% h(2).FaceColor = 'yellow';

% Properties of the bar graph as required
ax.YGrid = 'on';
ax.GridLineStyle = '-';
xticks(ax,[1 2 3]);

% Naming each of the bar groups
xticklabels(ax,{ 'Test-14', 'Test-7', 'Test-9'});

% X and Y labels
xlabel ('Map Number');
ylabel ('Average Number of Times Strategies Switched (n)');

% Creating a legend and placing it outside the bar plot
lg = legend('Non-Stressed Switcher','Stressed Switcher V.1','Stressed Switcher V.2','Stressed Switcher V.3','Stressed Switcher V.4','AutoUpdate','off');
lg.Location = 'EastOutside';
lg.Orientation = 'Vertical';
hold on;

% Finding the number of groups and the number of bars in each group
ngroups = size(model_series, 1);
nbars = size(model_series, 2);

% Calculating the width for each bar group
groupwidth = min(0.8, nbars/(nbars + 1.5));

% Set the position of each error bar in the centre of the main bar
% Based on barweb.m by Bolu Ajiboye from MATLAB File Exchange
for i = 1:nbars
    % Calculate center of each bar
    x = (1:ngroups) - groupwidth/2 + (2*i-1) * groupwidth / (2*nbars);
    errorbar(x, model_series(:,i), model_error(:,i), 'k', 'linestyle', 'none');
end