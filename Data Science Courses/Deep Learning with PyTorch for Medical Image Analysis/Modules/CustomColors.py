import colorsys
import numpy as np


def hsl_to_rgb(h, s, l):
    return [int(255 * i) for i in colorsys.hls_to_rgb(h, l, s)]


def rgb_to_hsl(rgb):
    r, g, b = tuple(i / 255 for i in rgb)
    hls = colorsys.rgb_to_hls(r, g, b)
    return (hls[0], hls[2], hls[1])


def hex_to_rgb(hex):
    hex = hex.lstrip("#")
    length = len(hex)
    return tuple(
        int(hex[i : i + length // 3], 16) for i in range(0, length, length // 3)
    )


def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def hsl_array_to_hex(h_array, s_array, l_array):
    colors = []
    hsl_array = np.concatenate((h_array, s_array, l_array)).reshape(3, -1).T
    for hsl in hsl_array:
        r, g, b = hsl_to_rgb(hsl[0], hsl[1], hsl[2])
        colors.append(rgb_to_hex(r, g, b))
    return colors


def color_space_checker(color, color_space):
    if color_space == "hex":
        return rgb_to_hsl(hex_to_rgb(color))
    elif color_space == "rgb":
        return rgb_to_hsl(color)
    elif color_space == "hsl":
        color = (
            color[0],
            *[float(i.rstrip("%")) if type(i) == str else i for i in color[1:]],
        )
        return [color[0] / 360, color[1] / 100, color[2] / 100]
    exception = Exception("This color space is not supported.")
    raise exception


def calm_color_generator(n):
    hue = np.repeat(np.random.random(), n)
    hue_interval = np.linspace(0, 1, n, endpoint=False)
    saturation = 0.6 + np.random.random() / 5.0 * np.random.choice([-1, 1])
    lightness = 0.5 + np.random.random() / 10.0 * np.random.choice([-1, 1])
    h = hue + hue_interval
    h_array = np.where(h > 1, h - 1, h)
    s_array = np.repeat(saturation, n)
    l_array = np.repeat(lightness, n)
    return hsl_array_to_hex(h_array, s_array, l_array)


def gradient_color_generator(hsl, n, gradient):
    h, s = hsl[:2]
    h_array = np.repeat(h, n)
    s_array = np.repeat(s, n)
    if gradient == "upward":
        l_array = np.linspace(0.65, 0.9, n, endpoint=True)
    elif gradient == "downward":
        l_array = np.linspace(0.9, 0.65, n, endpoint=True)
    else:
        exception = Exception(
            "Please make sure the gradient direction is set correctly."
        )
        raise exception
    return h_array, s_array, l_array


def gradient_dark_generator(color, n, color_space="hex"):
    hsl = color_space_checker(color, color_space)
    h_array, s_array, l_array = gradient_color_generator(hsl, n, "downward")
    return hsl_array_to_hex(h_array, s_array, l_array)


def gradient_light_generator(color, n, color_space="hex"):
    hsl = color_space_checker(color, color_space)
    h_array, s_array, l_array = gradient_color_generator(hsl, n, "upward")
    return hsl_array_to_hex(h_array, s_array, l_array)
