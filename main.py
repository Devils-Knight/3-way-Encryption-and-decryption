#This is the main file compiling all the modelue for the given project
from captcha import captcha
from stegno import stegno
c=captcha() #Object for captcha class
s=stegno() #Object for stegno class

def main():
    print("*************Welcome to 3 way encryption & decryption method*************\n\t\t\t\t\tBY- Shubham malik\n")
    while True:
        choice=input("Do you want to encrypt or decrypt(e/d/q): ")
        if choice=="E" or choice=="e":
            image_loc=input("\nEnter the image name: ")
            captcha_loc=input("Enter the created captcha image name: ")
            embed_loc=input("Enter the embedded message image name: ")            
            c.drawcaptcha(image_loc,captcha_loc)
            special_num=c.get_special_num()
            s.embed(embed_loc,captcha_loc,special_num)
        elif choice=="D" or choice=="d":
            encrypt_loc=input("\nEnter the encrypted image name: ")
            captcha=input("Enter the captcha: ")
            special_num_2=c.special_number(captcha)
            message=s.extract(encrypt_loc,special_num_2)
            print("Message: ",message,"\n\n")
        else:
            break


if __name__ == '__main__':
    main()