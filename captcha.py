from PIL import Image,ImageDraw,ImageFont
import random

class captcha:
    def __init__(self):
        self.__special_num=0

    def __getcaptcha(self):
        alphabets_array=list(map(lambda y:chr(y),list(filter(lambda x: x<91 or x>96,list(range(65,123))))))
        number_array=list(map(str,range(0,10)))
        num_count=random.randint(1,3)
        captchaa=[]
        for i in range(5):
            if i<num_count:
                captchaa.append(random.choice(number_array))
                continue
            else:
                captchaa.append(random.choice(alphabets_array))
        random.shuffle(captchaa)
        captchaa="".join(captchaa)
        self.__special_num=self.special_number(captchaa)
        return captchaa

    def special_number(self,captcha):
        #I have generated basic special number you can add more complexity to it
        num=0
        for i in captcha:
            num+=ord(i)
        return num%50

    def get_special_num(self):
        return self.__special_num

    def drawcaptcha(self,Image_location,Final_location):
        canvas=Image.open("image/"+Image_location)
        size=canvas.size
        pen=ImageDraw.Draw(canvas)
        fnt = ImageFont.truetype('c:/windows/fonts/FREESCPT.TTF', size=85)
        captcha=self.__getcaptcha()
        captcha_size=pen.textsize(text=captcha,font=fnt)
        fg_color=150,56,10
        pen.text(xy=((size[0]-captcha_size[0])/2, (size[1]- captcha_size[1])/2),text=captcha,font=fnt,fill=fg_color)
        canvas.save("image/"+Final_location)
        print("\n\n<<<<<<<<<<<< Captcha Created >>>>>>>>>>>>>\n")

