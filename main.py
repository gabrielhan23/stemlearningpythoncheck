from files import app
from waitress import serve

#main 
if __name__ == '__main__':
  ''' app.run(
    host="0.0.0.0",  # or 127.0.0.1
    port=8080,  # make sure this is a non privileged port
    debug=True  # this will allow us to easily fix problems and bugs
  )'''
  serve(app, host='0.0.0.0', port=5000)