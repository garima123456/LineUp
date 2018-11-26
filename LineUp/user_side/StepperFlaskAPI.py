from flask import Flask, render_template, jsonify, request
from werkzeug.utils import cached_property, escape
from werkzeug.debug.console import Console
from werkzeug._compat import range_type, PY2, text_type, string_types, to_native, to_unicode
from werkzeug.filesystem import get_filesystem_encoding
import os
import json
from directory import data
app = Flask(__name__)
 
server_files_path=r"../server_files/"	
directory='directory.json' 

@app.route("/lookup/<IFSC_code>")
def result(IFSC_code):

	search_id_code_handler=open(os.path.join(server_files_path,directory),'r')
	search_id_code= search_id_code_handler.read()
	json_data=json.loads(search_id_code)
	if IFSC_code in json_data:
		print json.dumps ({ k:v for k,v in json_data.items() if IFSC_code in k })
		return json.dumps ({ k:v for k,v in json_data.items() if IFSC_code in k })
	else:
		return json.dumps('Enter valid IFSC code',0)


@app.route("/book/<IFSC_code>")
def hello_user(IFSC_code):

	search_id_code_handler=open(os.path.join(server_files_path,directory),'r')
	search_id_code= search_id_code_handler.read()
	json_data=json.loads(search_id_code)
	if IFSC_code in json_data:
		return json.dumps ({ k:v for k,v in json_data.items() if IFSC_code in k })

@app.route("/search_id/<IFSC_code>")
def search_id_num(IFSC_code):
	search_id_code_handler=open(os.path.join(server_files_path,directory),'r')
	search_id_code= search_id_code_handler.read()
	json_data=json.loads(search_id_code)

	if IFSC_code in json_data:
		print 'ID not available'
		return json.dumps ('ID not available',0)
	else:
		print 'Available'
		return json.dumps('Available',0)

@app.route('/render_ticket/', methods = ['GET','POST'])
def render_ticket():
	client_data = request.get_json()
	data = json.loads(client_data)
	IFSC_code=str(data[u'IFSC_code'])
	with open(os.path.join(server_files_path,directory), 'r+') as f:# directory.json should be created by merchants apps with OPEN WINDOW command
		json_data = json.load(f)
		json_data[IFSC_code]['status']+=1
		f.seek(0)
		f.write(json.dumps(json_data))
		f.truncate()

	data['status']=json_data[IFSC_code]['status']
	user_database_handler=data['IFSC_code']+'.json'
	status=data['status']
	name=data['name']
	dictionary={status:name}
	
	users_data="{}"

	with open(user_database_handler,'a+') as user_data :
		if user_data.read()=="":
			json_data=json.loads(users_data)	
			user_data.write(json.dumps(json_data))
		else:
			user_data.close()
	    
	with open(user_database_handler,'r+') as user_data :
	    json_data = json.load(user_data)
	    json_data[status] = name
	    user_data.seek(0)
	    user_data.write(json.dumps(json_data)+"\n")
	    user_data.truncate()
	print json.dumps (dictionary)
	return json.dumps (dictionary)


@app.route("/display_queue/<IFSC_code>")
def display_queue_details(IFSC_code):

	token_number=IFSC_code[11:]
	IFSC_code=IFSC_code[0:11]

	if token_number==str(0) :
		user_data=open(os.path.join(server_files_path,directory),'r+')
		json_data=json.load(user_data)
		json_data[IFSC_code]['window'] = 'Close'
		purchased_tokens=json_data[IFSC_code]['Tokens']
		user_data.seek(0)
		user_data.write(json.dumps(json_data)+"\n")
		user_data.truncate()
		return json.dumps('window closed')

	else:


		user_data=open(os.path.join(server_files_path,directory),'r+')
		json_data=json.load(user_data)

		json_data[IFSC_code]['window'] = 'open'
		purchased_tokens=json_data[IFSC_code]['Tokens']
		user_data.seek(0)
		user_data.write(json.dumps(json_data)+"\n")
		user_data.truncate()
		display_queue_handler=IFSC_code[0:11]+'{}'.format('.json')	
		display_queue=open(os.path.join(server_files_path,display_queue_handler),'r')
		json_data=json.loads(display_queue.read())
		display_queue.close()
	
		if int(purchased_tokens)>=len(json_data.keys()):
			try:
				name =json_data[token_number] 
				return json.dumps({token_number:name})	
			except KeyError:
				return json.dumps({0:'no queue'})			
		else:
			user_data=open(os.path.join(server_files_path,directory),'r+') 
			json_data=json.load(user_data)
			json_data['PUNB0019600']['Tokens']=0	
			user_data.close()						
			return json.dumps({0:'Empty token balance'})




@app.route("/available_tokens/<IFSC_code>")
def check_available_tokens(IFSC_code):
	directory_handler=open(os.path.join(server_files_path,directory),'r')
	json_data= json.load(directory_handler)
	IFSC_code=str(IFSC_code)
	directory_handler.close()
	'''if IFSC_code in json_data:
		print IFSC_code
		print 'found'
	else:
		print json_data['PUNB0019600']['Tokens']
		remaining_tokens=json_data['PUNB0019600']['Tokens']
		print remaining_tokens
	return json.dumps(str(remaining_tokens))'''

	try:
		remaining_tokens=json_data['PUNB0019600']['Tokens']
		return json.dumps(str(remaining_tokens))
	except KeyError:
		return json.dumps(str('Some error'))



		
if __name__ == '__main__':
    app.run(host = 'localhost', port = 5000, debug = True)








