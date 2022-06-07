# Coupled oscillations
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np
import matplotlib.patches as patches


def draw_spring(xs1, xs2, turn_spring, half_width_spring):
    x_start = min(xs1, xs2)
    x_end = max(xs1, xs2)
    len_spring = abs(x_start - x_end)
    pitch_spring = len_spring / turn_spring
    # Draw 1st line
    ax.plot([x_start, x_start + pitch_spring / 4], [0., half_width_spring], c='black')
    # Draw last line
    ax.plot([x_end, x_end - pitch_spring / 4], [0., - half_width_spring], c='black')
    # Draw other lines
    for i in range(turn_spring):
        xo_start = x_start + pitch_spring * i + pitch_spring / 4
        ax.plot([xo_start, xo_start + pitch_spring * 2 / 4], [half_width_spring, - half_width_spring], c='black')
    for i in range(turn_spring - 1):
        xo_start = x_start + pitch_spring * i + pitch_spring * 3 / 4
        ax.plot([xo_start, xo_start + pitch_spring * 2 / 4], [- half_width_spring, half_width_spring], c='black')


def start():
    global is_dragged, in_drag, force1, a1, v1, force2, a2, v2
    in_drag = False
    is_dragged = False
    force1 = 0.
    a1 = 0.
    v1 = 0.

    force2 = 0.
    a2 = 0.
    v2 = 0.


def on_button_release(event):
    global in_drag, force1, a1, v1, force2, a2, v2
    in_drag = False
    force1 = 0.
    a1 = 0.
    v1 = 0.

    force2 = 0.
    a2 = 0.
    v2 = 0.


def on_button_press(event):
    global in_drag, is_dragged
    if event.button == 1:
        in_drag = True
        is_dragged = True


def motion(event):
    global x_ball1, y_ball1, x_ball2, y_ball2
    if (event.xdata is None) or (event.ydata is None):
        return
    if in_drag:
        if event.xdata < -1:
            x_ball1 = event.xdata
            if x_ball1 - x_ball_ini1 > x_limit:
                x_ball1 = x_limit + x_ball_ini1
            if x_ball1 - x_ball_ini1 < - x_limit:
                x_ball1 = - x_limit + x_ball_ini1
        elif event.xdata > 1:
            x_ball2 = event.xdata
            if x_ball2 - x_ball_ini2 > x_limit:
                x_ball2 = x_limit + x_ball_ini2
            if x_ball2 - x_ball_ini2 < - x_limit:
                x_ball2 = - x_limit + x_ball_ini2
        else:
            pass


def change_k1(value):
    global k1
    k1 = float(value)


def change_k2(value):
    global k2
    k2 = float(value)


def change_k3(value):
    global k3
    k3 = float(value)


def change_m1(value):
    global mass1
    mass1 = float(value)


def change_m2(value):
    global mass2
    mass2 = float(value)


def stop():
    global force1, a1, v1, x_ball1, force2, a2, v2, x_ball2
    force1 = 0.
    a1 = 0.
    v1 = 0.
    x_ball1 = x_ball_ini1

    force2 = 0.
    a2 = 0.
    v2 = 0.
    x_ball2 = x_ball_ini2


def set_axis():
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title('Coupled oscillations')
    ax.set_xlabel('x')
    tm_adjust = resolution / y_max  # To adjust time scale and line-space
    ax.set_ylabel('t * ' + str(f'{tm_adjust:.1f}'))
    ax.grid()
    ax.set_aspect("equal")
    ax.set_xticks([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])


def update(f):
    ax.cla()  # Clear ax
    set_axis()

    global x_ball1, y_ball1, force1, a1, v1, x1, x_ball2, y_ball2, force2, a2, v2, x2, dx1, dx2, ds2
    ax.text(x_min, y_max * 0.9, " Step(as t)=" + str(f))
    # Draw ball
    c1 = patches.Circle(xy=(x_ball1, y_ball1), radius=radius_ball, fc='black', ec='black')
    ax.add_patch(c1)
    c2 = patches.Circle(xy=(x_ball2, y_ball2), radius=radius_ball, fc='black', ec='black')
    ax.add_patch(c2)
    # Draw line
    x_roll1 = np.roll(x1, 1)
    x1 = x_roll1
    x1[0] = x_ball1
    ax.plot(x1, y, label="dx1")
    x_roll2 = np.roll(x2, 1)
    x2 = x_roll2
    x2[0] = x_ball2
    ax.plot(x2, y, label="dx2")
    ds2_roll2 = np.roll(ds2, 1)
    ds2 = ds2_roll2
    ds2[0] = dx2 - dx1
    ax.plot(ds2, y, linestyle=':', linewidth='1', label="dx2-dx1")
    ax.legend(prop={"size": 8}, loc="best")
    # Draw spring
    draw_spring(x_min, x_ball1 - radius_ball, turn_s, half_ws)
    draw_spring(x_ball2 + radius_ball, x_max, turn_s, half_ws)
    draw_spring(x_ball1 + radius_ball, x_ball2 - radius_ball, turn_s, half_ws)
    # Draw explanations
    ax.text(x_ball1, y_max * 0.1, "m1")
    ax.text(x_ball2, y_max * 0.1, "m2")
    ax.text((x_ball1 + x_min) / 2, y_max * 0.1, "k1")
    ax.text(x_ball1 + (x_ball2 - x_ball1) / 2, y_max * 0.1, "k2")
    ax.text(x_ball2 + (x_max - x_ball2) / 2, y_max * 0.1, "k3")
    ax.plot([x_ball1, x_ball1], [0., y_min], c='black', linewidth='1', linestyle=':')
    ax.plot([x_ball2, x_ball2], [0., y_min], c='black', linewidth='1', linestyle=':')
    ax.text(x_ball1, y_min * 0.5, "F1(=-k1*dx+k2(dx2-dx1))=" + str(f'{force1:.2f}'))
    allow_f_len1 = force1
    ax.annotate(
        '', xy=[x_ball1 + allow_f_len1, y_min * 0.6], xytext=[x_ball1, y_min * 0.6],
        arrowprops=dict(width=1, headwidth=4, headlength=4, facecolor='red', edgecolor='red')
        )
    ax.text(x_ball2, y_min * 0.7, "F2(=-k3*dx-k2(dx2-dx1))=" + str(f'{force2:.2f}'))
    allow_f_len2 = force2
    ax.annotate(
        '', xy=[x_ball2 + allow_f_len2, y_min * 0.8], xytext=[x_ball2, y_min * 0.8],
        arrowprops=dict(width=1, headwidth=4, headlength=4, facecolor='red', edgecolor='red')
        )
    # Calculate motion of balls
    if not is_dragged and not in_drag:
        dx1 = x_ball1 - x_ball_ini1
        dx2 = x_ball2 - x_ball_ini2
        force1 = - k1 * dx1 + k2 * (dx2 - dx1)
        a1 = force1 / mass1
        v1 = v1 + a1
        x_ball1 = x_ball1 + v1

        force2 = - k3 * dx2 - k2 * (dx2 - dx1)
        a2 = force2 / mass2
        v2 = v2 + a2
        x_ball2 = x_ball2 + v2


# Global variables
x_min = -12.
x_max = 12.
y_min = -4.
y_max = 10.

is_dragged = False
in_drag = False

# Parameters
x_ball_ini1 = -4.
x_ball1 = x_ball_ini1
y_ball1 = 0.

x_ball_ini2 = 4.
x_ball2 = x_ball_ini2
y_ball2 = 0.

k1 = 1.
k2 = 1.
k3 = 1.

mass1 = 50.
mass2 = 50.

x_limit = 3.
radius_ball = 0.5
turn_s = 6     # Turn of spring
half_ws = 0.4   # Half width of spring

force1 = 0.
a1 = 0.
v1 = 0.

force2 = 0.
a2 = 0.
v2 = 0.

dx1 = 0.
dx2 = 0.

# Generate Line space
resolution = 200
y = np.linspace(0, y_max, resolution)
x1 = y * 0. + x_ball_ini1
x2 = y * 0. + x_ball_ini2
ds2 = y * 0.    # diff of spring2

# Generate tkinter
root = tkinter.Tk()
root.title("Coupled oscillations")

# Generate figure and axes
fig = Figure(figsize=(8, 4))
fig.canvas.mpl_connect('motion_notify_event', motion)
fig.canvas.mpl_connect('button_press_event', on_button_press)
fig.canvas.mpl_connect('button_release_event', on_button_release)
ax = fig.add_subplot(111)

# Embed a figure in canvas
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

# Animation
anim = animation.FuncAnimation(fig, update, interval=50)

# Toolbar
toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

# Label and spinbox for k (spring constant)
label_k1 = tkinter.Label(root, text="k1(Spring constant)")
label_k1.pack(side='left')
var_k1 = tkinter.StringVar(root)  # variable for spinbox-value
var_k1.set(k1)  # Initial value
s_k1 = tkinter.Spinbox(
    root, textvariable=var_k1, format="%.1f", from_=0.1, to=2.0, increment=0.1,
    command=lambda: change_k1(var_k1.get()), width=4
    )
s_k1.pack(side='left')

label_k2 = tkinter.Label(root, text=", k2")
label_k2.pack(side='left')
var_k2 = tkinter.StringVar(root)  # variable for spinbox-value
var_k2.set(k2)  # Initial value
s_k2 = tkinter.Spinbox(
    root, textvariable=var_k2, format="%.1f", from_=0.1, to=2.0, increment=0.1,
    command=lambda: change_k2(var_k2.get()), width=4
    )
s_k2.pack(side='left')

label_k3 = tkinter.Label(root, text=", k3")
label_k3.pack(side='left')
var_k3 = tkinter.StringVar(root)  # variable for spinbox-value
var_k3.set(k2)  # Initial value
s_k3 = tkinter.Spinbox(
    root, textvariable=var_k3, format="%.1f", from_=0.1, to=2.0, increment=0.1,
    command=lambda: change_k3(var_k3.get()), width=4
    )
s_k3.pack(side='left')

# Label and spinbox for mass
label_m1 = tkinter.Label(root, text="m1(Mass)")
label_m1.pack(side='left')
var_m1 = tkinter.StringVar(root)  # variable for spinbox-value
var_m1.set(mass1)  # Initial value
s_m1 = tkinter.Spinbox(
    root, textvariable=var_m1, format="%.1f", from_=50., to=100., increment=1,
    command=lambda: change_m1(var_m1.get()), width=4
    )
s_m1.pack(side='left')

label_m2 = tkinter.Label(root, text="m2")
label_m2.pack(side='left')
var_m2 = tkinter.StringVar(root)  # variable for spinbox-value
var_m2.set(mass2)  # Initial value
s_m2 = tkinter.Spinbox(
    root, textvariable=var_m2, format="%.1f", from_=50., to=100., increment=1,
    command=lambda: change_m2(var_m2.get()), width=4
    )
s_m2.pack(side='left')

# Label
m = tkinter.Label(root, relief="sunken", text='Drag the balls, then click start button!')
m.pack(side='left')
# Start button
b = tkinter.Button(root, text="Start", command=start)
b.pack(side='left')
# Reset button
b = tkinter.Button(root, text="Stop", command=stop)
b.pack(side='left')

# main loop
set_axis()
tkinter.mainloop()
