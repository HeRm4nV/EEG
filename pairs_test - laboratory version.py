#!/usr/bin/env python2.7
# coding=utf-8
# Copyright (c) 2020, Alvaro Rivera-Rei, rivera.rei@gmail.com

#1980x1090

"""
tested in Python 2.7.18
"""
import csv, pygame , random, sys, os
from pygame.locals import FULLSCREEN, USEREVENT, KEYDOWN, KEYUP, K_SPACE, K_RETURN, K_ESCAPE, K_LCTRL, K_RCTRL, QUIT, Color
from os.path import join
from random import seed, sample, randint, shuffle, randrange, choice
from time import gmtime, strftime
from copy import deepcopy
import math, string
from collections import deque
import unicodedata

## Configurations:
FullScreenShow = True # Pantalla completa autom�ticamente al iniciar el experimento
keys = [pygame.K_SPACE] # Teclas elegidas para mano derecha o izquierda

word_time_min  = 600 # duracion estimulo de palabra
word_time_max  = 700 # duracion estimulo de palabra
word_delay_min = 400
word_delay_max = 600
blank_time_min = 1200 # tiempo en blanco entre conjuntos de palabras
blank_time_max = 1500 # tiempo en blanco entre conjuntos de palabras
blank_before_question = 1000 # tiempo en blanco entre palabra y pregunta
wait_time = 5000 # tiempo de pantalla para pensar en palabras
base_words_for_block = 18

date_name = strftime("%Y-%m-%d_%H-%M-%S", gmtime())
religion_words_C  = []
religion_words_I  = []
magic_words_C     = []
magic_words_I     = []
secular_words_C   = []
secular_words_I   = []

## Port address and triggers
lpt_address     = 0xD100
trigger_latency = 5
start_trigger   = 254
stop_trigger    = 255

# secular
SCP = 001
SCT = 002
SIP = 011
SIT = 012
question_start_secular = 021
yes_answer_secular = 031
no_answer_secular = 032
correct_answer_secular = 041
wrong_answer_secular = 042

# religious
RCP = 101
RCT = 102
RIP = 111
RIT = 112
question_start_religious = 121
yes_answer_religious = 131
no_answer_religious = 132
correct_answer_religious = 141
wrong_answer_religious = 142

# magic
MCP = 201
MCT = 202
MIP = 211
MIT = 212
question_start_magic = 221
yes_answer_magic = 231
no_answer_magic = 232
correct_answer_magic = 241
wrong_answer_magic = 242

code_access = {"secular" = 0, "religious" = 1, "magic" = 2, "congruent" = 0, "incongruent" = 1, "prime" = 1, "target" = 2, "question_start" = 21, "yes_answer" = 31, "no_answer" = 32, "correct_answer" = 41, "wrong_answer" = 42}

with open('media/words_list.csv', 'r') as csvfile:

    for i in range(2):
        csvfile.next()

    reader = csv.DictReader(csvfile)
    line_counter = 0
    for row in reader:
        line_counter += 1

        religion_words_C.append([row['Religiosa_RCP'].decode('utf-8'), row['Religiosa_RCT'].decode('utf-8')])

        religion_words_I.append([row['Religiosa_RIP'].decode('utf-8'), row['Secular_RIT'].decode('utf-8')])

        if (row['Magica_MCP'] == 'psí­quica'):
            magic_words_C.append([("psiquica".replace("i","í",1)).decode('utf-8'), row['Magica_MCT'].decode('utf-8')])
        elif (row['Magica_MCT'] == 'psí­quica'):
            magic_words_C.append([row['Magica_MCP'].decode('utf-8'), ("psiquica".replace("i","í",1)).decode('utf-8')])
        else:
            magic_words_C.append([row['Magica_MCP'].decode('utf-8'), row['Magica_MCT'].decode('utf-8')])


        if (row['Magica_MIP'] == 'psí­quica'):
            magic_words_I.append([("psiquica".replace("i","í",1)).decode('utf-8'), row['Secular_MIT'].decode('utf-8')])
        else:
            magic_words_I.append([row['Magica_MIP'].decode('utf-8'), row['Secular_MIT'].decode('utf-8')])


        secular_words_C.append([row['Secular_SCP'].decode('utf-8'), row['Secular_SCT'].decode('utf-8')])

        secular_words_I.append([row['Secular_SIP'].decode('utf-8'), row['Religiosa_SIT'].decode('utf-8')])

shuffle(religion_words_C)
shuffle(religion_words_I)
shuffle(magic_words_C)
shuffle(magic_words_I)
shuffle(secular_words_C)
shuffle(secular_words_I)

block_names_list = ["religious_congruent", "religious_incongruent", "magic_congruent", "magic_incongruent", "secular_congruent", "secular_incongruent"]

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
    'intructions_religious': [
        u"Instrucciones bloque palabras religiosas:",
        " ",
        u"A continuación se presentará una secuencia de pares de palabras religiosas.",
        u" ",
        u"En algunas ocasiones le preguntaremos si una letra específica es parte o no de la última palabra observada.",
        " ",
        u"Cuando estés listo presione la barra espaciadora.",
        " "
        ],
    'intructions_magic': [
        u"Instrucciones bloque palabras mágicas:",
        " ",
        u"A continuación se presentará una secuencia de pares de palabras mágicas.",
        u" ",
        u"En algunas ocasiones le preguntaremos si una letra específica es parte o no de la última palabra observada.",
        " ",
        u"Cuando estés listo presione la barra espaciadora.",
        " "
        ],
    'intructions_secular': [
        u"Instrucciones bloque palabras seculares:",
        " ",
        u"A continuación se presentará una secuencia de pares de palabras seculares.",
        u" ",
        u"En algunas ocasiones le preguntaremos si una letra específica es parte o no de la última palabra observada.",
        " ",
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

# EEG Functions
## Functions:

def init_lpt(address):
    """Creates and tests a parallell port"""
    try:
        from ctypes import windll
        global io
        io = windll.dlportio  # requires dlportio.dll !!!
        #dll_name = "DLPortIO.dll"
        #dirname = os.path.dirname(sys.argv[0])
        #dll_dir = (dirname + "\\media\\dlportio-32\\" + dll_name)
        #print(dll_dir)
        #io = windll.LoadLibrary(dll_dir)
        print('Parallel port opened')
    except:
        pass
        print("Oops!", sys.exc_info(), "occurred.")
        print('The parallel port couldn\'t be opened')
    try:
        io.DlPortWritePortUchar(address, 0)
        print('Parallel port set to zero')
    except:
        pass
        print('Failed to send initial zero trigger!')

def send_trigger(trigger, address, latency):
    """Sends a trigger to the parallell port"""
    try:
        io.DlPortWritePortUchar(address, trigger)  # Send trigger
        pygame.time.delay(latency)  # Keep trigger pulse for some ms
        io.DlPortWritePortUchar(address, 0)  # Get back to zero after some ms
        print('Trigger ' + str(trigger) + ' sent')
    except:
        pass
        print('Failed to send trigger ' + str(trigger))

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

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

def wait_answer(key1, key2, limit_time = 0):
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
                if event.key == key1:
                    answer = "Si"
                    switch = False
                elif event.key == key2:
                    answer = "No"
                    switch = False
            if event.type == TIME_OUT_WAIT and limit_time != 0:
                if ((pygame.time.get_ticks() - tw) > limit_time):
                    switch = False
                    pygame.time.set_timer(TIME_OUT_WAIT, 0)

    return answer, (pygame.time.get_ticks() - tw)

def show_word_list(block_type, word_list, subj_name, dfile, block_number, in_word, is_question, block_names):
    """Main game"""

    last_word = ""
    question_count = 0
    for i in range(len(word_list)):
        between_words = False
        for word in word_list[i]:
            screen.fill(background)
            pygame.display.flip()

            if (between_words):
                # time between_words
                word_delay = randrange(word_delay_min, word_delay_max)

                screen.blit(fix, fixbox)
                pygame.display.update(fixbox)
                pygame.time.delay(word_delay)
                screen.fill(background)
                pygame.display.flip()
                pygame.event.clear()                    # CLEAR EVENTS
                last_word = word
                send_trigger((code_access[block_type])*100 + code_access[('incongruent' if ('incongruent' in block_names[i]) else 'congruent')]*10 + code_access["target"], lpt_address, trigger_latency)  # second word trigger
            else:
                first_word = word
                send_trigger((code_access[block_type])*100 + code_access[('incongruent' if ('incongruent' in block_names[i]) else 'congruent')]*10 + code_access["prime"], lpt_address, trigger_latency)  # first word trigger

            word_show = bigchar.render(word, True, char_color)
            wordbox   = word_show.get_rect(centerx = center[0], centery = center[1])
            word_time = randrange(word_time_min, word_time_max)
            screen.blit(word_show, wordbox)
            pygame.display.update(wordbox)
            pygame.time.delay(word_time)

            pygame.event.clear()                    # CLEAR EVENTS

            between_words = True

        if (is_question[i]):
            screen.fill(background)
            pygame.display.flip()
            pygame.time.delay(blank_before_question)

            target_word = remove_accents(last_word)

            letra = " "
            is_in_word = in_word[question_count]

            question_count += 1

            if (is_in_word):
                letra = choice(target_word)
                correct_answer = "Si"
            else:
                letra = choice(string.ascii_lowercase)
                while letra in target_word:
                    letra = choice(string.ascii_lowercase)
                correct_answer = "No"

            rise = 0
            color = char_color

            text = [u"¿Estaba la letra " + letra + u" en la última palabra que observaste?", " ", " ", u"Presione CTRL Izq para Si o CTRL Der para No"]

            screen.fill(background)
            row = center[1] - 20 * len(text)
            for line in text:
                phrasebox = pygame.Rect((resolution[0]/8, rise + 0 + row, resolution[0]*6/8, resolution[1]*5/8))
                final_lines, phrase = render_textrect(line, char,  pygame.Rect((resolution[0]/8, resolution[1]/8, resolution[0]*6/8, resolution[1]*6/8)), color, background)
                screen.blit(phrase, phrasebox)
                row += 40 * len(final_lines)
            pygame.display.flip()

            send_trigger(code_access[block_type]*100 + code_access["question_start"], lpt_address, trigger_latency)  # show question trigger

            actual_answer, r_time = wait_answer(K_LCTRL, K_RCTRL, limit_time = 0)

            if (actual_answer == "Si"):
                send_trigger(code_access[block_type]*100 + code_access["yes_answer"], lpt_address, trigger_latency)  # SI answer trigger
            else:
                send_trigger(code_access[block_type]*100 + code_access["no_answer"], lpt_address, trigger_latency)  # NO answer trigger

            is_correct = (actual_answer == correct_answer)

            if (is_correct):
                send_trigger(code_access[block_type]*100 + code_access["correct_answer"], lpt_address, trigger_latency)  # correct answer trigger
            else:
                send_trigger(code_access[block_type]*100 + code_access["wrong_answer"], lpt_address, trigger_latency)  # wrong answer trigger

        else:
            letra = ""
            r_time = ""
            actual_answer = ""
            correct_answer = ""
            is_correct = ""

        if dfile != None:
            dfile.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (subj_name, block_names[i], unicodedata.normalize('NFKD', first_word).encode('ascii', 'ignore'), unicodedata.normalize('NFKD', last_word).encode('ascii', 'ignore'), letra, str(r_time), actual_answer, correct_answer, is_correct))

        blank_time = randrange(blank_time_min, blank_time_max)
        screen.fill(background)
        pygame.display.flip()
        pygame.time.delay(blank_time)

    pygame.event.clear()                    # CLEAR EVENTS

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

    init_lpt(lpt_address)

    # Si no existe la carpeta data se crea
    if not os.path.exists('data/'):
        os.makedirs('data/')

    subj_name = raw_input("Escriba un nombre de archivo y presione ENTER para iniciar: ")
    csv_name  = join('data', date_name + '_' + subj_name + '.csv')
    dfile = open(csv_name, 'w')
    dfile.write("ID,BlockName,FirstWord,SecondWord,Character,Rt,Answer,CorrectAnswer,isCorrect\n")
    init()

    send_trigger(start_trigger, lpt_address, trigger_latency)  # start EEG recording

    slide(slides['welcome1'] , False , K_SPACE)

    actual_block = 1

    words_list = [religion_words_C, religion_words_I, magic_words_C, magic_words_I, secular_words_C, secular_words_I]

    blocks = len(words_list) / 2

    intructions_list = ["intructions_religious", "intructions_magic", "intructions_secular"]

    for i in range (blocks):

        slide(slides[intructions_list[i]] , False , K_SPACE)

        # letra está dentro de la palabra?
        in_word = [True] * 15 + [False] * 15
        # Este conjunto tiene pregunta?
        is_question = [True] * 30 + [False] * 30

        block_names = [block_names_list[i]] * 60 + [block_names_list[i+1]] * 60

        shuffle(is_question)
        is_question_block = is_question
        shuffle(is_question)
        is_question_block += is_question

        shuffle(in_word)
        in_word_temp = in_word
        shuffle(in_word)
        in_word_temp += in_word

        in_word_block = []

        cont = 0
        # Se hace la conexión con in_word para las is_question
        for actual_is_question in is_question:
            if (actual_is_question):
                in_word_block.append(in_word_temp[cont])
                cont+=1
            else:
                in_word_block.append("to_delete")

        actual_words_list = words_list[i*2] + words_list[(i*2) + 1]

        temp = list(zip(is_question_block, actual_words_list, in_word_block, block_names))
        random.shuffle(temp)
        is_question_block, actual_words_list, in_word_block, block_names = zip(*temp)

        is_question_block = list(is_question_block)
        actual_words_list = list(actual_words_list)
        in_word_block = list (in_word_block)
        block_names = list (block_names)

        try:
            while True:
                in_word_block.remove("to_delete")
        except ValueError:
            pass

        if i == 0:
            block_type = "religious"
        elif i == 1:
            block_type = "magic"
        else:
            block_type = "secular"

        show_word_list(block_type, actual_words_list, subj_name, dfile, actual_block, in_word_block, is_question_block, block_names)

        screen.fill(background)
        pygame.display.flip()

        block_text = "Fin del bloque número " + str(actual_block)
        intermission_text = [block_text.decode('utf-8'), ""]
        slide(intermission_text, True , K_SPACE)

        actual_block += 1

    dfile.close()
    pygame.time.delay(blank_time_max)
    slide(slides['farewell'], True , K_SPACE)
    send_trigger(stop_trigger, lpt_address, trigger_latency)  # stop EEG recording
    ends()

## Experiment starts here...
if __name__ == "__main__":
    main()
