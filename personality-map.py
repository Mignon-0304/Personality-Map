from flask import Flask, render_template, request

app = Flask(__name__)

#紀錄名字
Name = ['']

#測驗分成四部分，每部分判斷一個人格類型字母，並有一些題目。以下是每個選項對應的比例，如果被選到就要加上這個數字：
part_one = [15, 0, 15, 0, 25, 10, 0, 0, 15, 0, 15, 0, 15]
part_two = [19,0,19,0,19,0,15,0,24,0,19]
part_three = [16, 8, 0, 16, 8, 0, 16, 8, 0, 16, 10, 0, 18, 14, 8, 0, 18, 14, 8, 0]
part_four = [18, 23, 12, 5, 0, 17, 0, 20, 10, 0, 17, 0, 23, 20, 10, 0]

#紀錄四個字母的%數
EorI = [0]
AorS = [0]
OorC = [0]
CorS = [0]

#紀錄四個字母
result=['', '', '', '']

#特質
lol=['獨處內斂','社交','野心勃勃','自持守己','自由開放','傳統保守','資本主義','社會主義']

#四個字母可有以下16種可能：
type=['EAOC','EAOS','EACC','EACS','ESOC','ESOS','ESCC','ESCS','IAOC','IAOS','IACC','IACS','ISOC','ISOS','ISCC','ISCS']

#16張結果圖
pic={'EAOC':'https://i.pinimg.com/736x/dd/9a/13/dd9a13bf3eab2b435f654ec97a7ecf33.jpg', 'EAOS':'https://i.pinimg.com/736x/65/9f/63/659f63e87d10f17eb5a02aee5103fe9e.jpg', 'EACC':'https://i.pinimg.com/736x/f2/ea/c5/f2eac556226833895c0002872888fd76.jpg', 'EACS':'https://i.pinimg.com/736x/aa/a9/1f/aaa91f669dca4a702f8d9686d7d3ad33.jpg', 'ESOC':'https://i.pinimg.com/736x/f6/d1/ad/f6d1ad6fac5d1dedce6b750256b61cb5.jpg', 'ESOS':'https://i.pinimg.com/736x/c8/2b/a8/c82ba86453a6fe210626a6e60b4891bb.jpg', 'ESCC':'https://i.pinimg.com/736x/1c/7c/4e/1c7c4ea9731e4b6fdc1e1cbc01d49a6f.jpg', 'ESCS':'https://i.pinimg.com/736x/eb/30/12/eb30122413a6773087029bf2a697d394.jpg', 'IAOC':'https://i.pinimg.com/736x/89/3c/0e/893c0ec45201771db3f63e30dae81ee6.jpg', 'IAOS':'https://i.pinimg.com/736x/fd/9c/0e/fd9c0e02fc9e60d413b7414493632280.jpg', 'IACC':'https://i.pinimg.com/originals/04/f4/b5/04f4b55d258e690786d0e7b3f50e2ec2.jpg', 'IACS':'https://i.pinimg.com/736x/c8/ed/ab/c8edabf47c0ad09e125bc0ecd87ebf1a.jpg', 'ISOC':'https://i.pinimg.com/736x/63/7b/d4/637bd47cf36d4200ed0bbb713be7d9a6.jpg', 'ISOS':'https://i.pinimg.com/736x/29/b7/0e/29b70ebcd47883311c99b43a9e2f1992.jpg', 'ISCC':'https://i.pinimg.com/736x/f9/57/38/f9573882e1c6f440388bd1dd1c6bdb46.jpg', 'ISCS':'https://i.pinimg.com/736x/a2/96/ba/a296ba92ed7629c9a9b9d212ed511ba8.jpg'}

#避免輸入陣列兩次的東西
F=[0, 0, 0, 0, 0, 0]

@app.route('/') #本頁摘要：得到使用者名字、初始化所有東西
def index():

    #初始化
    Name[0]='' ; EorI[0]=0 ; AorS[0]=0 ; OorC[0]=0 ; CorS[0]=0
    for i in range(6):
        F[i]=0
    for i in range(4):
        result[i]=''

    a = render_template('post.html') #把這隻html召喚出來的魔法
    return a

@app.route('/form', methods=['GET']) #本頁摘要：人格測驗本人
def form():

    a = render_template('green.html')
    a += '''<form action='/personality', methods=['GET']>
    '''

    #以下這段for迴圈：每次讀出一題和該題的所有選項加到a裡面。總共22題，執行22次。
    n=0
    for i in range(22):

        if request.values.get('name') is not None:
            Name[0] = request.values.get('name')

        with open('questions.txt','r') as f: #開啟這個文字檔，然後把裡面的問題讀出來
            ques = f.readlines()[i] #每一次只讀第i行

        a += '''
        <section id="{}"><h4>{}</h4></section>'''.format(i, ques) 
        #建立section，因為等一下想要做出可以「按下選項就跳到下一題」的程式。

        f.close()
        a += '''<label for="radio"></label>''' #開始單選題

        # 以下這段while迴圈：讀出該題所有選項。一個選項就是一行，而F[1]代表讀到哪一行。
        # 所有題目的選項加起來共81行，故條件式：F[1]<81。
        while(n<81):
            with open('options.txt', 'r') as f:
                option = f.readlines()[n]

            if (option == '\n'): #讀到空的行（=只有換行字元），代表一題的所有選項已經都讀完了
                n += 1 #下個題目的選項從本文檔的下一行開始讀
                break #因為本題的選項已經讀完，所以要直接結束while迴圈不讀下一行了。

            else: #沒讀到空的行，代表這是本題的選項之一，要把它變成單選題選項！
                a += '''
                <label><input type="radio" name='option{}' id="radio_{}_{}" value="{}" required='required' 
                onclick=javascript:location.href='#{}'>{}
                </label><br><br>
                '''.format(i, i, n, option, i+1, option)
                # onclick=javascript:location.href='#{}'的意思：用力召喚一個javascript用法onclick。
                # 只要使用者點選這個選項，就會跳到下一個id是i+1的section
                # (id是在剛剛設定的，本選項的id是i，下個選項的id是i+1)，要指名的id前面要加井字號。
                n += 1

    a += '''
    <br><br><p class='submit'>作答完成: </p><input type='submit'></form><br><br>'''

    return a

@app.route('/personality', methods=['GET']) #本頁摘要：輸出測驗結果
def personality():
    html = []
    for i in range(22): #得到使用者所有22題的答案，加進陣列
        choice = request.values.get('option{}'.format(i))
        html.append(choice.strip()) #strip()：要去掉程式碼自己生出來的字元，例如換行字元，再加進陣列

    a = []
    #以下這段for迴圈：
    for i in range(81):
        with open('options.txt','r') as f:
            ques = f.readlines()[i]
        if ques == '\n':
            continue

        if ques not in a:
            a.append(ques.strip())
        f.close()
    #part_one計算：人格類型的第一個字母，共六題。
    for i in range(6):
        for j in range(13):
            if html[i] == a[j]: 
            #html是使用者的回答，六題就有六個回答。a代表題目的所有選項，這六題共13個選項。
                EorI[0] += part_one[j] #找到使用者選的選項後，加上那個選項占的%數
                break
    #part_two計算
    for i in range(5):
        for j in range(11):
            if html[6+i] == a[13+j]: #從第七題開始
                AorS[0] += part_two[j]
                break
    #part_three計算
    for i in range(6):
        for j in range(20):
            if html[11+i] == a[24+j]:
                OorC[0] += part_three[j]
                break
    #part_four計算
    for i in range(5):
        for j in range(16):
            if html[17+i] == a[44+j]:
                CorS[0] += part_four[j]
                break

    #下面四個if else：產出四個字母組成一個人格類型！
    if EorI[0]>=50:
        result[0]='I'
    else:
        result[0]='E'

    if AorS[0]>=50:
        result[1]='A'
    else:
        result[1]='S'

    if OorC[0]>=50:
        result[2]='O'
    else:
        result[2]='C'

    if CorS[0]>=50:
        result[3]='C'
    else:
        result[3]='S'

    person='{}{}{}{}'.format(result[0], result[1], result[2], result[3])
    imgurl=pic[person] #從pic裡面挑出 'person'代表的人格特質 的 圖片網址

    #紀錄每個特質佔了多少%
    I=EorI[0]
    E=100-EorI[0]
    A=AorS[0]
    S1=100-AorS[0]
    O=OorC[0]
    C1=100-OorC[0]
    C2=CorS[0]
    S2=100-CorS[0]

    ha=[I, E, A, S1, O, C1, C2, S2] #把每個特質佔了多少%紀錄進一個陣列

    final_result=render_template('final.html')

    final_result+='''
    <body>
    <p class='x'>{}，你的測驗結果為：</p>
    <h1>{}</h1>'''.format(Name[0], person)

    for i in range(8):
        if ha[i]>=50:
            final_result+='''<p class='y'><strong><font size="4">#{} {}% 
  '''.format(lol[i], ha[i]) #把超過50%的特質列出來顯示在網頁上

    final_result+='<br><br>與你最像的國家:</font></strong></p><br>'
    final_result+='''
    <img src="{}"><br>'''.format(imgurl)
    final_result +='''
          <iframe width='10%' src="https://www.youtube.com/embed/lrE8fWHHyW4?si=EGwba7R7v82A2H23&autoplay=1&mute=0&loop=1" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
    '''
    #下面這段：marquee跑馬燈！（好像是過時的代碼但還沒淘汰它的樣子）內容是播放歌曲的名稱。
    #其中，width代表跑馬燈長度；bgcolor代表跑馬燈背景顏色
    final_result+='<marquee width="500" bgcolor=#EAFAA6>歌曲：winter _____ . | peaceful acoustic</marquee>'

    final_result+='''<br><br><a href="/">回首頁</a><br>
    <a href="/all_countries">國家類型一覽</a>
    </body>'''

    return final_result

@app.route('/all_countries') #本頁摘要：所有國家、人格類型
def all_countries():
    html='<title>All Types 國家類型一覽</title><h1 align="center" style="white-space: nowrap;"><font color="#FFFFFF" style="background-color:#CA8B4F;">-國家類型一覽-</font></h1>'
    for i in range(16):
        html+='''<h1 align="center">{}.{}<br>
        <img src="{}" width="400px"></h1>'''.format(i+1,type[i], pic[type[i]])
    html +='''<br><center><a href="/">回首頁</a></center>'''

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)