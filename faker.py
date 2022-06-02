import random

import requests
from flask import Flask


@app.route('/downloadFile')
def download_file():
    return send_from_directory(output_directory, "myfile.txt", as_attachment=True)



url = 'http://api.open-notify.org/astros.json'
res = requests.get(url)


if __name__ == '__main__':
    app.run()
