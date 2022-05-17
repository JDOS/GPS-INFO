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


class MainApplication(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.PastaEntrada = PATH + '\\INPUT'
		self.PastaSaida =  PATH + '\\OUTPUT'

		self.lbentrada = tk.Label(self, text= self.PastaEntrada, fg='red')
		self.lbentrada.pack(pady=10,padx=10)

		self.lbsaida = tk.Label(self, text="Pasta de Saida: " + self.PastaSaida )
		#self.lbsaida.pack(pady=10,padx=10)

		btnFind = tk.Button(self, text="Pasta de Entrada", command=self.getFolderPath)
		btnFind.pack()
		
		self.canvas = tk.Canvas(width=200, height=200)
		self.canvas.pack(expand=False, fill=None)

		self.lbstatus = tk.Text(self, height= 5, width = 50, bg='black', fg='white')
		self.lbstatus.pack(pady=10,padx=10)
		
		self.lbImage = tk.Label(self)
		self.pack()

		start = tk.Button(self, text="Mudar Datas",command=self.start)
		start.pack()

		notequals = tk.Button(self, text="Ver Erros",command=self.getNotEqual)
		notequals.pack()

	def status(self, text):
		for l in text:
			self.lbstatus.configure(state='normal')
			self.lbstatus.insert(tk.END,l + '\n')
			self.lbstatus.configure(state='disable')

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

 
	def getNotEqual(self):
		paths = []
		for root, dirs, files in os.walk(self.PastaEntrada):
			for d in dirs:
				print(root + d)		
				paths.append(os.path.join(root, d))

		erros=[]
		for p in paths:
			for p in paths:
				print(p)
				for filename in glob.glob(p + '//*.JPG'): 
					foto = Exif(filename)

					self.showImage(filename)
					self.update()

					if(foto.data != foto.set_file_modification_format()):
						erros.append(p+'/'+filename)
						self.status([p+'/'+filename])
						self.update()

		print(erros)

	def start(self):
		paths = []
		for root, dirs, files in os.walk(self.PastaEntrada):
			for d in dirs:
				print(root + d)		
				paths.append(os.path.join(root, d))

		for p in paths:
			print(p)
			for filename in glob.glob(p + '//*.JPG'): 

				gps_flag = True

				foto = Exif(filename)
				print("Open foto: ",foto.nome)
				print("Open foto: ",foto.set_file_modification())

				if(foto.gps==''):
					print('Não Possui GPS')
					gps_flag = False
				else:
					print("GPS: ",foto.gps)


				self.showImage(filename)
				self.update()

				self.status([foto.nome, 'Tirada em: ' + foto.data + ' ' + foto.hora, 'Data de Modificação: ' + foto.set_file_modification(),''])


				exif_dict = piexif.load(filename, key_is_name=False)

				
				EXE = PATH + '/tools/exiftool.exe' + ' -FileModifyDate="'+foto.set_file_modification() + '" ' + ' -FileCreateDate="' + foto.set_file_modification() + '" ' + '"' + filename + '"'

				#EXE1  = PATH + '/tools/exiftool.exe' + ' -FileModifyDate="'+foto.set_file_modification()+'" ' + '"' + filename + '"'
				#EXE2  = PATH + '/tools/exiftool.exe' + ' -FileCreateDate="'+foto.set_file_modification()+'" ' + '"' + filename + '"'

				try:
					if str(exif_dict['0th'][piexif.ImageIFD.DateTime]) != '':
						print(str(exif_dict['0th'][piexif.ImageIFD.DateTime]) + ' -> ' + foto.set_file_modification())
						exif_dict['0th'][piexif.ImageIFD.DateTime]          = foto.set_file_modification()
				except:
					print("DATA TIME - Não encontrado")

				try:
					if str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]) != '':
						print(str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]) + ' -> ' + foto.set_file_modification())
						exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]  = foto.set_file_modification()
				except:
					print("DATA TIME Original Não encontrado")

				try:
					if str(exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized]) != '':
						print(str(exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized]) + ' -> ' + foto.set_file_modification())
						exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = foto.set_file_modification()
				except:
					print("DATA TIME Digitized - Não encontrado")

				try:
					if gps_flag == True:
						print(str(exif_dict['GPS'][piexif.GPSIFD.GPSDateStamp])  + ' -> ' + foto.set_file_modification()[:-8])
						exif_dict['GPS'][piexif.GPSIFD.GPSDateStamp]        = foto.set_file_modification()
				except:
					print("Erro ao escrever o GPS TIME")
					
				self.update()

				
				try:
					print(foto.set_file_modification() + ' ' + foto.data)
					print(str(exif_dict['0th'][piexif.ImageIFD.DateTime]) + ' -> ' + foto.set_file_modification())
				except:
					print("Não foi possivel ler o EXIF ")
				

				try:
					exif_dict['0th'][piexif.ImageIFD.DateTime]          = foto.set_file_modification()
					exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal]  = foto.set_file_modification()
					
				except:
					print("Erro para outras datas...")
				#

				try:
					exif_bytes = piexif.dump(exif_dict)
					img = Image.open(filename)
					img.save(filename, exif=exif_bytes)
				except:
					print("Erro ao gravar Exif")

				print ("Executando: ",EXE)
				try:
					process = subprocess.Popen(EXE, shell=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
					for output in process.stdout:
						print(output)
				except:
					print("ERRO NA EXECUÇÂO")

				#print ("Executando: ",EXE2)


				#try:
				#	process = subprocess.Popen(EXE2, shell=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
				#	for output in process.stdout:
				#		print(output)
				#except:
				#	print("ERRO NA EXECUÇÂO")



				self.showImage(filename)
				self.update()





if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()