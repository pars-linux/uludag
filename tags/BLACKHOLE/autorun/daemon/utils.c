/**
 * @file utils.c
 * @brief Common utility functions.
 *
 * File containing common utility functions.
 *
 * Copyright (c) 2005, TUBITAK/UEKAE
 * @author S.Çağlar Onur <caglar@uludag.org.tr>
 *
 * Copyright 2001 Xandros Corporation.  All rights reserved.
 * @author Richard Rak <rakr@xandros.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 *
 */

#include "autorun.h"

int testDir(const char *path)
{
    struct stat buf;

    if (stat(path, &buf) == -1) 
    {
#ifdef DEBUG
        fprintf(stdin,"File %s does not exist.\n", path);
#endif
        return 0;
    }
    if (S_ISDIR(buf.st_mode)) 
    {
#ifdef DEBUG
        fprintf(stdin,"Directory %s exists.\n", path);
#endif
        return 1;
    } 
    else 
    {
#ifdef DEBUG
        fprintf(stdin,"File %s exists, but is not a directory.\n", path);
#endif
        return 0;
    }
    // We should never get here.
    return 0;
}


/*
 * Create a temporary directory and return the name in a malloc()'d string.
 *
 * @return A malloc()'d string containing the location (absolute) of the
 *         temporary directory, or 0 if an error occured.
 */
char *makeTempDir()
{
    char *template = "autorunXXXXXX";
    char *temp = 0;
    char *tempDir = 0;
    temp = getenv("TMP");
    if (!temp)
    {
        temp = "/tmp";
    }
    tempDir = malloc(sizeof(char) * (strlen(template) + strlen(temp) + 2));
    if (!tempDir)
    {
        return 0;
    }
    sprintf(tempDir, "%s/%s", temp, template);
    if (!mkdtemp(tempDir))
    {
        free(tempDir);
        return 0;
    }
    return tempDir;
}

/*
 * Find out the actual type of data disk (WINE, LOKI, etc.)
 *
 * @param path The path to check for identifying files
 *
 * @return Return the proper code for the detected disk type.
 */
DISK_TYPE checkDataDisk(const char *const path)
{
    int fd;
    char *buffer = malloc(sizeof(char) * (strlen(path) + 13));

    if (!buffer)
    {
        return UNKNOWN;
    }

    sprintf(buffer, "%s/VIDEO_TS", path);
    if (testDir(buffer))
    {
        free(buffer);
        return VIDEO;
    }
    //ASW need to write toupper() one of these days
    sprintf(buffer, "%s/video_ts", path);
    if (testDir(buffer))
    {
        free(buffer);
        return VIDEO;
    }

    //ASW check for Video CD (VCD) which should have vcd, mpegav, cdda, segment, karaoke,
    //and optionally ext and cdi directories 
    sprintf(buffer, "%s/vcd", path);
    if (testDir(buffer))
    {
        sprintf(buffer, "%s/mpegav", path);
        if (testDir(buffer))
        {
            free(buffer);
            return VCDVIDEO;
        }
    }


    sprintf(buffer, "%s/setup.sh", path);
    fd = open(buffer, O_RDONLY | O_NONBLOCK);
    if (-1 != fd)
    {
        free(buffer);
        close(fd);
        return LOKI;
    }
    else
    {
        int bFoundOffice = 0;
        sprintf(buffer, "%s/autorun.inf", path);
        fd = open(buffer, O_RDONLY | O_NONBLOCK);
        if (-1 != fd)
        {
            FILE *f = fdopen(fd, "r");
            char buf[2048];
            while (!feof(f))
            {
                memset(buf, 0, sizeof(char) * 2048);
                fgets(buf, 2048, f);
                if (strstr(buf, "Microsoft Office"))
                {
                    bFoundOffice = 1;
                    break;
                }
            }
            fclose(f);
            free(buffer);
            if (bFoundOffice)
            {
                return WINE_OFFICE;
            }
            else
            {
                return WINE;
            }
        }
    }
    free(buffer);
    return DATA;
}

/**
 * Get the name of the program to run from an autorun.inf.
 *
 * @param path The path to the mounted CD-ROM.
 *
 * @return A malloc()'d string containing the program name to run.
 */
char *getAutorunProgram(const char *const path)
{
    FILE *f = 0;
    char buffer[256];
    int pathLen = strlen(path);
    char *retVal = malloc(sizeof(char) * (pathLen + 256));
    char *filename = malloc(sizeof(char) * (pathLen + 13));

    if (0 == retVal)
    {
        if (0 != filename)
        {
            free(filename);
        }
        return 0;
    }
    if (0 == filename)
    {
        free(retVal);
        return 0;
    }
    snprintf(filename, (pathLen + 13), "%s/autorun.inf", path);

    if (0 == (f = fopen(filename, "r")))
    {
        fprintf(stderr, "Could not open %s.\n", filename);
        free(retVal);
        free(filename);
        return 0;
    }

    free(filename);

    while(!feof(f))
    {
        memset(buffer, 0, sizeof(char) * 256);
        fgets(buffer, 256, f);
        if (0 == strncasecmp(buffer, "open", 4))
        {
            char *end = buffer + 5;
            while (end && *end && !isspace(*end))
            {
                end++;
            }
            *end = 0;
            DPRINTF("Found program to run:  \"%s\".\n", (buffer + 5));
            snprintf(retVal, (pathLen + 256), "%s/%s", path, (buffer + 5));
            fclose(f);
            return retVal;
        }
    }
    fclose(f);
    free(retVal);
    DPRINTF("Could not find \"open=\" in autorun.inf.\n");
    return 0;
}
