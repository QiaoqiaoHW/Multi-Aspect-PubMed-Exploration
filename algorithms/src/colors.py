import random
chosen_colors = [
    "#BE3559", "#aeaa00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", \
    "#006FA6", "#0089A3", "#0000A6", "#B79762", "#004D43", "#8FB0FF", \
    "#5A0007", "#BA0900", "#1B4400", "#4FC601", "#3B5DFF", "#00C2A0", \
    "#549E79", "#BC23FF", "#C895C5", "#FF2F80", "#009271", "#00FECF", \
    "#A4E804", "#FFB500", "#6B002C", "#FF9408", "#CC0744", "#D790FF", \
    "#5B4534", "#E83000", "#6F0062", "#b65141", "#C20078", "#7A4900", 
    "#FF90C9", "#6508ba",
]

lables = [i for i in range(len(chosen_colors))]
colors_new_legend = dict(zip(lables, chosen_colors))
colors_new_legend[-1]='black'

def generate_colors(num):
    colors_new_legend = {}
    colors_new_legend[-1]='black'
    for i in range(num):
        color = "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        colors_new_legend[i] = color
    return colors_new_legend