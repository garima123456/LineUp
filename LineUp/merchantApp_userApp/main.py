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
error=['Enter IFSC code','window closed']
id_registration_error=['ID not available','']
lst=range(1,100)
class CounterWindow(BoxLayout):
	"""docstring for CounterWindow"""

	data= DictProperty({})
	status=ListProperty(['','','',''])
	search_available_id=ObjectProperty()
	search_reg_id=ObjectProperty()	
	verify_password=ObjectProperty()
	re_verify_password=ObjectProperty()
	email_id=ObjectProperty()
	mobile_number=ObjectProperty()
	check_password=ObjectProperty()	

	def check_available_id(self):

		if self.search_input.text=="":
			data='Enter ID code'
			request=None

		else:
			search_template="http://localhost:5000/search_id/"+"{}"
			search_url=search_template.format(self.search_input.text.upper())
			request=UrlRequest(search_url,self.register_id_num)
	def register_id_num(self,request,data):
		item_strings= ObjectProperty()
		Availability=[json.loads(str(data))]
		print data
		self.search_available_id.item_strings = Availability

	def check_password(self):
		item_strings= ObjectProperty()		
		if len(str(search_input.text))>=7:
			self.verify_password.item_strings = 'Password is valid'

	def register_window_details():
		pass
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
		print data
		
		'''data['IFSC_code']=str(self.status[0])
		window_detail = json.dumps(data)			
		window_detail_handler = requests.post("http://localhost:5000/render_ticket/", json=window_detail)
		window_detail_handler=window_detail_handler.text
		
	def args_converter(self,index,data_item):
		print data_item
		token_number,name=data_item
		return {'token_data':(token_number,name)}'''
	

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
	token_search_result=ObjectProperty()
	display_token=ObjectProperty()
	token_data=ListProperty(['',''])
	def close_window(self):
		IFSC_code=str(self.status[0])
		
		search_url="http://localhost:5000/display_queue/"+IFSC_code+str(0)	
		request=UrlRequest(search_url, self.queue_status)	
	def book_position(self):
		IFSC_code=str(self.status[0])
		search_url="http://localhost:5000/book/"+IFSC_code
		request=UrlRequest(search_url, self.NewStatus_retrieved)
		
	def NewStatus_retrieved(self, request, data):
		data = json.loads(data.decode()) if not isinstance(data, dict) else data
		for key in data:
			status_details = [(data[key]['status']),(data[key]['window'])]
			self.current_status=status_details[0]
			self.available_position=status_details[0]+1
			self.working_hours=status_details[1]
		
	def available_Tokens(self):
		IFSC_code=str(self.status[0])
		
		search_url="http://localhost:5000/available_tokens/"+IFSC_code+str(0)	
		request=UrlRequest(search_url, self.display_available_tokens)	
	def display_available_tokens(self,request,data):
		data=json.loads(data.decode()) if not isinstance(data, dict) else data
		item_strings= ObjectProperty()
		self.display_token.item_strings=[data]		
	def counter(self):
		num=lst.pop(0)
		return num
	def start_queue(self):
		IFSC_code=str(self.status[0])
		num=1
		search_url="http://localhost:5000/display_queue/"+IFSC_code+str(num)
		request=UrlRequest(search_url, self.queue_status)

	def next_in_queue(self):
		#when nxt in queue is asked for the token no wil be sent by the server

		IFSC_code=str(self.status[0])
		num=self.counter()
		search_url="http://localhost:5000/display_queue/"+IFSC_code+str(num)
		request=UrlRequest(search_url, self.queue_status)

	def queue_status(self,request,data):
		data=json.loads(data.decode()) if not isinstance(data, dict) else data
		
		item_strings= ObjectProperty()
		for key in data:
			if data==error[1]:
				token_details=[error[1],'']
			else:
				token_details = [key,data[key]]
		self.token_search_result.item_strings=token_details
		#self.token_search_result.adapter.data[:]
		#self.token_search_result.adapter.data.extend(token_details)
		#self.token_search_result._trigger_reset_populate()
	
		


class SelectionButton(ListItemButton):
	status=ListProperty()
class RegisterIdButton(ListItemButton):
	availableID=ListProperty()

class StatusRoot(BoxLayout):
	counter_window=ObjectProperty()
	user_form=ObjectProperty()
	dict_filled_from_form = {}
	status=ListProperty(['','',0])
	data= DictProperty({})
	token_number=ListProperty(['',''])

	def show_current_status(self, status):
		self.clear_widgets()

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

	def edit_window_details(self):
		self.clear_widgets()
		self.counter_window=CounterWindow()
		#self.counter_window.availableID = availableID
		self.add_widget(self.counter_window)

	
class SearchBranchName(BoxLayout):
	search_input = ObjectProperty()
	search_results=ObjectProperty()
	search_results2=ObjectProperty()
	search_available_id=ObjectProperty()
	available_position=NumericProperty()
	search_reg_id=ObjectProperty()


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

	def check_available_id(self):
		if self.search_input.text=="":
			data='Enter ID code'
			request=None

		else:
			search_template="http://localhost:5000/search_id/"+"{}"
			search_url=search_template.format(self.search_input.text.upper())
			request=UrlRequest(search_url,self.register_id_num)
	def register_id_num(self,request,data):
		item_strings= ObjectProperty()

		data=[json.loads(str(data))]
		if data==[id_registration_error[0]]:
			self.search_available_id.item_strings = data
		else:
			self.search_reg_id.item_strings = data
			self.search_reg_id.adapter.data[:]
			self.search_reg_id.adapter.data.extend(data)
			self.search_reg_id._trigger_reset_populate()
	def args_converter(self,index,data_item):
		if len(data_item)==2:
			IFSC_code, BankAddress=data_item
			return {'status':(IFSC_code,BankAddress)}		
		else:
			return  {'availableID':(data_item)}			

class merchantApp(App):
	pass
if __name__=='__main__':
	merchantApp().run()