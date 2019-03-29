import cv2
import math
import numpy as np
import sys
DEG2RAD = math.pi/180.0
cam_heading=90.0
cam_pitch=90.0
cam_fov=90.0

if __name__ == '__main__':
  cam_pitch = float(sys.argv[1])
  cam_heading = float(sys.argv[2])
  img=cv2.imread("src.jpg")
  src_width = img.shape[1]
  src_height = img.shape[0]
  dest_width=720
  dest_height=480

  #calculate camera plane
  theta_fac=src_height/math.pi
  phi_fac=src_width*0.5/math.pi
  ratioUp=2.0*math.tan(cam_fov*DEG2RAD/2.0);
  ratioRight=ratioUp*1.33;

  camDirX=math.sin(cam_pitch*DEG2RAD)*math.sin(cam_heading*DEG2RAD);
  camDirY=math.cos(cam_pitch*DEG2RAD);
  camDirZ=math.sin(cam_pitch*DEG2RAD)*math.cos(cam_heading*DEG2RAD);

  camUpX=ratioUp*math.sin((cam_pitch-90.0)*DEG2RAD)*math.sin(cam_heading*DEG2RAD);
  camUpY=ratioUp*math.cos((cam_pitch-90.0)*DEG2RAD);
  camUpZ=ratioUp*math.sin((cam_pitch-90.0)*DEG2RAD)*math.cos(cam_heading*DEG2RAD);

  camRightX=ratioRight*math.sin((cam_heading-90.0)*DEG2RAD);
  camRightY=0.0;
  camRightZ=ratioRight*math.cos((cam_heading-90.0)*DEG2RAD);

  camPlaneOriginX=camDirX + 0.5*camUpX - 0.5*camRightX;
  camPlaneOriginY=camDirY + 0.5*camUpY - 0.5*camRightY;
  camPlaneOriginZ=camDirZ + 0.5*camUpZ - 0.5*camRightZ;
  FOV = math.pi * 130./180.; #FOV of the fisheye, eg: 180 degrees   
  #print(camPlaneOriginX,camPlaneOriginY,camPlaneOriginZ)    
  size = dest_height, dest_width, 3
  dest = np.zeros(size, dtype=np.float) 
  #print(src_width,src_height)
  for i in range(1,dest_height):
    for j in range(1,dest_width):
      fx=float(j)/float(dest_width);
      fy=float(i)/float(dest_height);
      rayY=camPlaneOriginX + fx*camRightX - fy*camUpX;
      rayX=camPlaneOriginY + fx*camRightY - fy*camUpY;
      rayZ=camPlaneOriginZ + fx*camRightZ - fy*camUpZ;
      rayNorm=math.sqrt(rayX*rayX + rayZ*rayZ);

      # Calculate fisheye angle and radius
      theta = math.atan2(rayZ,rayX);
      phi = math.atan2(rayNorm,rayY);
      r = src_height * phi / FOV;

      # Pixel in fisheye space
      theta_i=math.floor(0.5 * src_width + r * math.sin(theta));
      phi_i=math.floor(0.5 * src_height - r * math.cos(theta));
      # rayNorm=1.0/Math.sqrt(rayX*rayX + rayY*rayY + rayZ*rayZ);
      dest_offset=(i*dest_width+j);
      src_offset=(phi_i*src_width + theta_i);
      y = max(min(int(phi_i),src_height-1),1)
      x = max(min(int(theta_i),src_width-1),1)
      #print(img[y,x,0])
      #print(fx)
      #dest[i,j,0] = 0.5
      #dest[i,j,1] = 0.5
      #dest[i,j,2] = 0.5
      
      dest[i,j,0] = img[y,x,0]/255.
      dest[i,j,1] = img[y,x,1]/255.
      dest[i,j,2] = img[y,x,2]/255.
      #pixels[dest_offset+1]   = img_buffer[src_offset+1];
      #pixels[dest_offset+2]   = img_buffer[src_offset+2];
      #pixels[dest_offset+3] = img_buffer[src_offset+3];

  #print(width)
  #print(height)

  cv2.imshow('show',dest)
  cv2.waitKey(3000)
  cv2.destroyAllWindows()