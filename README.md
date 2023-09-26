## gRPC learning
asynchrony gRPC - server.


### generate proto files
```bash
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. --pyi_out=.  ./proto/*.proto

```
hint: 
```bash 
python3 -m grpc_tools.protoc --help
```

### documentations

grpc_quick-start: https://grpc.io/docs/languages/python/quickstart/
gprc-interseptors: https://grpc-interceptor.readthedocs.io/en/latest/#async-server-interceptors
api: https://grpc.github.io/grpc/python/grpc.html
grpc-reflection: https://github.com/grpc/grpc/blob/master/doc/python/server_reflection.md
grpc_helth-check: https://github.com/grpc/grpc/blob/master/doc/health-checking.md
