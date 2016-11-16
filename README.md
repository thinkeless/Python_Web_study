# Python_Web_study
##1.log大法
```python
def log(*args, **kwargs):
  print('log', *args, **kwargs)
```
##2.server 接收 request, 并根据path 返回 response
```python
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
