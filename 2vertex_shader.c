#version 440

//in layout(location=0) vec3 vertexPos;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform sampler2D atlas;

out vec4 color;

//vec2 quadVerticies[4] = { 
//	vec2(-1.0, -1.0), vec2(1.0, -1.0), vec2(-1.0, 1.0), vec2(1.0, 1.0)};

vec3 cubeVerticies[16];

#define SAMPLEWIDTH 64
#define TILING 4
#define WIDTH 16


int depthLUT[TILING * TILING];

void populateDepthLUT()
{
	int currentDepth = 0;

	for (int x = 0; x < TILING; x++)
	{
		for (int y = 0; y < TILING; y++)
		{
			if (x * y + x > TILING*TILING)
				return;

			depthLUT[x * y + x] = currentDepth;
			currentDepth++;			
			
			//depthLUT[x][y] = currentDepth;
		}
	}
}

int getDepth(vec2 point)
{
	int x = int(point.x);
	int y = int(point.y);
	if (x * y + x > TILING*TILING)
		return 0;

	return depthLUT[x * y + x];
}


vec2 getSampleCoordinate(int index)
{
	int x = 0;
	int y = 0;
	
	for (int i = 0; i < index; i++)
	{
		if (x == SAMPLEWIDTH - 1)
		{
			y++;
			x = 0;
		}
		else
			x++;
	}

	return vec2(float(x), float(y));
}

vec2 getVolumeCoordinate(vec2 sCoord)
{
	int x = int(sCoord.x) % WIDTH;
	int y = int(sCoord.y) % WIDTH;

	return vec2(float(x), float(y));
}

int getTile(int x)
{
	int x_ = 0;

	for (int i = 0; i < SAMPLEWIDTH; i + WIDTH)
	{
		if (x >= i && x < i + WIDTH)
		{
			return x_;
		}

		x_++;
	}
}

vec2 getTileCoordinate(vec2 sampleCoord)
{
	int x = int(sampleCoord.x);
	int y = int(sampleCoord.y);

	int x_ = getTile(x);
	int y_ = getTile(y);

	return vec2(float(x_), float(y_));
}

vec3 getPointOnVolume(int index)
{
	vec2 sCoord = getSampleCoordinate(index);
	vec2 tCoord = getTileCoordinate(sCoord);
	vec2 vCoord = getVolumeCoordinate(sCoord);

	// return vec3(vCoord.x, vCoord.y, float(depthLUT[int(tCoord.y)][int(tCoord.x)])) / 16.;

	sCoord = sCoord / float(SAMPLEWIDTH);
	vec3 tSample = vec3(texture(atlas, sCoord).rgb);
	
	if (tSample != vec3(.0))
	{
		color = vec4(0., 0., 1., tSample.r);
		return vec3(vCoord.x, vCoord.y, float(getDepth(tCoord))) / float(WIDTH);
		
		// return vec3(vCoord.x, vCoord.y, float(depthLUT[int(tCoord.x)][int(tCoord.y)])) / float(WIDTH);
	}
	
	color = vec4(0.);
	return vec3(0.);
}

void main()
{
	populateDepthLUT();
	vec3 vertexPos = getPointOnVolume(gl_VertexID);
	gl_PointSize = 10.0;
	gl_Position = projectionMatrix * modelMatrix * vec4(vertexPos, 1.0);
}
