imu = [2;0];
vps = [1;1];
hps = [0;2];
fs = [0;2];
mc = [1;0];
bas = [1;0];
comms = [0;2];
t = [0;2];

tbatt = t, tambiant = tbatt, tlim = tambiant;

FLCU = imu + vps + hps + fs + comms;
FRCU = imu + vps + hps + fs +comms;
MSCU = imu + vps + tbatt + 2*tlim + comms;
RLCU = imu + vps + hps + mc + tambiant + comms;
RRCU = imu + vps + hps + bas + pambiant + comms;

pinType = {'Digital';'Analog';}
T = table(FLCU,FRCU,MSCU,RLCU,RRCU,'RowNames',pinType)