from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.lang import Builder
import random
from PIL import Image
import json
import os

imagedic={}
max=1
layers=[]
images= {}
not_found=True
meta_data_name="kehehe"
meta_data_des="hahaha"
active_layer=""


class MainWindow(Screen):
    folder=ObjectProperty(None)
    label=ObjectProperty(None)
    max_i=ObjectProperty(None)
    def btn(self):
        global max
        global layers
        global folderp
        folderp=self.folder.text
        for i in os.listdir(self.folder.text):
            imagedic[i] = {}
            for c in os.listdir(self.folder.text + "\\" + i):
                imagedic[i][c] = 0
        layers = list(imagedic.keys())
        print(layers)
        max=1
        for i in imagedic:
            max *= len(imagedic[i])
        s2 = self.manager.get_screen("second")
        s2.label.text=f"You can create maximum {max} png\nHow much do you want to create? "
        print(max)
    def setmax(self):
        global max
        max=int(self.max_i.text)
        print(max)
class CustomWidget(Widget):
    root_widget = ObjectProperty()
    bttn=ObjectProperty()
    save_btn=ObjectProperty()
    inputc=ObjectProperty()
    def on_press(self, **kwargs):
        self.root_widget.btn(self.bttn)
    def on_press_save(self, **kwargs):
        self.root_widget.save(self.bttn,self.inputc)
    pass
class CustomWidget2(Widget):
    root_widget=ObjectProperty()
    img=ObjectProperty()
    inputp=ObjectProperty()

    def on_pressx(self, **kwargs):
        self.root_widget.btn_save(self.img,self.inputp)



class SecondWindow(Screen):
    global max
    meta_name=ObjectProperty(None)
    meta_des=ObjectProperty(None)
    maxi=ObjectProperty(None)
    def meta(self):
        global meta_data_des
        global meta_data_name
        global max
        global layers
        meta_data_des=self.meta_des.text
        meta_data_name=self.meta_name.text
        max=int(self.maxi.text)
        s3=self.manager.get_screen("third")

        s3.layer.data=[{"button_text": i,"layer_text":str(layers.index(i)),  'root_widget': self} for i in layers]
    def btn(self,btn):
        global layers
        global active_layer
        active_layer=btn.text
        s4 = self.manager.get_screen("fourth")
        self.manager.transition.direction = "left"
        s4.layerx.data = [{"img_text": i,"layer_text":str(imagedic[btn.text][i]),"label_text":"%"+str(100*imagedic[active_layer][i]//max), 'root_widget': s4} for i in imagedic[btn.text]]
        self.manager.current = "fourth"

    def save(self,btn,inp):
        global layers
        index=layers.index(btn.text)
        layers.pop(index)
        layers.insert(int(inp.text),btn.text)
        s3=self.manager.get_screen("third")
        s3.layer.data=[{"button_text": i,"layer_text":str(layers.index(i)),  'root_widget': self} for i in layers]







class ThirdWindow(Screen):
    layer=ObjectProperty(None)
    layer_list=ObjectProperty(None)
    label=ObjectProperty(None)
    inputx=ObjectProperty(None)
    global imagedic
    global layers
    def btn2(self):
        global layers
        index=layers.index(self.label.text)
        layers.pop(index)
        layers.insert(int(self.inputx.text),self.label.text)
        s2=self.manager.get_screen("second")
        self.layer.data=[{"text": i,  'root_widget': s2} for i in layers]
    def distall(self):
        global imagedic
        global max
        k=""
        for i in imagedic:
            if max % len(imagedic[i]) == 0:
                for b in imagedic[i]:
                    imagedic[i][b] = max // len(imagedic[i])
            else:
                for b in imagedic[i]:
                    imagedic[i][b] = max // len(imagedic[i])
                    k = b
                imagedic[i][k] += max % len(imagedic[i])
    pass


class FourthWindow(Screen):
    layerx=ObjectProperty(None)
    def btn_save(self,img,inputx):
        global imagedic
        global max
        imagedic[active_layer][img.text] = int(inputx.text)
        self.layerx.data[list(imagedic[active_layer]).index(img.text)]={"img_text": img.text, "layer_text": str(imagedic[active_layer][img.text]),
                            "label_text": "%" + str(100 * imagedic[active_layer][img.text] // max), 'root_widget': self}



    def dist(self):
        global max
        k=""

        if max % len(imagedic[active_layer]) == 0:
            for b in imagedic[active_layer]:
                imagedic[active_layer][b] = max // len(imagedic[active_layer])
        else:
            for b in imagedic[active_layer]:
                imagedic[active_layer][b] = max // len(imagedic[active_layer])
                k = b
            imagedic[active_layer][k] += max % len(imagedic[active_layer])
        s4 = self.manager.get_screen("fourth")
        s4.layerx.data = [{"img_text": i, "layer_text": str(imagedic[active_layer][i]),
                            "label_text": "%" + str(100 * imagedic[active_layer][i] // max), 'root_widget': s4} for i
                           in imagedic[active_layer]]

    pass

class FifthWindow(Screen):
    folder_inp=ObjectProperty(None)
    def btn(self):
        global folderp
        global imagedic
        global layers
        global max
        folder=self.folder_inp.text
        for b in range(max):
            images[b] = []
            for i in layers:
                not_found = True
                while not_found:
                    if len(list(imagedic[i].values())) > 0:
                        trait = random.choice(list(imagedic[i].keys()))
                        if imagedic[i][trait] > 0:
                            imagedic[i][trait] -= 1
                            not_found = False
                            images[b].append(trait)

                    else:
                        break
        jsondic = {}
        for i in list(images.keys()):
            try:
                l2 = images[i]
            except KeyError:
                continue
            for b in list(images.keys()):
                l1 = images[b]
                if i != b:
                    if (l1 == l2):
                        del images[b]
        new_images={}
        for i in images:
            new_images[list(images.keys()).index(i)]=[]
            for c in images[i]:
                new_images[list(images.keys()).index(i)].append(c)
        max=len(list(new_images.keys()))
        path = os.path.join(folder, "Metadatas")
        if not os.path.isdir(path):
            os.mkdir(path)
        metadatas = []

        for b in range(max):
            jsondic["attributes"] = []
            for i in range(len(list(imagedic.keys()))):
                a = {}
                a["trait type"] = layers[i]
                a["value"] = images[b][i]
                jsondic["attributes"].append(a)
            jsondic["description"] = meta_data_des
            jsondic["edition"] = b + 1
            jsondic["name"] = f"{meta_data_name}#{b + 1}"
            metadatas.append(jsondic.copy())
            json_object = json.dumps(jsondic)
            completeName = os.path.join(path, f"{meta_data_name}#{b + 1}" + ".json")

            with open(completeName, "w") as f:
                f.write(json_object)
        all_image = []
        image_paths = []
        for i in metadatas:
            image_paths = []
            for b in i["attributes"]:
                image_path = folderp + "\\" + b["trait type"] + "\\" + b["value"]
                image_paths.append(image_path)
            all_image.append(image_paths)
        path2=os.path.join(folder, "Images")
        if not os.path.isdir(path2):
            os.mkdir(path2)
        m = 1
        for i in all_image:
            result = Image.open(i[0]).convert("RGBA")
            print(i)
            for b in range(1, len(i)):
                Img2 = Image.open(i[b]).convert("RGBA")
                result = Image.alpha_composite(result, Img2)
            print(f"{meta_data_name}#{m}.png saved")
            result.save(os.path.join(path2,f"{meta_data_name}#{m}.png"))
            result = None
            m += 1

class WindowManager(ScreenManager):
    pass

kv = Builder.load_string("""
WindowManager:
    MainWindow:
    SecondWindow:
    ThirdWindow:
    FourthWindow:
    FifthWindow:

<CustomWidget>
    inputc:inputc
    bttn:id_button
    button_text:"btn"
    layer_text:"0"
    save_btn:save_btn
    Button:
        id:id_button
        on_press:root.on_press()
        text:root.button_text
        pos:root.x, root.y
        size:(root.width*2)/5,100
        background_color : (0.5, 0.5, 0.5, 1)
        font_size : root.width/20

    TextInput:
        id:inputc
        pos:(root.width*2)/5, root.y
        text:root.layer_text
        size:(root.width*2)/5,100
        multiline:False
        font_size : root.width/20
        halign:"center"
        padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]

    Button:
        id:save_btn
        text:"Save"
        on_press:root.on_press_save()
        pos:(root.width*4)/5,root.y
        size:root.width/5,100
        background_color : (0.5, 0.5, 0.5, 1)
        font_size : root.width/20
<CustomWidget2>
    inputp:inputc
    img:id_img
    img_text:"btn"
    layer_text:"0"
    label_text:"%"
    Button:
        id:save_btn
        text:"Save"
        on_release:root.on_pressx()
        pos:(root.width*3)/4,root.y
        size:root.width/4,60
        background_color : (0.5, 0.5, 0.5, 1)
        font_size : root.width/25
    Label:
        id:id_img
        text:root.img_text
        pos:root.x, root.y
        size:root.width/2,60
        background_color : (0.5, 0.5, 0.5, 1)
        font_size : root.width/25

    TextInput:
        id:inputc
        pos:root.width/2, root.y
        text:root.layer_text
        size:root.width/8,60
        font_size : root.width/25
        halign:"center"
        padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
    Label:
        pos:(root.width*5)/8, root.y
        text:root.label_text
        size:root.width/8,60
        font_size : root.width/25
        halign:"center"




<MainWindow>
    max_i:max

    folder:folder_input
    name:"main"
    id: layout
    BoxLayout:
        orientation:"vertical"
        size: root.width, root.height
        padding:20
        BoxLayout:
            orientation:"horizontal"
            height:30
            size_hint:1,0.1

            TextInput:
                id: folder_input
                font_size:self.width//20
                multiline: False
                halign:"center"
                padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
            Button:
                text:"Chose the folder"
                font_size:self.width//20
                on_press: root.btn()
                on_release:
                    app.root.current="second"
                    root.manager.transition.direction="left"

        FileChooserIconView:
            id: chooser
            dirselect:True
            on_selection: folder_input.text = self.selection and self.selection[0] or ''




<SecondWindow>
    name:"second"
    meta_name:meta_name
    meta_des:meta_des
    maxi:max
    label:label

    BoxLayout:
        orientation:"vertical"
        size: root.width, root.height
        padding:20
        BoxLayout:
            orientation:"vertical"
            height:30
            size_hint:1,0.2

            Label:
                id: label
                text:""
                font_size:self.height//3


            TextInput:
                id: max
                multiline: False
                font_size:self.height//3
                halign:"center"
                padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        BoxLayout:
            orientation:"vertical"
            size_hint:1,0.2

            Label:

                text:"What's the collection name?"
                font_size:self.height//3
            TextInput:
                id:meta_name
                multiline: False
                font_size:self.height//3
                halign:"center"
                padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        BoxLayout:
            orientation:"vertical"
            size_hint:1,0.2

            Label:
                text:"What's the description?"
                font_size:self.height//3
            TextInput:
                id: meta_des
                multiline: False
                font_size:self.height//3
                halign:"center"
                padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]
        BoxLayout:
            orientation:"horizontal"
            height:30
            size_hint:1,0.1

            Button:
                text:"Back"
                font_size:self.width//20
                on_release:
                    app.root.current = "main"
                    root.manager.transition.direction="right"

            Button:
                text:"Next"
                font_size:self.width//20
                on_press: root.meta()
                on_release:
                    app.root.current = "third"
                    root.manager.transition.direction="left"



<ThirdWindow>
    name:"third"
    layer:layer
    BoxLayout:
        orientation:"vertical"
        size: root.width, root.height
        padding:20

        RecycleView:
            id: layer

            viewclass: 'CustomWidget'

            RecycleBoxLayout:

                default_size: None, 100
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'



        BoxLayout:
            orientation:"horizontal"
            height:30
            size_hint:1,0.1

            Button:
                text:"Back"
                font_size:self.width//10
                on_release:
                    app.root.current = "second"
                    root.manager.transition.direction="right"

            Button:
                text:"Finish"
                font_size:self.width//10
                on_release:
                    app.root.current="fifth"
                    root.manager.transition.direction="left"
            Button:
                text:"Distiribute all"
                font_size:self.width//10
                on_release: root.distall()

<FourthWindow>
    name:"fourth"
    layerx:layer



    BoxLayout:
        orientation:"vertical"
        size: root.width, root.height
        padding:20

        RecycleView:
            id: layer

            viewclass: 'CustomWidget2'

            RecycleBoxLayout:
                default_size: None, 100
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
        BoxLayout:
            orientation:"horizontal"
            height:30
            size_hint:1,0.1

            Button:
                text:"Back"
                font_size:self.width//20
                on_release:
                    app.root.current = "third"
                    root.manager.transition.direction="right"
            Button:
                text:"Distirubate equally"
                font_size:self.width//20

                on_release: root.dist()

<FifthWindow>
    name:"fifth"
    folder_inp:folder_inp
    BoxLayout:
        orientation:"vertical"
        size: root.width, root.height
        padding:20
        BoxLayout:
            orientation:"horizontal"
            height:30
            size_hint:1,0.1

            TextInput:
                id: folder_inp
                font_size:self.width//20
                multiline: False
                halign:"center"
                padding_y: [self.height / 2.0 - (self.line_height / 2.0) * len(self._lines), 0]

            Button:
                text:"Chose the folder and Create"
                font_size:self.width//20
                on_press: root.btn()


        FileChooserIconView:
            id: chooser
            dirselect:True
            on_selection: folder_inp.text = self.selection and self.selection[0] or ''
""")
class MyApp(App):
    global layers
    def build(self):
        return kv
if __name__== "__main__":
    MyApp().run()

