from tkinter import *
from PIL import Image, ImageTk
import data as dt
import sys
from heapq import heappush, heappop, heapify


# CONSTANTS
CITY_OPTION = []


# get data set from data.py
dt.create_DataSet()
GRAPH = dt.GRAPH
cities = dt.CITIES_DATA_SET
for i in range(len(cities)):
    # add to option box
    CITY_OPTION.append(cities[i].name)

print(len(CITY_OPTION))
# start GUI app
tk = Tk()
tk.title("MapAi App")
tk.geometry("1350x700")
iconFile = PhotoImage(file="assets/appicon.png")
tk.wm_iconphoto(False, iconFile)

# create canvas for darw and other stuff
canvas = Canvas(master=tk, width=950, height=700)
canvas.pack(side=LEFT)

SOURCE_CITY = StringVar()
DESTINATION_CITY = StringVar()

# set image to canvas
imageTemp = (Image.open("assets/worldmap.png"))
image_re = imageTemp.resize((950, 700), Image.ANTIALIAS)
final_image = ImageTk.PhotoImage(image_re)
canvas.create_image(0, 0, anchor=NW, image=final_image)


# create frame for buttons
frame = Frame(master=tk, width=370, height=700)
frame.pack(side=RIGHT)
frame.pack_propagate(0)


# make label for choose country
label_source = Label(master=frame, text="Choose City")
label_source.pack()
label_source.place(x=5, y=10)
label_source.config(font=("Courier", 12))


# make option box for choose country
SOURCE_CITY.set(CITY_OPTION[0])
city_for_source = CITY_OPTION
choose_source = OptionMenu(frame, SOURCE_CITY, SOURCE_CITY)
choose_source.pack()
choose_source.place(x=5, y=40)


# for destination city
label_dest = Label(master=frame, text="Choose City")
label_dest.pack()
label_dest.place(x=5, y=90)
label_dest.config(font=("Courier", 12))

DESTINATION_CITY.set(CITY_OPTION[1])
city_for_dest = CITY_OPTION
choose_destination = OptionMenu(frame, DESTINATION_CITY, *CITY_OPTION)
choose_destination.pack()
choose_destination.place(x=5, y=120)

# add option box for choose country
for i in range(len(city_for_source)):
    choose_source['menu'].add_command(
        label=city_for_source[i], command=lambda value=city_for_source[i]: SOURCE_CITY.set(value))

# for i in range(len(city_for_dest)) :
#     choose_destination['menu'].add_command(label = city_for_dest[i], command = lambda value=city_for_dest[i]: DESTINATION_CITY.set(value))

# draw cities on map
cities_dot = []

def draw_cities():
    global cities_dot
    # destroy all cities
    # for l in cities_dot:
    #     canvas.delete(l)
    for i in range(len(cities)):
        x = cities[i].x
        y = cities[i].y
        line = canvas.create_oval(x, y, x+5, y+5, fill="black")
        cities_dot.append(line)

print(cities_dot)

mouseX = 0
mouseY = 0
eventTrigger = 0


def set_city_base_on_mouse_click():
    global mouseX
    global mouseY
    global eventTrigger
    global cities_dot
    for i in range(len(cities)):
        x = cities[i].x
        y = cities[i].y
        if mouseX > x and mouseX < x+5 and mouseY > y and mouseY < y+5 and eventTrigger == 0:
            SOURCE_CITY.set(cities[i].name)
            # Draw red dot
            canvas.create_oval(x, y, x+7, y+5, fill="red")
            canvas.create_text(x, y-8, text=cities[i].name)
            # change dot color
            # if cities_dot != []:
            #     for l in cities_dot:
            #         if l.x == x and l.y == y:
            #             canvas.itemconfig(l, fill="red")
            eventTrigger = 1
            break
        elif mouseX > x and mouseX < x+7 and mouseY > y and mouseY < y+5 and eventTrigger == 1:
            # check if source and destination is same
            if cities[i].name != SOURCE_CITY.get():
                DESTINATION_CITY.set(cities[i].name)
                canvas.create_oval(x, y, x+7, y+5, fill="blue")
                # display city name on map
                canvas.create_text(x, y-8, text=cities[i].name)
                # if cities_dot != []:
                #     for l in cities_dot:
                #         if l.x == x and l.y == y:
                #             canvas.itemconfig(l, fill="blue")
                eventTrigger = 0
                break


def get_mouse_position(event):
    global mouseX
    global mouseY
    mouseX = event.x
    mouseY = event.y
    # print(mouseX, mouseY)
    set_city_base_on_mouse_click()


canvas.bind("<Button-1>", get_mouse_position)


label_path = Label(master=frame, text="Path : ")
label_path.pack()
label_path.place(x=1, y=370)

label_cost = Label(master=frame, text="distance : ")
label_cost.pack()
label_cost.place(x=1, y=350)

# functoin for display graph


def darw_graph(ask):
    global GRAPH
    global canvas
    # link all cities in graph
    for city in GRAPH:
        for i in range(len(GRAPH[city])):
            for j in range(len(cities)):
                if cities[j].name == city:
                    x1 = cities[j].x
                    y1 = cities[j].y
                if cities[j].name == GRAPH[city][i][0]:
                    x2 = cities[j].x
                    y2 = cities[j].y
            canvas.create_line(x1, y1, x2, y2, fill="red", width=1)
            # display distance
            canvas.create_text(
                (x1+x2)/2, (y1+y2)/2, text=GRAPH[city][i][1], fill="black", font=("Poppines", 9))

# draw path


def draw_path(path):
    global canvas
    draw_cities()
    # canvas.delete(line)
    for i in range(len(path)-1):
        for j in range(len(cities)):
            if cities[j].name == path[i]:
                x1 = cities[j].x
                y1 = cities[j].y
            if cities[j].name == path[i+1]:
                x2 = cities[j].x
                y2 = cities[j].y
        canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

# check if destination city is adjacent to source city
def is_adjacent(src, dest):
    if dest in GRAPH[src]:
        return True

def dijkstra(graph, src, dest):
    global for_label_path
    global label_path
    inf = sys.maxsize
    node_data = {}
    for node in graph:
        node_data[node] = {"distance": inf, "previous": []}
    node_data[src]["distance"] = 0
    visited = []
    temp = src
    # print(len(graph))
    for i in range(0, len(graph)):
        if temp not in visited:
            visited.append(temp)
            min_heap = []
            for node in graph[temp]:
                # print(node)
                if node[0] not in visited:
                    cost = node_data[temp]["distance"] + node[1]
                    # print(cost)
                    if cost < node_data[node[0]]["distance"]:
                        node_data[node[0]]["distance"] = cost
                        node_data[node[0]]["previous"].append(temp)

                        # print(node_data[node[0]]["previous"])
                    heappush(
                        min_heap, (node_data[node[0]]["distance"], node[0]))
                    # print(min_heap)
        heapify(min_heap)
        # print(min_heap)
        if len(min_heap) != 0:
            temp = heappop(min_heap)[1]
            # print(temp)
    # draw path
    path = []
    path.append(src)
    if (len(node_data[dest]["previous"]) != 0):
        path += node_data[dest]["previous"]
        path.append(dest)
        label_cost.config(text="distance : " + str(node_data[dest]["distance"]))
        label_path.config(text="Path : " + str(path))
        # for_label_path.append(path)
        draw_path(path)
    elif is_adjacent(src, dest):
        path = [src, dest]
        label_path.config(text="Path : " + str(path))
        label_cost.config(text="distance : " + str(GRAPH[src][0][1]))
        draw_path(path)
    else :
        label_cost.config(text="distance : No Way" )
        label_path.config(text="Path : No Way" )
    # draw line btw cities in path


# make button for find path
findPath = Button(master=frame, text="Find Path", command=lambda: dijkstra(
    GRAPH, SOURCE_CITY.get(), DESTINATION_CITY.get()))
findPath.pack()
findPath.place(x=5, y=190)

displayGraph = Button(master=frame, text="Display Graph",
                      command=lambda: darw_graph(True))
displayGraph.pack()
displayGraph.place(x=5, y=230)

# label for show path


draw_cities()
tk.mainloop()
