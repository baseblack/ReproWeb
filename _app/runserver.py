import sys
import os
sys.path.insert(0, os.path.join( os.path.dirname(os.path.abspath(__file__)), '3rdParty/python') )

from repoweb import app
app.run(debug=True,host='0.0.0.0',port=4000)
