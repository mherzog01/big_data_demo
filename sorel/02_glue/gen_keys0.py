import asyncio

def logmsg(msg):
    print(msg)

logmsg('Starting jobs')
padding = 2
for i in range(256):
    filter_chars = f'{i:0{padding}x}'
    print(i, filter_chars)
    asyncio.run(asyncio.create_subprocess_shell(f'python3 gen_keys.py {filter_chars}'))
    #if i > 2:
        #break
logmsg('Complete')
