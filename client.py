"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import logging
import time

import grpc

from proto import hw_pb2, hw_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = hw_pb2_grpc.GreeterStub(channel)
        for i in range(3):
            time.sleep(1)
            print('.'*(i+1))
        response = stub.SayHello(hw_pb2.HelloRequest(name='NAME'))

    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
