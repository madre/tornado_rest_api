# -*- coding: utf-8 -*-
import json

from RestFramework.encoders import JSONEncoder


class JSONSerializer(object):
    content_type = "application/json"
    encoding = "UTF-8"

    def get_content_type(self):
        return "{}; charset={}".format(self.content_type, self.encoding)

    def serialize(self, data):
        return self.to_json(data)

    def to_json(self, data):
        return json.dumps(
            data, cls=JSONEncoder, sort_keys=True, ensure_ascii=False
        )
