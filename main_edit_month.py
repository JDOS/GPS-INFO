from exif import Exif 
import os
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageOps
from PIL import ImageTk
import piexif
from PIL.ExifTags import TAGS,  GPSTAGS

import csv
import subprocess, os
import time 

PATH = os.path.abspath(os.path.dirname(__file__))


def add_border(input_image, output_image, border):
    img = Image.open(input_image)
    if isinstance(border, int) or isinstance(border, tuple):
        bimg = ImageOps.expand(img, border=border)
    else:
        raise RuntimeError('Border is not an integer or tuple!')
    bimg.save(output_image)


def write_Image(list_text,input_file, output_file):
	img = Image.open(input_file)

	exif_dict = piexif.load(input_file, key_is_name=False)
	del exif_dict["thumbnail"]
	#del exif_dict["1st"]
	try:
		exif_bytes = piexif.dump(exif_dict)
	except:
		print("Algum erro na captação de dados da foto")
		exif_bytes =''

	draw = ImageDraw.Draw(img)
	width, height = img.size
	print("Resolução: ", str(width) + " X " + str(height))
	border = 20
	
	#ajusta a fonte de acordo com a resolução
	font_size = round(width/28)
	#Cria Fonte
	font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", font_size)
	padding = 10
	padding_data_hora = 150
	border = 20

	for idx, item in enumerate(list_text):
		w, h = font.getsize(item)
		draw.text(((width-w-padding),height-font_size*(len(list_text)-idx)-padding*(len(list_text)-idx)),item,(255,255,0), align='right', font=font)

	img = ImageOps.expand(img, border=border)

	if(exif_bytes!=''):
		img.save(output_file, exif=exif_bytes)
	else:
		img.save(output_file)
	#piexif.transplant(input_file,output_file)


def csv_Image(output_file, nome, gps_utm_info, data, hora):
	with open(output_file + '\\DATA.csv', 'a', newline='\n', encoding='utf-8') as file:
		file.write(nome + ";" + gps_utm_info[0] + ";" + gps_utm_info[1] + ";" + data + ";"+ hora)
		file.write('\n')



class MainApplication(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.PastaEntrada = PATH + '\\INPUT'
		self.PastaSaida =  PATH + '\\OUTPUT'

		self.lbentrada = tk.Label(self, text= self.PastaEntrada)
		self.lbentrada.pack(pady=10,padx=10)

		self.lbsaida = tk.Label(self, text="Pasta de Saida: " + self.PastaSaida )
		self.lbsaida.pack(pady=10,padx=10)

		self.lbstatus = tk.Label(self, text="STATUS")
		self.lbstatus.pack(pady=10,padx=10)

		btnFind = tk.Button(self, text="Pasta de Entrada", command=self.getFolderPath)
		btnFind.pack()
		
		self.edit_set = tk.IntVar()
		self.check1 = tk.Checkbutton(self, text='Edit GPS INFO',variable=self.edit_set, onvalue=1, offvalue=0)
		self.check1.pack()

		self.no_name = tk.IntVar()
		self.check2 = tk.Checkbutton(self, text='Remover Nome',variable=self.no_name, onvalue=1, offvalue=0)
		self.check2.pack()	

		self.canvas = tk.Canvas(width=200, height=200)
		self.canvas.pack(expand=False, fill=None)

		
		self.lbImage = tk.Label(self)
		self.pack()

		start = tk.Button(self, text="Criar Imagens",command=self.start)
		start.pack()

		csv_output = tk.Button(self, text="Escrever CSV",command=self.csv_output)
		csv_output.pack()
		

	def showImage(self, filename):
		img = Image.open(filename)
		img = img.resize((200, 200), Image.ANTIALIAS)
		self.canvas.image = ImageTk.PhotoImage(img)
		self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')		

	def getFolderPath(self):
		folder_selected = tk.filedialog.askdirectory()
		if(folder_selected !=''):
			self.PastaEntrada=folder_selected
			self.lbentrada["text"] = folder_selected

 
	def start(self):
		TYPES = ['.JPG','.jpg','.jpeg']

		for typ in TYPES:

			for filename in glob.glob( self.PastaEntrada + '/*' + typ): 
				foto = Exif(filename)
				output_file = self.PastaSaida + '/' + os.path.basename(filename)
				if(foto.data!=''):
					data=list(foto.data)
					data[4]=str(2)
					foto.data="".join(data)

				self.showImage(filename)
				self.update()

				print(foto.nome + ' ' +foto.get_gps_utm())


				if(foto.get_gps_utm()=='' or self.edit_set.get()==1):
					gps_utm_info = foto.get_gps_utm()
					gps_utm_info = tk.simpledialog.askstring("GPS INFO","Insira a geolocalização:", parent=self, initialvalue=gps_utm_info)
					if(gps_utm_info=='' or gps_utm_info==None):
						gps_utm_info ='UTM: Not Found'
						output_file = output_file +'not-found'+ '.'+ foto.extension

				else:
					gps_utm_info = 'UTM: ' + foto.get_gps_utm()
				
				if(foto.data==''):
					foto.data = tk.simpledialog.askstring("GPS INFO","Insira a data:", parent=self, initialvalue='')

				if(foto.hora==''):
					foto.hora = tk.simpledialog.askstring("GPS INFO","Insira a hora:", parent=self, initialvalue='')

				

				if (self.no_name.get()==1):
					write_Image([foto.hora, foto.data, gps_utm_info.rstrip()], filename, output_file)
				else:	
					write_Image([foto.hora, foto.data, foto.nome, gps_utm_info.rstrip()], filename, output_file)
				self.showImage(output_file)
				self.update()

	def csv_output(self):
		for filename in glob.glob( self.PastaEntrada + '/*.JPG'): 
			foto = Exif(filename)
			output_file = self.PastaSaida + '/' + os.path.basename(filename)

			print(foto.nome + ' ' + foto.get_gps_utm() + ' ' + foto.data + ' ' + foto.hora)

			if(foto.get_utm() == ''):
				gps_utm_info = ['-','-']

			else:
				gps_utm_info = foto.get_utm()

			csv_Image(self.PastaSaida, foto.nome, gps_utm_info, foto.data, foto.hora)

		output = self.PastaSaida + '\\DATA.csv'
		print(output)
		os.startfile(output)

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()