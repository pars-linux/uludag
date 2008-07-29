sudo cp ./action/tr.org.pardus.comar.user.manager.policy /usr/share/PolicyKit/policy/
sudo cp ./comar/model.xml /etc/comar/

cd ./comar
sudo hav register baselayout User.Manager ./User_Manager_Baselayout.py

cd ../ui
./generatepy.sh
