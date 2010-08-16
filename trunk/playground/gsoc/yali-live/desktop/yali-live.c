#include <unistd.h>

main()
{
    setuid(0);
	system("xhost +; /usr/bin/yali4-bin");
}
