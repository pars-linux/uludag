{{strip}}
<table border=0 width="100%" cellpadding=2>
{{section name=k loop=$Menuler}}
{{if $Menuler[k].AltMenuler}}
{{assign var="S" value=$Menuler[k].Sira}}
<tr>
    <td class=menu><b>{{$Menuler[k].Isim}}</b></td>
</tr>
    {{foreach item=Eleman from=$Menuler[k].AltMenuler}}
    <tr><td style="padding-left:10px"><a class="menu" href="{{$AdminAnaSayfa}}/index.php?Page={{$Eleman.Adres}}">{{$Eleman.Isim}}</a></td></tr>
    {{/foreach}}
{{else}}
    <tr><td style="padding-left:10px"><a class="menu" href="{{$AdminAnaSayfa}}/index.php?Page={{$Menuler[k].Adres}}">{{$Menuler[k].Isim}}</a>[!]</td></tr>
{{/if}}
{{/section}}
</tr>
</table>
{{/strip}}