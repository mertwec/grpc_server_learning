import asyncio
from concurrent import futures

import grpc
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from grpc_reflection.v1alpha import reflection

from proto import hw_pb2_grpc
from server import Greeter
from tools.settings import logger, settings
from tools.interseptors import AsyncExceptionToStatusInterceptor


_cleanup_coroutines = []


async def collect_health_service(server: grpc.Server, service_names: list|tuple):
    health_servicer = health.HealthServicer(
        experimental_non_blocking=True,
        experimental_thread_pool=futures.ThreadPoolExecutor(max_workers=3),
    )
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    for service in service_names:
        health_servicer.set(service, health_pb2.HealthCheckResponse.SERVING)


async def collect_greeter_servince(server):
    hw_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)


async def serve(grpc_channel, workers):

    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=workers),
                             interceptors=[AsyncExceptionToStatusInterceptor(), ])    
    
    SERVICES_NAMES = (
        settings.SERVICE_NAME,        
        health.SERVICE_NAME,
        reflection.SERVICE_NAME,
    )    
    logger.info(f"services: {SERVICES_NAMES}")
    
    await collect_greeter_servince(server)
    await collect_health_service(server, SERVICES_NAMES)
    
    reflection.enable_server_reflection(service_names=SERVICES_NAMES, 
                                        server=server)
    
    server.add_insecure_port(grpc_channel)
    logger.info("Server started, listening on " + settings.grpc_channel)
    await server.start()
    
    async def server_graceful_shutdown() -> None:
        logger.info("Starting graceful shutdown...")
        await server.stop(5)
        logger.info('Server stopped')

    _cleanup_coroutines.append(server_graceful_shutdown())
    
    await server.wait_for_termination()



if __name__ == "__main__":
    
    # asyncio.run(serve(grpc_channel=settings.grpc_channel, 
    #                   workers=settings.WORKERS))
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(
            serve(grpc_channel=settings.grpc_channel, workers=settings.WORKERS)
            )
    except KeyboardInterrupt:
        logger.info("stop server manualy")
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
