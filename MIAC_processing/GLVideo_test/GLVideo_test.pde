/**
 *  On Raspberry Pi: increase your GPU memory, to avoid
 *  OpenGL error 1285 at top endDraw(): out of memory
 */

import gohai.glvideo.*;
GLMovie video;

void setup() {
  size(560, 406, P2D);
  video = new GLMovie(this, "/home/pi/Miac/Video/01.mp4");
  video.loop();
}

void draw() {
  background(0);
  if (video.available()) {
    video.read();
  }
  image(video, 0, 0, width, height);
}
