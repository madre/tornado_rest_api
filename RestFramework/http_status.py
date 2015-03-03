#!/usr/bin/env python
# coding=utf-8
"""
http status对应的返回文字
__created__ = '2015/3/3'
__author__ = 'deling.ma'
"""

# 成功
HTTP_STATUS_OK = 200
HTTP_STATUS_CREATED = 201
HTTP_STATUS_ACCEPTED = 202
HTTP_STATUS_NOT_MODIFIED = 304

# 客户端错误
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNATHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_METHOD_NOT_ALLOWED = 405
HTTP_STATUS_CONFLICT = 409
HTTP_STATUS_GONE = 410
HTTP_STATUS_UNPROCESSABLE_ENTITY = 422

# 服务器出错
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500
HTTP_STATUS_NOT_IMPLEMENTED = 501

# 列出所有的http status 返回给前端的Message
RESPONSES = {
    100: '继续',
    101: '切换协议',

    200: '请求成功',
    201: '创建成功',
    202: '接受成功',
    203: '第三方非验证信息',
    204: '无内容',
    205: '重置内容',
    206: '不完整内容',

    300: '多选择结果',
    301: '请求被永久转换为新路径',
    302: '重定向',
    303: 'POST重定向为GET',
    304: '未修改可用缓存',
    305: '请通过代理访问',

    400: '客户端请求有误',
    401: "身份验证出错",
    402: '需要支付',
    403: '禁止访问',
    404: '未找到路径',
    405: '不支持该Http方法',
    406: '无法接受该请求',
    407: '代理身份验证未通过',
    408: '客户端请求超时',
    409: '数据冲突，请重新提交',
    410: '服务被移除',
    411: '请添加Content-Length',
    412: '请求条件不足',
    413: '请求数据理过大',
    414: 'URI过长',
    415: '服务器不支持该种数据格式',
    417: '请求头信息格式有误',
    422: '请求语义出错',

    500: '服务器出错',
    501: '服务器无法识别该请求',
    503: '服务器忙碌，请稍候',
    505: '不支持该版本的HTTP请求',
}
