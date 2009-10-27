/*
    Copyright (c) 2009      by Marcin Kurczych          <tharkang@gmail.com>

    *************************************************************************
    *                                                                       *
    * This program is free software; you can redistribute it and/or modify  *
    * it under the terms of the GNU General Public License as published by  *
    * the Free Software Foundation; either version 2 of the License, or     *
    * (at your option) any later version.                                   *
    *                                                                       *
    *************************************************************************
*/
#include <QApplication>

#include "mainwindow.h"

#include "../integrator/QtPulseAudioIntegrator.h"
#include "../bindings/context.h"

#include <pulse/pulseaudio.h>

#include <iostream>
#include <assert.h>

int main(int argc, char *argv[])
{
	//Q_INIT_RESOURCE(systray);
	QApplication app(argc, argv);

	QtPulseAudio::Integrator pai;

	QtPulseAudio::Context *context = new QtPulseAudio::Context(&pai,"PulseAudio Qt Volume Manager");
	QApplication::setQuitOnLastWindowClosed(false);
	MainWindow * mw = new MainWindow(context);

	if ( context->connectToPulse(NULL, (pa_context_flags_t) 0, NULL) < 0) {
		std::cout << "Unable to connect pulse context" << std::endl;
    }

	mw->show();
	app.exec();

	return 0;
}
