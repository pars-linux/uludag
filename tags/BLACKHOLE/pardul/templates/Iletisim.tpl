{{strip}}
{{if $Kaydedildi}}
        <br><center class="uyari">{{t}}Görüþ ve önerileriniz için teþekkürler...{{/t}}</center>
{{/if}}
<br>
<center><h3>{{t}}ÝLETÝÞÝM FORMU{{/t}}</h3></center>
<table border=0 width=75% cellpadding=5 align=center>
<tr><td colspan=2>{{t}}Sitemizle ilgili görüþ ve önerilerinizi aþaðýdaki form aracýlýðýyla bize iletebilirsiniz.{{/t}}</td></tr>
<form action="{{$Burasi}}" method="POST" onsubmit="javascript:return kontrol(this);">
         {{if NOT $OturumVar}}
    <tr>
                <td width=30% align=right nowrap><b>{{t}}Adýnýz Soyadýnýz :{{/t}}</b></td>
                <td><input type=text name="N_AdSoyad" size=30 alt="{{t}}Adýnýz Soyadýnýz{{/t}}"></td>
        </tr>
    <tr>
                <td align=right nowrap><b>{{t}}E-Posta Adresiniz :{{/t}}</b></td>
                <td><input type=text name="N_EPosta1" size=30 alt="{{t}}E-Posta Adresiniz{{/t}}"></td>
        </tr>
         {{/if}}
    <tr>
                <td align=right nowrap><b>{{t}}Mesajýnýz :{{/t}}</b></td>
                <td><textarea name="N_Mesaj" alt="{{t}}Mesajýnýz{{/t}}" cols=50 rows=10></textarea></td>
        </tr>
         <tr>
                <td colspan=2 align=right><input type="submit" name="Gonder" value="{{t}}Gönder{{/t}}" class=buton></td>
        </tr>
</form>
</table>
{{/strip}}