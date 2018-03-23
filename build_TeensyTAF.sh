
SKETCHDIR=WN_TeensyTAF_Buffered_F32_OutputSpect_Adaptive
SKETCHFILE=$SKETCHDIR/$SKETCHDIR.ino

if [ -d $SKETCHDIR/build ]
then
rm -r $SKETCHDIR/build
fi

mkdir $SKETCHDIR/build
cp $SKETCHFILE $SKETCHDIR/build

arduino --pref sketchbook.path=/home/brad/Arduino --pref build.path=$SKETCHDIR/build --verify $SKETCHDIR/"$SKETCHDIR".ino
teensy_post_compile -file=$SKETCHDIR.ino -path=/home/brad/Arduino/TeensyTAF/$SKETCHDIR/build/ -tools=/home/brad/packages/arduino-1.8.4/hardware/tools

