# Forum Website Example
Deneme amaçlı oluşturulmuş, bir forum sitesinin temel işlevlerini yerine getiren basit bir web sitesidir. Bu web sitesinde;
<ul>
<li>Siteye giren herkes kullanıcıların oluşturduğu başlıkları görebilir.</li>
<li>Siteye üye olan herkes kullanıcıların oluşturdukları başlıkları okuyabilir ve yorum yapabilir.</li>
<li>Kullanıcılar kendi oluşturdukları başlıkları silebilir veya düzenleyebilir, yaptıkları yorumları ise silebilirler.</li>
<li>Moderatör olmayı belirten isModerator flag'i etkinleştirilmiş olan kullanıcılar bütün yorumları ve başlıkları silebilir. Bütün başlıkları yoruma açabilir veya kapatabilir.</li>
</ul>

## Açıklamalar
Bu web sitesi örneği Python 3.8.10 ve Flask 2.0.1 versiyonu kullanılarak deneme amaçlı oluşturulmuştur.

***Flask 2.0 versiyonundan itibaren değişmiş olan yeni routing metodları kullanıldığından 2.0 öncesi versiyonlarda hata verecektir!***

Uygulamanın HerokuApp üzerinde çalışan versiyonu için
<a target="_blank" href="https://forum-website-regaipkurt.herokuapp.com/">tıklayın!</a>

Test Kullanıcısı E-mail: 	***sanane@gmail.com***

Test Kullanıcı Parolası: ***sanane06***

## 1. Veritabanı Yapısı
Veritabanı SQLite veritabanı kullanılarak oluşturulmuştur. Tek bir database dosyası içinde oluşturulan Users, Messages ve Posts tabloları kullanılarak bir forum sitesindeki en temel işlemler 
yerine getirilmeye çalışılmıştır.

### ***User*** tablosu için Create ifadesi aşağıdaki gibidir:
```sql
CREATE TABLE "User" (
	"id"	INTEGER NOT NULL UNIQUE,
	"username"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"isModerator"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
); 
```
User verirabanında password hash algoritması için NIST tarafından standart olarak kabul edilen pbkdf2 algoritması kullanılmıştır.

### ***Post*** tablosu için Create ifadesi:
```sql
CREATE TABLE "Post" (
	"id"	INTEGER NOT NULL UNIQUE,
	"ownerID"	INTEGER NOT NULL,
	"header"	TEXT NOT NULL,
	"body"	TEXT NOT NULL,
	"openComments"	INTEGER NOT NULL,
	"postDate"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
```

### Son olarak ***Message*** tablosu için Create ifadesi:
```sql
CREATE TABLE "Message" (
	"id"	INTEGER NOT NULL UNIQUE,
	"ownerID"	INTEGER NOT NULL,
	"postID"	INTEGER NOT NULL,
	"message"	TEXT NOT NULL,
	"messageDate"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
```
</code></pre>

## 2. Yükleme adımları
***a) HerokuApp Yükleme Adımları***
- Heroku'yu <a href="https://devcenter.heroku.com/articles/heroku-cli#download-and-install" target="_blank">buradan</a> indirerek bilgisayarınıza yükleyin. 
- <a href="https://dashboard.heroku.com/" target="_blank">Heroku Dashboard</a> sayfanız üzerinden bir app oluşturun

- Bu repoyu ```git clone https://github.com/RegaipKURT/ForumWebsiteExample``` komutu ile bilgisayarınıza alın.
- İndirilen klasör içine girerek önce heroku login komutunu çalıştırın ve tarayıcı üzerinden hesabınıza giriş yapın.
- İndirilen kasör içindeki ".git" dosyasını silin ve ardından ```git init ``` komutunu klasör içinde çalıştırın.
- Uygulamayı hesabınıza eklemek için ```heroku git:remote -a "uygulama_adınız"``` komutunda "uygulama_adınız" yerine oluşturduğunuz heroku uyugulamanızın adını yazın
- Daha sonra normal bir git reposuna ekleme yapar gibi şu üç komutu çalıştırın: ```git add .```, ```git commit -m "yükleme mesajınız"``` ve ardından ```git push heroku master```

Bu adımların ardından uygulamanız heroku üzerinde deploy edilecektir.

## ÖNEMLİ NOT:

Uygulama deneme amaçlı yapılmış ve güvenlik bakış açısıyla test edilmemiştir. Bu yüzden heroku üzerinde çalışan sisteme kaydolurken lütfen başka sistemlerde kullandığınız kullanıcı adı ve parolası ile kayıt yapmayın.