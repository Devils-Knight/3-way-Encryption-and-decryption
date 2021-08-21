import cv2
import AES

class stegno:
    def __init__(self):
        self.__signature=500

    def getbits(self,variable):
        return [variable>>5,(variable>>2)&7,variable&3]

    def getbyte(self,bits):
        return (((bits[0]<<3)| bits[1])<<2)| bits[2]

    def __embedding_points(self,number):
        # taking the normalized size of captcha image i.e(300,100)
        # and also using the special number(0,50) using captcha we have to find points
        #points will lie in range(0+number,300-number) and increasing y
        #p.s you can add your special and complex algoritm to randomize the points to make it more secure
        x=number
        # interval=number%10
        y=1
        points=[]
        for _ in range(self.__signature):
            if(x<(200-number)): 
                x+=5 
            else:
                x=number
                y+=2
            points.append((y,x))
        return points
    def __normalize_signature(self,x):
        return x[:self.__signature].ljust(self.__signature,'*')

    def embed(self,resultImage, srcImage,number):
        image = cv2.imread("image/"+srcImage, cv2.IMREAD_COLOR)
        if image is None:
            print(srcImage, 'not found')
            return
        message=input("Write your message: ")
        message=AES.Encryption(message)
        normalized = self.__normalize_signature(message)
        embedAt = self.__embedding_points(number)
        cnt = 0
        for x, y in embedAt:
            data = ord(normalized[cnt]) #ord gives the ASCII of the character
            bits = self.getbits(data)
            image[x][y][2] = (image[x][y][2] & ~7) | bits[0] #red band
            image[x][y][1] = (image[x][y][1] & ~7) | bits[1]#green band
            image[x][y][0] = (image[x][y][0] & ~3) | bits[2]#blue band
            cnt+=1
        #save back
        cv2.imwrite("image/"+resultImage, image)
        print("\n<<<<<<<<<<<< Message Embedded >>>>>>>>>>>>>\n\n")

    def extract(self,resultImage,number):
        image = cv2.imread("image/"+resultImage, cv2.IMREAD_COLOR)
        if image is None:
            print(resultImage, 'not found')
            return
        extractFrom = self.__embedding_points(number)
        cnt = 0
        sign = ''
        for x, y in extractFrom:
            bit1 = (image[x][y][2] & 7) #red band
            bit2 = (image[x][y][1] & 7)#green band
            bit3 = (image[x][y][0] & 3)#blue band
            data = self.getbyte([bit1,bit2,bit3])
            sign = sign+ chr(data) #chr converts ASCII to text
            cnt+=1
        #remove the padding
        sign.strip('*')
        try:
            message=AES.Decryption(sign)
            return message
        except:
            return None