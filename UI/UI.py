from flask import Flask, render_template
from Logic.ImageList import ImageList
import json


class UI:
    app = Flask(__name__)

    @staticmethod
    @app.route('/')
    def root():
        non_jpegs = ImageList.fetch_non_jpegs()
        if non_jpegs:
            non_jpegs.convert_all()
        img_list = ImageList.fetch_jpegs()
        uris = list(img.gen_view_uri() for img in img_list)
        orientations = img_list.get_orientations()
        metadata = list((uris[i], orientations[i]) for i in range(len(img_list)))
        json_metadata = json.dumps(metadata)
        timeout_sec = 15
        return render_template('root.html', metadata=json_metadata, timeout_sec=timeout_sec)

    @staticmethod
    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    @classmethod
    def run(cls):
        cls.app.run()


if __name__ == '__main__':
    UI.run()
