{{strip}}
<!-- Haber Icerikleri -->
<table border=0 width=100% cellpadding=5>
{{if $Haberler}}
 {{foreach item=Haber from=$Haberler name=Haber}}
         {{if $Detay}}

                 <tr><td><h1>{{$Haber.Baslik}}</h1></td><td class="Tarih">{{$Haber.Tarih}}</td></tr>
                 <tr><td>{{$Haber.Icerik}}<br><br></td></tr>
         {{else}}
                 <tr>
                 <TD>
                         <h1>{{$Haber.Baslik}}</h1>
                         {{$Haber.HaberSlogan}} <div id="devam2"><a href="{{$SSayfa}}Haberler&HaberNo={{$Haber.No}}">{{t}} Devamı için...{{/t}}</a></div>
                 </TD></tr>
        {{/if}}
 {{/foreach}}
{{else}}
 <tr><td align=center><b>{{t}}Kayıtlı Haber bulunmamaktadır.{{/t}}</b></td></tr>
{{/if}}
</table>
{{/strip}}
