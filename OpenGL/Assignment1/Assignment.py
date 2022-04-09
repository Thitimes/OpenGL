## all 1.1 , 1.2 ,1.3 ,1.4,2.1,3.1,3.2,3.3, 3.4,4 missing 2.2 2.3
import sys, os
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import pandas as pd
import imgui
import math as m
from imgui.integrations.glut import GlutRenderer
from gl_helpers import *

impl, vao = None, None
shininess = 50
Ka, Kd, Ks, clear_color = [0.05, 0.05, 0.05], [0.5, 1.0, 0.2], [0.9, 0.9, 0.9], [0.1, 0.6, 0.6]
light_intensity, light_pos, eye_pos = [1, 1, 1], [0, 0, 0], [0, 0, 0]
specular_on, selection = True, 0
angleX = 0
angleY = 0
zoomValue = 1
panX = 0
panY = 0


def draw_gui():
    global selection, light_intensity, Ka, Kd, Ks, shininess, specular_on, clear_color
    impl.process_inputs()
    imgui.new_frame()                    # Start the Dear ImGui frame   
    imgui.begin("Control")               # Create a window
    imgui.push_item_width(300)
    _, light_intensity = imgui.color_edit3("Light Intensity", *light_intensity)
    if imgui.radio_button("OpenGL Lighting", selection == 0): 
        selection = 0
    imgui.same_line()
    if imgui.radio_button("Gouraud Shading", selection == 1): 
        selection = 1   
    imgui.same_line()
    if imgui.radio_button("Phong Shading", selection == 2): 
        selection = 2     
    _, specular_on = imgui.checkbox("Specular Enabled", specular_on)
    imgui.text("Light Position")
    imgui.push_item_width(100)
    _, light_pos[0] = imgui.slider_float("X###light_pos_x", light_pos[0], -10, 10)
    imgui.same_line()
    _, light_pos[1] = imgui.slider_float("Y###light_pos_y", light_pos[1], -10, 10)
    imgui.same_line()
    _, light_pos[2] = imgui.slider_float("Z###light_pos_z", light_pos[2], -10, 10)
    imgui.text("Eye Position")
    _, eye_pos[0] = imgui.slider_float("X###eye_pos_x", eye_pos[0], -10, 10)
    imgui.same_line()
    _, eye_pos[1] = imgui.slider_float("Y###eye_pos_y", eye_pos[1], -10, 10)
    imgui.same_line()
    _, eye_pos[2] = imgui.slider_float("Z###eye_pos_z", eye_pos[2], -10, 10)
    _, clear_color = imgui.color_edit3("Clear Color", *clear_color)
    imgui.text("Ka")
    _, Ka[0] = imgui.slider_float("X###Ka_pos_x", Ka[0], -10, 10)
    imgui.same_line()
    _, Ka[1] = imgui.slider_float("Y###Ka_pos_y", Ka[1], -10, 10)
    imgui.same_line()
    _, Ka[2] = imgui.slider_float("Z###Ka_pos_z", Ka[2], -10, 10)
    imgui.text("Kd")
    _, Kd[0] = imgui.slider_float("X###Kd_pos_x", Kd[0], -10, 10)
    imgui.same_line()
    _, Kd[1] = imgui.slider_float("Y###Kd_pos_y", Kd[1], -10, 10)
    imgui.same_line()
    _, Kd[2] = imgui.slider_float("Z###Kd_pos_z", Kd[2], -10, 10)
    imgui.text("Ks")
    _, Ks[0] = imgui.slider_float("X###Ks_pos_x", Ks[0], -10, 10)
    imgui.same_line()
    _, Ks[1] = imgui.slider_float("Y###Ks_pos_y", Ks[1], -10, 10)
    imgui.same_line()
    _, Ks[2] = imgui.slider_float("Z###Ks_pos_z", Ks[2], -10, 10)
    imgui.pop_item_width()
    imgui.text("Shininess")
    _, shininess = imgui.slider_float("###Shininess",shininess, 0.5, 100)


    imgui.text("Application average %.3f ms/frame (%.1f FPS)" % \
        (1000 / imgui.get_io().framerate, imgui.get_io().framerate))
    imgui.pop_item_width()
    imgui.end()

def reshape(w, h):
    global win_w, win_h, proj_mat
    
    win_w, win_h = w, h
    glViewport(0, 0, w, h)
    proj_mat = Perspective(60, w/h, 0.1, 100)
    glMatrixMode(GL_PROJECTION)
    glLoadMatrixf(proj_mat.T)
    
def display():
    global eye_pos
    global panX,panY
    glClearColor(*clear_color, 0)
    eye_pos += (panY,panX,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    model_mat = Rotate(angleX,1,0,0) @ Rotate(angleY,0,1,0)
    view_mat = LookAt(*eye_pos * zoomValue , *centroid, 0, 1, 0)
    if(selection ==0):
        #opengl lighting
        glUseProgram(0)
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(view_mat.T)
        glMultMatrixf(model_mat.T)
     

      
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_intensity)

        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_intensity)

        if(specular_on == True):
            glLightfv(GL_LIGHT0, GL_SPECULAR, light_intensity)
        else:
            glLightfv(GL_LIGHT0, GL_SPECULAR, 0)


        glLightfv(GL_LIGHT0, GL_POSITION, [*light_pos,1])

        
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, Ka)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, Kd)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR,Ks)

        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
        glVertexPointer(3, GL_FLOAT, 0, positions)
        glColorPointer(3, GL_FLOAT, 0, colors)
        glNormalPointer(GL_FLOAT, 0, normals)
        glTexCoordPointer(2, GL_FLOAT, 0, uvs)  

    if(selection != 0):
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        glUseProgram(prog_id)
        glUniform3fv(glGetUniformLocation(prog_id, "Kd"), 1, Kd)
        glUniform3fv(glGetUniformLocation(prog_id, "Ka"), 1, Ka)
        glUniform3fv(glGetUniformLocation(prog_id, "Ks"), 1, Ks)
        glUniform1f(glGetUniformLocation(prog_id, "shininess"),shininess)
        glUniform3fv(glGetUniformLocation(prog_id, "Il"), 1, light_intensity)
        glUniform3fv(glGetUniformLocation(prog_id, "eye_pos"), 1, eye_pos)
        glUniform3fv(glGetUniformLocation(prog_id, "light_pos"), 1, light_pos)
        glUniform1i(glGetUniformLocation(prog_id, "specular_on"),specular_on)
        glUniform1i(glGetUniformLocation(prog_id, "selection"),selection)
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
    panX = 0
    panY = 0
    glutSwapBuffers()

wireframe = False
def keyboard(key, x, y):
    global wireframe
    global selection
    global isShift

 
    
    key = key.decode("utf-8")
    if key == 'w':
        wireframe = not wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE if wireframe else GL_FILL)        
    elif key == 'q':
        impl.shutdown()
        os._exit(0)
    elif key == '1':
        selection = 0
    elif key == '2':
        selection = 1
    elif key == '3':
        selection = 2

    
   # if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
       # print("Shift is pressed")
    


  

def idle():
    glutPostRedisplay()
def mouseCB(button, state, x,y):
    global isClicked
    global isMMClicked
    
    global start_pos
 
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        isClicked = True
        start_pos = [x,y]
    else:
        isClicked = False
    if button == GLUT_MIDDLE_BUTTON and state == GLUT_DOWN:
        isMMClicked = True
        start_pos = [x,y]
    else:
        isMMClicked = False
   
def motionCB(x,y):
    global angleX,angleY
    global panX,panY
    global zoomValue
    global isShift
    isShift = False
    if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
        isShift = True
        
    else:
        isShift = False
   
    if isClicked == True and isShift == False:
        angleX += (y - start_pos[1]) * 0.05
        angleY += (x - start_pos[0]) * 0.05
        glutPostRedisplay()


    elif isMMClicked == True:
        zoomValue += (x - start_pos[0]) * 0.0005
        glutPostRedisplay()



    elif isShift == True and isClicked == True:
        panX = (y - start_pos[1]) * 0.0005
        panY = (x - start_pos[0]) * 0.0005
        glutPostRedisplay()
 


def initialize():
    global impl

    imgui.create_context()
    imgui.style_colors_dark()
    impl = GlutRenderer()
    impl.user_keyboard_func(keyboard)
    impl.user_mouse_func(mouseCB)
    impl.user_motion_func(motionCB)
    impl.user_reshape_func(reshape)
    imgui.set_next_window_position(500, 10)
    imgui.set_next_window_collapsed(True)

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

    vert_code = '''
#version 140
in vec3 position,normal;
uniform vec3 Ka, Kd, Ks; // Material Properties of ambient, diffuse, specular
uniform float shininess;
uniform vec3 Il; // Light Intensity
uniform vec3 light_pos; // Light Position
uniform vec3 eye_pos; // Eye Position
uniform bool specular_on;
out vec3 phong_color;
uniform int selection;
uniform mat4 model_mat, view_mat, proj_mat;
out vec3 fP, fN;
void main()
{
    fP = vec3(0,0,0);
    fN = vec3(0,0,0);
    if(selection == 1){
        gl_Position = proj_mat * view_mat * model_mat * vec4(position, 1);
        vec3 P = (model_mat * vec4(position, 1)).xyz;
        vec3 L = normalize(light_pos - P);
        vec3 V = normalize(eye_pos - P);
        vec3 N = (model_mat * vec4(normal, 0)).xyz;
        vec3 R = 2 * dot(L,N) * N - L;
        vec3 ambient = Ka * Il;
        vec3 diffuse = Kd * max(dot(N, L), 0) * Il;
        vec3 specular = Ks * pow(max(dot(V, R), 0), shininess) * Il;
        if (dot(N, L) < 0)
            specular = vec3(0, 0, 0);
        if(specular_on == false){
            specular = vec3(0, 0, 0);
        }
        phong_color = ambient + diffuse + specular;
    }
    if(selection == 2){
        gl_Position = proj_mat * view_mat * model_mat * vec4(position, 1);
        fP = (model_mat * vec4(position, 1)).xyz;
        fN = (model_mat * vec4(normal, 0)).xyz;
    }

}'''
    frag_code = '''
#version 140
in vec3 phong_color;
uniform int selection;
uniform vec3 Ka, Kd, Ks; // Material Properties of ambient, diffuse, specular
uniform float shininess;
uniform vec3 Il; // Light Intensity
uniform vec3 light_pos; // Light Position
uniform vec3 eye_pos; // Eye Position
uniform bool specular_on;
in vec3 fP, fN;
void main()
{
   if(selection == 1) {
    gl_FragColor = vec4(phong_color, 1);
   }
    if(selection == 2){
        vec3 L = normalize(light_pos - fP);
        vec3 V = normalize(eye_pos - fP);
        vec3 N = normalize(fN);
        vec3 R = 2 * dot(L,N) * N - L;
        vec3 ambient = Ka * Il;
        vec3 diffuse;
        diffuse = Kd * max(dot(N, L), 0) * Il;
        vec3 specular = Ks * pow(max(dot(V, R), 0), shininess) * Il;
        if (dot(N, L) <= 0)
            specular = vec3(0, 0, 0);
        if(specular_on == false){
            specular = vec3(0, 0, 0);
        }
        gl_FragColor.rgb = ambient + diffuse + specular;
    }
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
    print_program_info_log(prog_id, "Link error")

    global n_vertices, positions, colors, normals, uvs, centroid, bbox
    global light_pos, eye_pos

    df = pd.read_csv("../models/teapot.tri", delim_whitespace=True,
                     comment='#', header=None, dtype=np.float32)
    centroid = df.values[:, 0:3].mean(axis=0)
    bbox = df.values[:, 0:3].max(axis=0) - df.values[:, 0:3].min(axis=0)
    light_pos = centroid + (0, 0, 5)
    eye_pos = centroid + (0, 0, 5)

    positions = df.values[:, 0:3]
    colors = df.values[:, 3:6]
    normals = df.values[:, 6:9]
    uvs = df.values[:, 9:11]
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
    glutInitWindowSize(800, 600)
    glutCreateWindow("Phong Lighting Model Exercise")
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glEnable(GL_DEPTH_TEST)
    initialize()
    create_shaders()
    show_versions()

    glutMainLoop()

def show_versions():
    lists = [['Vendor', GL_VENDOR], ['Renderer',GL_RENDERER],
            ['OpenGL Version', GL_VERSION],
            ['GLSL Version', GL_SHADING_LANGUAGE_VERSION]]
    for x in lists:
        print("%s: %s" % (x[0], glGetString(x[1]).decode("utf-8")))

if __name__ == "__main__":
    main()