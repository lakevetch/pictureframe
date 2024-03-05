from flask import Flask, render_template, request, redirect
from Logic.ImageList import ImageList
from Logic.Project import Project
import json
import os
import pickle


class UI:
    app = Flask(__name__)
    img_list = None
    path_constants = None
    timeout_sec = 15
    focus = None

    @staticmethod
    @app.route('/')
    def root():
        img_list = UI.img_list
        if not img_list.get_focus():
            img_list.random_focus()
        focus = img_list.get_focus()
        img_list = img_list.return_slice(focus, focus + 5)
        uris = list(img.gen_view_uri() for img in img_list)
        orientations = img_list.get_orientations()
        metadata = list((uris[i], orientations[i]) for i in range(len(img_list)))
        json_metadata = json.dumps(metadata)
        timeout_sec = UI.timeout_sec
        return render_template(
            'root.html', metadata=json_metadata, timeout_sec=timeout_sec, focus=img_list.get_focus()
        )

    @staticmethod
    @app.route('/settings')
    def settings():
        if 'focus' in request.args:
            focus = request.args.get('focus')
            UI.img_list.set_focus(focus)
        timeout_sec = UI.timeout_sec
        return render_template('settings.html', timeout_sec=timeout_sec)

    @staticmethod
    @app.route('/settings-confirm', methods=['POST'])
    def settings_confirm():
        if 'timeout-sec' in request.form and request.form['timeout-sec']:
            UI.timeout_sec = int(request.form['timeout-sec'])
            UI.set_timeout_sec()
        return redirect('/')

    @classmethod
    def init_imgs(cls):
        non_jpegs = ImageList.fetch_non_jpegs()
        if non_jpegs:
            non_jpegs.convert_all()
        cls.img_list = ImageList.fetch_jpegs()
        return cls.img_list

    @classmethod
    def run(cls):
        cls.path_constants = Project()
        cls.load_timeout_sec()
        cls.init_imgs()
        cls.app.run()

    @classmethod
    def load_timeout_sec(cls):
        os.chdir(cls.path_constants.get_static())
        if os.path.exists('timeout.pickle'):
            cls.timeout_sec = pickle.load(open('timeout.pickle', 'rb'))

    @classmethod
    def set_timeout_sec(cls):
        os.chdir(cls.path_constants.get_static())
        pickle.dump(cls.timeout_sec, open('timeout.pickle', 'wb'))


if __name__ == '__main__':
    UI.run()
