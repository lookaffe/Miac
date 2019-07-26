/**
 *  On Raspberry Pi: increase your GPU memory, to avoid
 *  OpenGL error 1285 at top endDraw(): out of memory
 */

import gohai.glvideo.*;
GLMovie video1;
GLMovie video2;

void setup() {
  size(560, 406, P2D);
  video1 = new GLMovie(this, "/home/pi/Miac/Video/01.mp4");
  video2 = new GLMovie(this, "/home/pi/Miac/Video/02.mp4");
  
}

void draw() {
  background(0);
  if (video1.available()) {
    video1.read();
  }
  image(video1, 0, 0, width, height);
}
