import random
import time
import xml.dom.minidom
from typing import Tuple
from xml.dom import minidom
from xml.dom.minidom import DOMImplementation
from core.perlin import perlinNoise, fractalBrownianMotion
from core.genimage import setPixel, initImage, savePNG
import os
#width = 300
#height = 300

terrain_map = []
#image = initImage(width, height)


#mapsize = {height, width}
mapsymbols = {
    "water": '~',
    "grass": ',',
    "mountain": '^',
    "sand": '.',
    "tree": '/'
}

mapcolors = {
    "water": (0, 0, 255),
    "grass": (0, 255, 0),
    "mountain": (192, 192, 192),
    "sand": (255, 255, 0),
    "tree": (64, 48, 32)
}



#for symbol in mapsymbols:
#    print(mapsymbols[symbol])



#root = minidom.Document()

def get_terrain_color(value: float) -> Tuple[str, Tuple[int, int, int]]:
    if value < -0.1:
        return "water", (0, 0, 255)
    elif value < 0.5:
        return "grass", (0, 255, 0)
    elif value < 0.7:
        return "sand", (255, 255, 0)
    else:
        return "mountain", (192, 192, 192)

def initDocument(root, width, height):
    html = root.documentElement
    html.setAttribute('xmlns', 'http://www.w3.org/1999/xhtml')


    head = root.createElement('head')
    html.appendChild(head)

    title = root.createElement('title')
    text = root.createTextNode("test")
    head.appendChild(title)
    title.appendChild(text)

    body = root.createElement('body')
    html.appendChild(body)

def generateMapToPNG(width, height):
    image = initImage(width, height)

    terrain_types = list(mapsymbols.keys())

    for y in range(height):

        for x in range(width):
            terrain = random.choices(terrain_types, weights=(30, 50, 20, 10, 20), k=1)[0]
            terrain_map.append(terrain)



            terrainVal = fractalBrownianMotion(x, y, 6)

            setPixel(image, get_terrain_color(terrainVal)[1], x, y)


    current_dir = os.path.dirname(__file__)
    map_path = os.path.abspath(os.path.join(current_dir, '..', 'map.png'))
    savePNG(image, map_path)

def generateMapXHTML(width, height):
    image = initImage(width, height)

    imp = DOMImplementation()
    doctype = imp.createDocumentType(
        qualifiedName='html',
        publicId='',
        systemId=''
    )

    root = imp.createDocument(None, 'html', doctype)
    root.doctype = xml.dom.minidom.DocumentType('html')

    initDocument(root, width, height)

    terrain_types = list(mapsymbols.keys())
    body = root.getElementsByTagName("body")[0]



    for y in range(height):

        pixelsize = 3

        row_div = root.createElement('div');

        row_div.setAttribute('style', 'display:flex')
        body.appendChild(row_div)
        for x in range(width):
            terrain = random.choices(terrain_types, weights=(30, 50, 20, 10, 20), k=1)[0]
            terrain_map.append(terrain)



            terrainVal = fractalBrownianMotion(x, y, 6)



            subdiv = root.createElement('div')
            setPixel(image, get_terrain_color(terrainVal)[1], x, y)
            subdiv.setAttribute('style',
                                f'background-color: rgb{mapcolors[get_terrain_color(terrainVal)[0]]}; height:{pixelsize}px; width:{pixelsize}px')

            row_div.appendChild(subdiv)


    xhtml_str = root.toprettyxml(indent="\t")
    save_path_file = "test.xhtml"
    with open(save_path_file, "w") as f:
        f.write(xhtml_str)  # Experimental xhtml file generation

    img_path_file = "../map.png"
    savePNG(image, img_path_file)





#initDocument(root)
#generateMap(root)







#img_path_file = "map.png"

#savePNG(image, img_path_file)







#for i in map:
#    print(i)

#print(len(map))
#print([len(v) for v in map])