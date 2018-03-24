import requests
import urllib.request
import sys
import time
from time import sleep
from os import listdir
from os.path import isfile,join
import zipfile

url = "http://www.vap.aau.dk/rgb-d-face-database/"
fileExtn = ".zip"
httpString = "http://"
downloadDir = "D:\MyWorks\DataScience\FaceID\dataset"
dirSeparator = "\\"
extractDir = downloadDir + "\\extracted"

def reporthook(count, block_size, total_size):
	global start_time
	if count == 0:
		start_time = time.time()
		#workaround to prevent division by zero. sleeping the program for 50ms
		sleep(0.05)
		return
	duration = time.time() - start_time
	progress_size = int(count * block_size)
	speed = int(progress_size / (1024 * duration))
	percent = min(int(count * block_size * 100 / total_size),100)
	sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
					(percent, progress_size / (1024 * 1024), speed, duration))
	sys.stdout.flush()

def downloadFile():
	r = requests.get(url)
	content = r.content.decode(r.encoding)
	index1 = content.find(fileExtn)
	while(index1 != -1):
		start = content.rfind(httpString,0,index1)
		end = (index1+len(fileExtn))
		downloadUrl = content[start:end]
		#print("Downnload url = " + downloadUrl)
		if downloadUrl:
			print("Downnload url = " + downloadUrl)
			fileNameStart = downloadUrl.rfind("/")
			extractedFileName = downloadUrl[fileNameStart+1:]
			urllib.request.urlretrieve(downloadUrl,downloadDir+dirSeparator+extractedFileName,reporthook)
			#print("FileName = " + fileName)
		content = content[end:len(content)]
		index1 = content.find(fileExtn)
	r.close()

def extractZipFiles():
	zipFiles = [f for f in listdir(downloadDir) if isfile(join(downloadDir,f))]
	for file in zipFiles:
		folderName = file[:file.rfind('.')]
		print(file +"-"+folderName)
		zip_ref = zipfile.ZipFile(downloadDir+dirSeparator+file,'r')
		zip_ref.extractall(extractDir)
		zip_ref.close()

extractZipFiles()