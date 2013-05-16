LOG=$1

URLNUM=$(cat $LOG|  wc -l)
#log中的url是否有重复的?尽然木有
#Urlnum=`awk 'BEGIN{FS="\t"} {print $5}' $LOG |sort |uniq |wc -l`
#echo $Urlnum
RES=`awk 'BEGIN{FS=":"} {if(NR<='''$URLNUM''') print $1 '\n'}' $LOG |sort|uniq  -c`

Stime=`awk 'BEGIN{FS="\t";} {if(NR == 1) start=$2 }END{print start;}' $LOG`
Etime=`awk 'BEGIN{FS="\t";} {if(NR=='''$URLNUM''') end=$2;}END{print end}' $LOG`


echo $Stime
echo $Etime
let "Subtime=(`date -d "$Etime" +%s`-`date -d "$Stime" +%s`)/60"

echo urls:$URLNUM
echo used: $Subtime min
let "Speed=URLNUM/Subtime"
speed=`awk 'BEGIN{printf "%.10f\n",('''$URLNUM'''/'''$Subtime''')/60}'`
echo speed: $Speed/min
echo $speed/s
printf "$RES\n"
SuceNum=`echo $RES|awk -v list=1 '{while($list!="Success"&&list<=NF){list=list+1}if(list<=NF){print $(list-1)}else{print 0}}'`
echo ++++++++++Failedmsg:
Errormsg= awk 'BEGIN{FS="\t"}{if(NF==7){print $(NF-1)} }' $LOG | sort|uniq -c
echo ++++++++++Unfailedmsg:
Badresmsg= awk 'BEGIN{FS="\t"}{if(NF==5){print $(NF-1)} }' $LOG | sort|uniq -c

SuceRate=`awk 'BEGIN{printf "%.2f%\n",('''$SuceNum'''/'''$URLNUM''')*100}'`
echo sucessRate :$SuceRate

REALNUM=$(printf "$RES"| awk 'BEGIN{num=0}{ num+=$1}END{print num}') 
if [ $REALNUM == $URLNUM ];then
    echo \(sum right\)
else
    echo sum is $REALNUM,ERROR
fi
