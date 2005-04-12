#ifdef ENABLE_NLS
#    include <locale.h>
#    include <libintl.h>
#    define _(String) gettext (String)
#    ifdef gettext_noop
#        define N_(String) gettext_noop (String)
#    else
#        define N_(String) (String)
#    endif
#else
/* Stubs that do something close enough. */
#    define textdomain(String)
#    define bindtextdomain(Domain,Directory)
#    define bind_textdomain_codeset(Domain, Codeset)
#    define _(String) (String)
#    define N_(String) (String)
#    define gettext(String) (String)
#    define dgettext(Domain,Message) (Message)
#    define dcgettext(Domain,Message,Type) (Message)
#endif
