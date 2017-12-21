Lv=Amplitude of C3
    compare to threshold
Rv=Amplitude of C4
    compare to normalization

DV='cursor movement verticle"
S="voltage"
a="mean voltage for prior"
S1="left voltage"
S2="right Voltage"
av_h="intercept"
bv_h="gain"
#Cursor Movement Type 1
DV=bv[(S1+S2)-av]
DH=bh[(S1+S2)-ah]

#Cursor movemnt type 2
wrv=1
wlv=1
Mv=av(wrv*Rv+wlv*Lv+bv)

wrh=1
wlh=-1
Mh=ah(wrh*Rh+wlh*Lh+bh)
#LMS used to update weights
import pyautogui
pyautogui.moveTo(100, 150)
pyautogui.moveRel(0, 10)  # move mouse 10 pixels down
pyautogui.dragTo(100, 150)
pyautogui.dragRel(0, 10) move mouse 10 pixels down
