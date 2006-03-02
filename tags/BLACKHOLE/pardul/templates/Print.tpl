{{strip}}
<body onload="javascript:print();">
<table border=0 width=100% cellpadding=5>
{{if $Haberler}}
{{foreach item=Haber from=$Haberler name=Haber}}
 		<tr><td colspan="3"><h1>{{$Haber.Baslik}}</h1><span class="Tarih"><br><b>{{$Haber.HaberSlogan}}</b><br><br>{{$Haber.Tarih}} - {{$Haber.Kaynak}}</span><hr></td></tr>
 		<tr><td  colspan="3">{{$Haber.Icerik}}</td></tr>
{{/foreach}}
{{/if}}
{{if $Soylesiler}}
{{foreach item=Soylesi from=$Soylesiler name=Soylesi}}
	<tr>
	<td>
	{{$Soylesi.SoylesiIcerik}}<br>
	</td>
</tr>
{{/foreach}}	
{{/if}}
{{if $KoseYazilari}}
{{foreach item=KoseYazi from=$KoseYazilari name=KoseYazi}}
	<tr>
	<td>
	<h1>{{$KoseYazi.Konu}}</h1><br>
	</td>
	</tr>
	<tr>
	<td>
	{{$KoseYazi.Icerik}}<br>
	</td>
</tr>
{{/foreach}}
{{/if}}
</table>
</body>
{{/strip}}
