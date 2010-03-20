# This shader example is based on test-shader.c from the clutter sources.
# The used shader sources may not work for all GPU's, but they do for mine.

import sys
import clutter

SHADER_BRIGHTNESS_CONTRAST = """
uniform sampler2D tex;
uniform float x_step, y_step;
uniform float brightness, contrast;
void main (){
  vec4 color = texture2D (tex, vec2(gl_TexCoord[0]));
 color.rgb /= color.a;
 color.rgb = (color.rgb - vec3(0.5, 0.5, 0.5)) * contrast +
vec3 (brightness + 0.5, brightness + 0.5, brightness + 0.5);
 color.rgb *= color.a;
  gl_FragColor = color;
  gl_FragColor = gl_FragColor * gl_Color;
}
"""

SHADER_BOX_BLUR = """
uniform sampler2D tex;
uniform float x_step, y_step;
vec4 get_rgba_rel(sampler2D tex, float dx, float dy)
{
  return texture2D (tex, gl_TexCoord[0].st
                         + vec2(dx, dy) * 2.0);
}
void main (){
  vec4 color = texture2D (tex, vec2(gl_TexCoord[0]));
  float count = 1.0;
  color += get_rgba_rel (tex, -x_step, -y_step); count++;
  color += get_rgba_rel (tex, -x_step,  0.0);    count++;
  color += get_rgba_rel (tex, -x_step,  y_step); count++;
  color += get_rgba_rel (tex,  0.0,    -y_step); count++;
  color += get_rgba_rel (tex,  0.0,     0.0);    count++;
  color += get_rgba_rel (tex,  0.0,     y_step); count++;
  color += get_rgba_rel (tex,  x_step, -y_step); count++;
  color += get_rgba_rel (tex,  x_step,  0.0);    count++;
  color += get_rgba_rel (tex,  x_step,  y_step); count++;
  color = color / count;
  gl_FragColor = color;
  gl_FragColor = gl_FragColor * gl_Color;
}
"""

SHADER_INVERT = """
uniform sampler2D tex;
uniform float x_step, y_step;
void main (){
  vec4 color = texture2D (tex, vec2(gl_TexCoord[0]));
  color.rgb /= color.a;
  color.rgb = vec3(1.0, 1.0, 1.0) - color.rgb;
  color.rgb *= color.a;
  gl_FragColor = color;
  gl_FragColor = gl_FragColor * gl_Color;
}
"""

SHADER_GRAY = """
uniform sampler2D tex;
uniform float x_step, y_step;
void main (){
  vec4 color = texture2D (tex, vec2(gl_TexCoord[0]));
  float avg = (color.r + color.g + color.b) / 3.0;
  color.r = avg;
  color.g = avg;
  color.b = avg;
  gl_FragColor = color;
  gl_FragColor = gl_FragColor * gl_Color;
}
"""

SHADER_COMBINED_MIRROR = """
uniform sampler2D tex;
uniform float x_step, y_step;
void main (){
  vec4 color = texture2D (tex, vec2(gl_TexCoord[0]));
  vec4 colorB = texture2D (tex, vec2(gl_TexCoord[0].ts));
  float avg = (color.r + color.g + color.b) / 3.0;
  color.r = avg;
  color.g = avg;
  color.b = avg;
  color = (color + colorB)/2.0;
  gl_FragColor = color;
  gl_FragColor = gl_FragColor * gl_Color;
}
"""

SHADER_EDGE_DETECT = """
uniform sampler2D tex;
uniform float x_step, y_step;
float get_avg_rel(sampler2D texB, float dx, float dy)
{
  vec4 colorB = texture2D (texB, gl_TexCoord[0].st + vec2(dx, dy));
  return (colorB.r + colorB.g + colorB.b) / 3.0;
}
void main (){
  vec4 color = texture2D (tex, vec2(gl_TexCoord[0]));
  mat3 sobel_h = mat3( 1.0,  2.0,  1.0,
                       0.0,  0.0,  0.0,
                      -1.0, -2.0, -1.0);
  mat3 sobel_v = mat3( 1.0,  0.0, -1.0,
                       2.0,  0.0, -2.0,
                       1.0,  0.0, -1.0);
  mat3 map = mat3( get_avg_rel(tex, -x_step, -y_step),
                   get_avg_rel(tex, -x_step, 0.0),
                   get_avg_rel(tex, -x_step, y_step),
                   get_avg_rel(tex, 0.0, -y_step),
                   get_avg_rel(tex, 0.0, 0.0),
                   get_avg_rel(tex, 0.0, y_step),
                   get_avg_rel(tex, x_step, -y_step),
                   get_avg_rel(tex, x_step, 0.0),
                   get_avg_rel(tex, x_step, y_step) );
  mat3 gh = sobel_h * map;
  mat3 gv = map * sobel_v;
  float avgh = (gh[0][0] + gh[0][1] + gh[0][2] +
                gh[1][0] + gh[1][1] + gh[1][2] +
                gh[2][0] + gh[2][1] + gh[2][2]) / 18.0 + 0.5;
  float avgv = (gv[0][0] + gv[0][1] + gv[0][2] +
                gv[1][0] + gv[1][1] + gv[1][2] +
                gv[2][0] + gv[2][1] + gv[2][2]) / 18.0 + 0.5;
  float avg = (avgh + avgv) / 2.0;
  color.r = avg * color.r;
  color.g = avg * color.g;
  color.b = avg * color.b;
  gl_FragColor = color;
  gl_FragColor = gl_FragColor * gl_Color;
}
"""

SHADERS = [
    ('brightness-contrast', SHADER_BRIGHTNESS_CONTRAST),
    ('box-blur', SHADER_BOX_BLUR),
    ('invert', SHADER_INVERT),
    ('gray', SHADER_GRAY),
    ('combined-mirror', SHADER_COMBINED_MIRROR),
    ('edge-detect', SHADER_EDGE_DETECT)
]


class ShaderTest(object):
    def __init__(self, filename=None):
        self.shader_no = -1
        self.stage = clutter.Stage()
        self.stage.connect('destroy', clutter.main_quit)
        self.stage.connect('button-press-event', self.on_button_press)
        self.actor = clutter.Texture()

        if not filename:
            filename = 'redhand.png'
        try:
            self.actor.set_from_file(filename)
        except Exception, e:
            print "Can't load texture '%s': %s" % (filename, e)
            sys.exit(1)

        self.stage.add(self.actor)

    def on_button_press(self, stage, event):
        self.apply_next_shader()

    def apply_next_shader(self):
        self.shader_no += 1
        if self.shader_no >= len(SHADERS):
            self.shader_no = 0

        shader_name = SHADERS[self.shader_no][0]
        shader_source = SHADERS[self.shader_no][1]
        shader = clutter.Shader()
        shader.set_fragment_source(shader_source)

        try:
            shader.compile()
        except Exception, e:
            print "Can't compile shader '%s': %s" % (shader_name, e)
            return
        self.actor.set_shader(shader)

        self.actor.set_shader_param_int('tex', 0)
        self.actor.set_shader_param_float('radius', 3.0)
        self.actor.set_shader_param_float('brightness', 0.4)
        self.actor.set_shader_param_float('contrast', -1.9)

        tex_width = round(self.actor.get_width())
        tex_height = round(self.actor.get_height())
        self.actor.set_shader_param_float('x_step', 1.0 / tex_width)
        self.actor.set_shader_param_float('y_step', 1.0 / tex_height)

        print "Loaded shader '%s'" % (shader_name)

    def main(self):
        self.stage.show()
        clutter.main()

if __name__ == '__main__':
    if not clutter.feature_available(clutter.FEATURE_SHADERS_GLSL):
        print "GLSL shaders are not available"
        sys.exit(1)

    if len(sys.argv) == 2:
        filename = sys.argv[1]
    else:
        filename = None

    shader_test = ShaderTest(filename)
    shader_test.main()

