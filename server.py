"""The Python implementation of the GRPC helloworld.Greeter server."""
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from grpc.aio import ServicerContext
from grpc import StatusCode

from proto import hw_pb2, hw_pb2_grpc
from tools.settings import logger


class Greeter(hw_pb2_grpc.GreeterServicer):
    async def SayHello(self, request: hw_pb2.HelloRequest, context: ServicerContext) -> hw_pb2.HelloReply:
        logger.info("say hello")
        name: str = request.name
        # digit name is forbidden
        if name.isdigit():
            logger.warning("invalid Argument: name is digits")
            context.abort(code = StatusCode.INVALID_ARGUMENT, 
                          details="ERROR name cant be digit")


        # metadata
        context.set_trailing_metadata((("key", 'value'),("user", "1")))
        metadata = context.invocation_metadata()
        logger.debug(metadata)
        
        return hw_pb2.HelloReply(message='Hello, %s!' % request.name, 
                                 model=_wrappers_pb2.StringValue(value = "ada"))


    async def SayHelloStreamReply(self, request, context):
        logger.info("say hello stream")
        for single in request.name:
            yield hw_pb2.HelloReply(message='Hello, %s!' % single)
