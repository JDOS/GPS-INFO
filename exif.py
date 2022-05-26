import subprocess, os
import datetime
import re
import utm
import os


PATH = os.path.abspath(os.path.dirname(__file__))
EXE  = PATH + '/tools/exiftool.exe'


class Exif:


	def __init__(self, input_file, **kwards):
		self.input_file = input_file
		self.metadata = self.get_dict()
		self.data = self.set_data()
		self.hora = self.set_time()
		self.gps  = self.set_gps()
		self.nome = self.set_nome()
		self.extension = self.set_extension()


	def get_dict(self):
		si = subprocess.STARTUPINFO()
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		process = subprocess.Popen([EXE, self.input_file], stdout = subprocess.PIPE, stderr=subprocess.STDOUT,startupinfo=si)

		metadata = []
		for output in process.stdout:

			info = {}
			line = output.decode("utf-8", errors='ignore').strip().split(':',1)

			info[line[0].strip()] = line[1].strip()
			metadata.append(info)

		for v in metadata:
			print(v)
		return metadata

	def set_file_modification(self):
		for e in self.metadata:
			for k,v in e.items():
				if (k == 'File Modification Date/Time'):
					if not '-' in v:
						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S')
							data = data_hora_info.strftime('%Y:%m:%d %H:%M:%S')
						except :
							print('Não foi possivel reconhecer a data de modificação', v)

					else:
						try :
							data_hora_info = datetime.datetime.strptime(v[:-6], '%Y:%m:%d %H:%M:%S')
							data = data_hora_info.strftime('%Y:%m:%d %H:%M:%S')
						except :
							print('Não foi possivel reconhecer a data de modificação', v)

		return 	str(data)

	def set_file_modification_format(self):
		for e in self.metadata:
			for k,v in e.items():
				if (k == 'File Modification Date/Time'):
					if not '-' in v:
						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data de modificação', v)

					else:
						try :
							data_hora_info = datetime.datetime.strptime(v[:-6], '%Y:%m:%d %H:%M:%S')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data de modificação', v)

		return 	str(data)

	def set_nome(self):
		nome = str(os.path.basename(self.input_file))
		nome = nome.split('.')
		nome = '.'.join([str(elem) for elem in nome[:-1]])
		print("NOME:", nome)

		return nome

	def set_extension(self):
		extension = str(os.path.basename(self.input_file))
		extension = extension.split('.')
		return extension[-1]

	def set_data(self):
		data = ''
		for e in self.metadata:
			for k,v in e.items():

				if (k == 'Date/Time Original'):

					if not '-' in v :
						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data (1)', v)

						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S.%f')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data (2)', v)


					else:
						try :
							data_hora_info = datetime.datetime.strptime(v[:-6], '%Y:%m:%d %H:%M:%S')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data (3)', v)

						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S.%f')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data (4)', v)		


				if (k == 'File Modification Date/Time') and data == '':
					if not '-' in v :
						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data (5)', v)

						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S.%f')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data (6)', v)


					else:
						try :
							data_hora_info = datetime.datetime.strptime(v[:-6], '%Y:%m:%d %H:%M:%S')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data (7)', v)

						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S.%f')
							data = data_hora_info.strftime('%d/%m/%Y')
						except :
							print('Não foi possivel reconhecer a data (8)', v)

				

		print("DATA CAPTURADA:",data)

		return 	data
				

	def set_time(self):
		hora=''
		for e in self.metadata:
			for k,v in e.items():

				if (k == 'Date/Time Original'):

					if not '-' in v:
						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S')
							hora = str(data_hora_info.strftime('%H:%M:%S'))
						except :
							print('Não foi possivel reconhecer a hora (1)', v)

						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S.%f')
							hora = str(data_hora_info.strftime('%H:%M:%S'))
						except :
							print('Não foi possivel reconhecer a hora (2)', v)


					else:
						try :
							data_hora_info = datetime.datetime.strptime(v[:-6], '%Y:%m:%d %H:%M:%S')
							hora = str(data_hora_info.strftime('%H:%M:%S'))
						except :
							print('Não foi possivel reconhecer a hora (3)', v)

						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S.%f')
							hora = str(data_hora_info.strftime('%H:%M:%S'))
						except :
							print('Não foi possivel reconhecer a hora (4)', v)				

				if (k == 'File Modification Date/Time') and hora=='':
					if not '-' in v:
						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S')
							hora = str(data_hora_info.strftime('%H:%M:%S'))
						except :
							print('Não foi possivel reconhecer a hora (5)', v)

						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S.%f')
							hora = str(data_hora_info.strftime('%H:%M:%S'))
						except :
							print('Não foi possivel reconhecer a hora (6)', v)


					else:
						try :
							data_hora_info = datetime.datetime.strptime(v[:-6], '%Y:%m:%d %H:%M:%S')
							hora = str(data_hora_info.strftime('%H:%M:%S'))
						except :
							print('Não foi possivel reconhecer a hora (7)', v)

						try :
							data_hora_info = datetime.datetime.strptime(v, '%Y:%m:%d %H:%M:%S.%f')
							hora = str(data_hora_info.strftime('%H:%M:%S'))
						except :
							print('Não foi possivel reconhecer a hora (8)', v)




		print("HORA CAPTURADA:",hora)

		return 	hora
				
	def set_gps(self):
		gps_info_mf = ''
		for e in self.metadata:
			for k,v in e.items():
				if (k == 'GPS Position'):
					v = v.replace('deg','º')
					gps_info = v
					v = v.replace(' ', '')
					if(v != ''):
						gps_info_mf = re.split('[º\',"]+', v)

		return gps_info_mf	

	def get_gps_dms(self):
		if (self.gps!=''):
			return self.gps[0] + 'º ' + self.gps[1] + "' "  + self.gps[2] + "''"  + self.gps[3] + ", "  + self.gps[4] +'º ' + self.gps[5]+ "' " + self.gps[6] + "'' "+ self.gps[7]
		else:
			return ''

	def get_gps_dec(self):
		if (self.gps!=''):
			lat = self.dms2dec(self.gps[0],self.gps[1],self.gps[2], self.gps[3])
			log = self.dms2dec(self.gps[4],self.gps[5],self.gps[6], self.gps[7])
			return lat, log
		else:
			return 0,0

	def get_gps_utm(self):
		if(self.gps!=''):
			lat, log = self.get_gps_dec()
			gps_utm_info = utm.from_latlon(lat, log)
			gps_utm_info = str(gps_utm_info[2]) + ' SUL E ' + '{:_}'.format(round(gps_utm_info[0],2)) + 'm N ' + str('{:_}'.format(round(gps_utm_info[1], 2))) + 'm'
			gps_utm_info = gps_utm_info.replace('.',',')
			gps_utm_info = gps_utm_info.replace('_','.')
			return gps_utm_info
		else:
			return ''


	def get_utm(self):
		if(self.gps!=''):
			lat, log = self.get_gps_dec()
			gps_utm_info = utm.from_latlon(lat, log)
			gps_utm_info = ['{:_}'.format(round(gps_utm_info[0],2)) + 'm', str('{:_}'.format(round(gps_utm_info[1], 2))) + 'm']
			gps_utm_info[0] = gps_utm_info[0].replace('.',',')
			gps_utm_info[0]= gps_utm_info[0].replace('_','.')
			gps_utm_info[1] = gps_utm_info[1].replace('.',',')
			gps_utm_info[1]= gps_utm_info[1].replace('_','.')
			return gps_utm_info
		else:
			return ''

	def dms2dec(self, d, min, sec, hemisferio= 'N',):
		if hemisferio == 'S' or hemisferio == 'W' :
			aux=-1
		else:
			aux=1
		return (int(d) + int(min)/60 + float(sec)/3600) * aux	


		 



#for filename in glob.glob( PATH + '/INPUT/*.JPG'): 
#	foto = Exif(filename)
#	print(foto.extension + ' ' +foto.get_gps_utm() )
