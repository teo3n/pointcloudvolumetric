This is A Real-Time GPU Accelerated 3D Point Cloud Based Volumetric Viewer. A demo video can be found at https://www.youtube.com/watch?v=uB-b-hXqfhc.

Controls: orbit the camera with WASD (AD - left-right, WS - forwards/backwads), TR is increase/decrease threshold, EQ is up/down, YH is increase/decrease point size
Run volumetricviewer.py with python3.

Requirements: GLSL 4.30 support (right now configured for 4.40). GLSL 4.30 is required for multidimensional array support. Python libraries: pillow, numpy, pyopengl and pygame. OpenCV (opencv-python) is required for generating atlases.
Note: On Windows the depth might fail to render. This is a known bug which unfortunately I do not have time to fix. Using Linux with supported hardware is recommended.

This program has been tested on Ubuntu 19.04 and OpenSuse Tumbleweed and the latest (43x) NVidia drivers installed. The volumetric viewer achieves a stable framerate of 60Hz on GTX1080 with i7-4770 when rendering the default brain.

To view other files:
Change the defines in vertex_shader.c. If experiementing with different form factors (currently set to 256x256 tiling, 4096x4096 image therefore tiling is 16). In addition, the amount of verticies has to be defined in volumetricviewer.py in the drawcall to be the same as the amount of pixels in the atlas.

An atlas can be generated using either createAtlas.py, in which you can define your own mathematical formula by which to generate the atlas. Additionally formatBrainData.py can be used to generate an atlas from a image sequence. The viewer reads the data from bottom to up, left to right. The generated atlases have to be rotated -90d before they are usable in the viewer.
Color of the mesh is defined by the color of the sample, including alpha.
