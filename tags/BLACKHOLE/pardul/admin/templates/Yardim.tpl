{{strip}}
{{include file="Header.tpl"}}
{{include file="HataGoster.tpl" Uyari=$Uyari YetkiHataMesaj=$YetkiHataMesaj}}
<table width=100%>
 <tr class=tabbas1><td>YARDIM</td></tr>
</table>

<table border=1 width=50% cellpadding=3>
{{foreach item=AnaSayfa from=$AnaSayfalar}}	
	<tr class=tabbas3><td id="Ana{{$AnaSayfa.No}}">{{$AnaSayfa.Isim}}</td></tr>
	{{foreach item=AltSayfa from=$AnaSayfa.AltSayfalar name=AltSayfa}}		
		{{if $smarty.foreach.AltSayfa.iteration is odd}} <tr class=tabloliste1> {{else}} <tr class=tabloliste2> {{/if}}
			<td>&nbsp;&nbsp;<a href="#Alt{{$AltSayfa.No}}">{{$AltSayfa.Isim}}</a></td>
		</tr>
	{{/foreach}}
{{/foreach}}
</table>

<br><br>

<table border=0 width=50% cellpadding=5 cellspacing=5>
{{foreach item=AnaSayfa from=$AnaSayfalar}}	
	<tr><td class=uyari>{{$AnaSayfa.Isim}}</td><td align=right><a href="#Ana2">Baþa Dön</a></td></tr>
	{{foreach item=AltSayfa from=$AnaSayfa.AltSayfalar name=AltSayfa}}		
		<tr class=tabloliste1> 
			<td colspan=2 align=left id="Alt{{$AltSayfa.No}}"><b>{{$AltSayfa.Isim}}</b></td>
		</tr>
		<tr><td colspan=2>&nbsp;&nbsp;{{$AltSayfa.Metin}}</td></tr>
	{{/foreach}}
{{/foreach}}
</table>
{{/strip}}
