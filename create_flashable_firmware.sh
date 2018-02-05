#!/bin/bash

if [ -z $1 ]; then
    echo "Usage: create_flashable_firmware.sh ROM_FILE"
    exit 1
fi

if [ ! -f $1 ]; then
    echo "** File not available."
    exit 1
fi

DATE=$(date "+%Y-%m-%d %H:%M:%S")
HOSTNAME=$(cat /etc/hostname)

function creatupscrpt() {
    cat > $2 << EOF
$(cat $1 | awk '/getprop/ && /ro.product.device/')
$(cat $1 | awk '/ui_print/ && /Target:/')
show_progress(0.200000, 10);

# Created by Xiaomi Flashable Firmware Creator
# $DATE - $HOSTNAME

ui_print("Patching firmware images...");
$(cat $1 | awk '/package_extract_file/ && /firmware-update\//')
show_progress(0.100000, 2);
set_progress(1.000000);
EOF
}

function checkupscrpt() {
    file=temp/META-INF/com/google/android/updater-script
    path=/firmware/image
    node=/dev/block/bootdevice/by-name
    if grep -wq "$path/sec.dat" $file
    then
        sed -i "s|$path/sec.dat|$node/sec|g" $file
    elif grep -wq "$path/splash.img" $file
    then
        sed -i "s|$path/splash.img|$node/splash|g" $file
    fi
}

mkdir temp/
mkdir temp/unzipped
unzip -qq $1 -d temp/unzipped/

if [ ! -f temp/unzipped/META-INF/com/google/android/update-binary ] || [ ! -f temp/unzipped/META-INF/com/google/android/updater-script ] || [ ! -d temp/unzipped/firmware-update ]; then
    echo "** This zip doesn't contain firmware directory."
    rm -rf temp/
    exit 1
fi

mv temp/unzipped/firmware-update temp/

mkdir -p temp/META-INF/com/google/android
mv temp/unzipped/META-INF/com/google/android/update-binary temp/META-INF/com/google/android/
creatupscrpt temp/unzipped/META-INF/com/google/android/updater-script temp/META-INF/com/google/android/updater-script

cd temp/
checkscrpt
zip -qq -r9 ../fw_$1 META-INF/ firmware-update/
cd ../

rm -rf temp/
