#Python_Web_study 笔记
##1.log大法
```python
def log(*args, **kwargs):
  print('log', *args, **kwargs)
```
##2.request格式
```python
request = 'GET {} HTTP/1.1\r\nhost:{}\r\nCollection:close\r\n\r\n'.format(path, host)
```
##3.server 接收 request, 并根据path 返回 response
```python
#使用with可以保证在程序中断的时候正确关闭socket并释放占用的端口
with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(3)
            connection, address = s.accept()
            request = connection.recv(1024)
            request = request.decode('utf-8')
            log('ip:{} and request:{}'.format(address, request))
            try:
                path = request.split()[1]
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            connection.close()
```
##4.response格式
```python
def error(code=404):
    e = {
        404: b'HTTP/1.x 404 NOT FOUND \r\n\r\n<h1>NOT FOUND</h1>'
    }
    r = e.get(code)
    return r


def route_index():
    """
    主页的处理函数，返回主页的相应
    """
    header = 'HTTP/1.x 200 OK\r\nContent-Type:text/html\r\n'
    body = '<h1>Hello Python</h1><img src="doge0.gif">'
    r = header + '\r\n' + body
    return r.encode('utf-8')


def route_image():
    with open('doge0.gif', 'rb') as f:
        header = b'HTTP/1.x 200 OK \r\nContent-Type:image/gif\r\n\r\n'
        img = header + f.read()
        return img


def response_for_path(path):
    r = {
        '/': route_index,
        '/doge0.gif': route_image,
    }
    response = r.get(path, error)
    return response()
```
##4.https
```python
import ssl
s = ssl.wrap_socket(socket.socket())
```
