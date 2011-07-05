#include <Python.h>
#include <qimage.h>
#include <stdlib.h>

QImage* image;
int **labels;
unsigned int ***images=NULL;
unsigned int **labelmosts=NULL;
unsigned int ** labellines;
int sizeLabelmosts = -1;
int curr = 0;
int labelIndex = 1;
unsigned int rgb = 0x222625;
unsigned int maxDiff = 20;
unsigned int minSize;

unsigned int difference(unsigned int first,unsigned int second){
	unsigned int blue = (first & 0xFF) > (second & 0xFF) ? (first & 0xFF) - (second & 0xFF) : (second & 0xFF) - (first & 0xFF);
	unsigned int green = (first & 0xFF00)>>8 > (first & 0xFF00)>>8 ? (first & 0xFF00)>>8 - (second & 0xFF00)>>8 : (second & 0xFF00)>>8 - (first & 0xFF00)>>8;
	unsigned int red = (first & 0xFF0000)>>16 > (second & 0xFF0000)>>16 ? (first & 0xFF0000)>>16 - (second & 0xFF0000)>>16 : (second & 0xFF0000)>>16 - (first & 0xFF0000)>>16;
	unsigned int max = blue > red ? blue : red;
	
	if (green > max)
		max = green;
	
    return max;
}

void next(int* reti,int* retj,int i,int j){
    /* an algorithm might be developed but
       now i dont see a need
       one algorithm could be to check if 
       i or j reached positive max then to decrement other
       and if i or j reached negative min increment...*/
	static int tablei [3][3] = {{0,-1,-1},{1,-2,-1},{1,1,0}};
	static int tablej [3][3] = {{-1,-1,0},{-1,-2,1},{0,1,1}};
    
	*reti = tablei[i+1][j+1];
	*retj = tablej[i+1][j+1];
}

void tracer(int* retx,int* rety,bool a,bool isExternal,int prevx,int prevy,int x,int y,int label){
	int i,j;
    if (a == true){    
        next(&i,&j,prevx-x,prevy-y);
        next(&i,&j,i,j);
    }else if (isExternal){
    	i = 1;
    	j = -1;
    }else{
    	i = -1;
    	j = 1;
    }
    for (int c = 0; c < 8; c++){
        if (x+i >= 0 and x+i < image->width() and y+j >= 0 and y+j < image->height() and difference(image->pixel(x+i,y+j),rgb) > maxDiff){
        	if(label>sizeLabelmosts){
        		sizeLabelmosts = label;
        		labelmosts = (unsigned int **)realloc(labelmosts, (sizeLabelmosts * sizeof(unsigned int *)));
        		labelmosts[label-1] = (unsigned int *)calloc(8,sizeof(unsigned int));
        		labelmosts[label-1][0] = image->width();
        		labelmosts[label-1][3] = image->height();
        		labelmosts[label-1][4] = 0;
        		labelmosts[label-1][7] = 0;
        	}else{
        		if(labelmosts[label-1][0] > x+i){//Leftmost point
        			labelmosts[label-1][0] = x+i;
        			labelmosts[label-1][1] = y+j;
	        	}else if(labelmosts[label-1][4] < x+i){//Rightmost point
	        		labelmosts[label-1][4] = x+i;
	        		labelmosts[label-1][5] = y+j;
	        	}
	        	if(labelmosts[label-1][3] > y+j){//Topmost point
	        		labelmosts[label-1][2] = x+i;
	        		labelmosts[label-1][3] = y+j;
	        	}else if(labelmosts[label-1][7] < y+j){//Bottommost point
	        		labelmosts[label-1][6] = x+i;
	        		labelmosts[label-1][7] = y+j;
	        	}
        	}
        	if(labels[x+i+1][y+j+1] == 0 or labels[x+i+1][y+j+1] == -1)
        		labels[x+i+1][y+j+1] = label;
            *retx = x+i;
            *rety = y+j;
            return;
        }else{
            labels[x+i+1][y+j+1] = -1;
        }
        next(&i,&j,i,j);
    }
    *retx = -1;
    *rety = -1;
    return;
}

void traceContour(bool isExternal,int sx,int sy,int label){
	int x,y;
    tracer(&x,&y,false,isExternal,-1,-1,sx,sy,label);
    int tx = x;
    int ty = y;
    int prevx = sx;
    int prevy = sy;
    int t = 0;
    bool first = true;
    while (x != -1 or y != -1){
    	first = false;
        tracer(&prevx,&prevy,true,false,prevx,prevy,x,y,label);
        t = x;
        x = prevx;
        prevx = t;
        t = y;
        y = prevy;
        prevy = t;
        if (prevx == sx and prevy == sy and x == tx and y == ty)
        	break;
    }
    if(first){
    	labelIndex--;
    	labels[sx+1][sy+1] = -1;
    	return;
    }
    if(labelmosts[label-1][3] > labelmosts[label-1][7]){
    		int a = labelmosts[label-1][7];
            labelmosts[label-1][7] = labelmosts[label-1][3];
            labelmosts[label-1][3] = a;
            a = labelmosts[label-1][6];
            labelmosts[label-1][6] = labelmosts[label-1][2];
            labelmosts[label-1][2] = a;
    }
    return;
}

extern "C" PyObject * extractor_extract(PyObject *self, PyObject *args){
	long L;
	
	if(!PyArg_ParseTuple(args,"liii",&L,&maxDiff,&rgb,&minSize))
		return NULL;
	
	image = (QImage *)L;
	
	labelIndex = 1;
	sizeLabelmosts = -1;
	curr = 0;
	images = NULL;
	labelmosts = NULL;
	
	labels = (int**)malloc((image->width()+2) * sizeof(int*));
	for(int i=0;i<image->width()+2;i++){
		labels[i] = (int*)calloc((image->height()+2),sizeof(int));
	}

	bool isExternal = false;
	bool isOut = true;
	char enter = 0;
	//bool doStep3 = true; //No need for inner side
	for (int j=0; j<image->height(); j++){
	    for (int i=0; i <image->width(); i++){
	    	//Try not to investigate components in contours
	    	// Commented out. causes too much complication
	    	/*if((labels[i][j+1] == 0 or labels[i][j+1]== -1) and 
	    	   (labels[i+1][j+1]!=0 and labels[i+1][j+1]!=-1)){
	    		//Approaching
	    		if((labels[i][j+2] != 0 and labels[i][j+2] != -1) or 
	    		   (labels[i+1][j+2] != 0 and labels[i+1][j+2] != -1) or 
	    		   (labels[i+2][j+2] != 0 and labels[i+2][j+2] != -1)){
	    			enter = 1;
	    		}else if((labels[i][j] != 0 and labels[i][j] != -1) or 
		    			(labels[i+1][j] != 0 and labels[i+1][j] != -1) or 
		    			(labels[i+2][j] != 0 and labels[i+2][j] != -1)){
		    		enter = 2;
	    		}else{
	    			enter = 0;
	    		}
	    	}
	    	if((labels[i+2][j+1] == 0 or labels[i+2][j+1]== -1) and 
    			(labels[i+1][j+1]!=0 and labels[i+1][j+1]!=-1)){
	    		//Getting out
	    		if((labels[i][j] != 0 and labels[i][j] != -1) or 
		    			(labels[i+1][j] != 0 and labels[i+1][j] != -1) or 
		    			(labels[i+2][j] != 0 and labels[i+2][j] != -1)){
		    		if(enter == 1){
		    			isOut = !isOut;//toggle
		    		}
	    		}
	    		else if((labels[i][j+2] != 0 and labels[i][j+2] != -1) or
		    	   (labels[i+1][j+2] != 0 and labels[i+1][j+2] != -1) or
		    	   (labels[i+2][j+2] != 0 and labels[i+2][j+2] != -1)){
		    		if(enter == 2){
		    			isOut = !isOut;//toggle
		    		}
		    	}
	    	}*/
	        if (difference(image->pixel(i,j),rgb) > maxDiff){
	        	//doStep3 = true;
	            isExternal = true;
	            if (isOut and labels[i+1][j+1] == 0 and (j-1<0 or difference(image->pixel(i,j-1),rgb) <= maxDiff)){
	                labels[i+1][j+1] = labelIndex;
	                traceContour(isExternal,i,j,labelIndex);
	                labelIndex+=1;
	                //doStep3 = false;
	            }
	            //No need for inner
	            /*if ((labels[i+1][j+2] != -1) and (j+1>=image->height() or difference(image->pixel(i,j+1),rgb) <= maxDiff)){
	            	if(labels[i+1][j+1] != 0 and labels[i][j+1] == -1){
	            		isExternal = false;
	            	}
	            	else if (labels[i+1][j+1] != 0){
	            		isExternal = true;
	            	}else{
	            		isExternal = false;
	            		labels[i+1][j+1] = labels[i][j+1];
	            	}
	            	traceContour(isExternal,i,j,labels[i+1][j+1]);
	            	doStep3 = false;
	            }
	            if (doStep3 and labels[i][j+1] != -1 and labels[i][j+1] != 0){
                    labels[i+1][j+1] = labels[i][j+1];
	            }*/
	        }
	    }
	}
	
	//printf("%d\n",sizeLabelmosts);
	
	images = (unsigned int***)malloc(sizeof(unsigned int **)*(sizeLabelmosts));
	for(int i = 0;i<sizeLabelmosts;i++){
		images[i] = (unsigned int**)malloc(sizeof(unsigned int *)*(labelmosts[i][7] - labelmosts[i][3]+2));
		for(int j=0;j<labelmosts[i][7] - labelmosts[i][3]+2;j++){
			images[i][j] = (unsigned int *)calloc(4,sizeof(unsigned int));
			images[i][j][0] = image->width();
		}
	}
	
	labellines = (unsigned int **)malloc((sizeLabelmosts)*sizeof(unsigned int*));
	for(int i=0;i<sizeLabelmosts;i++){
		labellines[i] = (unsigned int *)calloc(2,sizeof(unsigned int));
		//second one will show access
	}
	
	for (int j=0; j<image->height(); j++){
	    for (int i=0; i <image->width(); i++){
	    	if(labels[i+1][j+1] != 0 and labels[i+1][j+1] != -1){
	    		int label = labels[i+1][j+1]-1;
	    		int line = labellines[label][0];
	    		labellines[label][1] = 1; // access
	    		if (images[label][line][0] > i){
	    			images[label][line][0] = i;
	    			images[label][line][1] = j;
	    		}else if (images[label][line][2] < i){
	    			images[label][line][2] = i;
	    			images[label][line][3] = j;
	    		}
	    	}
	    }
	    for(int k=0;k<sizeLabelmosts;k++){
	    	if(labellines[k][1]){
	    		labellines[k][0]++;
	    		labellines[k][1]=0;
	    	}
	    }
	}
	
	for (int i=0;i<sizeLabelmosts;i++){
		if((labelmosts[i][4] - labelmosts[i][0]+1)*(labelmosts[i][7] - labelmosts[i][3]+1)>minSize){
			for(int j = 0;j<labellines[i][0];j++){
				for(int k = images[i][j][0]; k>0 and k>=labelmosts[i][0] and (labels[k][images[i][j][1]] == 0 or labels[k][images[i][j][1]] == -1 or labels[k][images[i][j][1]] == i+1);k--)
					images[i][j][0] = k;
				for(int k = images[i][j][2]; k<=labelmosts[i][4] and (labels[k][images[i][j][3]] == 0 or labels[k][images[i][j][3]] == -1 or labels[k][images[i][j][3]] == i+1);k++)
					images[i][j][2] = k;
			}
		}
	}
		
	/*QImage* im = new QImage(image->width(),image->height(),32);
	
	for (int j=0; j<image->height(); j++){
	    for (int i=0; i <image->width(); i++){
	    	if (labels[i+1][j+1] == 0 or labels[i+1][j+1] == -1)
	    		im->setPixel(i,j,qRgb(0,0,0));
	    	else
	    		im->setPixel(i,j,labels[i+1][j+1]*labels[i+1][j+1]*labels[i+1][j+1]);
	    }
	}
	im->save("out.bmp","BMP");*/
	
	return Py_BuildValue("i",1);
}

extern "C" PyObject * extractor_average(PyObject *self, PyObject *args){
	long L;
	QImage* im;
	
	if(!PyArg_ParseTuple(args,"l",&L))
		return NULL;
	
	im = (QImage *)L;
	
	unsigned long long red=0,green=0,blue=0; 
		
	unsigned int rgb;
	
	for(int i=0;i<im->width();i++){
		for(int j=0;j<im->height();j++){
			rgb = im->pixel(i,j);
			blue += rgb & 0xFF;
			green += (rgb >> 8) & 0xFF;
			red += (rgb >> 16) & 0xFF;
		}
	}
	
	red = red / (image->width() * image->height());
	green = green / (image->width() * image->height());
	blue = blue / (image->width() * image->height());
	
	rgb = (red << 16) + (green << 8) + blue;
	
	return Py_BuildValue("i",rgb);
}

extern "C" PyObject * extractor_nextImage(PyObject *self, PyObject *args){
	long L;
	QImage* im;
	
	if(!PyArg_ParseTuple(args,"l",&L))
		return NULL;
	
	im = (QImage *)L;
	
	if(sizeLabelmosts<=0 or curr >= sizeLabelmosts){
		//im = NULL;
		return Py_BuildValue("i",0);
	}else{
		for(;curr < sizeLabelmosts;curr++){
			if(((labelmosts[curr][4] - labelmosts[curr][0]+1)*(labelmosts[curr][7] - labelmosts[curr][3]+1))>minSize){
				im->create(labelmosts[curr][4] - labelmosts[curr][0]+1, labelmosts[curr][7] - labelmosts[curr][3]+1,32);
				im->fill(0);
				for(int i=0;i<labellines[curr][0];i++){
					bitBlt(im,images[curr][i][0] - labelmosts[curr][0],i,image,images[curr][i][0],images[curr][i][1],images[curr][i][2]-images[curr][i][0]+1,1);
				}
				if(!im->isNull()){
					curr++;
					break;
				}
			}
		}
		return Py_BuildValue("i",1);
	}
}

static PyMethodDef ExtractorMethods[] = {
	{"average",  extractor_average, METH_VARARGS,
	 "Computes average color of given image."},
    {"extract",  extractor_extract, METH_VARARGS,
     "Extract images from given image."},
    {"nextImage",  extractor_nextImage, METH_VARARGS,
     "Get the next image."}, 
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
init_extractor(void)
{
	(void) Py_InitModule("_extractor", ExtractorMethods);
}

/*int main(int argc, char **argv) {
	QImage* im = new QImage();
	im->load("deneme.bmp","BMP");
	extract(im,20,0x222625);
	
	QImage* tmpImage = new QImage();
	char fileName [100];
	int i=0;
	while(next(tmpImage,900000)){
		sprintf(fileName,"out%d.bmp",i);
		if(tmpImage->save(fileName,"BMP"))
			printf("%s saved\n",fileName);
		i++;
	}
}*/
