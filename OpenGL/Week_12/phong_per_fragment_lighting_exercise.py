import sys, os
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd
import imgui
from imgui.integrations.glut import GlutRenderer
from gl_helpers import *

impl, vao = None, None
win_w, win_h = 1280, 800
shininess = 50
Ka, Kd, Ks, clear_color = [0.05, 0.05, 0.05], [0.83, 0.69, 0.22], [0.9, 0.9, 0.9], [0, 0.45, 0.45]
Kd_b = [0.5,0.4,0.9]
I, light_pos, eye_pos = [1, 1, 1], [0, 0, 0], [0, 0, 0]
rot_y, specular_on, phong_on,twoside_on = 30, True, False,False

def draw_gui():
    global I, Ka, Kd, Kd_b, Ks, shininess, clear_color
    global rot_y, specular_on, phong_on , twoside_on
    impl.process_inputs()
    imgui.new_frame()                 # Start the Dear ImGui frame 
    imgui.set_next_window_position(win_w-450, 10, imgui.FIRST_USE_EVER)
    imgui.set_next_window_collapsed(True, imgui.FIRST_USE_EVER)
    imgui.begin("Control")            # Create a window
    imgui.push_item_width(300)
    _, I = imgui.color_edit3("Light Intensity", *I)
    _, Ka = imgui.color_edit3("Ka", *Ka)
    _, Kd = imgui.color_edit3("Kd", *Kd)
    _, Kd_b = imgui.color_edit3("Kd_b", *Kd_b)
    _, Ks = imgui.color_edit3("Ks", *Ks)
    _, shininess = imgui.slider_float("Shininess", shininess, 0.5, 200)    
    _, specular_on = imgui.checkbox("Specular Enabled", specular_on)
    _, twoside_on = imgui.checkbox("Two-Sided Lighting", twoside_on)
    if imgui.radio_button("Gouraud Shading", not phong_on): 
        phong_on = False
    imgui.same_line()
    if imgui.radio_button("Phong Shading", phong_on): 
        phong_on = True
    imgui.text("Light Position")
    imgui.push_item_width(100)
    _, light_pos[0] = imgui.slider_float("X###light_pos_x", light_pos[0], -10, 10)
    imgui.same_line()
    _, light_pos[1] = imgui.slider_float("Y###light_pos_y", light_pos[1], -10, 10)
    imgui.same_line()
    _, light_pos[2] = imgui.slider_float("Z###light_pos_z", light_pos[2], centroid[2]-5*bbox[2], centroid[2]+5*bbox[2])
    imgui.text("Eye Position")
    _, eye_pos[0] = imgui.slider_float("X###eye_pos_x", eye_pos[0], -10, 10)
    imgui.same_line()
    _, eye_pos[1] = imgui.slider_float("Y###eye_pos_y", eye_pos[1], -10, 10)
    imgui.same_line()
    _, eye_pos[2] = imgui.slider_float("Z###eye_pos_z", eye_pos[2], centroid[2]-5*bbox[2], centroid[2]+5*bbox[2])
    imgui.text("Eye At")
    _, eye_at[0] = imgui.slider_float("X###eye_at_x", eye_at[0], -10, 10)
    imgui.same_line()
    _, eye_at[1] = imgui.slider_float("Y###eye_at_y", eye_at[1], -10, 10)
    imgui.same_line()
    _, eye_at[2] = imgui.slider_float("Z###eye_at_z", eye_at[2], centroid[2]-5*bbox[2], centroid[2]+5*bbox[2])
    imgui.pop_item_width()
    _, rot_y = imgui.slider_float("Rotate Y", rot_y, -180, 180)    
    _, clear_color = imgui.color_edit3("Clear Color", *clear_color)

    imgui.text("Application average %.3f ms/frame (%.1f FPS)" % \
        (1000 / imgui.get_io().framerate, imgui.get_io().framerate))
    imgui.end()

def reshape(w, h):
    global win_w, win_h, proj_mat

    win_w, win_h = w, h
    glViewport(0, 0, w, h)
    proj_mat = Perspective(60, w/h, 0.1, 10)
    
def display():
    glClearColor(*clear_color, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    model_mat = Identity()
    view_mat = LookAt(*eye_pos, *centroid, 0, 1, 0)

    glUseProgram(prog_id)
    glUniform3fv(glGetUniformLocation(prog_id, "Kd"), 1, Kd)
    glUniform3fv(glGetUniformLocation(prog_id, "Kd_b"), 1, Kd_b)
    glUniform3fv(glGetUniformLocation(prog_id, "Ka"), 1, Ka)
    glUniform3fv(glGetUniformLocation(prog_id, "Ks"), 1, Ks)
    glUniform1f(glGetUniformLocation(prog_id, "shininess"),shininess)
    glUniform3fv(glGetUniformLocation(prog_id, "Il"), 1, I)
    glUniform3fv(glGetUniformLocation(prog_id, "eye_pos"), 1, eye_pos)
    glUniform3fv(glGetUniformLocation(prog_id, "light_pos"), 1, light_pos)
    glUniform1i(glGetUniformLocation(prog_id, "twoside"),twoside_on)
    model_mat_loc = glGetUniformLocation(prog_id, "model_mat")
    glUniformMatrix4fv(model_mat_loc, 1, GL_TRUE, model_mat)

    view_mat_loc = glGetUniformLocation(prog_id, "view_mat")
    glUniformMatrix4fv(view_mat_loc, 1, GL_TRUE, view_mat)

    proj_mat_loc = glGetUniformLocation(prog_id, "proj_mat")
    glUniformMatrix4fv(proj_mat_loc, 1, GL_TRUE, proj_mat)

    glBindVertexArray(vao)
    glDrawArrays(GL_TRIANGLES, 0, n_vertices)

    draw_gui()
    imgui.render()
    impl.render(imgui.get_draw_data())

    glutSwapBuffers()

wireframe = False
def keyboard(key, x, y):
    global wireframe

    key = key.decode("utf-8")
    if key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)        
    elif key == 'q':
        impl.shutdown()
        os._exit(0)

def idle():
    glutPostRedisplay()

def initialize():
    global impl

    show_versions()
    glEnable(GL_DEPTH_TEST)
    imgui.create_context()
    imgui.style_colors_dark()
    impl = GlutRenderer()
    impl.user_keyboard_func(keyboard)
    impl.user_reshape_func(reshape)
    load_texture("../texture_map/demon.png",1)

def print_shader_info_log(shader, prompt=""):
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not result:
        print("%s: %s" % (prompt, glGetShaderInfoLog(shader).decode("utf-8")))
        os._exit()

def print_program_info_log(shader, prompt=""):
    result = glGetProgramiv(shader, GL_LINK_STATUS)
    if not result:
        print("%s: %s" % (prompt, glGetProgramInfoLog(shader).decode("utf-8")))
        os._exit()
        
def create_shaders():
    global prog_id, vao, vbo

    vert_id = glCreateShader(GL_VERTEX_SHADER)
    frag_id = glCreateShader(GL_FRAGMENT_SHADER)

    vert_code = b'''
#version 130
in vec3 position, normal;
uniform mat4 model_mat, view_mat, proj_mat;
out vec3 fP, fN;
void main()
{
gl_Position = proj_mat * view_mat * model_mat * vec4(position, 1);
fP = (model_mat * vec4(position, 1)).xyz;
fN = (model_mat * vec4(normal, 0)).xyz;
}'''
    frag_code = b'''
#version 130
uniform vec3 Ka, Kd,Kd_b, Ks; // Material Properties of ambient, diffuse, specular
uniform float shininess;
uniform vec3 Il; // Light Intensity
uniform vec3 light_pos; // Light Position
uniform vec3 eye_pos; // Eye Position
uniform bool twoside;
in vec3 fP, fN;
void main()
{
   
    vec3 L = normalize(light_pos - fP);
    vec3 V = normalize(eye_pos - fP);
    vec3 N = normalize(fN);
    vec3 R = 2 * dot(L,N) * N - L;
    vec3 ambient = Ka * Il;
    vec3 diffuse;
    if(twoside){
        if(dot(N, V) <= 0 ){
            diffuse = Kd_b * abs(dot(N, L)) * Il;
        }
        else{
            diffuse = Kd * max(dot(N, L), 0) * Il;
        }
    }
    else{
        diffuse = Kd * max(dot(N, L), 0) * Il;
    }
    
    vec3 specular = Ks * pow(max(dot(V, R), 0), shininess) * Il;
    if (dot(N, L) <= 0)
        specular = vec3(0, 0, 0);
    gl_FragColor.rgb = ambient + diffuse + specular;
}'''
    glShaderSource(vert_id, vert_code)
    glShaderSource(frag_id, frag_code)

    glCompileShader(vert_id)
    glCompileShader(frag_id)
    print_shader_info_log(vert_id, "Vertex Shader")
    print_shader_info_log(frag_id, "Fragment Shader")

    prog_id = glCreateProgram()
    glAttachShader(prog_id, vert_id)
    glAttachShader(prog_id, frag_id)

    glLinkProgram(prog_id)
    print_program_info_log(prog_id, "Link Error")

    global n_vertices, positions, colors, normals, uvs, centroid, bbox
    global light_pos, eye_pos, eye_at

    df = pd.read_csv("../models/teapot_uv.tri", delim_whitespace=True, 
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)
    light_pos = centroid + (0, 0, 1.2*max(bbox))
    eye_pos = centroid + (0.5, 0, 1.2*max(bbox))
    eye_at = centroid + (0.5, 0, 0)

    positions = df.values[:, 0:3]
    if df.values.shape[1] > 8:
        colors = df.values[:, 3:6]
        start_idx = 6
    else:
        start_idx = 3
    normals = df.values[:, start_idx:start_idx+3]
    uvs = df.values[:, start_idx+3:start_idx+5]
    n_vertices = len(positions)

    glUseProgram(prog_id)
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    vbo = glGenBuffers(4)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, positions, GL_STATIC_DRAW)
    position_loc = glGetAttribLocation(prog_id, "position")
    glVertexAttribPointer(position_loc, 3, GL_FLOAT, GL_FALSE, 0, 
        c_void_p(0))
    glEnableVertexAttribArray(position_loc)
    color_loc = glGetAttribLocation(prog_id, "color")
    if color_loc != -1:
        glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
        glBufferData(GL_ARRAY_BUFFER, colors, GL_STATIC_DRAW)
        glVertexAttribPointer(color_loc, 3, GL_FLOAT, GL_FALSE, 0, 
            c_void_p(0))
        glEnableVertexAttribArray(color_loc)
    normal_loc = glGetAttribLocation(prog_id, "normal")
    if normal_loc != -1:
        glBindBuffer(GL_ARRAY_BUFFER, vbo[2])
        glBufferData(GL_ARRAY_BUFFER, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(normal_loc, 3, GL_FLOAT, GL_FALSE, 0, 
            c_void_p(0))
        glEnableVertexAttribArray(normal_loc)
    uv_loc = glGetAttribLocation(prog_id, "uv")
    if uv_loc != -1:
        glBindBuffer(GL_ARRAY_BUFFER, vbo[3])
        glBufferData(GL_ARRAY_BUFFER, uvs, GL_STATIC_DRAW)
        glVertexAttribPointer(uv_loc, 2, GL_FLOAT, GL_FALSE, 0, c_void_p(0))
        glEnableVertexAttribArray(uv_loc)

def main():
    global impl, clear_color
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowPosition(80, 0)
    glutInitWindowSize(win_w, win_h)
    glutCreateWindow("Phong Lighting Model Exercise")
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    initialize()
    create_shaders()

    glutMainLoop()

def show_versions():
    lists = [['Vendor', GL_VENDOR], ['Renderer',GL_RENDERER],
            ['OpenGL Version', GL_VERSION],
            ['GLSL Version', GL_SHADING_LANGUAGE_VERSION]]
    for x in lists:
        print("%s: %s" % (x[0], glGetString(x[1]).decode("utf-8")))

if __name__ == "__main__":
    main()