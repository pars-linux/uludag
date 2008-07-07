#!/bin/bash

hav call fingermanager User.Manager getStatus 1337
hav call fingermanager User.Manager saveData 1337 fingerprintttt imageeeeee
hav call fingermanager User.Manager loadData 1337
hav call fingermanager User.Manager eraseData 1337
hav call fingermanager User.Manager getStatus 1337
