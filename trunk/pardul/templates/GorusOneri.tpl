{{strip}}
{{if $Kaydedildi}}
        <br><center class="uyari">{{t}}G�r�� ve �nerileriniz i�in te�ekk�rler...{{/t}}</center>
{{/if}}
<br>
<center><h3>{{t}}�LET���M FORMU{{/t}}</h3></center>
<table border=0 width=75% cellpadding=5 align=center>
<tr><td colspan=2>{{t}}Sitemizle ilgili g�r�� ve �nerilerinizi a�a��daki form arac�l���yla bize iletebilirsiniz.{{/t}}</td></tr>
<form action="{{$Burasi}}" method="POST" onsubmit="javascript:return kontrol(this);">
         {{if NOT $OturumVar}}
    <tr>
                <td width=30% align=right nowrap><b>{{t}}Ad�n�z Soyad�n�z :{{/t}}</b></td>
                <td><input type=text name="N_AdSoyad" size=30 alt="{{t}}Ad�n�z Soyad�n�z{{/t}}"></td>
        </tr>
    <tr>
                <td align=right nowrap><b>{{t}}E-Posta Adresiniz :{{/t}}</b></td>
                <td><input type=text name="N_EPosta1" size=30 alt="{{t}}E-Posta Adresiniz{{/t}}"></td>
        </tr>
         {{/if}}
    <tr>
                <td align=right nowrap><b>{{t}}Mesaj�n�z :{{/t}}</b></td>
                <td><textarea name="N_Mesaj" alt="{{t}}Mesaj�n�z{{/t}}" cols=50 rows=10></textarea></td>
        </tr>
         <tr>
                <td colspan=2 align=right><input type="submit" name="Gonder" value="{{t}}G�nder{{/t}}" class=buton></td>
        </tr>
</form>
</table>
{{/strip}}