{{strip}}
{{include file="Header.tpl"}}
<table border="0" width=100%><tr class=tabbas1><td>�EVR�M��� �YELER</td></tr></table>
<table border=0 width=100% cellpadding=5>
<form action="{{$Burasi}}" method="POST">
<tr class=tabloliste1>
	<td width=3%>Son</td>
	<td width=5%><input type=text name=Dakika value="{{$Dakika}}" class=sayi size=2></td>
 	<td width=30%>dakika i�erisinde i�lem yapan kullan�c�lar�</td>
	<td align=left><input type=submit name=Listele value=Listele class=onay></td>
</tr>
</form>
</table>
<br>
{{if $UyeSayi OR $AnonimSayi}}
	<table border=0 width=100% cellpadding=5>
	<tr>
		<td colspan=2><b>{{$UyeSayi}}</b>&nbsp;<font color="red"><b>�ye</b></font> ve <b>{{$AnonimSayi}}</b><font color="blue"> Misafir</font> �evrimi�i</td>
		<td align=right>Toplam <b>{{$Toplam}}</b> Ziyaret�i</td>
	</tr>
	{{if $UyeSayi}}
	<tr class=tabbas1>
		<td>Kullanici Ad</td>
		<td>Ad Soyad</td>
		<td>Son ��lem Zaman�</td>
	</tr>
	{{foreach item=SonGiris	from=$SonGirisler name=SonGiris}}	
	{{if $smarty.foreach.SonGiris.iteration is odd}} <tr class=tabloliste1> {{else}} <tr class=tabloliste2> {{/if}}
		<td>{{$SonGiris.EPosta}}</td>
		<td>{{$SonGiris.AdSoyad}}</td>
		<td>{{$SonGiris.SonGiris}}</td>
	</tr>
	{{/foreach}}
	{{else}}
		<tr><td colspan=3><center class=uyari>Belirtti�iniz s�rede i�lem yapan �ye bulunamad�.</center></td></tr>
	{{/if}}
	</table>
{{else}}
	<br><br>
	<center class=uyari>Belirtti�iniz s�re zarf�nda i�lem yapan �ye ve misafir ziyaret�i bulunamad�!</center>
{{/if}}
{{/strip}}
