#include <menu.h>

#define ARRAY_SIZE(a) (sizeof(a) / sizeof(a[0]))
#define CTRLD   4

#include  <stdio.h>
#include <iksemel.h>

static int tmp=0;
static char *_name, *_id, *_size, *_path;

void add_version(char *name, char *id, char *size, char *path );
void list_version(void);

typedef struct _VERSION{

    char *name;
    char *id;
    char *size;
    char *path;
        struct _VERSION *Next, *Prev;

}VERSION;

VERSION *Head = NULL, *Tail = NULL;

char *choices[] = {
      "Choicıııe 1",
      "Choice 2",
      "Choice 3",
      "Choice 4",
      "Exit    ",
      (char *)NULL,
};
void print_in_middle(WINDOW *win, int starty, int startx, int width,
             char *string, chtype color);

int main()
{
    //parsing xml
    mainfonk();

  
    ITEM **my_items;
    int c;
    MENU *my_menu;
    WINDOW *my_menu_win;
    int n_choices, i;

    /* Curses kipini */
    initscr();
    start_color();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);
    init_pair(1, COLOR_RED, COLOR_BLACK);

    /* Öğeleri oluştur */
    n_choices = ARRAY_SIZE(choices);
    my_items = (ITEM **)calloc(n_choices, sizeof(ITEM *));
    for(i = 0; i < n_choices; ++i)
        my_items[i] = new_item(choices[i],"-----");

    /* Menüyü oluştur */
    my_menu = new_menu((ITEM **)my_items);

    /* Menü ile ilişiklendirilecek pencereyi oluştur */
    my_menu_win = newwin(10, 40, 4, 4);
    keypad(my_menu_win, TRUE);

    /* Ana pencereyi ve alt pencereleri ayarla */
    set_menu_win(my_menu, my_menu_win);
    set_menu_sub(my_menu, derwin(my_menu_win, 6, 38, 3, 1));

    /* Menü göstericisini " * " olarak ayarla*/
    set_menu_mark(my_menu, " * ");

    /* Ana pencere etrafında bir çerçeve çiz ve bir başlık yaz */
    box(my_menu_win, 0, 0);
    print_in_middle(my_menu_win, 1, 0, 40, "PARDUS", COLOR_PAIR(1));
    mvwaddch(my_menu_win, 2, 0, ACS_LTEE);
    mvwhline(my_menu_win, 2, 1, ACS_HLINE, 38);
    mvwaddch(my_menu_win, 2, 39, ACS_RTEE);
    mvprintw(LINES - 2, 0, "F1 to exit");
    refresh();

    /* Menüyü ekrana yaz */
    post_menu(my_menu);
   // wrefresh(my_menu_win);
    refresh();

    while((c = wgetch(my_menu_win)) != KEY_F(1))
    {
        switch(c)
        {
            case KEY_DOWN:
                menu_driver(my_menu, REQ_DOWN_ITEM);
                break;
            case KEY_UP:
                menu_driver(my_menu, REQ_UP_ITEM);
                break;
            case 10: /* Enter */
                move(20, 0);
                clrtoeol();
                mvprintw(LINES-4, 0, "Version : %s",
                item_name(current_item(my_menu)));
                pos_menu_cursor(my_menu);
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

    list_version();
}

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
         //   printf ("%s", name);
              if(strcmp(name,"Version")==0){
                // printf("*%s*", element);
                   tmp=2;
               }
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
        case IKS_CLOSE:
         //   printf ("</%s> ", name);
            break;
        case IKS_SINGLE:
         //   printf ("%s/>", name);
            break;
    }
    if (atts) {
        int i = 0;
        if(tmp==2)
            _id=atts[1];
      //  while (atts[i]) {
      //      printf ("%s=’%s’", atts[i], atts[i+1]);
      //      i += 2;
      //  }
    }
    return IKS_OK;
}
enum ikserror pr_cdata (void *udata, char *data, size_t len)
{
    int i; 
    if(tmp!=0){
      //    for (i = 0; i < len; i++)
              if(tmp==1)
                  _name=data;
      //            putchar (data[i]);
              if(tmp==3)
                  _size=data;
      //            putchar (data[i]);
              if(tmp==4)
                  _path=data;
      //            putchar (data[i]);
      //        if(tmp==4)
      //            putchar (data[i]);
        tmp=0;
      //   printf("\n");
    }
    
       return IKS_OK;
              }

int mainfonk ()
{

    char buffer[100000];
    FILE *dosya;
    char str[1000];
    dosya=fopen("surumler.xml","r");
    size_t file_size;
    int done;

    do{
        file_size = fread(buffer,sizeof(char),100000,dosya);
        dosya = file_size < sizeof(buffer);

         iksparser *p;
         p = iks_sax_new (NULL, pr_tag, pr_cdata);
         switch (iks_parse (p,buffer, 0, 1)) {
            case IKS_OK:
                puts ("OK");
                break;
            case IKS_NOMEM:
                puts ("Not enough memory");
                exit (1);
            case IKS_BADXML:
                 puts ("XML document is not well-formed");
                 exit (2);
            case IKS_HOOK:
                 puts ("Our hooks didn’t like something");
                 exit (2);
        }
        add_version(_name, _id, _size, _path);
        iks_parser_delete (p);
        return 0;
    }
    while(!done);
    fclose(dosya);
}

void add_version(char *name, char *id, char *size, char *path ){

    VERSION *vers = (VERSION *) malloc(sizeof(vers));
        if (vers == NULL) {
            printf("Not enough memory");
        }

        vers->name=name;
        vers->id=id;
        vers->size=size;
        vers->path=path;

        if (Head == NULL) {
            Head = vers;
            vers->Prev = NULL;
        }
        else {
            Tail->Next = vers;
            vers->Prev= Tail;
         }
         Tail = vers;
         vers->Next = NULL;
             printf("eklendi");
}




void list_version(void) {
        VERSION *vers;
        int count = 0;
               
        vers = Head;
        if (Head == NULL){
            printf("Listelenecek eleman yok!");
            return;
        }
        while (vers) {
            printf("Dosyanin ismi : %s\n", vers->name); 
            printf("Dosyanin buyuklugu : %d\n", vers->size);
            printf("Dosyanin ozelligi : %d\n", vers->id);
            printf("------------------------------\n"); 
            ++count;
            vers = vers->Next;
         }
            printf("\nToplam %d kayit listelendi\n", count);
}
