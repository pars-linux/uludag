var pisi_Speed = 5;	// yukselt hızlansın ..
var pisi_timer = 5;	// düşür hızlansın ..

var objectIdToSlideDown = false;
var pisi_activeId = false;
var pisi_renk = false;

function showHideContent(item){
	var numericId = item.id.replace(/[^0-9]/g,'');
	var answerDiv = document.getElementById('package_i' + numericId);
	if(!answerDiv.style.display || answerDiv.style.display=='none'){
		if(pisi_activeId &&  pisi_activeId!=numericId){
			objectIdToSlideDown = numericId;
			slideContent(pisi_activeId,(pisi_Speed*-10));
		}else{
			answerDiv.style.display='block';
			answerDiv.style.visibility = 'visible';
			slideContent(numericId,pisi_Speed);
		}
	}else{
		slideContent(numericId,(pisi_Speed*-10));
		pisi_activeId = false;
	}
}

function slideContent(inputId,direction){
	var obj =document.getElementById('package_i' + inputId);
	var contentObj = document.getElementById('package_ic' + inputId);
	height = obj.clientHeight;
	height = height + direction;
	rerunFunction = true;
	if(height>contentObj.offsetHeight){
		height = contentObj.offsetHeight;
		rerunFunction = false;
	}
	if(height<0){
		height = 0;
		rerunFunction = false;
	}

	obj.style.height = height + 'px';
	var topPos = height - contentObj.offsetHeight;
	if(topPos>0)topPos=0;
	contentObj.style.top = topPos + 'px';
	if(rerunFunction){
		setTimeout('slideContent(' + inputId + ',' + direction + ')',pisi_timer);
	}else{
		if(height==0){
			obj.style.display='none'; 
			if(objectIdToSlideDown && objectIdToSlideDown!=inputId){
				document.getElementById('package_i' + objectIdToSlideDown).style.display='block';
				document.getElementById('package_i' + objectIdToSlideDown).style.visibility='visible';
				slideContent(objectIdToSlideDown,pisi_Speed);				
			}
		}else{
			pisi_activeId = inputId;
		}
	}
}

function changeBackgroundColor(item){
    var numericId = item.id.replace(/[^0-9]/g,'');
    var divtitle = document.getElementById('package_t'+numericId);
    var divcheckbox = document.getElementById('checkboks_t'+numericId);
    if (item.checked) {
        divtitle.style.background='#533359';
        divcheckbox.style.background = '#533359';
    }
    else {
        if (numericId % 2) {
            divtitle.style.background='#3cBB39';
            divcheckbox.style.background = '#3cBB39';
        }
        else {
            divtitle.style.background='#3c8839';
            divcheckbox.style.background = '#3c8839';
        }
    }
}

function noselect(e){
    return false
}

function benable(){
    return true
}

if (window.sidebar){
    document.onmousedown=noselect
    document.onclick=benable
}
