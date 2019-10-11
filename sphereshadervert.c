#version 440

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform sampler2D atlas;

out vec4 color;

void main()
{

	float u = float(gl_VertexID) / 4096.;
	float angle = u * 3.141 * 2.0;
	float radius = 0.8;

	vec2 pos = vec2(cos(angle), sin(angle)) * radius;

	float aspect = 768.0 / 1280.0;
	vec2 scale = vec2(aspect, 1.);

	gl_Position = vec4(pos * scale, 0., 1.);
	gl_PointSize = 5.0;

	color = vec4(1.0);

}
