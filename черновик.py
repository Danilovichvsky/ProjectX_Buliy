
d={}
d={"1":1,"2":2,"3":3}
d["4"]=4
print(d)

a=1
while a<=5:
    print(a)
    a = a+1

import threading





# Теперь можно перейти к следующему действию
print("Программа продолжает выполнение после завершения потоков")

if __name__ == "__main__":
    def do(n):
        print(f"Поток {n} начал выполнение действия")
        # Какие-то действия, которые выполняются в потоке
        print(f"Поток {n} завершил выполнение действия")


    # Создаем несколько потоков
    p1 = threading.Thread(target=do, args=(1,))
    p2 = threading.Thread(target=do, args=(2,))

    p1.start()
    p2.start()