from tkinter import *
from words_base import Wordsbase
import sqlite3
from random import shuffle, choice

# init main window and connection to words database
# cards in db have following columns/params: oid, set name, word, definition
tk = Tk()
words_base = Wordsbase('words.db')

# define constants
pos = 0
state = 0
word = StringVar()
definition = StringVar()
shuffled = IntVar()
flashed = IntVar()
tk_set = StringVar()
# get existing sets of cards, include option 'all' sets, set first card set by default
tk_set_options = [''.join(i) for i in words_base.get_sets()] + ['all']
tk_set.set(tk_set_options[0])


def dictionary():
    ''' function to create a second window for work with cards/words'''
    def clear():
        '''function to clear entry fields '''
        etr_set.delete(0, 'end')
        etr_word.delete(0, 'end')
        etr_definition.delete(0, 'end')
        btn_edit['state'] = DISABLED
        btn_remove['state'] = DISABLED

    def submit():
        '''function to submit inserted cards info andsave it in the db '''
        new_set = etr_set.get()
        new_word = etr_word.get()
        new_def = etr_definition.get()
        # only if all fields are not empty
        if new_set and new_word and new_def:
            word_exists = int(*words_base.exists(new_word)[0])
            # add a new card to db if it doesn't exist
            if not word_exists:
                words_base.add_word(new_set, new_word, new_def)
                # create a label: notification; clear entry fields
                lbl_notif['text'] ='New word added'
                lbl_notif.after(3000, lambda: lbl_notif.config(text=''))
                clear()
            # if a word already in db, don't add
            # create a label with notification
            else:
                lbl_notif['text'] ='Word is already in cards!'
                lbl_notif.after(3000, lambda: lbl_notif.config(text=''))
        # if not all fields are filled in, create a label with notification
        else:
            lbl_notif['text'] ='Please fill in all fields'
            lbl_notif.after(3000, lambda: lbl_notif.config(text=''))

    def insert_word(event):
        '''function to insert card info in entry fields when clicking a word in words list field '''
        _ = lst_words.curselection()
        cur_word = lst_words.get(_).split('   ')[0]
        card_info = words_base.find_word(cur_word)
        clear()
        etr_set.insert(0, card_info[1])
        etr_word.insert(0, card_info[2])
        etr_definition.insert(0, card_info[3])
        # enable 'edit' and 'remove' buttons to work with a chosen card
        btn_edit.config(state=ACTIVE)
        btn_remove.config(state=ACTIVE)


    def delete_word():
        '''function to delete choosen card info from db'''
        # check if a word from entry field exists in db
        word_exists = int(*words_base.exists(etr_word.get())[0])
        # delete card info if the word exists
        if word_exists:
            words_base.delete_word(etr_word.get())
            #create widget: label with notification; clear entry fields and update words list field
            clear()
            lbl_notif['text'] ='Card is deleted'
            lbl_notif.after(3000, lambda: lbl_notif.config(text=''))
            new_window_set.set('')
        # if doesn't exist, create a label widget with notification
        else:
            lbl_notif['text'] ='Word is not in the cards'
            lbl_notif.after(3000, lambda: lbl_notif.config(text=''))

    def edit_word():
        # check if a word from entry field exists in db
        word_exists = int(*words_base.exists(etr_word.get())[0])
        # update card info if the word exists
        if word_exists:
            words_base.update_word(etr_set.get(), etr_word.get(), etr_definition.get())
            # create widget: label with notification; clear entry fields and update words list field
            clear()
            lbl_notif['text'] ='Card is successfully updated'
            lbl_notif.after(3000, lambda: lbl_notif.config(text=''))
            new_window_set.set('')
        # if doesn't exist, create a label widget with notification
        else:
            lbl_notif['text'] ='Word is not in the cards'
            lbl_notif.after(3000, lambda: lbl_notif.config(text=''))

    def show_words_list(event):
        '''function to handle mouse event and constantly update words list field '''
        # if Main window card set and Words window card set are different (user chose a new set in option menu)
        # get all cards from db and display them in words list field
        if tk_set.get() != new_window_set.get():
            new_window_set.set(tk_set.get())
            lst_words.delete(0, 'end')
            set_name = tk_set.get()
            cards = words_base.get_words(set_name)
            for word in cards:
                lst_words.insert(0, '   '.join(word[2:]))

    # var that helps to track change of a chosen card set in option menu widget
    new_window_set = StringVar()

    # init new window to work with words
    new_window = Tk()

    # create widgets: labels Set, Word and Definition, also empty label for notifications
    lbl_set = Label(new_window, text='Set', font=('Lucida Console', '12'), bg='#C9F5F6')
    lbl_word = Label(new_window, text='Word', font=('Lucida Console', '12'), bg='#C9F5F6')
    lbl_definition = Label(new_window, text='Definition', font=('Lucida Console', '12'), bg='#C9F5F6')
    lbl_notif = Label(new_window, text='', font=('Lucida Console', '10'), bg='#C9F5F6')
    # pack on the screen
    lbl_set.grid(row=0, column=0, sticky=W, pady=3, padx=5)
    lbl_word.grid(row=1, column=0, sticky=W, pady=3, padx=5)
    lbl_definition.grid(row=2, column=0, sticky=W, pady=3, padx=5)
    lbl_notif.grid(row=3, column=1, sticky='S', pady=5, padx=5)

    # create widgets: entry fields for text input for Set, Word and Definition
    etr_set = Entry(new_window, width=60)
    etr_word = Entry(new_window, width=60)
    etr_set.insert(0, 'set_1') # by default
    etr_definition = Entry(new_window, width=60)
    # pack on the screen
    etr_set.grid(row=0, column=1, ipady=4)
    etr_word.grid(row=1, column=1, ipady=4)
    etr_definition.grid(row=2, column=1, ipady=4)

    # create widgets: buttons to submit/add a word in db, clear entry fields and to finish work/close Words window
    btnsubmit = Button(new_window, text='Add', font=('Lucida Console', '12'), width=10, command=submit, bg='#E9F6F7')
    btnclear = Button(new_window, text='Clear', font=('Lucida Console', '12'), width=10, command=clear, bg='#E9F6F7')
    btn_finish = Button(new_window, text='Finish', font=('Lucida Console', '12'), width=10, command=new_window.destroy, bg='#E9F6F7')
    # pack on the screen
    btnsubmit.grid(row=0, column=2, pady=3, padx=5)
    btnclear.grid(row=1, column=2, pady=3, padx=5)
    btn_finish.grid(row=2, column=2, pady=3, padx=5)

    # create widgets: label for option menu, option menu to choose a working card set
    lbl_sets = Label(new_window, text='Choose a set', font=('Lucida Console', '12'), bg='#C9F5F6').grid(row=4, column=0, pady=3, padx=5)
    opt_sets = OptionMenu(new_window, tk_set, *tk_set_options)
    opt_sets.config(font=('Lucida Console', '12'), bg='#E9F6F7')
    opt_sets.grid(row=4, column=1, sticky='EW', pady=3, padx=5)

    # create widgets: label for listbox, listbox for displaying words and definitions of a chosen card set
    lbl_words = Label(new_window, text='Words', font=('Lucida Console', '12'), bg='#C9F5F6').grid(row=5, column=0, pady=3, padx=5)
    lst_words = Listbox(new_window, height=15, font=('Lucida Console', '10'))
    lst_words.grid(row=5, column=1, sticky='EW', pady=3, padx=5)

    # create widgets: buttons to remove/to edit a chosen word (disabled while a card is not clicked and inserted into the entry fields)
    btn_remove = Button(new_window, text='Remove', font=('Lucida Console', '12'), width=10, command=delete_word,bg='#E9F6F7',pady=3, state=DISABLED)
    btn_edit = Button(new_window, text='Edit', font=('Lucida Console', '12'), width=10, command=edit_word, bg='#E9F6F7', state=DISABLED)
    btn_remove.grid(row=4, column=2, pady=3, padx=5)
    btn_edit.grid(row=5, column=2, sticky='N', pady=3, padx=5)

    # bind mouse events: to insert card info into the entry fields and to update a words list
    lst_words.bind('<ButtonRelease-1>', insert_word)
    new_window.bind('<Enter>', show_words_list)
    lst_words.bind('<Enter>', show_words_list)

    # Word window configs
    new_window.title('Dictionary')
    new_window.geometry('640x420')
    new_window['bg'] = '#C9F5F6'


def restart():
    '''Hitting the last card in the list, suggest to restart practicing or exit app '''
    def _restart():
        ''' Helper function to set the app and widgets to its initial state'''
        global pos
        global state
        pos = 0
        state = 0
        lbl_restart.destroy()
        btn_restart.destroy()
        btn_exit.destroy()
        lbl_count.destroy()
        lbl_list.destroy()
        lbl_flash.destroy()
        word.set('')
        definition.set('')
        practice(shuffled.get())

    # create widgets: a label with message and buttons to restart and to exit
    lbl_restart = Label(tk, text='You finished your set.\nWanna start over?', font=('Lucida Console', '14'), bg='#C9F5F6')
    btn_restart = Button(tk, text='Restart', width=10, command=_restart, font=('Lucida Console', '12'), bg='#E9F6F7')
    btn_exit = Button(tk, text='Exit', width=10, command=tk.destroy, font=('Lucida Console', '12'), bg='#E9F6F7')
    btn_exit.pack(side='bottom', pady=3)
    btn_restart.pack(side='bottom', pady=3)
    lbl_restart.pack(side='bottom', pady=3)


def flash_cards(event):
    '''Show/hide a card definition on label when pressing 'Return' '''
    global pos
    # if flashed option is disabled, enable it and display a definition
    if flashed.get() == 0:
        flashed.set(1)
        def_ = cards[pos-1][3].replace(',', ',\n')
        definition.set(def_)
    # vice versa
    else:
        flashed.set(0)
        definition.set('')


def list_cards(event):
    '''List cards by index when pressing 'Space', display words on label '''
    global pos
    global state
    global lbl_count
    # clear display from prev cards
    definition.set('')
    if 0 < pos < len(cards):
        lbl_count.destroy()
    # try-except block to prevent exceeding an index range when hitting the final card
    try:
        word.set(cards[pos][2])
        # if flashed option is enabled, display a card definition
        if flashed.get() == 1:
            def_ = cards[pos][3].replace(',', ',\n')
            definition.set(def_)
    except IndexError:
        pass
    else:
        # create a widget: a label to track the current number of card of all number of cards
        lbl_count = Label(tk, text=f'word {pos+1} of {len(cards)}', font=('Lucida Console', '10'), bg='#C9F5F6')
        lbl_count.pack(side='bottom')
        # update card number
        pos += 1
        # if it's a last card, launch a restart function to suggest restart/exit
        if pos == len(cards):
            restart()

def practice(shuffled):
    '''function enables 'in progress' state '''
    global state
    global cards
    global lbl_list
    global lbl_flash
    if state == 0:
        # get a chosen card set and prepare respective cards       
        set_name = tk_set.get()
        cards = words_base.get_words(set_name)
        # if an option 'shuffle cards' is enabled, shuffle cards
        if shuffled:
            shuffle(cards)

        # create widgets: labels with instructions
        lbl_list = Label(tk, text='Press Space to list words', font=('Lucida Console', '10'), bg='#C9F5F6')
        lbl_flash = Label(tk, text='Press Enter to flash a definition', font=('Lucida Console', '10'), bg='#C9F5F6')
        lbl_list.pack(side=BOTTOM)
        lbl_flash.pack(side=BOTTOM)

        # destroy instructions in 5 secs from display
        lbl_list.after(5000, lambda: lbl_list.destroy())
        lbl_flash.after(5000, lambda: lbl_flash.destroy())

        # bind key events with functions
        tk.bind('<space>', list_cards)
        tk.bind('<Return>', flash_cards)
        # enable 'in progress' state. button 'practice' currently is not working
        state = 1

def greeting():
    ''' Get a random greeting message when launching the app '''
    greetings = ['Greetings, master!\nWanna learn Flashcards?', 
                 'What a good day for\nsome English!', 
                 'I see you wanna know\nsome English, huh?',
                 'Casual greetings to\nmy dearest friend!',
                 'Psss. I heard you learn\nEnglish. I can help',
                 'Worst practice is that\nhas never existed']

    return choice(greetings)

# main window configs
tk['bg'] = '#C9F5F6'
tk.title('Flashcards')
tk.geometry('400x600')
tk.iconbitmap('icon.ico')

# create upper widgets: a label with greeting message and buttons to practice and to open 'Words' window
lbl_hello = Label(tk, text=str(greeting()), font=('Lucida Console', '14'), bg='#C9F5F6').pack(pady=5, padx=5)
btn_learn = Button(tk, text='Practice', command=lambda: practice(shuffled.get()), font=('Lucida Console', '12'), bg='#E9F6F7')
btn_add = Button(tk, text='Words', command=dictionary, font=('Lucida Console', '12'), bg='#E9F6F7')
btn_learn.pack(fill='x', pady=1)
btn_add.pack(fill='x', pady=1)

# create medial widgets: labels to display word and definition
lbl_word = Label(tk, textvariable=word, font=('Lucida Console', '28'), bg='#C9F5F6').pack(ipady=35)
lbl_def = Label(tk, textvariable=definition, font=('Lucida Console', '18'), bg='#C9F5F6')
lbl_def.pack(ipady=35)

# create a frame for lower widgets with  app settings
frm_options = Frame(tk, relief='ridge', bd=5, bg='#E9F6F7')
frm_options.pack(side='bottom', fill='x')

# create widgets: a label 'options', checkbuttons for options 'shuffle cards' and 'flashed' mode
# and an option menu for choosing a working set of cards
lbl_options = Label(tk, text='Options', font=('Lucida Console', '12'), bg='#C9F5F6').pack(side='bottom')
Checkbutton(frm_options, text='Shuffle cards', font=('Lucida Console', '12'), variable=shuffled, onvalue=1, offvalue=0).grid(row=1,column=0, padx=3, ipadx=3)
Checkbutton(frm_options, text='Flashed', font=('Lucida Console', '12'), variable=flashed, onvalue=1, offvalue=0).grid(row=1,column=1, padx=3, ipadx=3)
opt_set = OptionMenu(frm_options, tk_set, *tk_set_options)
opt_set.config(font=('Lucida Console', '12'))
opt_set.grid(row=1, column=2, sticky='W', padx=3, ipadx=3)

# start main loop
tk.mainloop()