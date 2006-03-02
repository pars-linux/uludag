{{strip}}
{{include file="TableTop.tpl"  bgcolor="#FFFFFF"}}
<TABLE border=0 width=96% cellpadding=10 cellspacing=0 align="center">
{{if $Haberler}}
 {{foreach item=Haber from=$Haberler name=Haber}}
         {{if $Detay}}
                 <TR><TD colspan="3"><H3>{{$Haber.Baslik}}</H3><SPAN class="Tarih"><BR><B>{{$Haber.HaberSlogan}}</B><BR><BR>{{$Haber.Tarih}} - {{$Haber.Kaynak}}</SPAN><HR></TD></TR>
                 <TR><TD  colspan="3"><DIV align="justify">{{$Haber.Icerik}}</DIV></TD></TR>
                 <TR>
                 <TD align="right" border="0">
                <TABLE border="0" cellspacing="5" cellpadding="3">
                <tr>
                <td align="center"><img src="{{$WebResimler}}/yorum.png"></td>
                <td align="center"><img src="{{$WebResimler}}/printer.png"></td>
                <td align="center"><img src="{{$WebResimler}}/tavsiye.png"></td>
                <TR>
                <TD align="center">
                <A href="javascript:OzelPencere('{{$SSayfa}}YorumEkle&HaberNo={{$Haber.No}}','Oku',600,500,1,1);">{{t}}Yorum Yaz{{/t}}</A>
                </TD>
                <TD align="center">
                 <A href="javascript:OzelPencere('{{$SSayfa}}Print&HaberNo={{$Haber.No}}&Yer=Haberler','Oku',600,500,1,1);">{{t}}Yazdýr{{/t}}</A>
                <TD align="center">
                 <A href="javascript:OzelPencere('{{$SSayfa}}TavsiyeMail&No={{$Haber.No}}&Yer=Haberler','Oku',600,500,1,1);">{{t}}Tavsiye Et{{/t}}</A>
                </TR></TABLE>
                </TD>
                 </TR>
                 <TR><TD colspan="3"><H3>{{t}}Yorumlar{{/t}}</H3></TD></TR>
                 {{if $Yorumlar}}
                         {{foreach item=Yorum from=$Yorumlar name=Yorum}}
                                 <TR><TD>&#187; {{$Yorum.Yorum}}</TD></TR>
                             <TR><TD><B>{{if $Yorum.Yazan==0}}{{t}}Anonim Ziyaretçi{{/t}}{{else}}{{$Yorum.Yazan}} - {{$Yorum.Yazan}}{{/if}}</B></TD></TR>
                     {{/foreach}}

                 {{else}}
                         <TR><TD align="center"><B>{{t}}Bu Haber için Yorum Bulunmamaktadýr...{{/t}}</B></TD></TR>
                 {{/if}}
         {{else}}

                 <TR>
                 <TD>
                         <H3>{{$Haber.Baslik}}</H3>
                         <DIV align="justify">{{$Haber.HaberSlogan}}</DIV><A href="{{$SSayfa}}Haberler&HaberNo={{$Haber.No}}">{{t}} Devamý için...{{/t}}</A>
                 </TD></TR>

        {{/if}}
 {{/foreach}}
{{else}}
 <TR><TD align=center><B>{{t}}Kayýtlý Haber bulunmamaktadýr.{{/t}}</B></TD></TR>
{{/if}}
 </TABLE>

{{include file="TableFoot.tpl"}}
{{/strip}}
