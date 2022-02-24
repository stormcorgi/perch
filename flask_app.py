from flask import *
from perchdb import *
import subprocess
from hls_dl import *

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("main.html", actresses=get_actresses())


@app.route("/actress/<name>")
def actress(name):
    actress = get_actressdata_by_name(name)
    movies = get_movies_by_actressid(actress.actressid)
    return render_template("actress.html", actress=actress, movies=movies)


@app.route("/player")
# http://192.168.10.110:8000/player?id=KYB&name=hogefuga
def player():
    fileid = request.args.get('id', default=None, type=str)
    filepath = fileid + ".info"
    filename = request.args.get('name', default=None, type=str)
    return render_template("player.html", filepath=filepath, filename=filename)


# @app.route("/downloader")
# def downloader():
#     target = request.args.get('target', default=None, type=str)
#     if None is not target:
#         srcAddr = videoTagParser_JavyNow(target)
#         print(srcAddr)
#         # args = ['hlsdl', srcAddr, '&']
#         # try:
#         #     res = subprocess.Popen(args)
#         # except:
#         #     print("Error.")
#     return render_template('downloader.html', addr=srcAddr)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000, threaded=True)
