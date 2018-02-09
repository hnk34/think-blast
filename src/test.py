import interface

in1 = interface.init_lsl(0)
while 1:
    time, sample = interface.read_lsl(in1)
    print(str(time) + str(sample) + "\n")
