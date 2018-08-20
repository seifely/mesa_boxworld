%% MB-P Informal Tests

map = [1 2 3];

map_one_basic = [7 7 6 8 7];
mob_switch = [2 2 3 2 1];
map_two_basic = [6 5 6 4 3];
mtb_switch = [3 2 3 9 2];
map_three_basic = [10 10 10 9 10];
mthb_switch = [9 9 9 9 9];

av_1 = mean(map_one_basic);
av_1_s = mean(mob_switch);
av_2 = mean(map_two_basic);
av_2_s = mean(mtb_switch);
av_3 = mean(map_three_basic);
av_3_s = mean(mthb_switch);

standard_performance_average = [av_1 av_2 av_3];
standard_switch_average = [av_1_s av_2_s av_3_s];

% % Test Versions

ver_1_score_map_1 = [4 2 3 4 2 4]; av_1_sc_1 = mean(ver_1_score_map_1);
ver_1_switch_map_1 = [5 9 1 1 8 4]; av_1_sw_1 = mean(ver_1_switch_map_1);

ver_2_score_map_1 = [3 3 4 2 4 3]; av_2_sc_1 = mean(ver_2_score_map_1);
ver_2_switch_map_1 = [12 1 1 9 1 2]; av_2_sw_1 = mean(ver_2_switch_map_1);

ver_3_score_map_1 = [7 7 8 2 4]; av_3_sc_1 = mean(ver_3_score_map_1); % test 14 with new build, without end switching
ver_3_switch_map_1 = [3 2 2 9 8]; av_3_sw_1 = mean(ver_3_switch_map_1);

ver_4_score_map_1 = [2 2 6 2 3]; av_4_sc_1 = mean(ver_4_score_map_1);
ver_4_switch_map_1 = [10 10 9 14 13]; av_4_sw_1 = mean(ver_4_switch_map_1);

 % 

ver_1_score_map_2 = [9 5 7 7 5];  av_1_sc_2 = mean(ver_1_score_map_2); % these need redoing or rewriting,  2 from end and 2 from original
ver_1_switch_map_2 = [12 19 16 6 15]; av_1_sw_2 = mean(ver_1_switch_map_2);

ver_2_score_map_2 = [7 7 7 6 8]; av_2_sc_2 = mean(ver_2_score_map_2);
ver_2_switch_map_2 = [6 9 15 9 8 10]; av_2_sw_2 = mean(ver_2_switch_map_2);

ver_3_score_map_2 = [2 2 2 3 2]; av_3_sc_2 = mean(ver_3_score_map_2);
ver_3_switch_map_2 = [1 1 1 1 1]; av_3_sw_2 = mean(ver_3_switch_map_2);

ver_4_score_map_2 = [3 3 2 2 1]; av_4_sc_2 = mean(ver_4_score_map_2);
ver_4_switch_map_2 = [4 4 1 2 2]; av_4_sw_2 = mean(ver_4_switch_map_2);

%

ver_1_score_map_3 = [3 9 7 7 6];  av_1_sc_3 = mean(ver_1_score_map_3);
ver_1_switch_map_3 = [56 9 9 9 9]; av_1_sw_3 = mean(ver_1_switch_map_3);

ver_2_score_map_3 = [3 4 4 9 6]; av_2_sc_3 = mean(ver_1_score_map_3);
ver_2_switch_map_3 = [51 48 57 9 9]; av_2_sw_3 = mean(ver_2_switch_map_3);

ver_3_score_map_3 = [2 7 3 4 3]; av_3_sc_3 = mean(ver_3_score_map_3);
ver_3_switch_map_3 = [30 9 22 23 26]; av_3_sw_3 = mean(ver_3_switch_map_3);

ver_4_score_map_3 = [7 6 10 7 6]; av_4_sc_3 = mean(ver_4_score_map_3);
ver_4_switch_map_3 = [9 9 9 9 9]; av_4_sw_3 = mean(ver_4_switch_map_3);

% % Plots

