{{strip}}
<BODY bgcolor="#999999">
{{include file="TableTop.tpl"  bgcolor="#FFFFFF"}}
<title>Yorum Ekle</title>
{{if $Gonderildi}}
        <br><br>
        <center class=uyari>{{t}} Yorumunuz kaydedildi. Te�ekk�rler{{/t}}</center>
{{else}}
<table width=100% cellpadding=5>
<form action="{{$Burasi}}" method="POSt" onsubmit="return kontrol(this);">
        <tr>
                <td>
                <h3>{{$Baslik}}</h3>
                </td>
        </tr>
        <tr>
                <td><b>{{$HaberSlogan}}</b></td>
        </tr>
        <tr>
                <td colspan=5><h2>{{t}}Bu Haber Hakk�ndaki Yorumunuz :{{/t}}</h2></td>
        </tr>
        <tr>
                <td colspan=5><b>{{t}}G�r��leriniz :{{/t}}</b></td>
        </tr>
        <tr>
                <td colspan=5 align=center>
                  <textarea name="N_Yorum" cols=60 rows=15 alt="G�r���n�z"></textarea>
                </td>
        </tr>
        <tr>
                <td colspan=5 align=right><input type=submit name="Gonder" value="{{t}}G�nder{{/t}}" class=buton></td>
        </tr>
        <input type="hidden" name="No" value="{{$No}}">
</form>
</table>
{{/if}}
{{include file="TableFoot.tpl"}}
</BODY>
{{/strip}}
