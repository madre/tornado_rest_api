#!/usr/bin/env python
# coding=utf-8
"""
参数格式验证

__created__ = '2015/3/4'
__author__ = 'deling.ma'
"""
from validator import validate  # 其他常用 Required, Not, Truthy, Blank, Range, Equals, In
from RestFramework.exceptions import APIError
from RestFramework.http_status import HTTP_STATUS_BAD_REQUEST


class ValidateMixin(object):
    """ 设置格式，参考文档 http://validatorpy.readthedocs.org/en/latest/index.html
    arguments_valid_rules = {
        "foo": [Required, Equals(123)],
        "bar": [Required, Truthy()],
        "baz": [In(["spam", "eggs", "bacon"])],
        "qux": [Not(Range(1, 100))]  # by default, Range is inclusive
    }
    验证结果 成功  (True, {})
    失败 (False, {
         'foo': ["must be equal to 123"],
         'bar': ['must be True-equivalent value'],
         'baz': ["must be one of ['spam', 'eggs', 'bacon']"],
         'qux': ['must not fall between 1 and 100']
        })
    """
    arguments_valid_rules = {}  # 定义参数验证格式

    def _validate(self):
        result = validate(self.arguments_valid_rules, self.request.DATA)
        if not result[0]:
            # 格式有误，直接报错
            try:
                error_dict = {arg: result[1][arg][0] for arg in result[1].keys()}
                error_info = ", ".join(["参数 %s 出错: %s" % (key, value) for key, value in error_dict.iteritems()])
                raise APIError(HTTP_STATUS_BAD_REQUEST, log_message=error_info)
            except (IndexError, KeyError):
                raise APIError(HTTP_STATUS_BAD_REQUEST, log_message="参数缺失或格式有误")