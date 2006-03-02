{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari}}
<table border=1 width=100% align=center cellpadding=3>
 <form action="{{$Burasi}}" method="POST" onsubmit="return kontrol(this);">
 <tr class=tabbas1><td colspan=3><b>YENÝ SÝSTEM DEÐÝÞKENÝ EKLEME :</b></td></tr>
 <td width=15%><b>Kategori</b></td>
  <td colspan=2>
    <select name="Kategori" alt="Kategori">
     {{html_options options=$Kategoriler}}
    </select> 
    ya da yeni kategori <input type="text" name="YeniKategori">
  </td>
 </tr>

 <tr>
  <td><b>Degiþken Ýsmi</b></td>
  <td><input type="text" name="N_Isim" size=20 alt="Deðiþken ismi"></td>
  <td>Türkçe karakter kullanmayýnýz!</td>
 </tr>

 <tr>
  <td><b>Deger</b></td>
  <td><input type="text" name="N_Deger" size=20 alt="Deðer"></td>
  <td>&nbsp;</td>
 </tr>

 <tr>
  <td><b>Açýklama</b></td>
  <td><textarea name="N_Aciklama" cols=40 rows=7 alt="Açýklama"></textarea></td>
  <td>Yönetici için deðiþkenin hangi amaç için kullanýldýðýný belirten açýklama.</td>
 </tr>

 <tr>
  <td><b>Deðerler</b></td>
  <td><textarea name="Degerler" cols=40 rows=7></textarea></td>
  <td>Deðiþken seçmeli deðerlerden birini alýrsa burada "Yapilsin,Yapilmasin" vb. gibi girilmelidir!</td>
 </tr>

 <tr>
  <td><b>Durum</b></td>
  <td>
    <input type="radio" name="Durum" value="Genel" checked id="Genel"><label for="Genel">Genel</label>&nbsp;&nbsp;
    <input type="radio" name="Durum" value="Ozel" id="Ozel"> <label for="Ozel">Özel</label>
  </td>
  <td>Yöneticinin görüp deðiþtirebileceði deðiþkenler "Genel", görmemesi gereken ve bize özel olan deðiþkenler ise "Özel" olmalýdýr.</td>
 </tr>

 <tr><td colspan=3 align=right><input type="submit" name="Ekle" value="Ekle" class=onay></td></tr> 
	 


 </form>
</table>
<br><hr><span class=uyari>Dikkat:</span> Sistem deðiþkenleri iþlem dosyalarýnda (*.php) "$sistem_DegiskenAdi" olarak kullanilir. Ayni degiskeni template dosyasinda { {$sistem_DegiskenAdi} } olarak kullanabilirsiniz.<br>

<table border=1 width=100% cellpadding=5 style="border-collapse:collapse">
 <tr class=tabbas1>
   <td>Ýsim</td>
   <td>Kategori</td>
   <td>Deger</td>
   <td>Aciklama</td>
   <td>Degerler</td>
   <td>Durum</td>
 </tr>
 {{foreach item=Degisken from=$Degiskenler name=Degiskenler}}
 {{if $smarty.foreach.Degiskenler.iteration is odd}} <tr class=tabloliste1> {{else}} <tr class=tabloliste2> {{/if}}
   <td>{{$Degisken.Isim}}</td>
   <td>{{$Degisken.Kategori}}</td>
   <td>{{$Degisken.Deger}}</td>
   <td>{{$Degisken.Aciklama}}</td>
   <td>{{$Degisken.Degerler}}</td>
   <td>{{$Degisken.Durum}}</td>
 </tr>
 {{/foreach}}
</table>
{{/strip}}
