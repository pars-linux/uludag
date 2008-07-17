#ifndef KNAZARBALLOON_H
#define KNAZARBALLOON_H

#include <qwidget.h>
#include <kactivelabel.h>

class KNazarActiveLabel : public KActiveLabel
{
	Q_OBJECT

public:
	KNazarActiveLabel( QWidget *parent = 0, const char* name = 0 );
	KNazarActiveLabel( const QString& text, QWidget *parent = 0, const char* name = 0 );
};

class KNazarBalloon : public QWidget
{
	Q_OBJECT

public:
	KNazarBalloon(const QString &text, const QString &pic);

	void setAnchor(const QPoint &anchor);

signals:
	void signalButtonClicked();
	void signalIgnoreButtonClicked();
	void signalBalloonClicked();

protected:
	virtual void updateMask();

private:
	QPoint mAnchor;
};

#endif

