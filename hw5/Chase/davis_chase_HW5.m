%% HW5
% Chase Davis
% 10/30/2023
clear; clc;

%% load water-level records

% load 6 min water level records for January 2023 in California and Oregon
load('HW4_vars.mat'); 
dt_dec_hours = 0.1;

%% calculate sample mean and standard deviation

ca_meanWaterLevel = mean(ca_waterLevel);
ca_stdWaterLevel = std(ca_waterLevel);
ca_samplemeanWaterLevel = ca_meanWaterLevel + (ca_stdWaterLevel/sqrt(length(ca_waterLevel)));

or_meanWaterLevel = mean(or_waterLevel);
or_stdWaterLevel = std(or_waterLevel);
or_samplemeanWaterLevel = or_meanWaterLevel + (or_stdWaterLevel/sqrt(length(or_waterLevel)));

%% remove sample mean from water-level records

ca_waterLevel = ca_waterLevel-ca_samplemeanWaterLevel;
or_waterLevel = or_waterLevel-or_samplemeanWaterLevel;

%% run t-tide function on california

addpath('C:\Users\Cheesy Chase\OneDrive - UNC-Wilmington\GradCourseWork\DataOce\HW5\t_tide_v1.5beta');

[ca_NAME,ca_FREQ,ca_TIDECON,ca_tidal_prediction]=t_tide(ca_waterLevel,'interval',dt_dec_hours);

% NAME = constituent abbreviation, e.g., M2, S2, etc.
% FREQ = constitutent frequency,
% TIDECON = [Amplitude, Error, Phase, Error],
% Amplitude= fit amplitude,
% Error = confidence interval,
% Phase = constituent phase relative the center of the input record,
% ηp = tidal prediction time series

%% estimate residual error 

ca_residual_err = ca_waterLevel - ca_tidal_prediction;

ca_waterLevel_var = sum((ca_waterLevel - mean(ca_waterLevel)).^2)/(length(ca_waterLevel)-1);
ca_resididual_err_var = sum((ca_residual_err - mean(ca_residual_err)).^2)/(length(ca_residual_err)-1);

ca_skill_score = 1 - (ca_resididual_err_var/ca_waterLevel_var); % 0.9936

%% how many constituents were significant (amplitude larger than the error)?

for i = 1:size(ca_TIDECON, 1)
    comparison_result(i,1) = ca_TIDECON(i, 1) > ca_TIDECON(i, 2);
end

num_of_sig_constituents = sum(comparison_result); % 23 out of 35

%% determine the best fit coefficients (a) udinh least-squares function (\)

% convert time record to hours 
time_hours = hours(time-time(1));

% define frequencies
omega_M2 = 2*pi/12.42; % lunar semidiurnal
omega_S2 = 2*pi/12;  % solar semidiurnal

% create columns for matrix
ca_cos_M2 = cos(omega_M2 * time_hours);
ca_sin_M2 = sin(omega_M2 * time_hours);
ca_cos_S2 = cos(omega_S2 * time_hours);
ca_sin_S2 = sin(omega_S2 * time_hours);

% combine coluimns intro matrix
ca_H = [ca_cos_M2, ca_sin_M2, ca_cos_S2, ca_sin_S2]; % should be a 7680x4 matrix

% determine best fit coefficients
ca_a = ca_H \ ca_waterLevel;

% compute the inverse covariance matrix
ca_covariance_inv = inv(ca_H'*ca_H);

%% estimate the residual error and the variance of the error. What is the skill score of the fit?

ca_least_square_tidal_prediction = ca_H*ca_a;

ca_residual_err_err = ca_waterLevel - ca_least_square_tidal_prediction;

% ca_waterLevel_var = sum((ca_waterLevel - mean(ca_waterLevel)).^2)/(length(ca_waterLevel)-1); % unchanged from above
ca_resididual_err_err_var = sum((ca_residual_err_err - mean(ca_residual_err_err)).^2)/(length(ca_residual_err_err)-1);

ca_skill_score_err_err = 1 - (ca_resididual_err_err_var/ca_waterLevel_var); % 0.4639

%% plot zero-mean signal, t_tide, and least-squares

figure(1); clf;
set(gcf,'color','w'); set(gcf,'position',[11 406 742 525]);
fname = 'Times New Roman';

plot(time,ca_waterLevel,'k','linewidth',4);
hold on;
plot(time,ca_tidal_prediction,'.g','linewidth',1);
plot(time,ca_least_square_tidal_prediction,'r','linewidth',1);
set(gca, 'FontName', fname);
set(ylabel('Water Level (m)','interpreter','latex'),'FontName',fname);
set(legend('zero-mean','t-tide','least-squares'),'FontName',fname,'Orientation','horizontal','Location','NorthOutside');
grid on; axis tight; fontsize;

%% calc the amplitude and phase of the M2 and S2 fits

% extract coeff of a
ca_a_M2 = ca_a(1);
ca_b_M2 = ca_a(2);
ca_a_S2 = ca_a(3);
ca_b_S2 = ca_a(4);

% calc amplitude and phase for M2
ca_A_M2 = ca_a_M2^2 + ca_b_M2^2;
ca_phi_M2 = atan2(ca_b_M2, ca_a_M2);

% calc amplitude and phase for S2
ca_A_S2 = ca_a_S2^2 + ca_b_S2^2;
ca_phi_S2 = atan2(ca_b_S2, ca_a_S2);

%% calc fraction of total variance that is explained by M2 and S2

ca_M2_total_var_fraction = ca_A_M2 / 2*ca_waterLevel_var;

ca_S2_total_var_fraction = ca_A_S2 / 2*ca_waterLevel_var;

%% compute % diff. in amplitude between least-squares fit and t-tide

A_ls = ca_A_M2 + ca_A_S2;
A_tt = sum(ca_TIDECON(:,1));

ca_percent_diff = 100*(abs(A_tt-A_ls)/(0.5*(A_tt+A_ls)));

%% what are Nd and Neff for both errors?

% v = Neff - 4 degrees of freedom
% Neff = N / Nd 
% N = # of observations
% Nd = decorrellation scale 

% estimate lagged auto-correlation for both errors out to 15 days 
N = length(time);
dt = time(2)-time(1);
M  = round(15/days(dt)); 

lags = 0:M;
t_tide_R    = nan(M+1,1);
for  m = 0:M
    ind0 = 1:N-m;
%     t_tide_R(M+1-m)    = sum(ca_residual_err(ind0  ).*ca_residual_err(ind0+m))/N; 
    t_tide_R(m+1)    = sum(ca_residual_err(ind0+m).*ca_residual_err(ind0  ))/N;    
end
t_tide_R=t_tide_R/t_tide_R(1);

least_square_R    = nan(M+1,1);

for  m = 0:M
    ind0 = 1:N-m;
%     least_square_R(M+1-m)    = sum(ca_residual_err_err(ind0  ).*ca_residual_err_err(ind0+m))/N; 
    least_square_R(m+1)    = sum(ca_residual_err_err(ind0+m).*ca_residual_err_err(ind0  ))/N;    
end
least_square_R = least_square_R/least_square_R(1);
% plot auto-correlation versus lag and indicate the intergral time scale
% for both with a vertical line 

figure(2); clf;
set(gcf,'color','w'); set(gcf,'position',[11 406 742 525]);
fname = 'Times New Roman';

plot(lags*days(dt),t_tide_R,'g','linewidth',2);
hold on;
plot(lags*days(dt),least_square_R,'r','LineWidth',2);
set(gca, 'FontName', fname);
set(xlabel('$\tau$ [days]','interpreter','latex'),'FontName',fname);
set(ylabel('$\rho_{\scriptscriptstyle U,T}$','interpreter','latex'),'FontName',fname);
grid on; axis tight; fontsize;

% calc Nd and Neff for each error
Nd_t_tide = find(t_tide_R <= 1/exp(1), 1, 'first'); % find where autocrrelation drops to 1/e of its initial value
Neff_t_tide = N / Nd_t_tide;

Nd_least_square = find(least_square_R <= 1/exp(1), 1, 'first'); % find where autocrrelation drops to 1/e of its initial value
Neff_least_square = N / Nd_least_square;

line([Nd_t_tide, Nd_t_tide]*days(dt), [min(t_tide_R), max(t_tide_R)], 'Color', 'g', 'LineStyle', '--', 'LineWidth', 3);
line([Nd_least_square, Nd_least_square]*days(dt), [min(least_square_R), max(least_square_R)], 'Color', 'r', 'LineStyle', '--', 'LineWidth', 2);
set(legend('t-tide error','least square error','t-tide time-scale','least-square time-scale'),'FontName',fname,'Location','Northeast');


%% determine ratio of confidence limits of lest-squares fit and compare to t-tide

% least-squares lower and upper bound

alpha = 0.05; % 95% confidence interval

nu = Neff_least_square - 4; % v = Neff - 4 degrees of freedom

t_score = tinv(1 - alpha/2, nu); % inverse student-t distribution

s_epsilon = sqrt(ca_resididual_err_err_var); % standard error

C_inv_1 = ca_covariance_inv(1, 1); % diagonal element of C^(-1)

confidence_interval = t_score * sqrt(s_epsilon * C_inv_1); % confidence interval for amplitudes

% calc lower and upper bounds of confidence interval
lower_bound = ca_A_M2 - confidence_interval;
upper_bound = ca_A_M2 + confidence_interval;

%% repeat 5 and 8 for oregon water level record

% run t-tide function on oregon

[or_NAME,or_FREQ,or_TIDECON,or_tidal_prediction]=t_tide(or_waterLevel,'interval',dt_dec_hours);
% NAME = constituent abbreviation, e.g., M2, S2, etc.
% FREQ = constitutent frequency,
% TIDECON = [Amplitude, Error, Phase, Error],
% Amplitude= fit amplitude,
% Error = confidence interval,
% Phase = constituent phase relative the center of the input record,
% ηp = tidal prediction time series

% estimate residual error 

or_residual_err = or_waterLevel - or_tidal_prediction;

or_waterLevel_var = sum((or_waterLevel - mean(or_waterLevel)).^2)/(length(or_waterLevel)-1);
or_resididual_err_var = sum((or_residual_err - mean(or_residual_err)).^2)/(length(or_residual_err)-1);

or_skill_score = 1 - (or_resididual_err_var/or_waterLevel_var); % 

% determine the best fit coefficients (a) udinh least-squares function (\)

% create columns for matrix
or_cos_M2 = cos(omega_M2 * time_hours);
or_sin_M2 = sin(omega_M2 * time_hours);
or_cos_S2 = cos(omega_S2 * time_hours);
or_sin_S2 = sin(omega_S2 * time_hours);

% combine coluimns intro matrix
or_H = [or_cos_M2, or_sin_M2, or_cos_S2, or_sin_S2]; % should be a 7680x4 matrix

% determine best fit coefficients
or_a = or_H \ or_waterLevel;

% compute the inverse covariance matrix
or_covariance_inv = inv(or_H'*or_H);

% estimate the residual error and the variance of the error. What is the skill score of the fit?

or_least_square_tidal_prediction = or_H*or_a;

or_residual_err_err = or_waterLevel - or_least_square_tidal_prediction;

% or_waterLevel_var = sum((or_waterLevel - mean(or_waterLevel)).^2)/(length(or_waterLevel)-1); % unchanged from above
or_resididual_err_err_var = sum((or_residual_err_err - mean(or_residual_err_err)).^2)/(length(or_residual_err_err)-1);

or_skill_score_err_err = 1 - (or_resididual_err_err_var/or_waterLevel_var); % 0.4639

% plot zero-mean signal, t_tide, and least-squares

figure(3); clf;
set(gcf,'color','w'); set(gcf,'position',[11 406 742 525]);
fname = 'Times New Roman';

plot(time,or_waterLevel,'k','linewidth',4);
hold on;
plot(time,or_tidal_prediction,'.g','linewidth',1);
plot(time,or_least_square_tidal_prediction,'r','linewidth',1);
set(gca, 'FontName', fname);
set(ylabel('Water Level (m)','interpreter','latex'),'FontName',fname);
set(legend('zero-mean','t-tide','least-squares'),'FontName',fname,'Orientation','horizontal','Location','NorthOutside');
grid on; axis tight; fontsize;

% calc the amplitude and phase of the M2 and S2 fits

% extract coeff of a
or_a_M2 = or_a(1);
or_b_M2 = or_a(2);
or_a_S2 = or_a(3);
or_b_S2 = or_a(4);

% calc amplitude and phase for M2
or_A_M2 = or_a_M2^2 + or_b_M2^2;
or_phi_M2 = atan2(or_b_M2, or_a_M2);

% calc amplitude and phase for S2
or_A_S2 = or_a_S2^2 + or_b_S2^2;
or_phi_S2 = atan2(or_b_S2, or_a_S2);

%% estimate the time-lag between the sites for both constituents

time_lag_M2 = (or_phi_M2 - ca_phi_M2)*(12.42/(2*pi));

time_lag_S2 = (or_phi_S2 - ca_phi_S2)*(12/(2*pi));







































