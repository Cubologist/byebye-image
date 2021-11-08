
from PIL import Image
import numpy as np

def open_img():
    f = open("Test2.jpg", "rb")  # Creats a file in Read Binary mode
    image = Image.open("Test2.jpg")  # Opens the image Test.png
    f.close()
    image = np.array(image)  # Converts the Image into a numpy array

    global row
    global column
    global w
    global b
    global b1

    row = image.shape[0]  # Points to the row
    column = image.shape[1]  # Points to the column
    w = image.shape[2]
    b = np.ones((row, column, w))
    b = b.astype(int)
    b1 = np.ones((w, column, row))
    b1 = b1.astype(int)

    return image

def Key():  # Takes the input from the user and takes the n value to generate various keys from the inputed key
    kk1 = abs(hash(input("enter the  key")))
    ke1 = [int(x) for x in str(kk1)]
    k2 = abs(hash(hex(kk1 % 99999)))
    ke2 = [int(y) for y in str(k2)]
    key_list = ke1 + ke2 # creates a master key list
    k1 = int(key_list[0] + key_list[2] + key_list[3])#takes 3 random integers from the keylist
    k2 = int(abs(key_list[0] - key_list[2] + key_list[4]))
    k3 = int(abs(key_list[1] + key_list[2] - key_list[3]))
    key_arr = np.array(key_list)
    key_arr = np.repeat(key_arr, (row * column * 3) / key_arr.size)#expands the array by repeating it
    if (key_arr.size < (row * column * w)):
        for i in range((row * column * w) - key_arr.size):
            key_arr = np.append(key_arr, [0])
    key_arr = np.reshape(key_arr, (row, column, w))
    key_arr1 = np.reshape(key_arr, (w, column, row))
    key_arr1= key_arr1.astype(int)
    key_arr = key_arr.astype(int)
    return key_arr , k1 , key_arr1 , k2 , k3

def shfenc(RGB_e):#swaps rows and columns for encoding
    i = 0
    while i < (row // 2):
        RGB_e[[i, (row - 1) - i], :] = RGB_e[[(row - 1) - i, i], :]
        i += 1
    j = 0
    while j < (column // 2):
        RGB_e[:, [j, (column - 1) - j]] = RGB_e[:, [(column - 1) - j, j]]
        j += 1
    return RGB_e

def shfdec(RGB_d): #swaps rows and colums for decoding
    i = 0
    while i < (row // 2):
        RGB_d[[(row - 1) - i, i], :] = RGB_d[[i, (row - 1) - i], :]
        i += 1
    j = 0
    while j < (column // 2):
        RGB_d[:, [(column - 1) - j, j]] = RGB_d[:, [j, (column - 1) - j]]
        j += 1
    return RGB_d

def enc():
    image = open_img()
    l = Key()
    key_arr=l[0]
    k1=l[1]
    key_arr1 = l[2]
    k2 = l[3]
    k3 = l[4]

    image = image.astype(int)
    global RGB

    RGB_enc = image * (key_arr + b)
    RGB_enc = shfenc(RGB_enc)
    RGB_enc = RGB_enc ^ k1
    RGB_encode = np.transpose(RGB_enc)

    RGB_encode = RGB_encode * (key_arr1 + b1)
    RGB_encode = RGB_encode ^ k2
    RGB_encode = np.transpose(RGB_encode)

    RGB_encode = RGB_encode * (key_arr + b)
    RGB_encode = shfenc(RGB_encode)
    RGB_encode = RGB_encode ^ k3
    RGB = np.transpose(RGB_encode)


    RGB_encrypt = RGB.astype(np.uint8)  # converts the entire matrix to uint
    RGB_encrypt = np.reshape(RGB_encrypt, (row, column, w))
    img = Image.fromarray(RGB_encrypt)  # Saves the image
    img.save("ENC.jpeg")
    print("ENCRYPTED!!!!!--------------------------------------------------------")

def dec():
    l = Key()
    key_arr = l[0]
    k1 = l[1]
    key_arr1 = l[2]
    k2 = l[3]
    k3 = l[4]
    RGB_dec = RGB


    RGB_dec = np.transpose(RGB_dec)
    RGB_dec = RGB_dec.astype(int)
    RGB_dec = RGB_dec ^ k3
    RGB_dec = shfdec(RGB_dec)
    RGB_dec = RGB_dec / (key_arr + b)

    RGB_dec = np.transpose(RGB_dec)
    RGB_dec = RGB_dec.astype(int)
    RGB_dec = RGB_dec ^ k2
    RGB_dec = RGB_dec / (key_arr1 + b1)

    RGB_dec = np.transpose(RGB_dec)
    RGB_dec = RGB_dec.astype(int)
    RGB_dec = RGB_dec ^ k1
    RGB_dec = shfdec(RGB_dec)
    RGB_dec = RGB_dec / (key_arr + b)

    RGB_decrypt = RGB_dec.astype(np.uint8)
    img = Image.fromarray(RGB_decrypt)  # Saves the image
    img.save("DEC.jpeg")
    print("DECRYPTED!!!!!--------------------------------------------------------")

if __name__=="__main__":
    enc()
    dec()


