#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard modules
import logging

# PiSi
import pisi

# Ahenk
from ahenk.agent import utils


def process(message, options):
    """
        Policy/command processor.

        Arguments:
            message: Message object
            options: Options
    """

    dryrun = options.dryrun

    if message.type == "policy":
        if "softwareRepositories" in message.policy:
            repositories = []
            # Build new repository list
            for repo in message.policy["softwareRepositories"]:
                try:
                    repo_name, repo_url = repo.split()
                except ValueError:
                    repositories = []
                    break
                repositories.append((repo_name, repo_url))
            # Set new repositories if necessary
            if len(repositories):
                set_repositories(repositories, dryrun)

        if "softwareUpdateSchedule" in message.policy:
            update_schedule = message.policy["softwareUpdateSchedule"][0]
        else:
            # Default update schedule is "03:00 everyday"
            update_schedule = "0 3 * * *"

        if "softwareUpdateMode" in message.policy:
            update_mode = message.policy["softwareUpdateMode"][0]
            if update_mode == "off":
                set_autoupdate("off", None, dryrun)
            elif update_mode in ["security", "full"]:
                set_autoupdate(update_mode, update_schedule, dryrun)
        else:
            set_autoupdate("off", None, dryrun)
    elif message.type == "command":
        if message.command == "software.packages":
            logging.info("Software: Listing packages.")
            packages = pisi.api.list_installed()
            message.reply("software.packages", packages)
        elif message.command == "software.repositories":
            logging.info("Software: Listing repositories.")
            repositories = get_repositories()
            message.reply("software.repositories", repositories)

def get_repositories():
    repo_db =  pisi.db.repodb.RepoDB()
    repositories = []
    for repo_url in repo_db.list_repo_urls():
        repo_name = repo_db.get_repo_by_url(repo_url)
        repositories.append((repo_name, repo_url))
    return repositories

def set_repositories(repositories_new, dryrun=False):
    repositories_now = get_repositories()
    if repositories_now != repositories_new:
        logging.info("Software: Setting new repositories.")
        if not dryrun:
            # Remove all repositories
            for repo_name, repo_url in repositories_now:
                pisi.api.remove_repo(repo_name)
            # Add new repositories
            for repo_name, repo_url in repositories_new:
                pisi.api.add_repo(repo_name, repo_url)

def set_autoupdate(mode, crondate=None, dryrun=False):
    if mode == "off" or not crondate:
        logging.info("Software: Auto update disabled.")
        if not dryrun:
            # Remove command from crontab, ignore arguments while matching records
            utils.update_cron("ahenk_software_update", noargs=True)
    elif mode == "security":
        logging.info("Software: Security updates will be made automatically.")
        if not dryrun:
            utils.update_cron("ahenk_software_update --security", crondate, noargs=True)
    elif mode == "full":
        logging.info("Software: All updates will be made automatically.")
        if not dryrun:
            utils.update_cron("ahenk_software_update", crondate, noargs=True)
