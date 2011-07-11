#include  <stdio.h>
#include  <stdlib.h>
#include  <string.h>
#include  <malloc.h>
#include <locale.h>
#include <libxml/xmlmemory.h>
#include <libxml/parser.h>

#include <menu.h>

#define ARRAY_SIZE(a) (sizeof(a) / sizeof(a[0]))
#define CTRLD   4
#define BUFFER_SIZE  100000
#define ROW_MIN 17
#define COL_MIN 53
#define MENU_SIZE 5 // 15 max


typedef struct vers {
    xmlChar *versionID;
    xmlChar *name;
    xmlChar *size;
    xmlChar *path;
} vers, *versPtr;

//0000000000000000000000000000000000000000000000000000000000000000000000000000000
//-----   PARSE XML   -----//

static versPtr parseVersion(xmlDocPtr doc, xmlNodePtr cur) {
    versPtr ret = NULL;

    /*
     * allocate the struct
     */
    ret = (versPtr) malloc(sizeof(vers));
    if (ret == NULL) {
        fprintf(stderr,"out of memory\n");
	return(NULL);
    }
    memset(ret, 0, sizeof(vers));

    /* We don't care what the top level element name is */
    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Version"))) {
	    ret->versionID = xmlGetProp(cur, (const xmlChar *) "id");
	    if (ret->versionID == NULL) {
		fprintf(stderr, "Project has no ID\n");
	    }
	}
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Name")) )
	    ret->name = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Size")) )
	    ret->size = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Path")) )
	    ret->path = xmlNodeListGetString(doc, cur->xmlChildrenNode, 1);
	cur = cur->next;
    }

    return(ret);
}

//--------------------------------------------------------------------------------------------------------
static void printVersion(versPtr cur) {
    int i;

    if (cur == NULL) return;
   	 printf("=======  Pardus\n");
    if (cur->versionID != NULL) 
	printf("versionID: %s\n", cur->versionID);
    if (cur->name != NULL) 
	printf("name: %s\n", cur->name);
    if (cur->size != NULL) 
	printf("size: %s\n", cur->size);
    if (cur->path != NULL) 
	printf("path: %s\n", cur->path);

}

//--------------------------------------------------------------------------------------------------------
typedef struct gversion {
    int nbversions;
    versPtr versions[500]; /* using dynamic alloc is left as an exercise */
} gVersion, *gVersPtr;


static gVersPtr parseGversFile(char *filename) {
    xmlDocPtr doc;
    gVersPtr ret;
    versPtr curvers;
    xmlNodePtr cur;

#ifdef LIBXML_SAX1_ENABLED
    /*
     * build an XML tree from a the file;
     */
    doc = xmlParseFile(filename);
    if (doc == NULL) return(NULL);
#else
    /*
     * the library has been compiled without some of the old interfaces
     */
    return(NULL);
#endif /* LIBXML_SAX1_ENABLED */


    cur = xmlDocGetRootElement(doc);

   
    ret = (gVersPtr) malloc(sizeof(gVersion));
    if (ret == NULL) {
        fprintf(stderr,"out of memory\n");
	xmlFreeDoc(doc);
	return(NULL);
    }
    memset(ret, 0, sizeof(gVersion));
    cur = cur->xmlChildrenNode;
    while ( cur && xmlIsBlankNode ( cur ) ) {
	cur = cur -> next;
    }
    if ( cur == 0 ) {
	xmlFreeDoc(doc);
	free(ret);
	return ( NULL );
    }

    cur = cur->xmlChildrenNode;
    while (cur != NULL) {
        if ((!xmlStrcmp(cur->name, (const xmlChar *) "Pardus")))  {
	    curvers = parseVersion(doc , cur);
	    if (curvers != NULL)
	        ret->versions[ret->nbversions++] = curvers;
            if (ret->nbversions >= 500) break;
	}
	cur = cur->next;
    }

    return(ret);
}




//============================================================================================================
void print_in_middle(WINDOW *win, int starty, int startx, int width,
    char *string, chtype color)
{
    int length, x, y;
    float temp;

    if(win == NULL)
        win = stdscr;
    getyx(win, y, x);
    if(startx != 0)
        x = startx;
    if(starty != 0)
        y = starty;
    if(width == 0)
        width = 80;

    length = strlen(string);
    temp = (width - length)/ 2;
    x = startx + (int)temp;
    wattron(win, color);
    mvwprintw(win, y, x, "%s", string);
    wattroff(win, color);
    refresh();

}
//-------------------------------------------------------------------------------
                        


void screen_size(WINDOW *win, int min_row, int min_col,int *r, int *c)
{   
    int row,col;
    getmaxyx(win,row,col);
    if ((row<min_row) || (col<min_col))
     {
         endwin();
         printf("\n\nScreen's too small..bitch!\n1-resize the screen\n2-restart the program.\n\n\n");
         exit(EXIT_SUCCESS);
     }
    
     *r = row;
     *c = col;
}
//--------------------------------------------------------------------------------------------------------
//--------------------------------------------------------------------------------------------------------


int main(int argc, char **argv)
{
    setlocale(LC_ALL , "");

//*****************************
    int i;
    gVersPtr cur;

    /* COMPAT: Do not genrate nodes for formatting spaces */
    LIBXML_TEST_VERSION
    xmlKeepBlanksDefault(0);

    for (i = 1; i < argc ; i++) {
	cur = parseGversFile(argv[i]);
	if ( cur )
	  for (i = 0; i < cur->nbversions; i++) printVersion(cur->versions[i]);
	else
	  fprintf( stderr, "Error parsing file '%s'\n", argv[i]);

    }

    /* Clean up everything else before quitting. */
    xmlCleanupParser();


//******************************
    ITEM **my_items;
    int c;
    MENU *my_menu;
    WINDOW *my_menu_win;
    int n_choices;

    /* Curses kipini */
    initscr();
    int row,col;
    screen_size(stdscr,ROW_MIN,COL_MIN,&row,&col);

    start_color();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    init_pair(1, COLOR_RED, COLOR_BLACK);
    init_pair(2, COLOR_CYAN, COLOR_BLACK);
    init_pair(3, COLOR_MAGENTA, COLOR_BLACK);
    
    /* Öğeleri oluştur */
    n_choices = cur->nbversions;
    my_items = (ITEM **)calloc(n_choices, sizeof(ITEM *));


    i=0;

    for (i = 0; i < cur->nbversions; i++) 
         my_items[i] = new_item(cur->versions[i]->name, "\t---");

    /* Menüyü oluştur */
    my_menu = new_menu((ITEM **)my_items);

    /* Menü ile ilişiklendirilecek pencereyi oluştur */
    my_menu_win = newwin( 20,60 , (*(&row)/2)-20/2, (*(&col)/2)-60/2);
    keypad(my_menu_win, TRUE);

    /* Ana pencereyi ve alt pencereleri ayarla */
    set_menu_win(my_menu, my_menu_win);
    set_menu_sub(my_menu, derwin(my_menu_win, 16, 58, 4, 2));
    set_menu_format(my_menu, 14, 1);  //tek bi sayfa için gösterilmesini istediğimiz satır sayısı 15


    /* Menü göstericisini " * " olarak ayarla*/
    set_menu_mark(my_menu, " * ");

    /* Ana pencere etrafında bir çerçeve çiz ve bir başlık yaz */
    box(my_menu_win, 0, 0);
    print_in_middle(my_menu_win, 1, 0, 60, "PARDUS", COLOR_PAIR(1));
    mvwaddch(my_menu_win, 2, 0, ACS_LTEE);
    mvwhline(my_menu_win, 2, 1, ACS_HLINE, 58);
    mvwaddch(my_menu_win, 2, 59, ACS_RTEE);
    
    attron(COLOR_PAIR(3));
    mvprintw(LINES - 3, 0, "ABCDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ");
    mvprintw(LINES - 2, 0, "F1 to exit\n,  abcdefgğhıijklmeoöprsştuüvyz");
    attroff(COLOR_PAIR(3));
    refresh();

    /* Menüyü ekrana yaz */
    post_menu(my_menu);
    //wrefresh(my_menu_win);
   // refresh();

    while((c = wgetch(my_menu_win)) != KEY_F(1))
    {
        switch(c)
        {
            int len=0, limit=0;
            case KEY_DOWN:
                if(cur->nbversions<limit){
                    len= strlen(cur->versions[i]->name)+strlen(cur->versions[i]->versionID)+ strlen(cur->versions[i]->size)+2*4;
                    attron(COLOR_PAIR(2));
                    menu_driver(my_menu, REQ_DOWN_ITEM);
                    move(60, 0);
                    clrtoeol();
                    mvprintw(LINES-10, 0, "\n");
                    mvprintw(LINES-10, (*(&col)/2)-len/2, "%s    %s    %s",
                    item_name(current_item(my_menu)),cur->versions[i]->versionID,cur->versions[i]->size);
                    pos_menu_cursor(my_menu);
                    attroff(COLOR_PAIR(2));
                    limit++;
                }
                break;
            case KEY_UP:
                 if(cur->nbversions<limit){
                    len= strlen(cur->versions[i]->name)+strlen(cur->versions[i]->versionID)+ strlen(cur->versions[i]->size)+2*4;
                    attron(COLOR_PAIR(2));
                    menu_driver(my_menu, REQ_DOWN_ITEM);
                    move(60, 0);
                    clrtoeol();
                    mvprintw(LINES-10, 0, "\n");
                    mvprintw(LINES-10, (*(&col)/2)-len/2, "%s    %s    %s",
                    item_name(current_item(my_menu)),cur->versions[i]->versionID,cur->versions[i]->size);
                    pos_menu_cursor(my_menu);
                    attroff(COLOR_PAIR(2));
		    limit--;
                  }
                break;
            case 10: /* Enter */

                break;
         }

        refresh();
     }


    /* Menüyü ekrandan sil ve tahsis edilen belleği geri ver */
     unpost_menu(my_menu);
     for(i = 0; i < n_choices; ++i)
         free_item(my_items[i]);
     free_menu(my_menu);
     endwin();

 return 0;
}

