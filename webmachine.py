from typing import Optional, Any
import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import TextInput, ColorPicker, Text


# set a stage and general properties
p = figure(plot_width=400, plot_height=800, tools='save')
linewidth=3.5 # warp and weft properties
a = 0 # top position warpA
b = 1 # top left position warpB
b2 = -1 # top right position warpB
color_picker = ColorPicker(color="#f666f0", title="Choose a color and hit return to start weaving:", width=400)
black= "#000000"
warpdefault0 = -2 # warp position on y axis, low end
warpdefault1 = 60 # warp position on y axis, high end
Y0A = -1.5 # the number of lines already woven
Y1A = Y0A + 1.5 # pattern position
Y0B = -2.5 # pattern position
Y1B = Y0B + 1.5 # pattern position
weft1=-2
weft2=118
n=1 # n should be the number of times that weft y has changed
zen=1
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p.yaxis.major_label_text_color = None
p.xaxis.major_label_text_color = None


def setcolor(attr, old, new): # initial color setting
    color_picker.visible = False
    warpA = p.segment(x0=range(0, 120, 4), y0=[warpdefault0] * 60, x1=range(a, (a + 120), 4), y1=[warpdefault1] * 60,
                      color=color_picker.color, line_width=linewidth)


color_picker.on_change('color', setcolor) # trigger initial color setting


# MAIN WARPS normal and alternating position + tiny lower warp part viisble
warpB = p.segment(x0=range(0, 120, 4), y0=[warpdefault0] * 60, x1=range(b, (b + 120), 4), y1=[warpdefault1] * 60, color=black, line_width=linewidth)
warpB2 = p.segment(x0=range(0, 120, 4), y0=[warpdefault0] * 60, x1=range(b2, (b2 + 120), 4), y1=[warpdefault1] * 60, color=black, line_width=linewidth)
WARPA = p.segment(x0=range(0, 120, 4), y0=[warpdefault0] * 60, x1=range(a, (a + 120), 4), y1=[warpdefault1] * 60, color=color_picker.color, line_width=linewidth)
warpB.visible = True
warpB2.visible = False
WARPA.visible = False


# colored lines already woven
def weave_pink(attr, old, new):
    global Y0A
    if Y0A < 56:
        Y0A += 2
        Y1A = Y0A + 1
        p.segment(x0=range(0, 120, 4), y0=[Y0A] * 60, x1=range(a, (a + 120), 4), y1=[Y1A] * 60, color=color_picker.color,
                  line_width=linewidth * 1.8)
    if n >= 56:
        return


# black lines already woven
def weave_black(attr, old, new):
    global Y0B
    global textbox
    if Y0B < 56:
        Y0B += 2
        Y1B = Y0B + 1
        if Y0B != -0.5:
            p.segment(x0=range(0, 120, 4), y0=[Y0B] * 60, x1=range(a, (a + 120), 4), y1=[Y1B] * 60, color=black,
                      line_width=linewidth * 1.8)
    if Y0B >= 56:
        textbox.title ='Your text_ile is done. Please save it with the floppy icon to your desktop'
        return


textbox = TextInput(value="", title='Please click into the textbox to start typing') # text input glyph


def weave(attr, old, new): # black warps exchange visibility, weft moves up, weaving is created
    if warpB.visible:
        warpB.visible = False
        warpB2.visible = True
        weftmove2(attr, old, new)
        weave_black(attr, old, new)
        patterncolor(attr, old, new)
    else:
        warpB.visible = True
        warpB2.visible = False
        weftmove1(attr, old, new)
        weave_pink(attr, old, new)
        patternblack(attr, old, new)


def weftmove1(attr, old, new): # weft grows one line to the left
    global n
    if n < 60:
        n += 1
        p.step([weft2, weft1] * n, range((n-2), n), line_width=linewidth * 1.5, mode="after", color='#545454')
    if n >= 60:
        return


def weftmove2(attr, old, new): # weft grows one line to the right
    global n
    if n < 60:
        n += 1
        p.step([weft1, weft2] * n, range((n-2), n), line_width=linewidth * 1.5, mode="after", color='#545454')
    if n == 2:
        p.segment(x0=range(0, 120, 4), y0=[warpdefault0] * 60, x1=range(a, (a + 120), 4), y1=0.008 * 60, color=color_picker.color,
                  line_width=linewidth)
    if n >= 60:
        return


zeny = -1 # pattern parameter
zenx = 4 # pattern parameter


def update(attr, old, new): # update weaving, pattern, limit input char range and initialize colored warp
    for char in textbox.value_input:
        print(ord(char))
    if ord(char) > 97 and ord(char) < 122 or ord(char) >= 44 and ord(char) <= 46:
        if WARPA.visible == False:
            WARPA.visible = True
            color_picker.visible = False
        thetrick(attr, old, new)
        weave(attr, old, new)
    else:
        return


def thetrick(attr, old, new): # create pattern according to char input
    for char in textbox.value_input:
        global zenx
        if char == ' ': zenx = 108
        elif char == '?': zenx = 112
        elif char == '.': zenx = 116
        elif char == ',': zenx = 0
        else: zenx = (ord(char)-97) * 4
        print(zenx)


def patterncolor(attr, old, new): # create pattern color
    global zeny
    global zenx
    if zeny < 56:
        zeny += 1
    p.oval(x=zenx, y=zeny, width=2, height=1, angle=0, color=color_picker.color)
    if n >= 56:
        return


def patternblack(attr, old, new): # create pattern black
    global zeny
    global zenx
    if zeny < 56:
        zeny += 1
    p.oval(x=zenx, y=zeny, width=2, height=1, angle=0, color=black)
    if n >= 56:
        return


textbox.on_change('value_input', update) # each time a character hit, update is executed

curdoc().add_root(column(textbox, p, color_picker)) # Document setup

# Run it like this: bokeh serve --show webmachine.py OR on server: bokeh serve webmachine.py
