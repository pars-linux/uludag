{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari}}
<table border=1 width=100% align=center cellpadding=3>
 <form action="{{$Burasi}}" method="POST" onsubmit="return kontrol(this);">
 <tr class=tabbas1><td colspan=3><b>YEN� S�STEM DE���KEN� EKLEME :</b></td></tr>
 <td width=15%><b>Kategori</b></td>
  <td colspan=2>
    <select name="Kategori" alt="Kategori">
     {{html_options options=$Kategoriler}}
    </select> 
    ya da yeni kategori <input type="text" name="YeniKategori">
  </td>
 </tr>

 <tr>
  <td><b>Degi�ken �smi</b></td>
  <td><input type="text" name="N_Isim" size=20 alt="De�i�ken ismi"></td>
  <td>T�rk�e karakter kullanmay�n�z!</td>
 </tr>

 <tr>
  <td><b>Deger</b></td>
  <td><input type="text" name="N_Deger" size=20 alt="De�er"></td>
  <td>&nbsp;</td>
 </tr>

 <tr>
  <td><b>A��klama</b></td>
  <td><textarea name="N_Aciklama" cols=40 rows=7 alt="A��klama"></textarea></td>
  <td>Y�netici i�in de�i�kenin hangi ama� i�in kullan�ld���n� belirten a��klama.</td>
 </tr>

 <tr>
  <td><b>De�erler</b></td>
  <td><textarea name="Degerler" cols=40 rows=7></textarea></td>
  <td>De�i�ken se�meli de�erlerden birini al�rsa burada "Yapilsin,Yapilmasin" vb. gibi girilmelidir!</td>
 </tr>

 <tr>
  <td><b>Durum</b></td>
  <td>
    <input type="radio" name="Durum" value="Genel" checked id="Genel"><label for="Genel">Genel</label>&nbsp;&nbsp;
    <input type="radio" name="Durum" value="Ozel" id="Ozel"> <label for="Ozel">�zel</label>
  </td>
  <td>Y�neticinin g�r�p de�i�tirebilece�i de�i�kenler "Genel", g�rmemesi gereken ve bize �zel olan de�i�kenler ise "�zel" olmal�d�r.</td>
 </tr>

 <tr><td colspan=3 align=right><input type="submit" name="Ekle" value="Ekle" class=onay></td></tr> 
	 


 </form>
</table>
<br><hr><span class=uyari>Dikkat:</span> Sistem de�i�kenleri i�lem dosyalar�nda (*.php) "$sistem_DegiskenAdi" olarak kullanilir. Ayni degiskeni template dosyasinda { {$sistem_DegiskenAdi} } olarak kullanabilirsiniz.<br>

<table border=1 width=100% cellpadding=5 style="border-collapse:collapse">
 <tr class=tabbas1>
   <td>�sim</td>
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
