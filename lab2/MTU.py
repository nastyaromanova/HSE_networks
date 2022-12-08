import sys
import subprocess
import platform

def binsearch_request(MTU):
    result = subprocess.run(f'ping {host} -c {count} -D -t 255 -s {MTU}', stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, shell=True)
    # for testing on macos
    if platform.system().lower() == 'darwin':
        if result.returncode == 0:
            return 0, ""
        elif result.returncode == 2:
            return 1, result.stderr
        else:
            return 2, result.stderr
    else:
        return result.returncode, result.stderr

if len(sys.argv) == 3:
    host, count = sys.argv[1], sys.argv[2]
else:
    host, count = sys.argv[1], 1

# print(type(host))
if count is None:
    count = 1
elif not count.isnumeric():
    print('Parameter c must be a number.')
    exit(1)
else:
    count = int(count)

left, right = 64 - 28, 1519 - 28  
while left + 1 < right:
    mid = (left + right) // 2
    # print(f'Last normal result: {left}; Current mid: {mid}')
    returncode, err = binsearch_request(mid)
    if returncode == 0:
        left = mid
    elif returncode == 1:
        right = mid
    else:
        print(f'Something goes wrong. An error is occured: {err}')
        exit(1)

print(f'MTU is {left + 28}')