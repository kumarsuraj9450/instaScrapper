from selenium import webdriver
from bs4 import BeautifulSoup
from xlsxwriter import Workbook
from time import sleep
import os
import requests
import shutil


class App:
	def __init__(self,username,password,target_username,path='instaPhotos'):
		if not os.path.exists(path):
			os.mkdir(path)
		self.username=username
		self.password=password
		self.target_profile=target_username
		self.path=path
		self.no_of_post=0
		self.error=False
		self.link=set()
		self.driver=webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe')
		self.main_url= 'https://www.instagram.com/accounts/login/'#'https://www.instagram.com/'
		self.driver.get(self.main_url)
		self.driver.maximize_window()
		self.log_in()
		if self.error is False:
			self.noti_off()
			self.open_target_profile()
		if self.error is False:
			self.scroll_down()
			self.done()
		if self.error is False:
			self.link2file()
			self.download_img()
			self.write_captions()


	def log_in(self,):
	    try:
	        #login_button=self.driver.find_element_by_xpath('//p[@class="izU2O"]/a')
	        #login_button.click()
	        #sleep(3)
	        try:
	            username=self.driver.find_element_by_xpath('//input[@name="username"]')
	            username.send_keys(self.username)
	            password = self.driver.find_element_by_xpath('//input[@name="password"]')
	            password.send_keys(self.password)
	            #login=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button')
	            #login.click()
	            sleep(2)
				password.submit()
	        except Exception:
	            print('Some error occurred while trying to find username and password ')
	            self.error=True
	    except Exception:
	        self.error=True
	        print('Unable to find login button')
	    sleep(3)
	

	def noti_off(self):
		try:
			not_now=self.driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]/button[2]')
			not_now.click()
		except Exception:
			print("Error occured while switching off Notification")


    
	def open_target_profile(self):
		try:
			# search_bar=self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input')
			# search_bar.send_keys(target_profile)

			sleep(3)

			target_url='https://www.instagram.com/'+self.target_profile #self.main_url
			#opening target profile
			self.driver.get(target_url)
			sleep(2)
		except Exception:
			self.error=True
			print('Could not find search bar')

   

	def scroll_down(self):
		profile=BeautifulSoup(self.driver.page_source,'lxml')
		#print(profile.prettify())
		file=open("no_of_post.txt",'w')
		no_post=(profile.find_all('span',class_='g47SY')[0].text)
		self.no_of_post=int(no_post.replace(',', ''))
		file.write("no of post of @"+target_profile+" => "+str(self.no_of_post))
		file.close()
		os.system('cls')
		print("no of post of @"+target_profile+" => "+str(no_post))
		
		print("Scrolling down will take around "+str(self.no_of_post/360)+" minute...............")
		print("Collecting all links.")
		print("?????????? DO NOT CLOSE WINDOW ???????")
		self.link=set()
		#link=[]
		for i in range(int(self.no_of_post//6)):
			self.driver.execute_script('window.scrollBy(0, 650);')
			img=BeautifulSoup(self.driver.page_source,'html5lib').find_all('img',class_='FFVAD')
			for _ in img:
				self.link.add(_)
			print(i)
			sleep(1)
		os.system('cls')
		

	
	def link2file(self):
		#profile=BeautifulSoup(self.driver.page_source,'html5lib')
		print("!!!!!!!!!!!!!  WAIT   !!!!!!!!!!!!!!!!!!")
		print("total links=",len(self.link))

		linkList=(list(map(str,list(self.link))))
		linkList=list(map(str.encode,linkList))
		linkList=(list(map(str,linkList)))

		file_name=self.target_profile+".txt"
		links=open(file_name,'w')

		for _ in linkList: 
			links.write(_+"\n")
		links.close()



	def download_img(self):
		print("\n\n!!!!!!!!!!!WAIT!!!!!!!!!!!!!\n\nDownloading images.. ")
		path=self.target_profile+".txt"
		link=open(path,'r')

		soup=BeautifulSoup(link,'html.parser')

		path="instaPhotos\\"+self.target_profile
		if not os.path.exists(path):
			os.mkdir(path)

		img_links=soup.find_all('img')

		for i, _ in enumerate(img_links):
			print("\n\n!!!!!!!!!!!  WAIT   !!!!!!!!!!!!!\n\nDownloading images..")
			print(str(i+1)+" of "+str(len(self.link)))

			filename=str(i+1)+".jpg"
			img_path = os.path.join(path, filename)

			
			try:
				url=_['src']
				response = requests.get(url, stream=True)
				with open(img_path, 'wb') as file:
					shutil.copyfileobj(response.raw, file)
			except Exception:
		 			url='not exist'
			

			os.system('cls')
			link.close()



	def write_captions(self):
		#print("\n\n!!!!!!!!!!!WAIT!!!!!!!!!!!!!\n\nWriting captions to file ")
		path=self.target_profile+".txt"
		link=open(path,'r')

		soup=BeautifulSoup(link,'html.parser')
		img_links=soup.find_all('img')

		path="instaPhotos\\"+self.target_profile+"\\captions"
		if not os.path.exists(path):
			os.mkdir(path)

		caption_file="\\"+self.target_profile+"_captions.xlsx"
		workbook=Workbook(path+caption_file)
		worksheet=workbook.add_worksheet()
		worksheet.write(0, 0, 'Image name')  # 3 --> row number, column number, value
		worksheet.write(0, 1, 'Caption')


		for i, _ in enumerate(img_links):
			print("\n\n!!!!!!!!!!!WAIT!!!!!!!!!!!!!\n\nWriting captions.. ")
			print(str(i+1)+" of "+str(len(self.link)))

			try:
				caption=_['alt']	
			except KeyError:
				caption=("NO CAPTION")

			#print("\n\nCAPTION => ",caption,end='\n')
			
			filename=str(i+1)+".jpg"
			worksheet.write(i+1, 0, filename)  # 3 --> row number, column number, value
			worksheet.write(i+1, 1, caption)
			os.system('cls')

		workbook.close()
		link.close()


	def done(self):
		sleep(5)
		self.driver.quit()
		path=self.target_profile+".txt"

	#i+=1
# file.close()

# sleep(5)
#driver.quit()

if __name__=='__main__':
    username=str(input("Enter Username of your Instagram account => "))
    password=(input("Enter Password of your Instagram account => "))
    target_profile=str(input("Enter Username of target Instagram account => "))
        
    app=App(username=username,password=password,target_username=target_profile)
    path=target_profile+".txt"
    os.remove(path)
    os.remove("no_of_post.txt")



