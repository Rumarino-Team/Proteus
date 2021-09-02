import cv2

class Detect:

    def __init__(self):
        self.h_low = 0
        self.h_high = 0
        self.s_low = 0
        self.s_high = 0
        self.v_low = 0
        self.v_high = 0
        self.not_found = 1
        self.GUI_ACTIVATED = True
        self.windows = ['Original', 'Thresholded']
    
    def detect(self, img, bbox):
        x,y,w,h = 0,0,0,0
        if self.GUI_ACTIVATED:
            self.createWindows(self.windows)
            self.createTrackbars('Thresholded')
        while(self.not_found):
            img_original = img
            #hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)#BGR to HSV-Space conversion
            blurred = cv2.GaussianBlur(img_original,(11,11),0)
            img = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

            #Path color parameters (yellow-green) 
            #lower_color = np.array([0,30,30], dtype = 'uint8')
            #upper_color = np.array([70,180,255], dtype = 'uint8')
            #Image Segmentation
            # Construct a mask for the desired color
            mask = cv2.inRange(img, (self.h_low, self.s_low, self.v_low), (self.h_high, self.s_high, self.v_high))

            #Morphological Functions
            # Perform a series of dilations and erosions to remove any small
            # blobs left in the mask
            #kernel = np.ones((9,9),np.uint8)
            mask = cv2.erode(mask, None, iterations=2)
            mask = cv2.dilate(mask, None, iterations=2)
            _,cnts,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                x,y,w,h = cv2.boundingRect(c)
            if self.GUI_ACTIVATED:
                cv2.imshow('Original', img_original)
                cv2.imshow('Thresholded', mask)
                cv2.waitKey(1)
        cv2.waitKey(-1)
        cv2.destroyAllWindows()

        return x,y,w,h
    
    def getTrackbarsPositions(self,x):
        if(x>=self.h_high):
            self.h_low = self.h_high
        else:
            self.h_low = x

    def getTrackbarsPositions1(self,x):
        self.h_high = x

    def getTrackbarsPositions2(self,x):
        if(x>=self.s_high):
            self.s_low = self.s_high
        else:
            self.s_low = x

    def getTrackbarsPositions3(self,x):
        self.s_high = x

    def getTrackbarsPositions4(self,x):
        if(self.v_low>=self.v_high):
            self.v_low = self.v_high
        else:
            self.v_low = x

    def getTrackbarsPositions5(self,x):
        self.v_high = x

    def getTrackbarsPositions6(self,x):
        self.found = x

    def createTrackbars(self,windowName):
        cv2.createTrackbar('H Low',windowName,0,179,self.getTrackbarsPositions)
        cv2.createTrackbar('H High',windowName,0,179,self.getTrackbarsPositions1)
        cv2.createTrackbar('S Low',windowName,0,255,self.getTrackbarsPositions2)
        cv2.createTrackbar('S High',windowName,0,255,self.getTrackbarsPositions3)
        cv2.createTrackbar('V Low',windowName,0,255,self.getTrackbarsPositions4)
        cv2.createTrackbar('V High',windowName,0,255,self.getTrackbarsPositions5)
        cv2.createTrackbar('found',windowName,0,1,self.getTrackbarsPositions6)
        cv2.setTrackbarPos('H Low',windowName,self.h_low)
        cv2.setTrackbarPos('H High',windowName,self.h_high)
        cv2.setTrackbarPos('S Low',windowName,self.s_low)
        cv2.setTrackbarPos('S High',windowName,self.s_high)
        cv2.setTrackbarPos('V Low',windowName,self.v_low)
        cv2.setTrackbarPos('V High',windowName,self.v_high)
    def createWindows(self,windowsNames):
        for name in windowsNames:
            cv2.namedWindow(name)