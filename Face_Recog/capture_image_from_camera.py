import cv2
cam_port = 0
cam = cv2.VideoCapture(cam_port)
# reading the input using the camera

inp = input('Enter person name')
while(1): 
        result,image = cam.read()
        cv2.imshow(inp, image)
        if cv2.waitKey(0):
         cv2.imwrite(inp+".png", image)
         print("image taken")
else:
	print("No image detected. Please! try again")
