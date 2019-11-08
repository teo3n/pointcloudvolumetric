#version 320 es

//in layout(location=0) vec3 vertexPos;
uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform sampler2D atlas;

uniform float cutoffThreshold;
uniform float pointSize;

uniform float maxVal;
uniform float minVal;

out vec4 color;

#define TILING 16
#define WIDTH 128
#define SAMPLEWIDTH 2048

//#define POINT_SIZE 1.5
//#define THRESHOLD vec3(0.27, 0.27, 0.27)


int depthLUT[TILING][TILING];
vec3 THRESHOLD;

void populateDepthLUT()
{
	int currentDepth = 0;

	for (int x = 0; x < TILING; x++)
	{
		for (int y = 0; y < TILING; y++)
		{
			depthLUT[x][y] = currentDepth;
			currentDepth++;
		}
	}
}

int getDepth(vec2 point)
{
	int x = int(point.x);
	int y = int(point.y);

	return depthLUT[x][y];
}


vec2 getSampleCoordinate(int index)
{
	int x = int(index % SAMPLEWIDTH);
	int y = int(index / SAMPLEWIDTH);

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

	for (int i = 0; i < SAMPLEWIDTH;)
	{
		if (x >= i && x < i + WIDTH)
		{
			return x_;
		}

		x_++;
		i += WIDTH;
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

vec4 remapColor(vec4 sColor)
{
	float fstThird = minVal + ((maxVal - minVal) / 3.0);
	float sndThird = minVal + (2. * (maxVal - minVal) / 3.0);

	if (sColor.w == 0.0)
		return sColor;

	float s = sColor.x;

	if (s < fstThird && s >= minVal)
	{
		return vec4(s, 0.0, 0.0, sColor.w);
	}
	else if (s < sndThird && s >= fstThird)
	{
		return vec4(0.0, s, 0.0, sColor.w);
	}
	else if (s <= maxVal && s >= sndThird)
	{
		return vec4(0.0, 0.0, s, sColor.w);
	}

	return vec4(1.);
}

vec3 getPointOnVolume(int index)
{
	vec2 sCoord = getSampleCoordinate(index);
	vec2 tCoord = getTileCoordinate(sCoord);
	vec2 vCoord = getVolumeCoordinate(sCoord);

	sCoord = sCoord / float(SAMPLEWIDTH);
	vec4 tSample = texture(atlas, sCoord);

	if (tSample.x > THRESHOLD.x && tSample.y > THRESHOLD.y && tSample.z > THRESHOLD.z)
	{
		color = remapColor(tSample);
		return vec3((vCoord.x - 64.)*2., (vCoord.y -64.)*2., float(getDepth(tCoord)) - 128.);
	}

	color = vec4(0.);
	return vec3(0.);
}

void main()
{
	THRESHOLD = vec3(cutoffThreshold);
	populateDepthLUT();
	vec3 vertexPos = getPointOnVolume(gl_VertexID);
	gl_PointSize = pointSize; //POINT_SIZE;
	gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPos, 1.0);
}
