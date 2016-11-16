import socket
import ssl

"""
作业 1
8.10

请参考上课板书内容
"""


# 1
# 补全函数 parsed_url
def parsed_url(url):
    '''
    url 可能的值如下
    g.cn
    g.cn/
    g.cn:3000
    g.cn:3000/search
    http://g.cn
    https://g.cn
    http://g.cn/

	NOTE:
    没有 protocol 时, 默认协议是 http

    在 http 下 默认端口是 80
    在 https 下 默认端口是 443
    :return : tuple, 内容如下 (protocol, host, port, path)
    '''

    #check the protocol
    protocol = 'http'
    if url[:7] == 'http://':
        u = url[7:]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url[8:]
    else:
        u = url

    #check the path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    #check the port
    port_dic = {
        'http': 80,
        'https': 443
    }
    port = port_dic[protocol]
    if host.find(':') != -1:
        h = host.split(':')
        host = h[0]
        port = h[1]

    return protocol, host, port, path


# 2
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下


def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)
    headers = {}
    for line in h[1:]:
        key, value = line.split(': ')
        headers[key] = value
    return status_code, headers, body


def get(url):
    '''
    返回的数据类型为 bytes
    '''
    protocol, host, port, path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nCollection:close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)
    status_code, headers, body = parsed_response(r)
    if status_code == 301:
        url = headers['Location']
        return get(url)
    return status_code, headers, body

"""
资料:
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型
"""


# 使用
def main():
    url = 'http://movie.douban.com/top250'
    response = get(url)
    print(response)


if __name__ == '__main__':
    main()
