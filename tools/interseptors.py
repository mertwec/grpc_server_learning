from grpc_interceptor.exceptions import GrpcException
from grpc_interceptor.server import AsyncServerInterceptor
from typing import Callable, Any
import grpc
from tools.settings import logger
              

class AsyncExceptionToStatusInterceptor(AsyncServerInterceptor):
    async def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        context: grpc.ServicerContext,
        method_name: str,
    ) -> Any:
        try:
            response_or_iterator = method(request_or_iterator, context)
            if method_name.split("/")[1] == "grpc.health.v1.Health":    # method_name=='/grpc.health.v1.Health/Check'
                logger.debug("service Health Check is not async")
                return response_or_iterator
            
            if not hasattr(response_or_iterator, "__aiter__"):
                logger.debug("-- unary method")
                # Unary, just await and return the response
                return await response_or_iterator
        except GrpcException as e:
            await context.set_code(e.status_code)
            await context.set_details(e.details)
            raise

        # Server streaming responses, delegate to an async generator helper.
        # Note that we do NOT await this.
        return self._intercept_streaming(response_or_iterator, context)

    async def _intercept_streaming(self, iterator, context):
        try:
            logger.debug("-- stream method")
            async for r in iterator:
                yield r
        except GrpcException as e:
            await context.set_code(e.status_code)
            await context.set_details(e.details)
            raise