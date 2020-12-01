import threading
from time import sleep

def delayer():
    print("今から処理を始めます！")
    sleep(5)
    print("処理が完了しました。")

def delayer2():
    print("今から長期処理します！")
    sleep(10)
    print("完了しました！")

print("処理中です。")
taskA = threading.Thread(name="taskA", target=delayer)
taskB = threading.Thread(name="taskB", target=delayer2)
taskA.start()
taskB.start()