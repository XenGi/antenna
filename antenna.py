#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from flask import Flask, request
from flask_restful import Resource, Api

from tlc5940 import TLC5940


app = Flask(__name__)
api = Api(app)

logger = logging.getLogger(__name__)

tower = [(0, 0, 0),  # lower stripes
         (0, 0, 0),
         (0, 0, 0),
         (0, 0, 0),  # upper stripes
         (0, 0, 0),
         (0, 0, 0),
         (0, 0, 0),
         (0, 0, 0)]

sphere = [(0, 0, 0),
          (0, 0, 0),
          (0, 0, 0),
          (0, 0, 0),
          (0, 0, 0),
          (0, 0, 0)]

def update_stripes():
    pass


class Help(Resource):
    def get(self):
        return {'help': 'Endpoints: /tower/<stripe_nr>, /sphere/<stripe_nr>\nSend: {\'rgb\': (0, 0, 0)}'}, 200


class Tower(Resource):
    def get(self, stripe):
        rgb = tower[stripe]
        if rgb:
            return {'rgb': rgb}, 200
        else:
            return {'error': 'No such stripe. Try something between 0 and 7.'}, 400

    def post(self, stripe):
        rgb = request.form['rgb']
        if type(rgb) is list and len(rgb) == 3:
            if tower[stripe]:
                tower[stripe] = [int(val) % 255 for val in rgb]
                update_stripes()
                return {'rgb': rgb}, 202
            else:
                return {'error': 'No such stripe. Try something between 0 and 7.'}, 400
        else:
            return {'error': 'Could not parse values. Try sending {\'rgb\': (0, 0, 0)}.'}, 400


class Sphere(Resource):
    def get(self, stripe):
        rgb = sphere[stripe]
        if rgb:
            return {'rgb': rgb}, 200
        else:
            return {'error': 'No such stripe. Try something between 0 and 7.'}, 400

    def post(self, stripe):
        rgb = request.form['rgb']
        if type(rgb) is list and len(rgb) == 3:
            if sphere[stripe]:
                sphere[stripe] = [int(val) % 255 for val in rgb]
                update_stripes()
                return {'rgb': rgb}, 202
            else:
                return {'error': 'No such stripe. Try something between 0 and 7.'}, 400
        else:
            return {'error': 'Could not parse values. Try sending {\'rgb\': (0, 0, 0)}.'}, 400


api.add_resource(Help, '/')
api.add_resource(Tower, '/tower/<int:stripe>')
api.add_resource(Sphere, '/sphere/<int:stripe>')


if __name__ == '__main__':
    app.run()
    update_stripes()
