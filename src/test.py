import interface

x,y = interface.csv_to_nparray("./cal_ssvep.csv")
x1 = interface.arr_to_feature(x)
print x1
