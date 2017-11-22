#!/usr/bin/env python3
import kivy
import requests
#import urllib2
import json
import pprint
import functools
#kivy.require('1.7.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import  ListProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListView
from functools import partial
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.core.text.markup import MarkupLabel

Builder.load_string('''
# define how clabel looks and behaves
<CLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos

<HeaderLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos
'''
)

class CLabel(ToggleButton):
    bgcolor = ListProperty([1,1,1])

class HeaderLabel(Label):
    bgcolor = ListProperty([0.108,0.476,0.611])


data_json = open('data.json')
data = json.load(data_json)

header = ['ID', 'Nome', 'Preco', 'IVA']
n_cols = len(header)
print("N_cols: " + str(n_cols))
col_size = [0.1, 0.5, 0.2, 0.2]
body_alignment = ["center", "center", "center", "center"]
#body_alignment = ["center", "left", "right", "right"]

products_list = []

counter = 0
class DataGrid(GridLayout):
    def add_row(self, row_data, row_align, cols_size, instance, **kwargs):
        print("add_row()")
        global counter
        self.rows += 1
        #self.rows = 2
        ##########################################################
        def change_on_press(self):
            childs = self.parent.children
            for ch in childs:
                if ch.id == self.id:
                    print (ch.id)
                    print (len(ch.id))
                    row_n = 0
                    if len(ch.id) == 11:
                        row_n = ch.id[4:5]
                    else:
                        row_n = ch.id[4:6]
                    for c in childs:
                        if ('row_'+str(row_n)+'_col_0') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
                        if ('row_'+str(row_n)+'_col_1') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
                        if ('row_'+str(row_n)+'_col_2') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
                        if ('row_'+str(row_n)+'_col_3') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
        def change_on_release(self):
            if self.state == "normal":
                self.state = "down"
            else:
                self.state = "normal"
        ##########################################################
        n = 0
        for item in row_data:
            cell = CLabel(text=('[color=000000]' + item + '[/color]'),
                                        background_normal="background_normal.png",
                                        background_down="background_pressed.png",
                                        halign=row_align[n],
                                        markup=True,
                                        on_press=partial(change_on_press),
                                        on_release=partial(change_on_release),
                                        text_size=(0, None),
                                        size_hint_x=cols_size[n],
                                        size_hint_y=None,
                                        height=40,
                                        id=("row_" + str(counter) + "_col_" + str(n)))
            cell_width = Window.size[0] * cell.size_hint_x
            cell.text_size=(cell_width - 30, None)
            cell.texture_update()
            self.add_widget(cell)
            n+=1
        counter += 1
        #self.rows += 1
    def remove_row(self, n_cols, instance, **kwargs):
        print("remove_row()")
        childs = self.parent.children   # DataGrid.children
        selected = 0
        for ch in childs:               # DataGrid.children[n] n = all children
            print("ch: " + str(ch))
            for c in reversed(ch.children): # DataGrid.children[n].children
                print("c: " + str(c))
                if c.id != "Header_Label":
                    print("c.id: " + str(c.id))
                    # HINT; google kivy datagrid state and find source that references kivy objects.
                    if c.state == "down":   # state can be ('normal', 'down', ...)
                        print (str(c.id) + '   -   ' + str(c.state), end='')
                        nml2 = MarkupLabel(c.text).markup
                        print(" N_cols: " + str(n_cols), end='')
                        print(" Id: " + str(c.id), end='')
                        print(" Length: " + str(len(ch.children)), end='')
                        print(" Value: " + nml2[1])
                        self.remove_widget(c)
                        #print (str(c.id) + '   -   ' + str(c.state))
                        selected += 1
        if selected == 0:   # None were found to be state='down' so delete something - the bottom row.
                            # But, interestingly, the bottom row on the screen is the first row in memory.
                            # Except that items that have .id == 'Header_Label' are the first row(s) in memory.
            for ch in childs:
                count_01 = n_cols
                count_02 = 0
                count = 0
                while (count < n_cols): # Number of columns in a row; must delete all columns in the row.
                    if n_cols != len(ch.children):
                        for c in ch.children:
                            if c.id != "Header_Label":
                                #print("Data: " + str(c.text))
                                nml2 = MarkupLabel(c.text).markup
                                #print("~m: {}".format(nml2))
                                print("N_cols: " + str(n_cols), end='')
                                print(" Count: " + str(count), end='')
                                print(" Id: " + str(c.id), end='')
                                print (" Length: " + str(len(ch.children)), end='')
                                print(" Value: " + nml2[1])

                                self.remove_widget(c) # there goes one of the columns in the row.
                                count += 1
                                break
                            else:
                                break
                    else:
                        break
        print("Done removing items.")

    def update_row(self, row_data, row_align, cols_size, instance, **kwargs):
        #def add_row(self, row_data, row_align, cols_size, instance, **kwargs):
        #def update_row(self, n_cols, instance, **kwargs):

        print("update_row()")
        doUpdate = True
        theData = {}
        childs = self.parent.children   # DataGrid.children
        selected = 0
        for ch in childs:               # DataGrid.children[n] n = all children
            print("ch: " + str(ch))
            for c in reversed(ch.children): # DataGrid.children[n].children
                print("c: " + str(c))
                if c.id != "Header_Label":
                    print("c.id: " + str(c.id))
                    # HINT; google kivy datagrid state and find source that references kivy objects.
                    if c.state == "down":   # state can be ('normal', 'down', ...)
                        print (str(c.id) + '   -   ' + str(c.state), end='')
                        nml2 = MarkupLabel(c.text).markup
                        print("A cell or column item on the selected row.", end='')
                        print(" N_cols: " + str(n_cols), end='')
                        print(" Id: " + str(c.id), end='')
                        print(" Length: " + str(len(ch.children)), end='')
                        print(" Value: " + nml2[1])
                        #self.remove_widget(c)
                        #print (str(c.id) + '   -   ' + str(c.state))
                        theData[selected] = nml2[1]  # Keep this data for update.
                        print("theData: " + str(theData))
                        selected += 1
        if selected == 0:   # None were found to be state='down' so delete something - the bottom row.
                            # But, interestingly, the bottom row on the screen is the first row in memory.
                            # Except that items that have .id == 'Header_Label' are the first row(s) in memory.
            for ch in childs:
                count_01 = n_cols
                count_02 = 0
                selected = 0
                while (selected < n_cols): # Number of columns in a row; must delete all columns in the row.
                    if n_cols != len(ch.children):
                        for c in ch.children:
                            if c.id != "Header_Label":
                                print("A cell or column item on the selected row.", end='')
                                #print("Data: " + str(c.text))
                                nml2 = MarkupLabel(c.text).markup
                                #print("~m: {}".format(nml2))
                                print("N_cols: " + str(n_cols), end='')
                                print(" Count: " + str(selected), end='')
                                print(" Id: " + str(c.id), end='')
                                print (" Length: " + str(len(ch.children)), end='')
                                print(" Value: " + nml2[1])

                                theData[selected] = nml2[1]  # Keep this data for update.
                                print("theData: " + str(theData))
                                #self.remove_widget(c) # there goes one of the columns in the row.
                                selected += 1
                                break
                            else:
                                break
                    else:
                        break
        if not doUpdate:
            # TODO; Display the error message in kivy so folks can see it.
            print("Can not doUpdate because of some previous error.")
            exit()
        print("If the data is OK then do the ENTRY and UPDATE here.")

        print("doUpdate")
        print("Data: " + str(theData))
        print("TODO; ENTRY screen")
        print("TODO; rob entry screen from add_row?")
        print("TODO; UPDATE DataGrid")
        print("TODO; UPDATE database")
        print("Done updating items.")

    def select_all(self, instance, **kwargs):
        print("select_all()")
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = "down"

    def unselect_all(self, instance, **kwargs):
        print("unselect_all()")
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = "normal"

    def show_log(self, instance, **kwargs):
        print("show_log()")
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    print (str(c.id) + '   -   ' + str(c.state) +  '   -   ' + str(c.text))

    def __init__(self, header_data, body_data, b_align, cols_size, **kwargs):
        print("__init__()")
        super(DataGrid, self).__init__(**kwargs)
        self.size_hint_y=None
        self.bind(minimum_height=self.setter('height'))
        self.cols = len(header_data)
        self.rows = len(body_data) + 1
        self.spacing = [1,1]
        n = 0
        for hcell in header_data:
            header_str = "[b]" + str(hcell) + "[/b]"
            self.add_widget(HeaderLabel(text=header_str,
                                                                    markup=True,
                                                                    size_hint_y=None,
                                                                    height=40,
                                                                    id="Header_Label",
                                                                    size_hint_x=cols_size[n]))
            n+=1

grid = DataGrid(header, data, body_alignment, col_size)
grid.rows = 10

scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x': .5, 'center_y': .5})
scroll.add_widget(grid)
scroll.do_scroll_y = True
scroll.do_scroll_x = False


###
def modal_insert(self):
    print("modal_insert()")
    lbl1 = Label(text='ID', id="lbl")
    lbl2 = Label(text='Nome', id="lbl")
    lbl3 = Label(text='Preco', id="lbl")
    lbl4 = Label(text='IVA', id="lbl")
    txt1 = TextInput(text='000', id="txtinp")
    txt2 = TextInput(text='Product Name', id="txtinp")
    txt3 = TextInput(text='123.45', id="txtinp")
    txt4 = TextInput(text='23', id="txtinp")

    insertion_grid = GridLayout(cols=2)
    insertion_grid.add_widget(lbl1)
    insertion_grid.add_widget(txt1)
    insertion_grid.add_widget(lbl2)
    insertion_grid.add_widget(txt2)
    insertion_grid.add_widget(lbl3)
    insertion_grid.add_widget(txt3)
    insertion_grid.add_widget(lbl4)
    insertion_grid.add_widget(txt4)
    # create content and assign to the view

    content = Button(text='Close me!')

    modal_layout = BoxLayout(orientation="vertical")
    modal_layout.add_widget(insertion_grid)

    def insert_def(self):
        input_list = []
        for text_inputs in reversed(self.parent.children[2].children):
            if text_inputs.id == "txtinp":
                input_list.append(text_inputs.text)
        print (input_list)
        grid.add_row(input_list, body_alignment, col_size, self)
        # def add_row(self, row_data, row_align, cols_size, instance, **kwargs):

        # print view
        # view.dismiss


    insert_btn = Button(text="Insert", on_press=insert_def)
    modal_layout.add_widget(insert_btn)
    modal_layout.add_widget(content)

    view = ModalView(auto_dismiss=False)

    view.add_widget(modal_layout)
    # bind the on_press event of the button to the dismiss function
    content.bind(on_press=view.dismiss)
    insert_btn.bind(on_release=view.dismiss)

    view.open()


def modal_update_old(self):
    print("modal_update_old()")
    #def modal_update(columnHeadings, rows):

    # How do I get this data from kivy; inside this function? drill down to the .text
    # Where are the columnHeading fields in kivy data? in cells with .id == "Header_Label".
    # grid object is present here.
    # - - - - - - - - - -
    print ("From DataGrid.remove_row(self, n_cols({}), instance, **kwargs)".format(n_cols))
    childs = grid.children
    print(str(childs))
    #childs = self.parent.children
    selected = 0    # No cells selected, yet.
    doUpdate = True
    theData = {}
    for ch in childs:
        print("ch: " + str(ch))
        for c in reversed(ch.children):
            print("c: " + str(c))
            if c.id != "Header_Label":
                print("c.id: " + str(c.id))
                if c.state == "down":
                    #print(str(c.state))
                    #print("self.remove_widget(c) was here.")
                    #self.remove_widget(c)
                    nml2 = MarkupLabel(c.text).markup
                    print(" Value: " + nml2[1])
                    print(str(c.id) + '   -   ' + str(c.state) + ' - ' + nml2[1])
                    theData[selected] = nml2[1] # Keep this data for update.
                    print("theData: " + theData)
                    selected += 1   # Another cell selected.
    if selected > 4:
        print("Only a single row may be selected for update.")
        doUpdate = False
    if selected == 0:   # If not selected, above; then pick the first row in memory which is the last row on the screen.
        print("You must select a row to be updated.")
        doUpdate = False
        #print(str(selected))
        #for ch in childs:
        #    print(str(ch))
        #    count_01 = n_cols
        #    count_02 = 0
        #    count = -1
        #    #count = 0
        #    # TODO; next 3 lines loop forever. grid.children must be the wrong object to set this to?
        #    while True:
        #        count += 1
        #        if count >= n_cols:
        #            break
        #        #while (count + + < n_cols):
        #        print(count)
        #        if n_cols != len(ch.children):
        #            for c in ch.children:
        #                print(c)
        #                if c.id != "Header_Label":
        #                    print("Length: " + str(len(ch.children)), end='')
        #                    print(" N_cols: " + str(n_cols + 1), end='')
        #
        #                    print(" self.remove_widget(c) was here.")
        #                    #self.remove_widget(c)
        #                    #count += 1
        #                    break
        #                else:
        #                    break
        #        else:
        #            break
    if not doUpdate:
        # TODO; Display the error message in kivy so folks can see it.
        print("Can not doUpdate because of some previous error.")
        exit()

    print("doUpdate")
    print("Data: " + theData)
    # - - - - - - - - - -
    columnHeadings = ['ID', 'Nome', 'Preco', 'IVA']
    # TODO; where are the product fields inside kivy data?
    rows = {1:['000', 'Product Name 1', '123.45', '23'],
            2:['001', 'Product Name 2', '234.56', '34'],
            3:['002', 'Product Name 3', '345.67', '45']
            }
    #def modal_update(self, columnHeadings, rows):
    print("modal_update {}".format(columnHeadings))
    print("{}".format(rows))
    # TODO; copied modal_insert to modal_update; now make modal_update work!
    # data should contain Column headings (labels) and Data.
    # columnHeadings = ['ID', 'Nome', 'Preco', 'IVA']
    # rows = {1:['000', 'Product Name 1', '123.45', '23'],
    #		  2:['001', 'Product Name 2', '234.56', '34']
    #		  3:['002', 'Product Name 3', '345.67', '45']
    # 			}
    # modal_update(self, columnHeadings, rows)

    # TODO; Make this variable according to the count of items in columnHeadings and rows['1']!
    elementsCH = len(columnHeadings)
    elementsR = len(rows[1]) 					# TODO; shouldn't we iterate through the selected rows?
    if elementsCH != elementsR:
        # TODO; logg or msgbox this!
        # error() inform somebody
        print("Something is wrong, the number of columnHeadings ({}) != the number of rows (())!".format(elementsCH, elementsR))
        exit()

    insertion_grid = GridLayout(cols=2)
    # TODO; Apply iteration here!
    # for elementsR:
    #	lbl? = Label(text=columnHeadings[?], id="lbl")
    #	txt? = TextInput(text=rows['?'][0], id="txtinp")
    lbl1 = Label(text=columnHeadings[0], id="lbl")
    txt1 = TextInput(text=rows[1][0], id="txtinp")
    insertion_grid.add_widget(lbl1)
    insertion_grid.add_widget(txt1)
    lbl2 = Label(text=columnHeadings[1], id="lbl")
    txt2 = TextInput(text=rows[1][1], id="txtinp")
    insertion_grid.add_widget(lbl2)
    insertion_grid.add_widget(txt2)
    lbl3 = Label(text=columnHeadings[2], id="lbl")
    txt3 = TextInput(text=rows[1][2], id="txtinp")
    insertion_grid.add_widget(lbl3)
    insertion_grid.add_widget(txt3)
    lbl4 = Label(text=columnHeadings[3], id="lbl")
    txt4 = TextInput(text=rows[1][3], id="txtinp")
    insertion_grid.add_widget(lbl4)
    insertion_grid.add_widget(txt4)
    #lbl1 = Label(text='ID', id="lbl")
    #lbl2 = Label(text='Nome', id="lbl")
    #lbl3 = Label(text='Preco', id="lbl")
    #lbl4 = Label(text='IVA', id="lbl")
    #txt1 = TextInput(text='000', id="txtinp")
    #txt2 = TextInput(text='Product Name', id="txtinp")
    #txt3 = TextInput(text='123.45', id="txtinp")
    #txt4 = TextInput(text='23', id="txtinp")

    # create content and assign to the view

    content = Button(text='Close me!')

    modal_layout = BoxLayout(orientation="vertical")
    modal_layout.add_widget(insertion_grid)

    def update_def(self):
        input_list = []
        for text_inputs in reversed(self.parent.children[2].children):
            if text_inputs.id == "txtinp":
                input_list.append(text_inputs.text)
        print (input_list)
        # TODO; how do I make this an UPDATE?
        print (input_list)
        grid.update_row(input_list, body_alignment, col_size, self)
        # def update_row(self, n_cols, instance, **kwargs):
        #grid.add_row(input_list, body_alignment, col_size, self)
        # def add_row(self, row_data, row_align, cols_size, instance, **kwargs):

    # print view
    # view.dismiss


    update_btn = Button(text="Update", on_press=update_def)
    modal_layout.add_widget(update_btn)
    modal_layout.add_widget(content)

    view = ModalView(auto_dismiss=False)

    view.add_widget(modal_layout)
    # bind the on_press event of the button to the dismiss function
    content.bind(on_press=view.dismiss)
    update_btn.bind(on_release=view.dismiss)

    view.open()


pp = partial(grid.add_row, ['001', 'Teste', '4.00', '4.00'], body_alignment, col_size)
# def add_row(self, row_data, row_align, cols_size, instance, **kwargs):
add_row_btn = Button(text="Add Row", on_press=pp)
del_row_btn = Button(text="Delete Row", on_press=partial(grid.remove_row, len(header)))

# TODO; need to lookup the selected row and give an error if not selected and pass data if selected to update.
# TODO; how do I do this without self?

ppUpdate = partial(grid.update_row, ['001', 'Teste', '4.00', '4.00'], body_alignment, col_size)


upt_row_btn = Button(text="Update Row", on_press=ppUpdate)
# def update_row(self, n_cols, instance, **kwargs):
#upt_row_btn = Button(text="Update Row", on_press=modal_update)
#ppUdate = partial(modal_update(columnHeadings, rows))
#ppUdate = partial(modal_update(columnHeadings, rows))
#upt_row_btn = Button(text="Update Row", on_press=ppUdate)
#ppUpdate = partial(grid.add_row, ['002', 'Testes', '4.10', '4.10'], body_alignment, col_size)
#upt_row_btn = Button(text="Update Row", on_press=ppUpdate)
slct_all_btn = Button(text="Select All", on_press=partial(grid.select_all))
unslct_all_btn = Button(text="Unselect All", on_press=partial(grid.unselect_all))

show_grid_log = Button(text="Show log", on_press=partial(grid.show_log))

add_custom_row = Button(text="Add Custom Row", on_press=modal_insert)

###
def json_fill(self):
    print("json_fill()")
    for d in data:
        print (d)
        grid.add_row(d, body_alignment, col_size, self)
        # def add_row(self, row_data, row_align, cols_size, instance, **kwargs):

json_fill_btn = Button(text="JSON fill", on_press=partial(json_fill))

btn_grid = BoxLayout(orientation="vertical")
btn_grid.add_widget(json_fill_btn)
btn_grid.add_widget(add_row_btn)
btn_grid.add_widget(del_row_btn)
btn_grid.add_widget(upt_row_btn)
btn_grid.add_widget(slct_all_btn)
btn_grid.add_widget(unslct_all_btn)
btn_grid.add_widget(show_grid_log)
btn_grid.add_widget(add_custom_row)

root = BoxLayout(orientation="horizontal")

root.add_widget(scroll)
root.add_widget(btn_grid)




class MainApp(App):
    def build(self):
        # grid = DataGrid(header, data, body_alignment, col_size)
        # interface = Interface()
        # print Window.size
        # return grid
        return root

if __name__=='__main__':
    MainApp().run()