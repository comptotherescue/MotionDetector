import cv2
import os
import datetime
import time

def CheckFileSize(a_sFILE_NAME):
    StatInfo=os.stat(a_sFILE_NAME)
    if(StatInfo.st_size > 10000000):
       return True
    else:
       return False
	   
def OldestFile(a_sDIR):
    print "Removed: "+min(os.listdir(a_sDIR))
    return min(os.listdir(a_sDIR))
	
def GetDirSize(a_DIR):
    l_itotal_size=0
    for dirpath,dirnames,filenames in os.walk(a_DIR):
        for f in filenames:
            l_sfd = os.path.join(dirpath,f)
            l_itotal_size += os.stat(l_sfd).st_size           
    return l_itotal_size	
	   
    
l_iVDetect = 0
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
while(True):
    
    if (vc.isOpened()):
        try:
            print "Camera Detected!"
            FILE_DIR = "/home/pi/Recording"
            Dt=datetime.datetime.now()
            FILE_NAME=FILE_DIR + "/RECORDING" + Dt.strftime('%d_%m_%y_T_%H_%M_%S_%f')+".avi"
            print FILE_NAME
            out = cv2.VideoWriter(FILE_NAME,cv2.cv.CV_FOURCC('M','P','E','G'), cv2.cv.CV_CAP_PROP_FPS, (640,480))
            if vc.isOpened(): # try to get the first frame
                    rval, frame = vc.read()
                    out.write(frame)
            else:
                    rval = False

            while rval:
                    cv2.imshow("preview", frame)
                    rval, frame = vc.read()
                    out.write(frame)
                    if(CheckFileSize(FILE_NAME)):
                       break 
                    key = cv2.waitKey(50)
                    if key & 0xFF == ord('q'): # exit on ESC
                                    break
                    if(GetDirSize(FILE_DIR) > 8000000000):
                            os.remove(os.path.join(FILE_DIR,OldestFile(FILE_DIR)))
            out.release()
        except :
            print "Exception occured"
    else:
        print "Camera not detected."
        time.sleep(4)
        vc = cv2.VideoCapture(0)
    key = cv2.waitKey(50)
    if key & 0xFF == ord('q'): # exit on ESC
     	break
    
cv2.destroyWindow("preview")
vc.release()


