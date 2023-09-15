% analyze temperature from a thermistor plunged into an ice bucket

dataFile = 'IceTest_207222_20220531_1357.csv';
data = readtable(dataFile);
data(1,:)

% extract the time and temperature data:
t    = datenum(table2array(data(:,1)));
T    = table2array(data(:,2));
N    = length(t);


% quick plot to identify start/end indices
fig0 = figure;
plot([1:N],T,'k','linewidth',2)
fprintf('\n\n zoom in on where the temperature begins to rapidly drop. Press return when finished.\n')
pause()
fprintf('\n click the point where the temperature begins to rapidly drop.\n')
plunge = ginput(1);

% Start
% X = 801
% Y = 24.761

% End
% X = 
% Y = 

% define start and end indices
iStart = round(plunge(1));
iEnd   = iStart + 30*2;

% extract the plunge data!
t = t(????:????);
T = T(????:????);

% convert time to seconds from start
ts       = (t-t(1))*86400;

% generate an equation format for fitting
fun      = fittype(@(Tf,Ti,ti,tau,x) (Tf +( Ti-Tf )*exp( -( x-ti )/tau ) ) );

% use built-in algorithm to determine the optimal coefficients
curve    = fit( ts, T, fun, 'startpoint', [T(end), T(1), ts(1), 1])