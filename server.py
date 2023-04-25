

from playlist_app import app

from playlist_app.controllers import users,playlists

import os





if __name__ == '__main__' :
    app.run( debug = True)
# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)
