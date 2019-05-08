from flask import Flask, request, redirect, render_template
import webbrowser, sys, json, urllib

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return redirect("/home", code=302)

@app.route('/<string:page>')
def pageLoader(page='home'):
	return render_template(page+'.html')

if __name__ == '__main__':
	app.run(debug = True, threaded=True, host='0.0.0.0')