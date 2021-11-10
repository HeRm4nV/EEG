#!/usr/bin/env python2.7
# coding=utf-8
# Copyright (c) 2020, Alvaro Rivera-Rei, rivera.rei@gmail.com

#1980x1090

"""
tested in Python 2.7.18
"""
import csv, pygame , random, sys, os
from pygame.locals import FULLSCREEN, USEREVENT, KEYDOWN, KEYUP, K_SPACE, K_RETURN, K_ESCAPE, QUIT, Color
from os.path import join
from random import seed, sample, randint, shuffle, randrange, choice
from time import gmtime, strftime
from copy import deepcopy
import math
from collections import deque

## Configurations:
FullScreenShow = True # Pantalla completa autom�ticamente al iniciar el experimento
keys = [pygame.K_SPACE] # Teclas elegidas para mano derecha o izquierda

fix_time   = 1000 # duracion cruz de fijacion
pfix_time  = 250 # duracion posterior de la cruz de fijacion
word_time  = 500 # duracion estimulo de palabra
word_delay_min = 500
word_delay_max = 1000
mental_time  = 16000 # duracion elaboracion mental
blank_time = 400 # tiempo entre que la palabra desaparece y la proxima cruz de fijacion
plus_minus = 200 # tiempo variable despues del blank time
wait_time = 5000 # tiempo de pantalla para pensar en palabras
base_words_for_block = 18

date_name = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
religion_words  = []
magic_words     = []
secular_words   = []

with open('media/words.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    line_counter = 0
    for row in reader:
        line_counter += 1
        if row['religion'] != '':
            religion_words.append(row['religion'].decode('utf-8'))
        if row['magic'] != '':
            magic_words.append(row['magic'].decode('utf-8'))
        if row['secular'] != '':
            secular_words.append(row['secular'].decode('utf-8'))

# This return the names dictionary from pygame
f=open("media/pygame_local_data.txt", "r")
pygame_dict_names = {}
fl =f.readlines()
for row in fl:
    array = row.split(" = ")
    if int(array[1][:-1]) in pygame_dict_names:
        print(array[0]+ " = " + pygame_dict_names[int(array[1][:-1])])
    pygame_dict_names[int(array[1][:-1])] = array[0]


## Onscreen instructions
slides = {
    'welcome1': [
        u"Bienvenido, gracias por tu participación.",
        " ",
        " ",
        u"Para continuar presione la barra espaciadora."
        ],
    'welcome2': [
        u"Instrucciones:",
        " ",
        u"A continuación, verás en pantalla palabras que aparecen por un breve periodo de tiempo.",
        u"Después que la palabra desaparezca, quedará una cruz en el centro de la pantalla",
        u"mientras esté presente, tendrás que pensar en conceptos relacionados con la palabra que acabas de ver.",
        u"Finalmente, cuando te indiquemos, tendrás que verbalizar (decir) las palabras que acabas de pensar.",
        " ",
        u"Primero haremos un ensayo.",
        u"Cuando estés listo presione la barra espaciadora.",
        " "
        ],
    'wait': [
        "+"
        ],
    'spell': [
        u"En voz alta, diga todas las palabras que acaba de pensar."
    ],
    'farewell': [
        u"El Experimento ha terminado.",
        "",
        u"Muchas gracias por su colaboración!!"
        ]
    }

## Functions:
def setfonts():
    """Sets font parameters"""
    global bigchar, char, charnext
    pygame.font.init()
    font     = join('media', 'Arial_Rounded_MT_Bold.ttf')
    bigchar  = pygame.font.Font(font, 96)
    char     = pygame.font.Font(font, 32)
    charnext = pygame.font.Font(font, 24)

def init():
    """Init display and others"""
    setfonts()
    global screen, resolution, center, background, char_color, charnext_color, fix, fixbox, fix_think, fixbox_think, izq, der, quest, questbox
    pygame.init() # soluciona el error de inicializacion de pygame.time
    pygame.display.init()
    #iconpath = join('media', 'spiderman.png')
    #icon     = pygame.image.load(iconpath)
    #pygame.display.set_icon(icon)
    pygame.display.set_caption("EEG")
    pygame.mouse.set_visible(False)
    if FullScreenShow:
        resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        screen     = pygame.display.set_mode(resolution, FULLSCREEN)
    else:
        try:
            resolution = pygame.display.list_modes()[3]
        except:
            resolution = (1280, 720)
        screen     = pygame.display.set_mode(resolution)
    center = (int(resolution[0] / 2), int(resolution[1] / 2))
    izq = (int(resolution[0] / 8), (int(resolution[1] / 8)*7))
    der = ((int(resolution[0] / 8)*7), (int(resolution[1] / 8)*7))
    background     = Color('gray20')
    char_color     = Color('white')
    charnext_color = Color('lightgray')
    fix            = bigchar.render('+', True, char_color)
    fixbox         = fix.get_rect(centerx = center[0], centery = center[1])
    fix_think      = bigchar.render('+', True, Color('red'))
    fixbox_think   = fix.get_rect(centerx = center[0], centery = center[1])
    quest          = bigchar.render('?', True, char_color)
    questbox       = quest.get_rect(centerx = center[0], centery = center[1])
    screen.fill(background)
    pygame.display.flip()

def blackscreen(blacktime = 0):
    """Erases the screen"""
    screen.fill(background)
    pygame.display.flip()
    pygame.time.delay(blacktime)

def render_textrect(string, font, rect, text_color, background_color, justification=1):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 left-justified
                    1 (default) horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    import pygame

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise(TextRectException, "The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise(TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise(TextRectException, "Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return final_lines, surface

def pygame_exit():
    pygame.quit()
    sys.exit()

def paragraph(text, just_info, key, rise = 0, color = None):
    """Organizes a text into a paragraph"""
    screen.fill(background)
    row = center[1] - 20 * len(text)

    if color == None:
        color = char_color
    
    for line in text:
        #try:
        #    phrase    = char.render(line, True, char_color)
        #    phrasebox = pygame.Rect((resolution[0]/8, 0 + row, resolution[0]*6/8, resolution[1]*5/8))
        #except:
        phrasebox = pygame.Rect((resolution[0]/8, rise + 0 + row, resolution[0]*6/8, resolution[1]*5/8))
        final_lines, phrase = render_textrect(line, char,  pygame.Rect((resolution[0]/8, resolution[1]/8, resolution[0]*6/8, resolution[1]*6/8)), color, background)
        screen.blit(phrase, phrasebox)
        row += 40 * len(final_lines)
    if just_info:
        if key == K_SPACE:
            foot = "Para continuar presione la BARRA ESPACIADORA..."
        elif key == K_RETURN:
            foot = "Para continuar presione la tecla ENTER..."
    else:
        foot = ""
    nextpage = charnext.render(foot, True, charnext_color)
    nextbox  = nextpage.get_rect(left = 15, bottom = resolution[1] - 15)
    screen.blit(nextpage, nextbox)
    pygame.display.flip()

def slide(text, info, key, limit_time = 0):
    """Organizes a paragraph into a slide"""
    paragraph(text, info, key)
    wait_time = wait(key, limit_time)
    return wait_time

def wait(key, limit_time):
    """Hold a bit"""

    TIME_OUT_WAIT = USEREVENT + 1
    if limit_time != 0:
        pygame.time.set_timer(TIME_OUT_WAIT, wait_time)

    tw = pygame.time.get_ticks()

    switch = True
    while switch:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame_exit()
            if event.type == KEYUP:
                if event.key == key:
                    switch = False
            if event.type == TIME_OUT_WAIT and limit_time != 0:
                if ((pygame.time.get_ticks() - tw) > limit_time):
                    switch = False
                    pygame.time.set_timer(TIME_OUT_WAIT, 0)

    return (pygame.time.get_ticks() - tw)

#create a cubir matrix with [type][block][word] matrix size = type_size(3)*list/block_size(5)*block_size(18)
#base_list is [[type_1],[type_2]....]
def words_to_matrix_conversion(base_list, block_size):
    final_matrix = []
    for i in range(len(base_list)):
        final_matrix.append([])
        for j in range(len(base_list[0])/block_size):
            final_matrix[i].append(base_list[i][j*block_size:(j+1)*block_size])
    return(final_matrix)  

def show_word_list(word_list, subj_name, dfile, block_number):
    """Main game"""

    for word in word_list:
        word_show = bigchar.render(word, True, char_color)
        wordbox   = word_show.get_rect(centerx = center[0], centery = center[1])

        screen.fill(background)
        pygame.display.flip()

        word_delay = randrange(word_delay_min, word_delay_max)

        screen.blit(fix, fixbox)
        pygame.display.update(fixbox)
        pygame.time.delay(word_delay)
        screen.fill(background)
        pygame.display.flip()
        pygame.event.clear()                    # CLEAR EVENTS

        screen.blit(word_show, wordbox)
        pygame.display.update(wordbox)
        pygame.time.delay(word_time)

        pygame.event.clear()                    # CLEAR EVENTS

    screen.fill(background)
    pygame.display.flip()

    screen.blit(fix, fixbox)
    pygame.display.update(fixbox)
    pygame.time.delay(mental_time)
    screen.fill(background)
    pygame.display.flip()
    pygame.event.clear()                    # CLEAR EVENTS

    r_time = slide(slides['spell'], True, K_RETURN, 20000)
    if dfile != None:
        dfile.write("%s,%s,%s,%s,%s\n" % (subj_name, block_number, word.encode('utf-8'), str(r_time), ""))

def polygon_creator (sides, x = 0, y = 0, radius = 1, rotation = 0):

    polygon = []

    rotation = math.radians(270) + math.radians(rotation)

    for i in range(sides):
        point_x = screen.get_width()/2 + x + radius * math.cos(rotation + math.pi * 2 * i / sides)
        point_y = screen.get_height()/2 + y + radius * math.sin(rotation + math.pi * 2 * i / sides)
        polygon.append( (int(point_x), int(point_y)) )

    return polygon

def minigame():
    screen.fill(background)
    pygame.display.flip()

    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)

    colors = [Color('#6b5b95'), Color('#feb236'), Color('#d64161'), Color('#ff7b25')] * 3
    shuffle(colors)
    colors = colors[:-3]

    sides_list = [3,4,5,6] * 3
    shuffle(sides_list)
    sides_list = sides_list[:-3]

    x_positions = [-screen.get_width()/4, 0, screen.get_width()/4]*3

    y_base_positions = deque([-screen.get_height()/4, 0, screen.get_height()/4])
    y_positions = []
    y_positions.extend(y_base_positions)
    y_base_positions.rotate(1)
    y_positions.extend(y_base_positions)
    y_base_positions.rotate(1)
    y_positions.extend(y_base_positions)
    
    for i in range(len(colors)):
        actual_sides = sides_list[i]
        if actual_sides == 4:
            actual_rotation = 45
        else:
            actual_rotation = 0
        polygon = polygon_creator(sides = actual_sides, x = x_positions[i], y = y_positions[i], radius = 70, rotation = actual_rotation)
        pygame.draw.polygon(screen, colors[i], polygon)

    pygame.display.update()
    
    pygame.time.delay(10000)

    return(sides_list, colors)

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            #font = pygame.font.SysFont('comicsans', 60)
            font = join('media', 'Arial_Rounded_MT_Bold.ttf')
            char = pygame.font.Font(font, 32)
            text = char.render(self.text, 1, (211,211,211))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
            
        return False

def answer_page(sides_list, colors):

    sides_choice = choice(sides_list)
    color_choice = choice(colors)

    question_block_rise = -100

    colors_transformation = { '(107, 91, 149, 255)': 'Lila' , '(214, 65, 97, 255)': 'Fucsia', '(254, 178, 54, 255)': 'Amarillento', '(255, 123, 37, 255)': 'Naranja'}

    sides_question = choice([True, False])
    
    if sides_question:
        question = unicode("Indique cuantos polígonos de " + str(sides_choice) + " lados había en la pantalla anterior.", "utf-8")
        correct_answer = sides_list.count(sides_choice)
        paragraph([question], False, None, rise = question_block_rise)
    else:
        question = unicode("Indique cuantos polígonos de color " + colors_transformation[str(color_choice)] + " había en la pantalla anterior.", "utf-8")
        correct_answer = colors.count(color_choice)
        paragraph([question], False, None, rise = question_block_rise, color = color_choice)
    
    answer = False
    pygame.mouse.set_visible(True)
    while not answer:
        button_size = 100
        zero_button = button((51,51,51), screen.get_width()/5 - (button_size/2), 2*screen.get_height()/3 + question_block_rise, button_size, button_size, '0')
        zero_button.draw(screen, (255,255,255))
        one_button = button((51,51,51), screen.get_width()/5*2 - (button_size/2), 2*screen.get_height()/3 + question_block_rise, button_size, button_size, '1')
        one_button.draw(screen, (255,255,255))
        two_button = button((51,51,51), screen.get_width()/5*3 - (button_size/2), 2*screen.get_height()/3 + question_block_rise, button_size, button_size, '2')
        two_button.draw(screen, (255,255,255))
        three_button = button((51,51,51), screen.get_width()/5*4 - (button_size/2), 2*screen.get_height()/3 + question_block_rise, button_size, button_size, '3')
        three_button.draw(screen, (255,255,255))
        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                answer = True
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if zero_button.isOver(pos):
                    selected = 0
                    #print("selected = " + str(selected))
                    answer = True
                elif one_button.isOver(pos):
                    selected = 1
                    #print("selected = " + str(selected))
                    answer = True
                elif two_button.isOver(pos):
                    selected = 2
                    #print("selected = " + str(selected))
                    answer = True
                elif three_button.isOver(pos):
                    selected = 3
                    #print("selected = " + str(selected))
                    answer = True

            if event.type == pygame.MOUSEMOTION:
                if zero_button.isOver(pos):
                    zero_button.color = (0,0,255)
                elif one_button.isOver(pos):
                    one_button.color = (0,0,255)
                elif two_button.isOver(pos):
                    two_button.color = (0,0,255)
                elif three_button.isOver(pos):
                    three_button.color = (0,0,255)
                else:
                    zero_button.color = (0,255,0)
                    one_button.color = (0,255,0)
                    two_button.color = (0,255,0)
                    three_button.color = (0,255,0)
                    
    pygame.mouse.set_visible(False)
    
    if sides_question:
        slide([unicode(("Correcto!" if (selected == correct_answer) else "Incorrecto") + " en la pregunta anterior habían " + str(correct_answer) + " polígonos de " + str(sides_choice) + " lados.", "utf-8")], True, K_SPACE)
    else:
        slide([unicode(("Correcto!" if (selected == correct_answer) else "Incorrecto") + " en la pregunta anterior habían " + str(correct_answer) + " polígonos de color " + colors_transformation[str(color_choice)] + ".", "utf-8")], True, K_SPACE)

def minigame_block(minigame_blocks = 1):

    slide([unicode("A continuación verás una serie de polígonos de distintos colores.", "utf-8"), unicode("Trata de memorizarlos lo mejor posible y luego responde la pregunta que verás.", "utf-8")], True, K_SPACE)
    
    for i in range(minigame_blocks):
        sides_list, colors = minigame()
        answer_page(sides_list, colors)
        
def ends():
    """Closes the show"""
    blackscreen()
    dot    = char.render('.', True, char_color)
    dotbox = dot.get_rect(left = 15, bottom = resolution[1] - 15)
    screen.blit(dot, dotbox)
    pygame.display.flip()
    while True:
        for evento in pygame.event.get():
            if evento.type == KEYUP and evento.key == K_ESCAPE:
                exit()

def main():
    """Game's main loop"""
    global is_word_key

    # Si no existe la carpeta data se crea
    if not os.path.exists('data/'):
        os.makedirs('data/')

    subj_name = raw_input("Escriba un nombre de archivo y presione ENTER para iniciar: ")
    csv_name  = join('data', date_name + '_' + subj_name + '.csv')
    dfile = open(csv_name, 'w')
    dfile.write("ID,Block,Word,Rt,Answer\n")
    init()
    
    slide(slides['welcome1'] , False , K_SPACE)
    slide(slides['welcome2'] , False , K_SPACE)

    actual_block = 1

    counts = [0, 0, 0]

    count_blocks = int((len(religion_words) + len(magic_words) + len(secular_words))/base_words_for_block)

    #shuffle(religion_words)
    #shuffle(magic_words)
    #shuffle(secular_words)

    #words = []
    #words.extend(religion_words)
    #words.extend(magic_words)
    #words.extend(secular_words)

    #words_for_block = base_words_for_block
    actual_list = 0

    words_list = words_to_matrix_conversion([religion_words, magic_words, secular_words], 18)

    random_orders = [[(1,1), (2,2), (3,3), (2,1), (3,4), (1,5), (3,5), (2,3), (1,4), (1,3), (2,5), (3,2), (2,4), (3,1), (1,2)], [(3,1), (2,4), (1,5), (1,2), (2,3), (3,4), (2,2), (3,5), (1,3), (3,3), (1,1), (2,5), (1,4), (2,1), (3,2)], [(2,3), (3,5), (1,1), (3,1), (1,5), (2,1), (2,5), (1,3), (3,4), (3,2), (2,4), (1,2), (1,4), (3,3), (2,2)]]

    selected_order = choice(random_orders)    

    for i in range (len(selected_order)):
        
        actual_words_list = words_list[selected_order[i][0]-1][selected_order[i][1]-1]
        #print("type: " + str(selected_order[i][0]-1))
        #print("block: " + str(selected_order[i][1]-1))
        #print(actual_words_list)
        #print(len(actual_words_list))

        #for j in range(base_words_for_block):
        #    if len(words) > 0:
        #        actual_words_list.append(words.pop(0))

        show_word_list(actual_words_list, subj_name, dfile, actual_block)

        if ( (i+1) % 3 == 0 ):
            minigame_block(3)

        block_text = "Fin del bloque número " + str(actual_block)
        intermission_text = [block_text.decode('utf-8'), ""]
        slide(intermission_text, True , K_SPACE)
        actual_block += 1

    dfile.close()
    pygame.time.delay(blank_time + plus_minus)
    slide(slides['farewell'], True , K_SPACE)
    ends()

## Experiment starts here...
if __name__ == "__main__":
    main()
