import cv2

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('/home/nickioan/Downloads/raw_video_feed.mp4')
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
 
    # Display the resulting frame
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    threshold = 64
    _, img_bin = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
    img_copy = img_bin[220,:]

    flag = 0
    #Check if last index is included
    for i in range(320):
        px = img_copy[i]
        if px == 0 and flag == 0:
            start = i
            flag = 1
        if flag == 1 and px == 255:
            end = i
            break

    center = int((end + start)/2)
    final_img = cv2.circle(frame,(center,220),12,(0,0,255),-1)
    cv2.imshow('Frame',final_img)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()
