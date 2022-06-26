from PIL import Image
from bs4 import BeautifulSoup
import requests  
from lxml import etree
import sqlite3

vt = sqlite3.connect("film_veri.sqlite3")
fvt = vt.cursor()
hata=0
page = 1
while page<1505:
    #bs4 ile aldığım listeleme method da boş karakterleri almıyorum
    i = [1,3,4,5,6,8,9,10,11,12,14,15,16,17,18,19]
    j = 0
    url = requests.get("https://www.beyazperde.com/filmler-tum/?page="+str(page))
    soup = BeautifulSoup(url.content, "html.parser")
    dom = etree.HTML(str(soup))

    movies = soup.find_all(class_="mdl")
    for movie in movies:  
        directors = []
        vdirector = ""
        kinds = []
        vkind = ""
        actors = []
        vactor =""
        image_name = ""
        
        img_url = movie.find(class_="card entity-card entity-card-list cf").find("a").find("img")
        imgurl = img_url
        name = movie.find("h2").find("a").string        
        
        #Bazen yönetmen sayısı birden fazfa oluyor bunun için 1 tane bile olsa listede sakladım
        try:
            director = movie.find("div",class_="meta-body-item meta-body-direction").find_all(class_="blue-link")
            for direc in director:
                directors.append(direc.string)
                vdirector = vdirector +"_"+direc.string
                
        except:
            vdirector = "bulunamadı"

        #resimlerin adresleri farklı özniteliklerde olabilir
        try:
            img_url = img_url["data-src"]
            img = Image.open(requests.get(img_url,stream=True).raw)
            img_name = name+vdirector+".jpg"
            img_name = "resimler/"+img_name.replace("?","_soru_").replace(":","_ikinokta_").replace("/","_slash_")
            img.save(img_name)
        except:
            try:
                img_url = img_url["src"]
                img = Image.open(requests.get(img_url,stream=True).raw)
                img_name = name+vdirector+".jpg"
                img_name = "resimler/"+img_name.replace("?","_soru_").replace(":","_ikinokta_").replace("/","_slash_")
                img.save(img_name)
            except:
                try:
                    img_url = movie.div.figure.span.img["data-src"]
                    img = Image.open(requests.get(img_url,stream=True).raw)
                    img_name = name+vdirector+".jpg"
                    img_name = "resimler/"+img_name.replace("?","_soru_").replace(":","_ikinokta_").replace("/","_slash_")
                    img.save(img_name)


                except:
                    try:
                        img_url = movie.div.figure.span.img["src"]
                        img = Image.open(requests.get(img_url,stream=True).raw)
                        img_name = name+vdirector+".jpg"
                        img_name = "resimler/"+img_name.replace("?","_soru_").replace(":","_ikinokta_").replace("/","_slash_")
                        img.save(img_name)
                    except:
                        img_name = "bulunamadı"
                        print(name)
                        # print(name+"*************************************Bulunamadı*******************************")
                        hata+=1

            
            
        try:
            date = movie.find("span",class_="date").string
        except:
            date = "bulunamadı"
        
        #etikete sahip olmadığı için xpath kullandım
        sure = dom.xpath('//*[@id="content-layout"]/section[3]/div[2]/ul/li['+str(i[j])+']/div/div[1]/div/div[1]/text()')[2]
        sure = sure.strip()
        
        #farklı sayıda ve farklı konumda veri için geliştiediğim bir çözüm
        kind = movie.find("div",class_="meta-body-item meta-body-info").find_all("span")
        if len(kind) == 3:
            kind = kind[2:]
        else:
            kind = kind[3:]
        
        for ki in kind:
            kinds.append(ki.string)
            vkind = vkind +"_"+ki.string
        

        try:
            actor = movie.find("div",class_="meta-body-item meta-body-actor").find_all()
            actor = actor[1:]
            for ac in actor:
                actors.append(ac.string)
                vactor = vactor+"_"+ac.string
        except:
            vactor = "bulunamadı"
        
        try:
            content = movie.find(class_="content-txt").string
        except:
            content = ""
        
        fvt.execute("INSERT INTO film (name,director,kind,actor,img_url,time,date,content) VALUES (?,?,?,?,?,?,?,?)",(name,vdirector,vkind,vactor,img_name,sure,date,content))
        vt.commit()
        j+=1
        
    print(page)
    print(hata)
    page+=1