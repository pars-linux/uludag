read -p "This is going to remove the baselayout scripts. You might need to reinstall baselayout afterwards."

sudo cp ./action/tr.org.pardus.comar.user.manager.policy /usr/share/PolicyKit/policy/
sudo cp ./comar/model.xml /etc/comar/

cd ./comar
sudo hav remove baselayout
sudo hav register baselayout User.Manager ./User_Manager_baselayout.py

cd ../ui
./generatepy.sh
