# TODO

New directory

make main just call directory main

edit encoder to have the watcher
add smart motor
use  threading to make PID update faster
or make the intterupts lean enought they can update the pid in the interrupt


## odometry
keep track of each wheel rotation and speed
for each time step, add real world speed in inches/s * dt to odometry vector
how to handle two wheels - if theres any scrubbing thats an issue