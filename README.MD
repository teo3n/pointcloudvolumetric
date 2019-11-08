note: the program requires GLSL 3.30 ES support. This should be available on nearly all modern-ish devices

This is A Real-Time GPU Accelerated 3D Point Cloud Based Volumetric Viewer done with python and OpenGL. A demo video can be found at https://www.youtube.com/watch?v=uB-b-hXqfhc.

Controls: orbit the camera with WASD (AD - left-right, WS - forwards/backwads), TR is increase/decrease threshold, EQ is up/down, YH is increase/decrease point size, b toggles between adaptive and absolute coloring profile

Run volumetricviewer.py with python3.

Requirements: GLSL 3.30 ES support. Python libraries: pillow, numpy, pyopengl, opencv-python and pygame.
Note: On Windows the depth might fail to render. This is a known bug which unfortunately I do not have time to fix. Using Linux with supported hardware is recommended.

This program has been tested on Ubuntu 19.04, Manjaro and OpenSuse Tumbleweed with the latest (43x) NVidia (bumblebee if required) drivers installed. The volumetric viewer achieves a stable framerate of 60Hz on GTX1080 with i7-4770 when rendering the default brain (4k atlas). On Intel 630 grpahics the 2k brain atlas renders at ~20fps.
Changing between 2k and 4k atlases doesn't change the quality drastically, but reduces the framerate significantly. Use what you can get away with.

To view other files:
Change the defines in vertex_shader.c. If experiementing with different form factors (currently set to 256x256 tiling, 4096x4096 image therefore tiling is 16). In addition, the amount of verticies has to be defined in volumetricviewer.py in the drawcall to be the same as the amount of pixels in the atlas.

An atlas can be generated using either createAtlas.py, in which you can define your own mathematical formula by which to generate the atlas. Additionally formatBrainData.py can be used to generate an atlas from a image sequence. The viewer reads the data from bottom to up, left to right. The generated atlases have to be rotated -90d before they are usable in the viewer.
Color of the mesh is defined by the color of the sample, including alpha. This (usually) grayscale data is then remapped to RGB for easier visualization.
