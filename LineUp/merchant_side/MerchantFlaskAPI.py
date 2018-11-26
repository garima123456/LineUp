from flask import Flask, render_template, jsonify, request
from werkzeug.utils import cached_property, escape
from werkzeug.debug.console import Console
from werkzeug._compat import range_type, PY2, text_type, string_types, to_native, to_unicode
from werkzeug.filesystem import get_filesystem_encoding
import json
import os

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

@app.route("/search_id/<IFSC_code>")
def search_id_num(IFSC_code):
	search_id_code_handler=open(os.path.join(server_files_path,directory),'r')
	search_id_code= search_id_code_handler.read()
	json_data=json.loads(search_id_code)
	if IFSC_code in json_data:
		return json.dumps ('ID not available',0)
	else:
		return json.dumps([IFSC_code])

@app.route("/book/<IFSC_code>")
def book_id(IFSC_code):
	search_id_code_handler=open(os.path.join(server_files_path,directory),'r')
	search_id_code= search_id_code_handler.read()
	json_data=json.loads(search_id_code)
	if IFSC_code in json_data:
		return json.dumps ({ k:v for k,v in json_data.items() if IFSC_code in k })

@app.route("/display_queue/<IFSC_code>")
def display_queue_details(IFSC_code):

	token_number=IFSC_code[11:]
	display_queue_handler=IFSC_code[0:11]+'{}'.format('.json')	
	display_queue=open(os.path.join(server_files_path,display_queue_handler),'r')
	json_data=json.loads(display_queue.read())
	display_queue.close()
	if token_number in json_data.keys():
		name=json_data[token_number]
		return json.dumps({token_number:name})
	else:
		return json.dumps({'0':'no value'})


if __name__ == '__main__':
	app.run(  debug = True)













