/* -*- Mode: C; tab-width: 8; indent-tabs-mode: t; c-basic-offset: 8 -*-
 *
 * Copyright (C) 2007 Richard Hughes <richard@hughsie.com>
 * Copyright (C) 2007 S.Çağlar Onur <caglar@pardus.org.tr>
 *
 * Licensed under the GNU General Public License Version 2
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
 * Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 */

#include <packagekit-glib/packagekit.h>
#include <pk-backend.h>
#include <pk-backend-spawn.h>

static PkBackendSpawn *spawn;

/**
 * backend_initialize:
 * This should only be run once per backend load, i.e. not every transaction
 */
static void
backend_initialize (PkBackend *backend)
{
	egg_debug ("backend: initialize");
	spawn = pk_backend_spawn_new ();
	pk_backend_spawn_set_name (spawn, "pisi");
}

/**
 * backend_destroy:
 * This should only be run once per backend load, i.e. not every transaction
 */
static void
backend_destroy (PkBackend *backend)
{
	egg_debug ("backend: destroy");
	g_object_unref (spawn);
}

/**
 * backend_get_groups:
 */
static PkBitfield
backend_get_groups (PkBackend *backend)
{
	int groups;
	groups = pk_bitfield_from_enums(
		   PK_GROUP_ENUM_ACCESSIBILITY,
		   PK_GROUP_ENUM_ACCESSORIES,
		   PK_GROUP_ENUM_ADMIN_TOOLS,
		   PK_GROUP_ENUM_COMMUNICATION,
		   PK_GROUP_ENUM_DESKTOP_GNOME,
		   PK_GROUP_ENUM_DESKTOP_KDE,
		   PK_GROUP_ENUM_DESKTOP_OTHER,
		   PK_GROUP_ENUM_DESKTOP_XFCE,
		   PK_GROUP_ENUM_EDUCATION,
		   PK_GROUP_ENUM_FONTS,
		   PK_GROUP_ENUM_GAMES,
		   PK_GROUP_ENUM_GRAPHICS,
		   PK_GROUP_ENUM_INTERNET,
		   PK_GROUP_ENUM_LEGACY,
		   PK_GROUP_ENUM_LOCALIZATION,
		   PK_GROUP_ENUM_MULTIMEDIA,
		   PK_GROUP_ENUM_NETWORK,
		   PK_GROUP_ENUM_OFFICE,
		   PK_GROUP_ENUM_OTHER,
		   PK_GROUP_ENUM_POWER_MANAGEMENT,
		   PK_GROUP_ENUM_PROGRAMMING,
		   PK_GROUP_ENUM_PUBLISHING,
		   PK_GROUP_ENUM_SECURITY,
		   PK_GROUP_ENUM_SERVERS,
		   PK_GROUP_ENUM_SYSTEM,
		   PK_GROUP_ENUM_VIRTUALIZATION,
		   PK_GROUP_ENUM_SCIENCE,
		   PK_GROUP_ENUM_DOCUMENTATION,
		   PK_GROUP_ENUM_ELECTRONICS,
		   PK_GROUP_ENUM_UNKNOWN,
		   -1);
	return groups;
}

/**
 * backend_get_filters:
 */
static PkBitfield
backend_get_filters (PkBackend *backend)
{
	return pk_bitfield_from_enums(
		PK_FILTER_ENUM_GUI,
		PK_FILTER_ENUM_INSTALLED,
		-1);
}

/**
 * backend_get_mime_types:
 */
static gchar *
backend_get_mime_types (PkBackend *backend)
{
	return g_strdup ("application/x-pisi");
}

/**
 * pk_backend_cancel:
 */
static void
backend_cancel (PkBackend *backend)
{
	/* this feels bad... */
	pk_backend_spawn_kill (spawn);
}

/**
 * backend_download_packages:
 */
static void
backend_download_packages (PkBackend *backend, gchar **package_ids, const gchar *directory)
{
	gchar *package_ids_temp;

	/* send the complete list as stdin */
	package_ids_temp = pk_package_ids_to_text (package_ids);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "download-packages", directory, package_ids_temp, NULL);
	g_free (package_ids_temp);
}

/**
 * backend_get_depends:
 */
static void
backend_get_depends (PkBackend *backend, PkBitfield filters, gchar **package_ids, gboolean recursive)
{
	gchar *filters_text;
	gchar *package_ids_temp;
	package_ids_temp = pk_package_ids_to_text (package_ids);
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "get-depends", filters_text, package_ids_temp, pk_backend_bool_to_text (recursive), NULL);
	g_free (filters_text);
	g_free (package_ids_temp);
}

/**
 * backend_get_details:
 */
static void
backend_get_details (PkBackend *backend, gchar **package_ids)
{
	gchar *package_ids_temp;
	package_ids_temp = pk_package_ids_to_text (package_ids);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "get-details", package_ids_temp, NULL);
	g_free (package_ids_temp);
}

/**
 * backend_get_files:
 */
static void
backend_get_files (PkBackend *backend, gchar **package_ids)
{
	gchar *package_ids_temp;
	package_ids_temp = pk_package_ids_to_text (package_ids);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "get-files", package_ids_temp, NULL);
	g_free (package_ids_temp);
}

/**
 * backend_get_packages:
 */
static void
backend_get_packages (PkBackend *backend, PkBitfield filters)
{
	gchar *filters_text;
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "get-packages", filters_text, NULL);
	g_free (filters_text);
}

/**
 * backend_get_requires:
 */
static void
backend_get_requires (PkBackend *backend, PkBitfield filters, gchar **package_ids, gboolean recursive)
{
	gchar *filters_text;
	gchar *package_ids_temp;
	package_ids_temp = pk_package_ids_to_text (package_ids);
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "get-requires", filters_text, package_ids_temp, pk_backend_bool_to_text (recursive), NULL);
	g_free (filters_text);
	g_free (package_ids_temp);
}

/**
 * backend_get_update_detail:
 */
static void
backend_get_update_detail (PkBackend *backend, gchar **package_ids)
{
	gchar *package_ids_temp;
	package_ids_temp = pk_package_ids_to_text (package_ids);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "get-update-detail", package_ids_temp, NULL);
	g_free (package_ids_temp);
}

/**
 * backend_get_updates:
 */
static void
backend_get_updates (PkBackend *backend, PkBitfield filters)
{
	gchar *filters_text;
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "get-updates", filters_text, NULL);
	g_free (filters_text);
}

/**
 * backend_install_packages:
 */
static void
backend_install_packages (PkBackend *backend, gchar **package_ids)
{
	gchar *package_ids_temp;

	/* check network state */
	if (!pk_backend_is_online (backend)) {
		pk_backend_error_code (backend, PK_ERROR_ENUM_NO_NETWORK, "Cannot install when offline");
		pk_backend_finished (backend);
		return;
	}

	/* send the complete list as stdin */
	package_ids_temp = pk_package_ids_to_text (package_ids);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "install-packages", package_ids_temp, NULL);
	g_free (package_ids_temp);
}

/**
 * backend_install_files:
 */
static void
backend_install_files (PkBackend *backend, gboolean trusted, gchar **full_paths)
{
	gchar *package_ids_temp;

	/* send the complete list as stdin */
	package_ids_temp = g_strjoinv (PK_BACKEND_SPAWN_FILENAME_DELIM, full_paths);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "install-files", pk_backend_bool_to_text (trusted), package_ids_temp, NULL);
	g_free (package_ids_temp);
}

/**
 * backend_refresh_cache:
 */
static void
backend_refresh_cache (PkBackend *backend, gboolean force)
{
	/* check network state */
	if (!pk_backend_is_online (backend)) {
		pk_backend_error_code (backend, PK_ERROR_ENUM_NO_NETWORK, "Cannot refresh cache whilst offline");
		pk_backend_finished (backend);
		return;
	}

	pk_backend_spawn_helper (spawn, "pisiBackend.py", "refresh-cache", NULL);
}

/**
 * pk_backend_remove_packages:
 */
static void
backend_remove_packages (PkBackend *backend, gchar **package_ids, gboolean allow_deps, gboolean autoremove)
{
	gchar *package_ids_temp;

	/* send the complete list as stdin */
	package_ids_temp = pk_package_ids_to_text (package_ids);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "remove-packages", pk_backend_bool_to_text (allow_deps), package_ids_temp, NULL);
	g_free (package_ids_temp);
}
/**
 * pk_backend_repo_enable:
 */
static void
backend_repo_enable (PkBackend *backend, const gchar *rid, gboolean enabled)
{
	if (enabled == TRUE) {
		pk_backend_spawn_helper (spawn, "pisiBackend.py", "repo-enable", rid, "true", NULL);
	} else {
		pk_backend_spawn_helper (spawn, "pisiBackend.py", "repo-enable", rid, "false", NULL);
	}
}

/**
 * pk_backend_search_details:
 */
static void
backend_search_details (PkBackend *backend, PkBitfield filters, const gchar *search)
{
	gchar *filters_text;
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "search-details", filters_text, search, NULL);
	g_free (filters_text);
}

/**
 * pk_backend_search_file:
 */
static void
backend_search_file (PkBackend *backend, PkBitfield filters, const gchar *search)
{
	gchar *filters_text;
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "search-file", filters_text, search, NULL);
	g_free (filters_text);
}

/**
 * pk_backend_search_group:
 */
static void
backend_search_group (PkBackend *backend, PkBitfield filters, const gchar *search)
{
	gchar *filters_text;
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "search-group", filters_text, search, NULL);
	g_free (filters_text);
}

/**
 * pk_backend_search_name:
 */
static void
backend_search_name (PkBackend *backend, PkBitfield filters, const gchar *search)
{
	gchar *filters_text;
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "search-name", filters_text, search, NULL);
	g_free (filters_text);
}

/**
 * pk_backend_update_packages:
 */
static void
backend_update_packages (PkBackend *backend, gchar **package_ids)
{
	gchar *package_ids_temp;

	/* check network state */
	if (!pk_backend_is_online (backend)) {
		pk_backend_error_code (backend, PK_ERROR_ENUM_NO_NETWORK, "Cannot install when offline");
		pk_backend_finished (backend);
		return;
	}

	/* send the complete list as stdin */
	package_ids_temp = pk_package_ids_to_text (package_ids);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "update-packages", package_ids_temp, NULL);
	g_free (package_ids_temp);
}

/**
 * pk_backend_update_system:
 */
static void
backend_update_system (PkBackend *backend)
{
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "update-system", NULL);
}

/**
 * pk_backend_resolve:
 */
static void
backend_resolve (PkBackend *backend, PkBitfield filters, gchar **package_ids)
{
	gchar *filters_text;
	gchar *package_ids_temp;
	filters_text = pk_filter_bitfield_to_text (filters);
	package_ids_temp = pk_package_ids_to_text (package_ids);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "resolve", filters_text, package_ids_temp, NULL);
	g_free (filters_text);
	g_free (package_ids_temp);
}

/**
 * pk_backend_get_repo_list:
 */
static void
backend_get_repo_list (PkBackend *backend, PkBitfield filters)
{
	gchar *filters_text;
	filters_text = pk_filter_bitfield_to_text (filters);
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "get-repo-list", filters_text, NULL);
	g_free (filters_text);
}

/**
 * pk_backend_repo_set_data:
 */
static void
backend_repo_set_data (PkBackend *backend, const gchar *rid, const gchar *parameter, const gchar *value)
{
	pk_backend_spawn_helper (spawn, "pisiBackend.py", "repo-set-data", rid, parameter, value, NULL);
}

PK_BACKEND_OPTIONS (
	"PiSi",					/* description */
	"S.Çağlar Onur <caglar@pardus.org.tr>",	/* author */
	backend_initialize,			/* initalize */
	backend_destroy,			/* destroy */
	backend_get_groups,			/* get_groups */
	backend_get_filters,			/* get_filters */
	backend_get_mime_types,			/* get_mime_types */
	backend_cancel,				/* cancel */
	backend_download_packages,		/* download_packages */
	NULL,					/* get_categories */
	backend_get_depends,			/* get_depends */
	backend_get_details,			/* get_details */
	NULL,					/* get_distro_upgrades */
	backend_get_files,			/* get_files */
	backend_get_packages,			/* get_packages */
	backend_get_repo_list,			/* get_repo_list */
	backend_get_requires,			/* get_requires */
	backend_get_update_detail,		/* get_update_detail */
	backend_get_updates,			/* get_updates */
	backend_install_files,			/* install_files */
	backend_install_packages,		/* install_packages */
	NULL,					/* install_signature */
	backend_refresh_cache,			/* refresh_cache */
	backend_remove_packages,		/* remove_packages */
	backend_repo_enable,			/* repo_enable */
	backend_repo_set_data,			/* repo_set_data */
	backend_resolve,			/* resolve */
	NULL,					/* rollback */
	backend_search_details,			/* search_details */
	backend_search_file,			/* search_file */
	backend_search_group,			/* search_group */
	backend_search_name,			/* search_name */
	backend_update_packages,		/* update_packages */
	backend_update_system,			/* update_system */
	NULL					/* what_provides */
);

