%{
/**
 * @file config.l
 * @brief Configuration file handler.
 *
 * File containing the configuration file parser.
 * Copyright (c) 2005, TUBITAK/UEKAE
 * @author S.Çağlar Onur <caglar@uludag.org.tr>
 *
 * Copyright 2001 Xandros Corporation.  All rights reserved.
 * @author Richard Rak
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
 */

#include "config.h"
#include "autorun.h"

#define YY_NO_UNPUT

static char *currentDevice = 0;
static char *previousDevice = 0;

char *splitConfigEntry(const char *const, const int);

%}

OPTION [a-zA-Z\- \t]*=.*\;
DEVICE_OPEN .*[ \t\n]+\{
DEVICE_CLOSE \}[ \t]*\;
COMMENT #.*$

%%
\n+                /* Stip new line characters */

{OPTION}        {
                    int index = 2;
                    char *option = splitConfigEntry(yytext, 0);
                    char *value = splitConfigEntry(yytext, index++);
                    char *extraOptions = 0;
                    device_map *device = 0;
                    if (previousDevice)
                    {
                        device = findDevice(deviceSettings, currentDevice);
                        if (!device)
                        {
                            if (!deviceSettings)
                            {
                                deviceSettings = allocDevice(0, currentDevice);
                                device = deviceSettings;
                            }
                            else
                            {
                                device = allocDevice(deviceSettings, currentDevice);
                            }
                        }
                    }
                    else
                    {
                        device = globalSettings;
                    }
                    DPRINTF("Setting %s to %s for %s.\n", option, value, device->device);
                    if (!updateDevice(device, option, value, 0))
                    {
                        fprintf(stderr, "Parse error parsing %s.\n", yytext);
                        return 127;
                    }
                    extraOptions = splitConfigEntry(yytext, index++);
                    while (extraOptions)
                    {
                        DPRINTF("Setting %s to %s with option %s for %s.\n", option, value, extraOptions, device->device);
                        if (!updateDevice(device, option, value, extraOptions))
                        {
                            fprintf(stderr, "Parse error parsing %s.\n", yytext);
                            return 127;
                        }
                        free(extraOptions);
                        extraOptions = splitConfigEntry(yytext, index++);
                    }
                    free(extraOptions);
                    free(option);
                    free(value);
                }

{DEVICE_OPEN}   {
                    if (previousDevice != 0)
                    {
                        fprintf(stderr, "Parse error parsing %s.\n", yytext);
                        return 127;
                    }
                    else
                    {
                        char *device = splitConfigEntry(yytext, 0);
                        if (device == 0)
                        {
                            fprintf(stderr, "Parse error parsing %s.\n", yytext);
                            return 127;
                        }
                        DPRINTF("Opening device block for %s.\n", device);
                        previousDevice = currentDevice;
                        currentDevice = device;
                    }
                }

{DEVICE_CLOSE}  {
                    if (previousDevice == 0)
                    {
                        fprintf(stderr, "Parse error parsing %s.\n", yytext);
                        return 127;
                    }
                    else
                    {
                        free(currentDevice);
                        currentDevice = previousDevice;
                        previousDevice = 0;
                    }
                }
                
{COMMENT}        /* Strip comments */

.*              {
                    fprintf(stderr, "Parse error parsing:  %s.\n", yytext);
                    return 127;
                }
%%

/**
 * Parse a config file to determine autorun entries.
 *
 * @param configFile The path to the config file to parse.
 *
 * @return Zero if an error occured.
 */
int parseConfig(const char *const configFile)
{
    FILE *f = fopen (configFile, "r");
    int yylexReturn = 0;
    currentDevice = strdup("global");
    if (!globalSettings)
    {
        globalSettings = allocDevice(0, currentDevice);
    }

    if (f == NULL)
    {
        return 0;
    }

    yyin = f;
    yyout = 0;

    yylexReturn = yylex();

    fclose(f);
    free(currentDevice);

    if (yylexReturn == 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

/**
 * Split a config line based upon white space and option delimiter characters.
 *
 * @param data A pointer to the buffer containing the config line.
 * @param index The entry to return from the line (zero indexed).
 *
 * @return A malloc()'d string containing the requested data.
 */
char *splitConfigEntry(const char *const data, const int index)
{
    char *buffer = strdup(data);
    char *p = buffer;
    char *start = 0;
    char *retVal = 0;
    int counter = -1;

    while (counter != index)
    {
        while (p && *p && (isspace(*p) || *p == ',') && *p != ';')
        {
            p++;
        }
        start = p;
        while (p && *p && !isspace(*p) && *p != ';' && *p != ',')
        {
            if (*p == '"')
            {
                char *startQuote = p;
                while (startQuote && *startQuote)
                {
                    *(startQuote-1) = *startQuote;
                    startQuote++;
                }
                while (p && *p && *p != '"')
                {
                    p++;
                }
                startQuote = (p + 1);
                while (startQuote && *startQuote)
                {
                    *(startQuote-1) = *startQuote;
                    startQuote++;
                }
                p--;
            }
            else if (*p == '$')
            {
                *p = '!';
            }
            p++;
        }
        *p++ = 0;
        if (strlen(start) == 0)
        {
            free(buffer);
            return 0;
        }
        counter++;
    }
    retVal = strdup(start);
    free(buffer);
    return retVal;
}
