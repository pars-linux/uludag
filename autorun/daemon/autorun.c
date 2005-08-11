/**
 * @file autorun.c
 * @brief Main autorun file.
 *
 * File containing the main autorun functions.
 *
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

#include "autorun.h"

int executeDevice (device_map * const device);
int checkScriptExists (const program_map * const program);
int parseConfigFiles ();
int validateConfig ();
int runProgram (const DISK_TYPE disk, device_map * device);

void scanDevices ();
void reloadConfig ();
void signalHandler (int signum);
void usage ();
void dumpConfig ();

/* Program globals */
device_map *globalSettings = 0;
device_map *deviceSettings = 0;
uid_t UID = 65535;
gid_t GID = 65535;
pid_t bindPID = 0;
int bUserConfig = 1;
int bInUserConfig = 0;

/* Other globals */
static char *configFile = SYSCONF "/autorun.conf";
static char *userConfigFile = 0;
static int bReloadConfig = 0;
static int bRemovableDrive = 0;

/*
 * Main function (entry point)
 *
 * @param argc The number of command line arguments.
 * @param argv The command line arguments.
 */
int main (int argc, char *argv[])
{
    int opt = 0, retval;
    char *home = getenv ("HOME");
    static const struct option long_options[] = {
        {"help", 0, 0, 'h'},
        {"config", 1, 0, 'c'},
        {"bind", 1, 0, 'b'},
        {"dump", 0, 0, 'd'},
        {0, 0, 0, 0},
    };
    userConfigFile = malloc (sizeof (char) * (strlen (home) + 15));
    sprintf (userConfigFile, "%s/.autorun.conf", home);
    opterr = 0;
    UID = getuid ();
    GID = getgid ();

    while ((opt = getopt_long (argc, argv, "hdb:c:", long_options, NULL)) != EOF)
    {
        switch (opt)
        {
            case 'h':
            {
                usage ();
                exit (0);
            }
            case 'c':
            {
                free (userConfigFile);
                userConfigFile = strdup (optarg);
                break;
            }
            case 'b':
            {
                bindPID = strtol (optarg, 0, 0);
                break;
            }
            case 'd':
            {
                if (!parseConfigFiles ())
                {
                    exit (125);
                }
                dumpConfig ();
                exit (0);
            }
            case '?':
            case ':':
            {
                fprintf (stderr, "Unknown option.\n");
                exit (1);
            }
        }
    }

    /* Check if were given a PID to bind to */
    if (!bindPID)
    {
        fprintf (stderr, "Unspecified or unknown PID, will use parent PID.\n");
        bindPID = getppid ();
    }

    /* Check if the PID we are monitoring actually exists */
    if (-1 == kill (bindPID, 0))
    {
        if (errno == ESRCH)
        {
            fprintf (stderr, "Could not bind to PID %d.\n", bindPID);
            exit (127);
        }
    }

    /* Warn if we are running as root */
    if (!UID)
    {
        fprintf (stderr, "Running as root.  All executed programs will have ");
        fprintf (stderr, "root access.\n");
        fprintf (stderr, "This is probably not a good idea.\n");
    }

    DPRINTF ("Will run as UID:  %d\n", UID);
    DPRINTF ("Will run as GID:  %d\n", GID);
    DPRINTF ("Bound to PID:  %d\n", bindPID);

    /* Parse the config files */
    if (!parseConfigFiles ())
    {
        fprintf (stderr, "Error loading configuration.\n");
        exit (125);
    }

#ifndef DEBUG
    if (daemon (0, 0))
    {
        fprintf (stderr, "Could not become daemon.\n");
        exit (127);
    }
#endif

    openlog ("autorun", LOG_PID, LOG_DAEMON);

    /* Setup our signal handlers */
    signal (SIGCHLD, signalHandler);
    signal (SIGHUP, signalHandler);
    signal (SIGUSR1, signalHandler);    /*used when removable drives are plugged in */
    signal (SIGUSR2, signalHandler);    /*used when removable drives are pulled out */

    /* Main program loop */
    while (1)
    {
        sleep (CHECK_INTERVAL);

        /* Check to see if the PID we are bound to is still running */
        if (-1 == kill (bindPID, 0))
        {
            if (errno == ESRCH)
            {
                DPRINTF ("Bound PID has died.  Exiting.\n");
                break;
            }
        }

        /* Check to see if we should reload our config */
        if (bReloadConfig == 1)
        {
            reloadConfig ();
        }

        /*For removable drives */
        if (bRemovableDrive)
        {
            /*this will mark all except last device as ready */
            device_map *device = deviceSettings;
            if (device)
            {
                while (device->next)
                {
                    device->status = READY;
                    device = (device_map *) device->next;
                }
               /*mark the last one appropriately */
               if (bRemovableDrive == 1)
                  device->status = NOT_READY;
               else if (bRemovableDrive == 2)
                  device->status = READY;
             }
            bRemovableDrive = 0;
        }

        /* Perform all of the device scanning */
        scanDevices ();

        /* Poke USB devices */
        retval = system("grep Driver=usb-storage /proc/bus/usb/devices > /tmp/autorun.usb");
        if (!retval)        //grep returns 0 on finding a match
        {
            retval = system ("grep Sub=06 /tmp/autorun.usb");
            // USB 1.1 specs say interface subclass of 6 means SCSI
        }
        if (!retval)
        {
            struct dirent **files;
            int countdir = 0;

            //count how many entries are in /proc/scsi/usb-storage
            countdir = scandir ("/proc/scsi/usb-storage", &files, 0, alphasort);
            countdir -= 2;    //get rid of . and ..
            if (countdir < 0)
            {
                countdir = 0;
            }
            //NOTE: countdir may not work in the long run because a new USB device
            //   will not take over the SCSI host number from previous unplugged devices.
        }
    }
    free (userConfigFile);
    closelog ();
    return 0;
}

/*
 * Display program usage on STDERR
 */
void usage ()
{
    char *prog_usage =
"\nautorun -- CD-ROM checking and autorunning utility.\n\
Copyright (C) 2005 TUBITAK/UEKAE.\n\
Email bug reports to S.Çağlar Onur <caglar@uludag.org.tr>\n\
Usage:  autorun [options]\n\
Options:\n\
\t--config, -c <file>\tUse an alternate user configuration file <file>\n\
\t--help, -h\t\tHelp (ie, this screen)\n\
\t--bind, -b <pid>\tBind to a given PID\n\
\t--dump, -d\t\tDump the configuration information and exit\n";
    fprintf (stderr, prog_usage);
}

/*
 * Parse all of the configuration files (global/user).
 *
 * @return 0 on an error, -1 otherwise.
 */
int parseConfigFiles ()
{
    DPRINTF ("Parsing config file %s.\n", configFile);
    if (!parseConfig (configFile))
    {
        return 0;
    }
    if (bUserConfig)
    {
        DPRINTF ("Parsing user config file %s.\n", userConfigFile);
        bInUserConfig = 1;
        parseConfig (userConfigFile);
    }
    else
    {
        DPRINTF ("Skipping user config file %s.\n", userConfigFile);
    }
    DPRINTF ("Loading modules and mapping devices from %s.\n", LIBDIR);
    if (!loadModules ())
    {
        return 0;
    }
    if (!validateConfig ())
    {
        return 0;
    }
    return -1;
}

/*
 * Called if we detect that we received a SIGHUP (reload config).
 */
void reloadConfig ()
{
    device_map *device = deviceSettings;
    freeDevice (globalSettings);
    globalSettings = 0;
    while (device)
    {
        device = freeDevice (device);
    }
    deviceSettings = 0;
    if (!parseConfigFiles ())
    {
        exit (125);
    }
    bReloadConfig = 0;
}

/*
 * Main function to perform device scanning.
 */
void scanDevices ()
{
    device_map *device = deviceSettings;
    while (device)
    {
        DISK_TYPE type = device->module->check (device);
        if ((UNKNOWN != type) && (READY != device->status))
        {
            device->status = READY;
            if ((type == DATA))
            {
                  /* Check to see it's real type */
                  /* Hack upon hack.  Use the VIDEO type so that the check=relaxed option is not used. */
                  type = checkDataDisk (device->mountPoint);
            }
#ifdef DEBUG
            switch (type)
            {
                case MIXED:
                {
                    DPRINTF ("Found mixed mode device on %s.\n",
                    device->device);
                    break;
                }
                case WINE:
                {
                    DPRINTF ("Found WINE device on %s.\n",
                    device->device);
                    break;
                }
                case WINE_OFFICE:
                {
                    DPRINTF ("Found WINE OFFICE device on %s.\n",
                    device->device);
                    break;
                }
                case LOKI:
                {
                    DPRINTF ("Found LOKI device on %s.\n",
                    device->device);
                    break;
                }
                case DATA:
                {
                    DPRINTF ("Found data device on %s.\n",
                    device->device);
                    break;
                }
                case AUDIO:
                {
                    DPRINTF ("Found audio device on %s.\n",
                    device->device);
                    break;
                }
                case VIDEO:
                {
                    DPRINTF ("Found video device on %s.\n",
                    device->device);
                    break;
                }
                case VCDVIDEO:
                {
                    DPRINTF ("Found VCD video device on %s.\n",
                    device->device);
                    break;
                }
                default:
                {
                    DPRINTF ("Found an unknown disk type.\n");
                }
            }
#endif
        if (!runProgram (type, device))
        {
            device->status = NOT_READY;
        }
    }
    else if (UNKNOWN == type)
    {
        device->status = NOT_READY;
    }
        device = (device_map *) device->next;
    }
}

/*
 * The main signal handler.  All signals go through this signal handler.
 *
 * @param signum The signal being sent to this program.
 */
void signalHandler (int signum)
{
    switch (signum)
    {
        case SIGCHLD:
        {
            int status;
            while (-1 != waitpid (0, &status, WNOHANG))
            {
            }
            return;
        }
        case SIGHUP:
        {
            bReloadConfig = 1;
            return;
        }
        /*signalled when removable drive is inserted */
        case SIGUSR1:
        {
            DPRINTF ("Caught signal SIGUSR1\n");
            bReloadConfig = 1;
            bRemovableDrive = 1;
            return;
        }
        /*signal when removable drive is detached */
        case SIGUSR2:
        {
            DPRINTF ("Caught signal SIGUSR2\n");
            bReloadConfig = 1;
            bRemovableDrive = 2;
            return;
        }
        default:
        {
            return;
        }
    }
}

/*
 * Check to see if a program exists and whether it is executable or not.
 *
 * @param program A pointer to a program map to check.
 *
 * @return 0 if the program doesn't exist, otherwise -1.
 */
int checkScriptExists (const program_map * const program)
{
    struct stat sb;

    /*
     * If the program->script is null then we are using the global settings
     * for this particular program type.  So do not perform any check and
     * give the A.OK.
     */
    if (!program->script)
    {
        return -1;
    }

    /* Stat the device/file */
    if (stat (program->script, &sb) < 0)
    {
        return 0;
    }

    /* Find out if the script is executable */
    if (!S_ISREG (sb.st_mode) && !((sb.st_mode & S_IXUSR) || (sb.st_mode & S_IXGRP) || (sb.st_mode & S_IXOTH)))
    {
        return 0;
    }

    return -1;
}

/*
 * Dump the parsed configuration file in a somewhat readable format.
 */
void dumpConfig ()
{
    if (globalSettings)
    {
        program_map *program = (program_map *) globalSettings->programs;
        printf ("Default options:\n");
        printf ("Program mappings:\n");
        while (program)
        {
            int i = 0;
            printf ("\tDISC Type:  ");
            switch (program->diskType)
            {
                case UNKNOWN:
                {
                    printf ("unknown");
                    break;
                }
                case DATA:
                {
                    printf ("data");
                    break;
                }
                case WINE:
                {
                    printf ("wine");
                    break;
                }
                case WINE_OFFICE:
                {
                    printf("wine-office");
                    break;
                }
                case LOKI:
                {
                    printf("Loki");
                    break;
                }
                case MIXED:
                {
                    printf("mixedmode");
                    break;
                }
                case AUDIO:
                {
                    printf("audio");
                    break;
                }
                case VIDEO:
                {
                    printf("video");
                    break;
                }
                case VCDVIDEO:
                {
                    printf("VCDvideo");
                    break;
                }
            }
        printf (".\n");
        printf ("\t\tEnabled:  %s\n", (program->enabled) ? "yes" : "no");
        printf ("\t\tProgram to call:  %s ", program->script);
        while (program->options[i])
        {
              printf ("%s ", program->options[i++]);
        }
        printf ("\n");
        program = (program_map *) program->next;
        }
    }
    if (deviceSettings)
    {
        device_map *device = deviceSettings;
        while (device)
        {
            program_map *program = (program_map *) device->programs;
            printf ("Device %s:\n", device->device);
            printf ("Type:  %s.\n", device->deviceType);
            if (device->mountPoint)
            {
                printf ("Mount Point:  %s.\n", device->mountPoint);
            }
            printf ("\nProgram mappings:\n");
            while (program)
            {
                int i = 0;
                printf ("\tDISC Type:  ");
                switch (program->diskType)
                {
                    case UNKNOWN:
                    {
                        printf ("unknown");
                        break;
                    }
                    case DATA:
                    {
                        printf ("data");
                        break;
                    }
                    case WINE:
                    {
                        printf ("wine");
                        break;
                    }
                    case WINE_OFFICE:
                    {
                        printf ("wine-office");
                        break;
                    }
                    case LOKI:
                    {
                        printf ("Loki");
                        break;
                    }
                    case MIXED:
                    {
                        printf ("mixed mode");
                        break;
                    }
                    case AUDIO:
                    {
                        printf ("audio");
                        break;
                    }
                    case VIDEO:
                    {
                        printf ("video");
                        break;
                    }
                    case VCDVIDEO:
                    {
                        printf ("VCD video");
                        break;
                    }
                }
                printf (".\n");
                printf ("\t\tEnabled:  %s\n", (program->enabled) ? "yes" : "no");
                if (program->script)
                {
                    printf ("\t\tProgram to call:  %s ", program->script);
                    while (program->options[i])
                    {
                        printf ("%s ", program->options[i++]);
                    }
                    printf ("\n");
                }
                else
                {
                    program_map *globalProgram = globalSettings->programs;
                    while (globalProgram)
                    {
                        if (program->diskType == globalProgram->diskType)
                        {
                            printf ("\t\tProgram to call:  %s ", globalProgram->script);
                            while (globalProgram->options[i])
                            {
                                printf ("%s ", globalProgram->options[i++]);
                            }
                        printf ("\n");
                        break;
                    }
                   globalProgram = (program_map *) globalProgram->next;
                  }
            }
            program = (program_map *) program->next;
        }
        device = (device_map *) device->next;
        }
    }
}

/*
 * Validate that the configuration is valid.  Check device nodes, programs, etc.
 *
 * @return 0 if the configuration is invalid, -1 otherwise.
 */
int validateConfig ()
{
    device_map *device = deviceSettings;
    program_map *prog = globalSettings->programs;

    while (prog)
    {
        if (!checkScriptExists (prog))
        {
            fprintf (stderr, "Could not find program %s.  Exiting.\n", prog->script);
            exit (125);
        }
        prog = (program_map *) prog->next;
    }

    while (device)
    {
        if (!device->module)
        {
            fprintf (stderr, "No module \"%s\" loaded to support %s. Exiting.\n", device->deviceType, device->device);
            return 0;
        }
        if (!device->module->verify (device))
        {
            fprintf (stderr, "%s is not a valid device node for the type %s. Exiting.\n", device->device, device->deviceType);
            // This causes external USB CD-ROMs to fail on disconnect:
            //return 0;
        }
        prog = device->programs;
        while (prog)
        {
            if (!checkScriptExists (prog))
            {
                fprintf (stderr, "Could not find program %s.  Exiting.\n", prog->script);
                return 0;
            }
            prog = (program_map *) prog->next;
        }
        device = (device_map *) device->next;
    }
    return -1;
}

/*
 * Run the programs for "device" where the disk type is "disk".
 *
 * @param disk The disk type to execute a program for.
 * @param device The device_map entry to run.
 *
 * @return 0 if an error occurs, otherwise -1.
 */
int runProgram (const DISK_TYPE disk, device_map * device)
{
    pid_t pid;
    program_map *prog = device->programs;
    program_map *global = globalSettings->programs;

    while (prog)
    {
        if (prog->diskType == disk)
        {
            break;
        }
        prog = (program_map *) prog->next;
    }

    while (global)
    {
        if (global->diskType == disk)
        {
            break;
        }
        global = (program_map *) global->next;
    }

    /*
     * Oops.  We don't have a configuration for this disk type.
     * Exit without error.  No global && No device config = DO NOT SUPPORT
     */
    if (!prog && !global)
    {
        DPRINTF ("Disk type inserted could not be found.\n");
        return -1;
    }

    /* Is this diskType enabled?  If not, gladly exit without error. */
    if (prog->enabled == 0)
    {
        DPRINTF ("Disk type inserted is not enabled.\n");
        return -1;
    }

    pid = fork ();
    switch (pid)
    {
        case 0:
        {
            pid_t PID;
            char *args[MAXOPTIONS + 2];
            int i = 0, x = 0;
            memset (args, 0, sizeof (char) * (MAXOPTIONS + 2));

            /* Setup all of the arguments */
            if (!prog || !prog->script)
            {
                prog = global;
            }

            if (disk == LOKI)
            {
                char *buff =
                malloc (sizeof (char) * strlen (device->mountPoint) + 10);
                DPRINTF("Found LOKI disk and modifying args[] as such.\n");
                if (!buff)
                {
                    _exit (100);
                }
                sprintf (buff, "%s/setup.sh", device->mountPoint);
                args[i++] = strdup ("/bin/sh");
                args[i++] = buff;
            }
            else if (disk == WINE)
            {
                args[i++] = strdup (prog->script);

                if (prog->options[0])
                    args[i++] = strdup (prog->options[0]);
                else
                    args[i++] = getAutorunProgram (device->mountPoint);
            }
            else if (disk == WINE_OFFICE)
            {
                args[i++] = strdup (prog->script);

                if (prog->options[0])
                    args[i++] = strdup (prog->options[0]);
                else
                    args[i++] = strdup (device->mountPoint);
            }
            else
            {
                args[i++] = strdup (prog->script);
                while (prog->options[x])
                {
                    if (!strcmp (prog->options[x], "!d"))
                    {
                        DPRINTF("Option expansion -- Device Node.\n");
                        args[i++] = strdup (device->device);
                    }
                    else if (!strcmp (prog->options[x], "!v"))
                    {
                        DPRINTF("Option expansion -- Volume Label.\n");
                        args[i++] = device->module->volumeLabel (device);
                    }
                    else if (!strcmp (prog->options[x], "!m"))
                    {
                        DPRINTF("Option expansion -- Mount Point.\n");
                        args[i++] = strdup (device->mountPoint);
                    }
                    else if (!strcmp (prog->options[x], "!u"))
                    {
                        char buff[16];
                        DPRINTF ("Option expansion -- UID.\n"); 
                        snprintf (buff, 16, "%d", UID);
                        args[i++] = strdup (buff);
                    }
                    else if (!strcmp (prog->options[x], "!g"))
                    {
                        char buff[16];
                        DPRINTF ("Option expansion -- GID.\n");
                        snprintf (buff, 16, "%d", GID);
                        args[i++] = strdup (buff);
                    }
                    else if (!strcmp (prog->options[x], "!c"))
                    {
                        char buff[16];
                        DPRINTF("Option expansion -- Copyrighted Disc.\n");
                        snprintf (buff, 16, "%d", device->copyright);
                        args[i++] = strdup (buff);
                    }
                    else
                    {
                        args[i++] = strdup (prog->options[x]);
                    }
                    x++;
                }
            }

#ifdef DEBUG
            fprintf (stderr, "About to execute: ");
            x = 0;
            while (args[x])
            {
                fprintf (stderr, " %s", args[x++]);
            }
           fprintf (stderr, "\n");
#endif

        PID = fork ();
        switch (PID)
        {
            case 0:
            {
                int null = open ("/dev/null", O_WRONLY);
                if (0 != setuid (UID))
                {
                    fprintf (stderr, "Could not setuid() to %d.\n",UID);
                    _exit (126);
                }
                if (0 != setgid (GID))
                {
                    fprintf (stderr, "Could not setgid() to %d.\n", GID);
                    _exit (126);
                }
                if (-1 != null)
                {
#ifndef DEBUG
                    dup2 (STDOUT_FILENO, null);
                    dup2 (STDERR_FILENO, null);
#endif
                    close (null);
                }
                execv (args[0], args);
                fprintf (stderr, "Could not execute script %s.\n", args[0]);
                _exit (127);
            }
            case -1:
            {
                _exit (127);
            }
            default:
            {
                int status;
                waitpid (PID, &status, 0);

                while (-1 != waitpid (0, &status, WNOHANG)) {}
                _exit (0);
            }
        }
    }
        case -1:
        {
            return 0;
        }
        default:
        {}
    }
    return -1;
}
