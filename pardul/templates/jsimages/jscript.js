function mailkontrol(strValue) 
{
  if((strValue.indexOf('ö')>=0)||(strValue.indexOf('þ')>=0)||(strValue.indexOf('ü')>=0)||(strValue.indexOf('ç')>=0)||(strValue.indexOf('ð')>=0)||(strValue.indexOf('Ö')>=0)||(strValue.indexOf('Þ')>=0)||(strValue.indexOf('Ü')>=0)||(strValue.indexOf('Ç')>=0)||(strValue.indexOf('Ð')>=0)||(strValue.indexOf('Ý')>=0)) return false;
  return (strValue.indexOf(".") > 2) && (strValue.indexOf("@") > 0);
}

function MailKontrolEt(Email)
{
  if(Email=="")
    return true;
  else
  {
   if(mailkontrol(Email)==false)
   {alert('Lütfen geçerli bir E-Posta adresi giriniz!');return false;} 
     else return true;
  }
}

function sifrekontrol(sifre1,sifre2,formad,mesaj,karakteraz)
{
    var formadi=eval("document."+formad);
    var sifredeger1=eval(formadi.name+"."+sifre1);
    var sifredeger2=eval(formadi.name+"."+sifre2);
    if (sifredeger1.value.length<6)
    {
      alert(karakteraz);
      return false;
    }
    if (sifredeger1.value!=sifredeger2.value)
    {
      alert(mesaj);
      return false;
    }
}

function hepsinisec(formname)
{
  var formad=eval("document."+formname);
  with (formad) {
    for (var i=0; i < elements.length; i++) {
        if (elements[i].type == 'checkbox')
           elements[i].checked = true;
    }
  }
}

function hepsinitemizle(formname)
{
  var formad=eval("document."+formname);
  with (formad) {
    for (var i=0; i < elements.length; i++) {
        if (elements[i].type == 'checkbox')
           elements[i].checked = false;
    }
  }
}

function BlokSaklaGoster(gelen)
        {
        kat = document.getElementById(gelen);
        if(kat.style.display=='none')
                { kat.style.display = 'block'; }
        else
                { kat.style.display = 'none'; }
        }
// ismi verilen div'i bulur
function DivBul(gelen)
	{
	if(document.layers)
		return eval('document.layers[`gelen]');
	else if(document.all)
		return eval('document.all[gelen]');
	else if(window.navigator.userAgent.toLowerCase().match("gecko"))
		return eval('document.getElementById(gelen)');
	}
// ismi verilen div'i gosterir
function goster(gelen,en,boy)
{
if(document.layers)
	document.poppedLayer = eval('document.layers[`gelen]');
else if(document.all)
	document.poppedLayer = eval('document.all[gelen]');
else if(window.navigator.userAgent.toLowerCase().match("gecko"))
	document.poppedLayer = eval('document.getElementById(gelen)');
if((en > 0) && (boy > 0))
	{
	document.poppedLayer.style.top = (screen.availWidth-boy)/2;
	document.poppedLayer.style.left = (screen.availWidth-en)/2;
	}
document.poppedLayer.style.visibility = "visible";
}

// ismi verilen div'i gizler
function sakla(gelen)
{
if(document.layers)
	document.poppedLayer = eval('document.layers[`gelen]');
else if(document.all)
	document.poppedLayer = eval('document.all[gelen]');
else if(window.navigator.userAgent.toLowerCase().match("gecko"))
	document.poppedLayer = eval('document.getElementById(gelen)');
document.poppedLayer.style.visibility = "hidden";
}

function TamEkranPencere(Adres)
{
    var TamPencere=window.open(Adres,"Pencere","toolbar=0,location=0,history=1,directories=0,status=1,menubar=0,scrollbars=1,resizable=yes");
    TamPencere.focus();
}
//tam ekran
function TamEkran()
{
  window.moveTo(0,0);
  if (document.all) {
   top.window.resizeTo(screen.availWidth,screen.availHeight);
  }
  else if (document.layers||document.getElementById)
  {
      if (top.window.outerHeight<screen.availHeight||
          top.window.outerWidth<screen.availWidth)
      {
          top.window.outerHeight = screen.availHeight;
          top.window.outerWidth = screen.availWidth;
       }
  }
}//function

function OzelPencere(Adres,Tanim,En,Boy,Scroll,YeniPencerede)
{
   var ScrollVar;
   if (Scroll==1) ScrollVar=1;else ScrollVar=0;
   if (YeniPencerede==1) Yenide='_blank';else Yenide='a';
   var Ust=(screen.availHeight-Boy)/2;
   var Sol=(screen.availWidth-En)/2;
   var OzelPencere=window.open(Adres,Yenide,"toolbar=0,location=0,history=1,directories=0,status=1,menubar=0,scrollbars="+ScrollVar+",left="+Sol+",top="+Ust+ ",width="+En+",height="+Boy+",resizable=no");
   OzelPencere.focus();
}


function kontrol(gelen)
{
var hatali=false;
var hatalirenk = "#FFFFCC";
var regexpI = /\b.*I_.*\b/;
var toplam = gelen.elements.length;
for(i=0;i<toplam;i++)
        {
        gelen.elements[i].style.background='#FFFFFF';
        if(gelen.elements[i].name.substring(0,2) == 'N_' && gelen.elements[i].value=='')
                {
                alert(gelen.elements[i].alt+' boþ olamaz!');
                gelen.elements[i].focus();
                gelen.elements[i].style.background=hatalirenk; 
                hatali = true;
                break;
                }
        else if(gelen.elements[i].name.match(regexpI) && isNaN(gelen.elements[i].value))
                {
                alert(gelen.elements[i].alt+' tamsayý olmalýdýr!');
                gelen.elements[i].focus();
                gelen.elements[i].style.background=hatalirenk; 
                hatali = true;
                break;
                }
        if ( (gelen.elements[i].name=='EPosta') || (gelen.elements[i].name=='N_EPosta') )
        {
            sonuc = MailKontrolEt(gelen.elements[i].value);
            if (sonuc==false)
            {
              gelen.elements[i].focus();
              gelen.elements[i].style.background=hatalirenk; 
              hatali=true;
              break;
            }
        }
         
        if (gelen.elements[i].type=="text")
        {
            var ad = gelen.elements[i].name;
            sayi = ad.indexOf('Tarih');
            if (sayi!=-1)
            {
               sonuc = TarihGecerli(gelen.elements[i].value);
               if (sonuc==false){alert('Lütfen geçerli bir tarih giriniz! Format: GG.AA.YYYY'); hatali=true;break;}
            }
        }

        }
if(hatali)      return false;
else            return true;
}

/** 
 * Sadece Rakam Girilebilir Input alanlari hazirlar.
 * 
 **/
function HarfYok()
{
 if (( (event.keyCode<48)&&(event.keyCode!=46)) || (event.keyCode>57))
     event.keyCode = 0;
}
}