from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
import datetime
import sqlite3
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFlatButton,MDRectangleFlatButton





class title(Screen):
	pass




class MyApp(MDApp):
	def build(self):
		Builder.load_file('ehr.kv')
		self.theme_cls.primary_palette="LightBlue"
		class newpatient(Screen):
			date=datetime.date.today()
			dateformat=date.strftime("%d-%m-%Y")
			def savetodatabase(self):
				con=sqlite3.connect("opddatabase.db")
				c=con.cursor()
				c.execute("CREATE TABLE if not exists database (opdno text ,name text,age text,place text,date text)")
				c.execute("INSERT INTO database VALUES (:opdno,:name,:age,:place,:date)",{"opdno":self.ids.opdnoentrynew.text,"name": self.ids.nameentrynew.text.lower(),"age":self.ids.ageentrynew.text,"place":self.ids.placeentrynew.text.lower(),"date":self.ids.dateentrynew.text})
				con.commit()
				con.close()
		

		class oldpatient(Screen):
			date=datetime.date.today()
			dateformat=date.strftime("%d-%m-%Y")
			def getdetails(self):
				con=sqlite3.connect("opddatabase.db")
				c=con.cursor()
				c.execute("SELECT *,opdno FROM database WHERE opdno=:opdno",{"opdno":self.ids.opdnoentryold.text})
				records=c.fetchall()
				self.ids.namelabel.text=records[0][1]
				self.ids.agelabel.text=records[0][2]
				self.ids.placelabel.text=records[0][3]
			def submittopddatabase(self):
				con=sqlite3.connect(f"{self.ids.opdnoentryold.text}.db")
				c=con.cursor()
				c.execute("CREATE TABLE if not exists ptdatabase (opdno text ,name text,age text,place text,date text,mobno text,dues text,labdues text,xraydues text, labtests text,xrays text,fees text,billno text)")
				c.execute("INSERT INTO ptdatabase VALUES (:opdno,:name,:age,:place,:date,:mobno,:dues,:labdues,:xraydues,:labtests,:xrays,:fees,:billno)",{"opdno":self.ids.opdnoentryold.text,"name": self.ids.namelabel.text.lower(),"age":self.ids.agelabel.text,"place":self.ids.placelabel.text,"date":self.ids.dateentryold.text,"mobno":self.ids.mobno.text,"dues":self.ids.duesentry.text,"labdues":self.ids.labduesentry.text,"xraydues":self.ids.xrayduesentry.text,"labtests":self.ids.labtestsentry.text,"xrays":self.ids.xraysentry.text,"fees":self.ids.fees.text,"billno":self.ids.billnoentry.text})
				con.commit()
				con.close()

		class findbyopdno(Screen):
			def searchbyopdno(self):
				con = sqlite3.connect(f"{self.ids.searchopdno.text}.db")
				c = con.cursor()
				c.execute("SELECT *,opdno FROM ptdatabase WHERE opdno=:opdno", {"opdno": self.ids.searchopdno.text})
				records = c.fetchall()
				table = MDDataTable(
						column_data=[("OPD no",dp(30)), ("Name",dp(30)), ("Age",dp(30)), ("Place",dp(30)), ("Date",dp(30)), ("Mob no.",dp(30)), ("Dues",dp(30)), ("Lab dues",dp(30)), ("Xray Dues",dp(30)), ("Lab Tests",dp(30)), ("Xrays",dp(30)), ("Fees",dp(30)), ("Bill no",dp(30)),("IID no.",dp(20))],
						row_data=records
					)
				self.add_widget(table)
				con.close()
		

		class findbyname(Screen):
			def findbyname(self):
				con=sqlite3.connect("opddatabase.db")
				c=con.cursor()
				c.execute("SELECT *,name FROM database WHERE name=:name",{"name":self.ids.searchname1.text})
				global records
				records=c.fetchall()
				word=""
				for record in records:
					word=f"{word}\n{record}"
					self.ids.showqueryname.text=word
		

		class findbynameplace(Screen):
			def findbynameplace(self):
				con=sqlite3.connect("opddatabase.db")
				c=con.cursor()
				c.execute("SELECT *,name FROM database WHERE name=:name AND place=:place",{"name":self.ids.searchname2.text.lower(),"place":self.ids.searchplace.text.lower()})
				records2=c.fetchall()
				word2=""
				for record in records2:
					word2=f"{word2}\n{record}"
					self.ids.showqueryname2.text=word2
		

		class showdues(Screen):
			def __init__(self, **kw):
				super().__init__(**kw)
				opdnolist=[]
				namelist=[]
				placelist=[]
				dueslist1=[]
				dueslist=[]
				con=sqlite3.connect("opddatabase.db")
				c=con.cursor()
				c.execute("SELECT *,oid FROM database")
				records=c.fetchall()     
				for record in records:
					opdnolist.append(record[0])
					namelist.append(record[1])
					placelist.append(record[4])
				
				for opdno in opdnolist:
					con=sqlite3.connect(f"{opdno}.db")
					c=con.cursor()
					c.execute("SELECT * FROM ptdatabase")
					records=c.fetchall()
					con.commit()
					con.close()
					for record in records:
						dueslist1.append(record[6])
					dueslist.append(dueslist1[len(dueslist1)-1])
				data=[]
				for opdno,name,place,dues in zip(opdnolist,namelist,placelist,dueslist):
					data.append((opdno))
					data.append((name))
					data.append((place))
					data.append((dues))
				print(data)
				finaldata=[tuple(data)]
				print(finaldata)
				table = MDDataTable(
							column_data=[("OPD no",dp(30)), ("Name",dp(30)), ("Place",dp(30)), ("Dues",dp(30))],	
								
							row_data=finaldata
						)
				self.add_widget(table)


		class show(Screen):
			def show(self):
				con=sqlite3.connect("opddatabase.db")
				c=con.cursor()
				c.execute("SELECT * FROM database")
				records=c.fetchall()
				print(records)
				word=""
				for record in records:
					word=f"{word}\n{record}"
					self.ids.showlabel.text=word
			
		screen_manager = ScreenManager()

		screen_manager.add_widget(title(name ="title"))

		screen_manager.add_widget(newpatient(name ="newpatient"))

		screen_manager.add_widget(oldpatient(name ="oldpatient"))

		screen_manager.add_widget(findbyopdno(name ="findbyopdno"))

		screen_manager.add_widget(findbyname(name ="findbyname"))


		screen_manager.add_widget(findbynameplace(name ="findbynameplace"))
		screen_manager.add_widget(showdues(name ="showdues"))
		screen_manager.add_widget(show(name ="show"))
		return screen_manager

if __name__=='__main__':
	MyApp().run()