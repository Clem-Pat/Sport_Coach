
def upgrade_pip():
    import pip
    pip.main(['install', '--upgrade', 'pip'])

def install_and_import(package):
    import importlib
    try:
        surname = importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        surname = importlib.import_module(package)
    return surname

# upgrade_pip()

wheel = install_and_import('wheel')
tk = install_and_import('tkinter')
np = install_and_import('numpy')
matplotlib = install_and_import('matplotlib')
plt = install_and_import('matplotlib.pyplot')
pynput = install_and_import('pynput')
try:
    PIL = install_and_import('Pillow')
except:
    PIL = install_and_import('PIL')


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
import time
import datetime
import os
import inspect
from pynput.keyboard import Key
from pynput.keyboard import Controller as key_Controller
from pynput.mouse import Button
from pynput.mouse import Controller as mouse_Controller
from statistics import mean
from PIL import ImageTk
from PIL import Image as pilImage


from Window import tkinterWindow as Window


class tkinterButton(tk.Button):
    """Créer les boutons de commande"""

    def __init__(self, id, application):
        tk.Button.__init__(self, application.fen)
        self.parent = application
        self.id = id
        if application.name == 'fen':
            if self.id == 0:
                self.x, self.y = 150, 330
                self.bg, self.fg, self.cursor = 'blue', 'black', 'hand2'
                self.config(text="C'est parti", width=10, height=1, bg=self.bg, fg=self.fg, font="Arial 15 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.enter)
                self.bind('<Return>', self.enter)

        if application.name == 'main':
            if self.id in range(0,4):
                self.x, self.y = 680, 200+self.id*50
                self.bg, self.fg, self.cursor = 'blue', 'black', 'hand2'
                self.config(text="+ {}".format(5*(self.id)**(2)+5), width=5, height=1, bg=self.bg, fg=self.fg, font="Arial 15 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.plus)
                self.bind('<Return>', self.plus)

            elif self.id == 4 :
                self.x, self.y = 500, 350

                self.bg, self.fg, self.cursor = 'red', 'black', 'hand2'
                self.config(text="Stop", width=10, height=1, bg=self.bg, fg=self.fg, font="Arial 15 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.stop)

            elif self.id == 5:
                #boutton pour accéder aux SETTINGS
                self.voisin = 5 #5, 10, 25 ou 50 (les bouttons '+')
                self.bg, self.fg, self.cursor = 'light blue', 'black', 'hand2'
                self.config(text=u'\u2699', bg=self.bg, relief=tk.FLAT, cursor=self.cursor,
                            fg=self.fg, width=2, font='Arial 12 bold', command=self.settings)
                self.x, self.y = 770, 204 + int(round(1.2739*np.log(self.voisin)-2.01707))

        if application.name == 'settings':
            if self.id == 0:
                self.x, self.y = 183, 270
                self.bg, self.fg, self.cursor = 'blue', 'black', 'hand2'
                self.config(text="C'est parti", width=10, height=1, bg=self.bg, fg=self.fg, font="Arial 15 bold",
                            relief=tk.RAISED, cursor=self.cursor, command=self.enter)
                self.bind('<Return>', self.enter)


    def enter(self, *args):
        self.parent.fen.destroy()
        if self.parent.name == 'fen':
            main()

    def plus(self, *args):
        global t_rep, nbre_serie_repetitions, nbre_repetition_par_serie, nbre_total_repetitions, L_Canvas, historique_serie_actuelle, t_serie_actuelle,L_plots

        nbre_total_repetitions += int(5*(self.id)**(2)+5)
        nbre_serie_repetitions += int(5*(self.id)**(2)+5)

        comparer() #pour savoir si on est en retard

        L_Canvas[1].itemconfig(L_Canvas[1].texts['nbre_total_repetitions'], text="{}".format(int(nbre_total_repetitions)))
        L_Canvas[2].itemconfig(L_Canvas[2].texts['nbre_serie_repetitions'], text="{}".format(int(nbre_serie_repetitions)))

        t_rep = int(time.time() - t_rep)  #t_rep est alors en secondes
        historique_serie_actuelle[nbre_serie_repetitions] = t_rep
        tracer_diagramme()

        if nbre_serie_repetitions >= nbre_repetition_par_serie:
            fin_de_serie()

        t_rep = time.time()

    def stop(self):
        global running, app
        running = False
        app.fen.destroy()

    def settings(self):
        global shortcut
        app_settings = Window('settings')

        L_Buttons_settings = create_L_Buttons(app_settings)
        L_Canvas_settings = create_L_Canvas(app_settings)
        L_Entry_settings = create_L_Entry(app_settings)
        L_Labels_settings = create_L_Labels(app_settings)
        L_plots_settings = create_L_plots(app_settings)

        placer_objets(L_Buttons_settings, L_Canvas_settings, L_Entry_settings, L_Labels_settings, L_plots_settings)
        mouse = mouse_Controller()

        run = True
        n_boucle = 0
        while run == True:
            if n_boucle < 5:
                n_boucle += 1

            shortcut = L_Entry_settings[0].value

            if n_boucle == 2:
                mouse.position = (785, 345)
                mouse.click(Button.left, 2)

            try:
                app_settings.fen.update()
            except:
                run = False


class tkinterEntry(tk.Entry):
    """boîtes d'entrée de texte pour consigne"""

    def __init__(self, id, application):
        tk.Entry.__init__(self, application.fen)

        self.value = 0
        self.id = id


        if application.name == 'fen':
            if self.id == 0:
                self.value = 500
                self.config(width=5, font='Arial 15')
                self.x, self.y = 60, 100
                self.insert(0, self.value)

            elif self.id == 1:
                self.value = 00
                self.config(width=2, font='Arial 15')
                self.x, self.y = 265, 100
                self.insert(0, str(self.value).zfill(2))

            elif self.id == 2:
                self.value = 25
                self.config(width=2, font='Arial 15', fg='black')
                self.x, self.y = 305, 100
                self.insert(0, str(self.value).zfill(2))

            elif self.id == 3:
                self.value = 00
                self.config(width=2, font='Arial 15', fg='black')
                self.x, self.y = 345, 100
                self.insert(0, str(self.value).zfill(2))

            elif self.id == 4:
                self.value = 20
                self.config(width=5, font='Arial 15', fg='black')
                self.x, self.y = 325, 160
                self.insert(0, self.value)

            elif self.id == 5:
                self.value = 'pompes'
                self.config(width=9, font='Arial 13', fg='black')
                self.x, self.y = 307, 220
                self.insert(0, self.value)

            elif self.id == 6:
                self.value = 'Séance_1'
                self.config(width=9, font='Arial 13', fg='black')
                self.x, self.y = 307, 280
                self.insert(0, self.value)

        elif application.name == 'settings':
            if self.id == 0:
                self.value = shortcut
                self.config(width=5, font='Arial 15')
                self.x, self.y = 340, 150
                self.insert(0, self.value)

        self.bind('<Return>', self.enter)


    def enter(self, state):

        if self.id in range(5):
            try:  # l'exception sert à ignorer si l'utilisateur entre une valeur absurde.
                self.value = int(self.get())
                if self.id == 1 or self.id == 2 or self.id == 3:
                    self.insert(0, str(int(self.value)).zfill(2))
                self.config(fg='green', font='Arial 15 bold')
                keyboard = key_Controller()
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)
            except:
                self.delete(0, tk.END)

        elif self.id == 5 or self.id == 6:
            self.value = str(self.get())
            self.config(fg='green', font='Arial 13 bold')
            keyboard = key_Controller()
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)


class tkinterLabel(tk.Label):

    def __init__(self, id, application):

        tk.Label.__init__(self, application.fen)
        self.id = id

        if application.name == 'fen':
            if self.id == 0:
                self.config(text='Choisis ton objectif', bg='light blue',
                            fg='blue', width=20, font='Arial 20 bold')
                self.x, self.y = 40, 20
            elif self.id == 1:
                self.config(text='pompes en', bg='light blue',
                            fg='black', font='Arial 15 bold')
                self.x, self.y = 135, 100
            elif self.id == 2 or self.id == 3:
                self.config(text=':', bg='light blue',
                            fg='black', font='Arial 15 bold')
                self.x, self.y = 290+(self.id-2)*40, 100
            elif self.id == 4:
                self.config(text='Nombre de pompes par série :', bg='light blue',
                            fg='black', font='Arial 13 bold')
                self.x, self.y = 35, 160
            elif self.id == 5:
                self.config(text="Aujourd'hui tu fais des : ", bg='light blue',
                fg='black', font='Arial 13 bold')
                self.x, self.y = 50, 220
            elif self.id == 6:
                self.config(text='Enregistrer les résultats sous : ', bg='light blue',
                            fg='black', font='Arial 13 bold')
                self.x, self.y = 30, 280
            elif self.id == 7:
                today = datetime.datetime.today()
                self.config(text='_pompes_{}_{}_{}.png'.format(today.day, today.month, today.year), bg='light blue', fg='black', font='Arial 8')
                self.x, self.y = 300, 305

        elif application.name == 'main':
            if self.id == 0:
                self.config(text='Objectif : {} {} en {}'.format(objectif_repetitions, type_repetition, objectif_temps_chrono), bg='light blue',
                            fg='blue', width=30, font='Arial 20 bold')
                self.x, self.y = 150, 50

        elif application.name == 'settings':
            if self.id == 0:
                self.config(text='Choisis ton shortcut', bg='light blue',
                            fg='blue', width=20, font='Arial 20 bold')
                self.x, self.y = 77, 40
            elif self.id == 1:
                self.config(text='En appuyant sur espace, je veux ajouter', bg='light blue',
                            fg='black', font='Arial 13 bold')
                self.x, self.y = 5, 150
            elif self.id == 2:
                self.config(text='{}'.format(type_repetition), bg='light blue',
                            fg='black', font='Arial 13 bold')
                self.x, self.y = 415, 150


class tkinterCanvas(tk.Canvas):
    """Console d'affichage"""

    def __init__(self, id, application):
        tk.Canvas.__init__(self, application.fen)
        self.id = id

        if self.id == 0:

            self.config(bg="white", height=200, width=300, relief='raised')
            self.x, self.y = 100, 200

            self.texts = {}
            self.texts['{}e_serie'.format(1)] = self.create_text(80, 20, text="{}e série de {} :".format(1, nbre_repetition_par_serie),
                                              font="GROBOLD.ttf 10 italic bold", fill="black")

            self.times = {}
            self.times['t{}e_serie'.format(1)] = self.create_text(200, 20, text="{}".format(t_serie_actuelle),
                                              font="GROBOLD.ttf 10 italic bold", fill="black")

            self.lines = []
            self.lines.append(self.create_line(20, 40, 280, 40))

        elif self.id == 1:
            self.config(bg="white", height=40, width=140, relief='raised')
            self.x, self.y = 495, 200

            self.texts = {}
            self.texts['total'] = self.create_text(45, 20, text="TOTAL :",
                                              font="Arial 14 italic bold", fill="black")
            self.texts['nbre_total_repetitions'] = self.create_text(110, 20, text="{}".format(int(nbre_total_repetitions)),
                                              font="Arial 15 italic bold", fill="black")
            self.texts['nbre_total_repetitions_objectif'] = self.create_text(110, 35, text="{}".format(int(nbre_total_repetitions_objectif)),
                                              font="Arial 8 italic bold", fill="black")

        elif self.id == 2:
            self.config(bg="white", height=40, width=140, relief='raised')
            self.x, self.y = 495, 270

            self.texts = {}
            self.texts['serie_actuelle'] = self.create_text(50, 20, text="Dans la série :",
                                              font="Arial 10 italic bold", fill="black")
            self.texts['nbre_serie_repetitions'] = self.create_text(120, 20, text="{}".format(nbre_serie_repetitions),
                                              font="Arial 15 italic bold", fill="black")
            self.texts['nbre_repetition_par_serie'] = self.create_text(130, 35, text="/{}".format(int(nbre_repetition_par_serie)),
                                              font="Arial 8 italic bold", fill="black")

        elif self.id == 3:
            self.config(bg="white", height=70, width=200, relief='raised')
            self.x, self.y = 540, 435

            self.texts = {}
            self.texts['t_serie_actuelle'] = self.create_text(100, 30, text="{}".format(t_serie_actuelle),
                                              font="Arial 30 italic bold", fill="black")
            self.texts['serie_actuelle'] = self.create_text(165, 60, text="Cette série",
                                              font="Arial 8 italic bold", fill="black")

        elif self.id == 4:
            self.config(bg="white", height=70, width=200, relief='raised')
            self.x, self.y = 540, 545

            self.texts = {}
            self.texts['t_tot'] = self.create_text(100, 30, text="{}".format(t_tot),
                                              font="Arial 30 italic bold", fill="black")
            self.texts['total'] = self.create_text(180, 60, text="Total",
                                              font="Arial 8 italic bold", fill="black")


class tkinterPlot():

    def __init__(self, id, application, new_x_ax=[], new_y_ax=[], old_x_ax=[], old_y_ax=[]):
        self.id = id

        if self.id == 0:
            self.x, self.y = 100, 435

            self.fig = Figure(figsize=(4, 2), dpi=96)
            self.ax = self.fig.add_subplot(111)
            self.ax.plot(old_x_ax, old_y_ax, color='orange', label='évolution précédente', marker="+", ls='-')
            self.ax.plot(new_x_ax, new_y_ax, color='blue', label='évolution actuelle', marker="+", ls='-')
            self.ax.legend(loc='best', shadow=True, fontsize='xx-small', markerscale=0.4)
            self.ax.set(ylabel='temps (s)')

            self.graph = FigureCanvasTkAgg(self.fig, master=application.fen)
            self.canvas = self.graph.get_tk_widget()


def plot_results():
    global L_t_serie_sec, objectif_temps_sec, objectif_temps_chrono, objectif_repetitions, nbre_total_repetitions, nbre_repetition_par_serie, nom_fichier, type_repetition

    L_t_serie_sec = [] #transformer L_t_serie = ['00:01:37','00,02,34'] en L_t_serie_sec = [97,154]
    for t in L_t_serie:
        t_list=list(t)
        L_t_serie_sec.append(int(t_list[7])+10*int(t_list[6])+60*(int(t_list[4])+10*int(t_list[3]))+3600*(int(t_list[1])+10*int(t_list[0])))

    today = datetime.datetime.today()
    mois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembtre", "Octobre", "Novembre", "Décembre"]

    plt.figure(nom_fichier + '_{}_{}-{}-{}.png'.format(type_repetition, today.day, today.month, today.year)) #changer le titre de la fenêtre
    plt.plot(range(1,len(L_t_serie_sec)+1), L_t_serie_sec, color='red', marker="+",ls='-')


    #calcul de la moyenne des durées :
    if L_t_serie_sec != []:
        moy_sec = mean(L_t_serie_sec)
        temps_tuple = time.gmtime(moy_sec)
        moy = time.strftime("%H:%M:%S", temps_tuple)
    else:
        moy = '###'


    #afficher le titre :
    plt.title(str(today.day) + " " + str(mois[time.localtime()[1]-1]) + " " + str(today.year) + "\nObjectif : "+str(int(objectif_repetitions))+" "+str(type_repetition)+" en "+str(objectif_temps_chrono) + "\nNombre de "+str(type_repetition)+" réalisé(e)s : "+str(int(nbre_total_repetitions))+" en "+str(t_tot)+ "\nTemps moyen pour une série de "+str(int(nbre_repetition_par_serie))+" "+str(type_repetition)+" : "+str(moy), fontsize=10)


    plt.xlabel('numéro de la série')
    plt.ylabel('durée de la série (sec)')

    plt.locator_params(axis="both", integer=True, tight=True) #faire en sorte qu'il n'y ait que des entiers sur les axes


    # afficher le nom des points :
    for i in range(len(L_t_serie_sec)):
        plt.text(i+1, L_t_serie_sec[i], 'série {} : {}'.format(i+1,L_t_serie[i]))


    #placer la fenêtre en (0,0) sur l'écran
    thismanager = plt.get_current_fig_manager()
    thismanager.window.wm_geometry("+0+0")


    #Agrandir la figure :
    figure = plt.gcf()
    figure.set_size_inches(12.5, 6.5)


    newpath = path + '/{}_{}_{}/'.format(today.day, today.month, today.year)
    if not os.path.exists(newpath):
        os.makedirs(newpath)


    if nom_fichier == 'test':
        plt.savefig(newpath + nom_fichier + '_{}_{}-{}-{}.png'.format(type_repetition, today.day, today.month, today.year), dpi=600) #Ajouter la date au nom d'enregistrement
    else:
        if not os.path.exists(newpath + nom_fichier + '_{}_{}-{}-{}.png'.format(type_repetition, today.day, today.month, today.year)):
            plt.savefig(newpath + nom_fichier + '_{}_{}-{}-{}.png'.format(type_repetition, today.day, today.month, today.year), dpi=600) #si le fichier n'existe pas sous ce nom, on l'enregistre à ce nom
        else:
            for i in range(2,10):
                if not os.path.exists(newpath + nom_fichier + '_{}_{}-{}-{} ({}).png'.format(type_repetition, today.day, today.month, today.year,i)):
                    plt.savefig(newpath + nom_fichier + '_{}_{}-{}-{} ({}).png'.format(type_repetition, today.day, today.month, today.year,i), dpi=600) #Sinon, on rajoute (i) aussi grand qu'il le faut
                    break

    plt.show()


def comparer():
    global app, nbre_total_repetitions, nbre_total_repetitions_objectif, L_Labels, t_modif

    t_modif = time.time()
    if nbre_total_repetitions_objectif > nbre_total_repetitions :
        app.fen.configure(bg="red")
        L_Labels[0].config(bg='red', fg='black')
        L_Buttons[5].config(bg='red')
    elif nbre_total_repetitions_objectif == nbre_total_repetitions :
        app.fen.configure(bg="light blue")
        L_Labels[0].config(bg='light blue', fg='blue')
        L_Buttons[5].config(bg='light blue')
    elif nbre_total_repetitions_objectif < nbre_total_repetitions:
        app.fen.configure(bg='lime green')
        L_Labels[0].config(bg='lime green', fg='black')
        L_Buttons[5].config(bg='lime green')


def tracer_diagramme():
    global historique_serie_actuelle, nbre_serie_repetitions, t_rep, L_plots, app

    new_x_ax = [repetition for repetition in historique_serie_actuelle.keys()]
    new_y_ax = [temps for temps in historique_serie_actuelle.values()]

    old_x_ax = [repetition for repetition in historique_serie_precedente.keys()]
    old_y_ax = [temps for temps in historique_serie_precedente.values()]

    L_plots[0] = tkinterPlot(0, app, new_x_ax=new_x_ax, new_y_ax=new_y_ax, old_x_ax=old_x_ax, old_y_ax=old_y_ax)
    L_plots[0].canvas.place(x=L_plots[0].x, y=L_plots[0].y)


def fin_de_serie():
    global L_Canvas, t1, numero_serie, nbre_serie_repetitions, historique_serie_actuelle, historique_serie_precedente, L_t_serie

    historique_serie_precedente = historique_serie_actuelle
    historique_serie_actuelle = {}
    historique_serie_actuelle[0]=0
    tracer_diagramme()
    nbre_serie_repetitions = 0
    L_t_serie.append(t_serie_actuelle)

    for i in range(1,numero_serie+1):

        (x,y) = L_Canvas[0].coords(L_Canvas[0].texts['{}e_serie'.format(i)])
        L_Canvas[0].coords(L_Canvas[0].texts['{}e_serie'.format(i)], x, y+40)

        (x,y) = L_Canvas[0].coords(L_Canvas[0].times['t{}e_serie'.format(i)])
        L_Canvas[0].coords(L_Canvas[0].times['t{}e_serie'.format(i)], x, y+40)

    numero_serie += 1
    L_Canvas[0].texts['{}e_serie'.format(numero_serie)] = L_Canvas[0].create_text(80, 20, text="{}e série de {} :".format(numero_serie, nbre_repetition_par_serie),
                                            font="GROBOLD.ttf 10 italic bold", fill="black")
    L_Canvas[0].times['t{}e_serie'.format(numero_serie)] = L_Canvas[0].create_text(200, 20, text="{}".format(t_serie_actuelle),
                                      font="GROBOLD.ttf 10 italic bold", fill="black")

    (x,y) = L_Canvas[0].coords(L_Canvas[0].texts['{}e_serie'.format(1)])
    L_Canvas[0].lines.append(L_Canvas[0].create_line(20, y+20, 280, y+20))

    t1 = time.time()


def plus_shortcut(state):
    global shortcut, t_rep, nbre_serie_repetitions, nbre_repetition_par_serie, nbre_total_repetitions, L_Canvas, historique_serie_actuelle, t_serie_actuelle,L_plots

    nbre_total_repetitions += int(shortcut)
    nbre_serie_repetitions += int(shortcut)

    comparer() #pour savoir si on est en retard

    L_Canvas[1].itemconfig(L_Canvas[1].texts['nbre_total_repetitions'], text="{}".format(int(nbre_total_repetitions)))
    L_Canvas[2].itemconfig(L_Canvas[2].texts['nbre_serie_repetitions'], text="{}".format(int(nbre_serie_repetitions)))

    t_rep = int(time.time() - t_rep)  #t_rep est alors en secondes
    historique_serie_actuelle[nbre_serie_repetitions] = t_rep
    tracer_diagramme()

    if nbre_serie_repetitions >= nbre_repetition_par_serie:
        fin_de_serie()

    t_rep = time.time()


def create_L_plots(application):
    L = []
    if application.name == 'fen':
        nbr_elemts = 0
    elif application.name == 'main':
        nbr_elemts = 1
    elif application.name == 'settings':
        nbr_elemts = 0

    for i in range(nbr_elemts):
        L.append(tkinterPlot(i, application))
    return L


def create_L_Buttons(application):
    L = []
    if application.name == 'fen':
        nbr_elemts = 1
    elif application.name == 'main':
        nbr_elemts = 6
    elif application.name == 'settings':
        nbr_elemts = 1

    for i in range(nbr_elemts):
        L.append(tkinterButton(i, application))
    return L


def create_L_Canvas(application):
    L = []
    if application.name == 'fen':
        nbr_elemts = 0
    elif application.name == 'main':
        nbr_elemts = 5
    elif application.name == 'settings':
        nbr_elemts = 0

    for i in range(nbr_elemts):
        L.append(tkinterCanvas(i, application))
    return L


def create_L_Entry(application):
    L = []
    if application.name == 'fen':
        nbr_elemts = 7
    elif application.name == 'main':
        nbr_elemts = 0
    elif application.name == 'settings':
        nbr_elemts = 1

    for i in range(nbr_elemts):
        L.append(tkinterEntry(i, application))
    return L


def create_L_Labels(application):
    L = []
    if application.name == "fen":
        nbr_elemts = 8
    elif application.name == 'main':
        nbr_elemts = 1
    elif application.name == 'settings':
        nbr_elemts = 3

    for i in range(nbr_elemts):
        L.append(tkinterLabel(i, application))
    return L


def placer_objets(L_Buttons, L_Canvas, L_Entry, L_Labels, L_plots):

    # place all objects :

    for i in range(len(L_Labels)):
        L_Labels[i].place(x=L_Labels[i].x, y=L_Labels[i].y)

    for i in range(len(L_Canvas)):
        L_Canvas[i].place(x=L_Canvas[i].x, y=L_Canvas[i].y)

    for i in range(len(L_Entry)):
        L_Entry[i].place(x=L_Entry[i].x, y=L_Entry[i].y)

    for i in range(len(L_plots)):
        L_plots[i].canvas.place(x=L_plots[i].x, y=L_plots[i].y)

    for i in range(len(L_Buttons)):
        L_Buttons[i].place(x=L_Buttons[i].x, y=L_Buttons[i].y)


def chronometre(t0):

    t = time.time() - t0
    # Conversion en tuple (1970, 1, 1, 0, 0, 4, 3, 1, 0)
    temps_tuple = time.gmtime(t)
    # reste = t - temps_tuple[3] * 3600.0 - temps_tuple[4] * \
    #     60.0 - temps_tuple[5] * 1.0  # on récupère le reste
    # # Affiche les dixièmes et centièmes de l'arrondi
    # reste = ("%.2f" % reste)[-2::]
    tt = time.strftime("%H:%M:%S", temps_tuple)
    return tt


def definir_objectif():
    global objectif_repetitions, objectif_temps_sec, objectif_temps_chrono, nbre_repetition_par_serie, nom_fichier, type_repetition

    app1 = Window('fen')

    L_Buttons_1 = create_L_Buttons(app1)
    L_Canvas_1 = create_L_Canvas(app1)
    L_Entry_1 = create_L_Entry(app1)
    L_Labels_1 = create_L_Labels(app1)
    L_plots_1 = create_L_plots(app1)

    placer_objets(L_Buttons_1, L_Canvas_1, L_Entry_1, L_Labels_1, L_plots_1)
    # app1.fen.bind('<BackSpace>', app1.move)

    mouse = mouse_Controller()

    today = datetime.datetime.today()
    run = True
    n_boucle = 0
    while run == True:
        if n_boucle < 5:
            n_boucle += 1

        objectif_repetitions = L_Entry_1[0].value


        objectif_temps_sec = int(L_Entry_1[1].value)*3600 + int(L_Entry_1[2].value)*60 + int(L_Entry_1[3].value)
        temps_tuple = time.gmtime(objectif_temps_sec)
        objectif_temps_chrono = time.strftime("%H:%M:%S", temps_tuple) #mettre le nombre de minutes sous la forme 00:25:00

        nbre_repetition_par_serie = L_Entry_1[4].value
        type_repetition = L_Entry_1[5].value
        nom_fichier = L_Entry_1[6].value

        if n_boucle == 2:
            mouse.position = (625, 530)

        try:
            L_Labels_1[1].config(text="{} en".format(type_repetition))
            L_Labels_1[4].config(text='Nombre de {} par série :'.format(type_repetition))
            L_Labels_1[7].config(text='_{}_{}_{}_{}.png'.format(type_repetition, today.day, today.month, today.year))
            app1.fen.update()
        except:
            run = False


def main():
    global shortcut, app, path, running, numero_serie, L_t_serie, t_rep, t_serie_actuelle, t_tot, t0, t1, objectif_repetitions, nbre_repetition_par_serie, objectif_temps_chrono, objectif_temps_sec, nbre_total_repetitions, nbre_serie_repetitions, L_Buttons, L_Canvas, L_Entry, L_Labels, L_plots, historique_serie_actuelle, historique_serie_precedente, t_modif, nbre_total_repetitions_objectif, nom_fichier, type_repetition

    shortcut = 5
    numero_serie = 1
    nbre_total_repetitions = 0
    nbre_total_repetitions_objectif = 0
    nbre_serie_repetitions = 0
    L_t_serie = []
    t_tot=0
    t_serie_actuelle=0
    t_modif = 0
    t_rep = time.time()
    today = datetime.datetime.today()

    app = Window('main')
    app.fen.bind('<space>', plus_shortcut)

    app.fen.title(str(objectif_repetitions) +" "+ str(type_repetition) + " en " + str(objectif_temps_chrono) +" "+ str(today.day) +"-"+ str(today.month) +"-"+ str(today.year))


    path = str(os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0])))
    # Chemin du dossier
    historique_serie_precedente = {}
    historique_serie_actuelle = {}
    historique_serie_actuelle[0]=0

    L_Buttons = create_L_Buttons(app)
    L_Canvas = create_L_Canvas(app)
    L_Entry = create_L_Entry(app)
    L_Labels = create_L_Labels(app)
    L_plots = create_L_plots(app)


    placer_objets(L_Buttons, L_Canvas, L_Entry, L_Labels, L_plots)


    t0 = time.time()
    t1 = time.time()
    running = True
    while running == True:

        t_tot = chronometre(t0)
        t_serie_actuelle = chronometre(t1)
        nbre_total_repetitions_objectif = int(((time.time()-t0)*objectif_repetitions)//objectif_temps_sec)

        try:
            if time.time()-t_modif > 1:
                app.fen.configure(bg="light blue")
                L_Labels[0].config(bg='light blue', fg='blue')
                L_Buttons[5].config(bg='light blue')


            L_Buttons[5].voisin = shortcut
            L_Buttons[5].y = 204 + int(round(1.2739*np.log(L_Buttons[5].voisin)-2.01707))*50
            L_Buttons[5].place(x=L_Buttons[5].x, y=L_Buttons[5].y)

            L_Canvas[0].itemconfig(L_Canvas[0].times['t{}e_serie'.format(numero_serie)], text="{}".format(t_serie_actuelle))
            L_Canvas[1].itemconfig(L_Canvas[1].texts['nbre_total_repetitions_objectif'], text="{}".format(nbre_total_repetitions_objectif))
            L_Canvas[3].itemconfig(L_Canvas[3].texts['t_serie_actuelle'], text="{}".format(t_serie_actuelle))
            L_Canvas[4].itemconfig(L_Canvas[4].texts['t_tot'], text="{}".format(t_tot))

            app.fen.update()

        except: running = False

    if nbre_total_repetitions != 0:
        plot_results()


if __name__ == '__main__':
    definir_objectif()
