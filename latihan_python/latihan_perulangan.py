# data = []
# for i in range (1, 100):
#     data.append(i)
#     print(i)
#     if i == 20:
#         break
#     for n in range(100,110):
#         print(n)
# print(data)

# angka = [1, 2, 3, 4]
# pangkat = [n**2 for n in angka]
# print(pangkat)

"""
Output:
[1, 4, 9, 16]
"""
"""
Buatlah sebuah variabel bertipe list bernama "evenNumber" dengan ketentuan:
- variabel tersebut menampung bilangan genap dari 0 hingga 500 (ingat 0 dan 500 termasuk).

Tips:
Anda bisa menggunakan loop dan if atau list comprehension untuk memudahkan.
"""

#Silakan buat kode Anda di bawah ini.
evenNumber = []
i = 0
while i <= 500:
    if i % 2 ==0:
        evenNumber.append(i)
    i += 1

print(evenNumber)

# evenNumber = []
# i = 0
# while i <= 500:
#     if i % 2 == 0:
#         evenNumber.append(i)
#     i += 1

# print(evenNumber)
