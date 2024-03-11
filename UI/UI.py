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

# view methods
    @staticmethod
    @app.route('/')
    def root():
        controller_vis = UI.parse_args(request.args)
        img_list = UI.img_list
        if img_list.get_focus() is None:
            img_list.random_focus()
        focus = img_list.get_focus()
        display_list = img_list.return_slice(focus, focus + 5)
        uris = list(img.gen_view_uri() for img in display_list)
        orientations = display_list.get_orientations()
        metadata = list((uris[i], orientations[i]) for i in range(len(display_list)))
        json_metadata = json.dumps(metadata)
        timeout_sec = UI.timeout_sec
        return render_template(
            'root.html',
            metadata=json_metadata,
            timeout_sec=timeout_sec,
            focus=focus,
            controller_vis=controller_vis
        )

    @staticmethod
    @app.route('/settings')
    def settings():
        if 'focus' in request.args:
            focus = int(request.args.get('focus'))
            UI.img_list.set_focus(focus)
        timeout_sec = UI.timeout_sec
        return render_template('settings.html', timeout_sec=timeout_sec)

    @staticmethod
    @app.route('/settings-confirm', methods=['POST'])
    def settings_confirm():
        uri = '/'
        if 'timeout-sec' in request.form and request.form['timeout-sec']:
            UI.timeout_sec = int(request.form['timeout-sec'])
            UI.set_timeout_sec()
        if 'refresh' in request.form and request.form['refresh']:
            uri += '?refresh'
        return redirect(uri)

# utils
    @classmethod
    def init_imgs(cls):
        non_jpegs = ImageList.fetch_non_jpegs()
        if non_jpegs:
            non_jpegs.convert_all()
        cls.img_list = ImageList.fetch_jpegs()
        return cls.img_list

    @classmethod
    def load_timeout_sec(cls):
        os.chdir(cls.path_constants.get_static())
        if os.path.exists('timeout.pickle'):
            cls.timeout_sec = pickle.load(open('timeout.pickle', 'rb'))

    @classmethod
    def parse_args(cls, args):
        controller_vis = 'none'
        if 'focus' in request.args:
            focus = int(request.args['focus'])
            cls.set_focus(focus)
        if 'skip' in request.args:
            controller_vis = 'flex'
        if 'refresh' in request.args:
            cls.init_imgs()
        return controller_vis

    @classmethod
    def set_timeout_sec(cls):
        os.chdir(cls.path_constants.get_static())
        pickle.dump(cls.timeout_sec, open('timeout.pickle', 'wb'))

    @classmethod
    def set_focus(cls, new_focus):
        length = len(cls.img_list)
        if new_focus < 0:
            new_focus += length
        if new_focus > length:
            cls.img_list.set_focus(new_focus - length)
        else:
            cls.img_list.set_focus(new_focus)

# run
    @classmethod
    def run(cls):
        cls.path_constants = Project.update_root('')
        cls.load_timeout_sec()
        cls.init_imgs()
        cls.app.run()

    @classmethod
    def create_app(cls):
        cls.path_constants = Project.update_root('')
        cls.load_timeout_sec()
        cls.init_imgs()
        return cls.app


if __name__ == '__main__':
    UI.run()
