# ForumWebsiteExample

## Açıklamalar
Bu web sitesi örneği Python 3.8.10 ve Flask 2.0.1 versiyonu kullanılarak deneme amaçlı oluşturulmuştur.

***Flask 2.0 versiyonundan itibaren değişmiş olan yeni routing metodları kullanıldığından 2.0 öncesi versiyonlarda hata verecektir!***

Uygulamanın HerokuApp üzerinde çalışan versiyonu için
<a target="_blank" href="https://forum-website-regaipkurt.herokuapp.com/">tıklayın!</a>

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