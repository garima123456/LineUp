from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty, StringProperty,NumericProperty, DictProperty
from kivy.network.urlrequest import UrlRequest
from kivy.uix.listview import ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory 
from kivy.uix.checkbox import CheckBox
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
import unicodedata
import sys
import json
import requests

exception=['Enter valid IFSC code', '']
error=['Enter IFSC code','']
class DispatchTicket(BoxLayout):
	token_number=ListProperty(['',''])
	name=StringProperty()
	number=StringProperty()

	def lock_entries():
		pass

class ConfirmButton(ListItemButton):
	token_data=ListProperty()

class CurrentStatus(BoxLayout):
	dict_filled_from_form = {}
	item_strings1=ObjectProperty()
	search_results1=ObjectProperty()
	status=ListProperty(['','','',''])
	current_status=NumericProperty()
	available_position=NumericProperty()
	working_hours=StringProperty()
	window=StringProperty()
	data= DictProperty({})
	user_data_detail=ObjectProperty()
	token_data=ListProperty(['',''])
	def book_position(self):
		IFSC_code=str(self.status[0])
		search_template="http://localhost:5000/"+"book/"+IFSC_code
		search_url=search_template
		request=UrlRequest(search_url, self.NewStatus_retrieved)
	def NewStatus_retrieved(self, request, data):
		data = json.loads(data.decode()) if not isinstance(data, dict) else data
		print data
		for key in data:
			print data[key]
			status_details = [(data[key]['status']),(data[key]['window'])]
			print status_details
			self.current_status=status_details[0]
			self.available_position=status_details[0]+1
			
			self.window=status_details[1]
	def add_entry(self,dict_of_form):
		dict_filled_from_form = dict_of_form
	def edit(self, data=None):
		if data is not None:
			self.data = data
		else:
			self.data = {}
	__events__=('on_save',)
	def on_save(self,data):
		item_strings= ObjectProperty()
		user_data_detail=ObjectProperty()
		user_data_detail_error=ObjectProperty()
		IFSC_code=str(self.status[0])
		data= dict(data)
		data['IFSC_code']=str(self.status[0])
		cotact_number=[i for i in list(data['mobileNumber'])]
		if len(cotact_number) ==10 and [ i in cotact_number in range(10)] and len(data['name'])>=3:
			user_detail = json.dumps(data)			
			user_detail_handler = requests.post("http://localhost:5000/render_ticket/", json=user_detail)
			user_detail_handler=user_detail_handler.text
			user_data = json.loads(user_detail_handler.decode()) if not isinstance(user_detail_handler, dict) else user_detail_handler
			for key in user_data:
				self.user_data_detail.item_strings=[(key,user_data[key])]
				self.user_data_detail.adapter.data[:]
 				self.user_data_detail.adapter.data.extend([(key,user_data[key])])
				self.user_data_detail._trigger_reset_populate()
		elif len(data['name'])<3:
			user_data=["user name should contain atleast three charecters"]
			self.user_data_detail_error.item_strings=user_data	
		else:
			user_data=["Please enter correct mobile number"]
			self.user_data_detail_error.item_strings=user_data	
		
	def args_converter(self,index,data_item):
		print data_item
		token_number,name=data_item
		return {'token_data':(token_number,name)}
				
class SelectionButton(ListItemButton):
	status=ListProperty()

class StatusRoot(BoxLayout):
	current_status=ObjectProperty()
	user_form=ObjectProperty()
	dict_filled_from_form = {}
	status=ListProperty(['','',0])
	data= DictProperty({})
	token_number=ListProperty(['',''])
	def show_current_status(self, status):
		self.clear_widgets()
		if self.current_status is None:
			self.current_status=CurrentStatus()
		if status is not None:
			self.current_status.status = status
			self.current_status.book_position()	
		self.add_widget(self.current_status)
	def show_search_branch(self):
		self.clear_widgets()
		self.add_widget(SearchBranchName())
	def render_ticket(self,token_number):
		self.clear_widgets()
		if token_number is not None:
			self.dispatch_ticket=DispatchTicket()			
			self.dispatch_ticket.token_number = token_number
		self.add_widget(self.dispatch_ticket)
	def show_status_page(self):
		self.clear_widgets()
		self.add_widget(CurrentStatus())
	
class SearchBranchName(BoxLayout):
	search_input = ObjectProperty()
	search_results=ObjectProperty()
	search_results2=ObjectProperty()
	available_position=NumericProperty()
	def search_IFSC_code(self):
		if self.search_input.text=="":
			data='Enter IFSC code'
			request=None
		else:
			search_template="http://localhost:5000/lookup/"+"{}"
			search_url=search_template.format(self.search_input.text.upper())
			request=UrlRequest(search_url, self.found_status)
			
	def found_status(self,request,data):
		item_strings= ObjectProperty()
		data = json.loads(data.decode()) if not isinstance(data, dict) else data
		if data==exception[0] :
			status_details=[(exception[0])]
			self.search_results2.item_strings=status_details
		else:
			for key in data:
				status_details = [(key,data[key]['Name'])]
			self.search_results.item_strings=status_details
			self.search_results.adapter.data[:]
			self.search_results.adapter.data.extend(status_details)
			self.search_results._trigger_reset_populate()
	def args_converter(self,index,data_item):
		print data_item
		IFSC_code, BankAddress=data_item
		return {'status':(IFSC_code,BankAddress)}

class StatusApp(App):
	pass
if __name__=='__main__':
	StatusApp().run()