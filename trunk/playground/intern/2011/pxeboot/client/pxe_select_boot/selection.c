#include <menu.h>

#define ARRAY_SIZE(a) (sizeof(a) / sizeof(a[0]))
#define CTRLD   4
#define BUFFER_SIZE  100000
#define ROW_MIN 17
#define COL_MIN 53
#define MENU_SIZE 5 // 15 max


#include  <stdio.h>
#include  <stdlib.h>
#include  <string.h>
#include  <malloc.h>

#include <iksemel.h>

static int tmp=0;
char *_name, *_id, *_size, *_path;
int count = 0;

void add_version(char *name, char *id, char *size, char *path );
typedef struct _VERSION{

    char *name;
    char *id;
    char *size;
    char *path;
        struct _VERSION *Next ,*Prev;

}VERSION;

VERSION **Head = NULL, *Tail = NULL;

//char *choices[] = {
//      "Choice 1",
//      "Choice 2",
//      "Choice 3",
//      "Choice 4",
//      "Exit    ",
//      (char *)NULL,
//};

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
                        //-----   PARSE XML   -----//

int pr_tag (void *udata, char *name, char **atts, int type)
{
    switch (type) {
        case IKS_OPEN:
              if(strcmp(name,"Name")==0){
                   tmp=1;
               }
               if(strcmp(name,"Size")==0){
                    tmp=3;
                }
               if(strcmp(name,"Path")==0){
                    tmp=4;
                 }
            break;
    }
    if (atts) {
        if (strcmp(atts[0],"id")==0){
            _id = (char *) malloc(sizeof(char)* (strlen(atts[1])+1));
            strcpy(_id,atts[1]);
        }}
    return 0;
}
//----------------------------------------------------------------------------------

int pr_cdata (void *udata, char *data, size_t len)
{

    if (tmp != 0) {
              if (tmp == 1){
                   _name = (char *) malloc(sizeof(char)* (len+1));
                  strncpy(_name,data,len);
                  _name[len]=NULL;
              }
              if (tmp==3){
                  _size = (char *) malloc(sizeof(char)* (len+1));
                  strncpy(_size,data,len);
                  _size[len]=NULL;
              }
              if(tmp==4){
                  _path = (char *) malloc(sizeof(char)* (len+1));
                  strncpy(_path,data,len);
                  _path[len]=NULL;

                  add_version(_name, _id, _size, _path);

                  free(_name);
                  free(_id);
                  free(_size);
                  free(_path);
              }
         tmp=0;
    }
       return 0;
}

//----------------------------------------------------------------------------------

int iksemel_parse ()
{
    char buffer[BUFFER_SIZE];
    FILE *dosya;
    iksparser *p;

    dosya=fopen("surumler.xml","r");

    if (dosya== NULL) {
        printf("Failed to open file\n");
        return 1;
     }
    size_t file_size;

    do{
         file_size = fread(buffer,sizeof(char),BUFFER_SIZE,dosya);
         p = iks_sax_new (NULL, pr_tag, pr_cdata);
         iks_parse (p,buffer, 0, 1);
         iks_parser_delete (p); 

    }while(!EOF);

    fclose(dosya);
    return 0;
}

//-------------------------------------------------------------------------------


void add_version(char *name, char *id, char *size, char *path ){

    VERSION *new = (VERSION *) malloc(sizeof(VERSION));

    new->name = (char *) malloc(sizeof(char)* (strlen(name)+1));
    new->id = (char *) malloc(sizeof(char)* (strlen(id)+1));
    new->size = (char *) malloc(sizeof(char)* (strlen(size)+1));
    new->path = (char *) malloc(sizeof(char)* (strlen(path)+1));

    if (new == NULL) {
        printf("Not enough memory");

    }

    new->Next = NULL ;
    new->Prev = NULL;

    strcpy(new->name,name);
    strcpy(new->id,id);
    strcpy(new->size,size);
    strcpy(new->path,path);

    if (Tail == NULL) {
        *Head = new;
        Tail = new;
    }
    else {
        new->Prev=Tail;
        Tail->Next = new;
        Tail = Tail->Next;
    }
     printf("eklendii\n");
}

//----------------------------------------------------------------------------------

void list_version() {
        VERSION *vers;

        vers = *Head;

        if (*Head == NULL){
            printf("Listelenecek eleman yok!");
        }
        while (vers) {
            printf("NAME:   %s\n", vers->name); 
            printf("ID:   : %s\n", vers->size);
            printf("SIZE : %s\n", vers->id);
            printf("------------------------------\n"); 
            ++count;
            vers = vers->Next;
         }
         printf("\nToplam %d kayit listelendi\n", count);
}


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


int main()
{
    Head=(VERSION **) malloc(sizeof(VERSION *));

    //parsing xml
    printf("main fonk\n");
    iksemel_parse();

    list_version();

    ITEM **my_items;
    int c;
    MENU *my_menu;
    WINDOW *my_menu_win;
    int n_choices, i;

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
    n_choices = count;
    my_items = (ITEM **)calloc(n_choices, sizeof(ITEM *));


    VERSION *vers;
    //int count = 0;
    vers = *Head;

    i=0;
        while (vers) {
            my_items[i] = new_item(vers->name, "\t---");
            vers=vers->Next;
            i++;
        }

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

    vers = *Head;
    while((c = wgetch(my_menu_win)) != KEY_F(1))
    {
        switch(c)
        {
            int len=0;
            case KEY_DOWN:
                if(vers!=NULL && vers->Next!=NULL){
                    vers=vers->Next;
                    len= strlen(vers->name)+strlen(vers->id)+ strlen(vers->size)+3*4;
                    attron(COLOR_PAIR(2));
                    menu_driver(my_menu, REQ_DOWN_ITEM);
                    move(60, 0);
                    clrtoeol();
                    mvprintw(LINES-10, 0, "\n");
                    mvprintw(LINES-10, (*(&col)/2)-len/2, "%s    %s    %s",
                    item_name(current_item(my_menu)),vers->id,vers->size);
                    pos_menu_cursor(my_menu);
                    attroff(COLOR_PAIR(2));
                }
                break;
            case KEY_UP:
                if(vers!=NULL && vers->Prev!=NULL){
                    vers=vers->Prev;
                    len= strlen(vers->name)+strlen(vers->id)+ strlen(vers->size)+3*4;
                    attron(COLOR_PAIR(2));
                    menu_driver(my_menu, REQ_UP_ITEM);
                    move(60, 0);
                    clrtoeol();
                    mvprintw(LINES-10, 0, "\n");
                    mvprintw(LINES-10, (*(&col)/2)-len/2, "%s    %s    %s",
                    item_name(current_item(my_menu)),vers->id,vers->size);
                    pos_menu_cursor(my_menu);
                    attroff(COLOR_PAIR(2));
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

