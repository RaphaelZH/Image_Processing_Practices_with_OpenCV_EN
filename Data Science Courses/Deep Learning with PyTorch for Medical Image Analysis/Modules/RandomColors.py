import random


def list_head_checker(list_1, list_2):
    for _ in range(len(list_2)):
        if list_1[-1] != list_2[0]:
            break
        head, list_2 = list_2[0], list_2[1:]
        list_2.append(head)
    return list_2


def list_connector(list_1, list_2):
    if list_1 != []:
        list_2 = list_head_checker(list_1, list_2)
    list_1 += list_2
    return list_1


def color_list_generator(n=100):
    termcolors = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
    font_colors_list = []
    for i in range(((n - 1) // 8 + 1)):
        if n <= 8:
            random_list = random.sample(termcolors, k=n)
            list_connector(font_colors_list, random_list)
        elif i < ((n - 1) // 8):
            random_list = random.sample(termcolors, k=8)
            list_connector(font_colors_list, random_list)
        else:
            k = n % 8
            if k == 0:
                random_list = random.sample(termcolors, k=8)
                list_connector(font_colors_list, random_list)
            elif k == 1:
                random_list = random.sample(termcolors, k=2)
                font_colors_list = list_connector(font_colors_list, random_list)[:-1]
            else:
                random_list = random.sample(termcolors, k=k)
                list_connector(font_colors_list, random_list)
    return font_colors_list
