{{strip}}
<script language="JavaScript">TamEkran();</script>
<title>�ye G�r�� Cevapla</title>
{{include file=HataGoster.tpl Uyari=$HataMesaj}}
<table border=0 width=100% cellpadding=3>
	<tr class=tabbas3>
		<td>{{$AdSoyad}}</td>
		<td align=right>{{$EPosta}} | {{$GondermeTarih}}</td>
	</tr>
	<tr class=tabbas2>
		<td colspan=2>{{$Mesaj}}</td>
	</tr>		
</table>
<br><br>
{{if $Cevap}}
<table border=0 width=100% cellpadding=3>
    <tr class=tabbas1>
        <td>Cevaplayan : {{$Cevaplayan}}</td>
        <td align=right>{{$CevapTarih}}</td>
    </tr>
    <tr class=tabbas2>
        <td colspan=2>{{$Cevap}}</td>
    </tr>
</table>
{{/if}}

<br><br>

{{if NOT $Cevap}}
<table border=0 width=100% cellpadding=3>
<form action="{{$Burasi}}" method="POST" onsubmit="return kontrol(this)">	
	<tr class=tabbas1>
		<td colspan=2>CEVAP G�NDERME</td>
	</tr>
	<tr>
		<td><b>Ba�l�k : </b></td>
		<td><input type=text name="N_Baslik" size=30 alt="EPosta i�in ba�l�k"></td>
	</tr>
	<tr>
        <td><b>Cevap : </b></td>
        <td><textarea name="N_Cevap" cols=60 rows=13 alt="EPosta i�in cevap"></textarea></td>
    </tr>
	<tr>
		<td colspan=2 align=right><input type="submit" name="Gonder" value="G�nder" class=onay></td>
	</tr>
	<input type="hidden" name="No" value="{{$No}}">
</form>
</table>
{{/if}}
{{/strip}}
