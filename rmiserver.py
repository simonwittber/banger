import asyncio
import json

def dispatch(obj):
    print(obj)

async def handle_client(reader, writer):
    while True:
        data = await reader.readline()
        if len(data) == 0: break

        message = data.decode()
        try:
            obj = json.loads(message)
        except Exception as e:
            writer.close()
            print(e)
            break

        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")

        response = dispatch(obj)
        if response is not None:
            response_data = json.dumps(response)
            write.write(response_data)
            await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8889)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())
