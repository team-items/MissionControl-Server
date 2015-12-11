#update the installed packages
echo "Updating the installed pacakges"
opkg update

#installing wget and curl (sources found at https://github.com/zeltner/libkipr_link_depth_sensor)
echo "installing wget"
opkg install http://netv.bunnie-bar.com/build/kovan-debug/LATEST/armv5te/wget_1.13.4-r13.1_armv5te.ip
echo "installing curl"
opkg install http://netv.bunnie-bar.com/build/kovan-debug/LATEST/armv5te/libcurl5_7.23.1-r0_armv5te.ipk
opkg install http://netv.bunnie-bar.com/build/kovan-debug/LATEST/armv5te/curl_7.23.1-r0_armv5te.ipk

#download latest release
echo "Downloading latest version from GitHub"
wget http://www.snoato.com/master.zip
unzip master.zip
rm master.zip
mv MissionControl-Server-master/ MissionControl-Server

cd MissionControl-Server
chmod +x main.py

#download pythonlib
echo "Downloading  and installing missing python parts"
wget http://www.snoato.com/python27lib.zip
unzip python27lib.zip
rm python27lib.zip

#install python lib
cp -nR python27lib /usr/lib/python2.7/

#remove download source
rm -r python27lib

#compile rsal
echo "Compiling RSAL"
gcc -o RSAL/RSAL RSAL/RSAL.c -lkovan

echo "Successfully installed! Switch into the MissionControl-Server directory and run ./main.py"