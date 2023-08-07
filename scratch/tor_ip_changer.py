import asyncio
import errno
import telnetlib3
from time import sleep

localhost = '127.0.0.1'
port = '14999'
timeout = 5


async def main():
    reader, writer = await telnetlib3.open_connection(localhost, port)

    writer.write("tor start\r\n")
    sleep(30)
    writer.write("interval 30\r\n")
    sleep(1)
    writer.write("changeip start\r\n")
    sleep(1)
    writer.write("exit\r\n")

    reply = await reader.read(1024)

    print('reply:', reply)

asyncio.run(main())
