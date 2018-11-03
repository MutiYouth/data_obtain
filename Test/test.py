import time
# from time import sleep
import sys


i_count = 0
while True:
    i_count += 1

    # sys.stdout.flush()
    print("\rRetrying", end="")
    # time consuming
    # ---------------------------------
    time.sleep(0.5)
    # sleep(100)
    # ---------------------------------
    # sys.stdout.flush()



    print("...", end="")

    # time consuming
    # ---------------------------------
    time.sleep(0.5)
    # sleep(100)
    # ---------------------------------
    # sys.stdout.flush()


    if i_count == 100:
        break

print('done!')




for i in range(10000):
    print("\r已完成    {:.2f}".format(i / 10000 * 100), end="")
    time.sleep(0.1)
