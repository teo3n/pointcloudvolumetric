
New controls: orbit the camera with WASD (AD - left-right, WS - forwards/backwads), TR is increase/decrease threshold, EQ is up/down
Run volumetricviewer.py with python3.

Reqiurements: glut and GLSL 4.30 support (right now configured for 4.40). Python libraries: pillow, numpy, pyopengl, pygame
note: the program can be run without glut by commenting lines import OPENGL.GLUT and glutInit(), though results are inconsistent at best. 


To view other file:
Change the defines in vertex_shader.c if experiementing with different form factors (ATM 256x256 tiling, 4096x4096 image therefore tiling is 16)
Color of the mesh is defined by the color of the sample, alpha is included


