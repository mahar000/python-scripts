#!/bin/bash
#----------------------------------------------------------------------------------------
# Script to run commands.
# ---------------------------------------------------------------------------------------
#Global Settings
script_dir=""
conf_dir="$script_dir/conf"
log_dir=""
log_files=""

#
#Exit function
Exit(){

echo "You have selected to exit the script"
exit 0

}
#
make_selection() {
    clear
    echo
    echo "******************************************************************"
    echo "***               log interactive options                   ***"
    echo "******************************************************************"
    file=$conf_dir/menu.csv
    cat $file|awk -F"|" '{print $1}'
    read -p "Enter the option: " option
    option1="$option)"
    choice=$(cat $file|grep ^"$option1"|awk -F")" '{print $1}')
    action=$(cat $file|grep ^"$option1"|awk -F"|" '{print $2}')
    desc=$(cat $file|grep ^"$option1"|awk -F")" '{print $2}'|awk -F"|" '{print $1}')
    echo "you have selected  option $option) $desc"
    
    if [ $option -eq 0 ] 
    then
     Exit
     else
    
    bash $script_dir/$conf_dir/$action

    fi 
}


# capture CTRL+C, CTRL+Z and quit singles using the trap
Finish()
{
echo -e "\n=================\nExit signal detected\n================="
exit 0
}

#-----------------------
trap Finish  HUP INT QUIT KILL TERM


#Main execution
while true
do
        make_selection
Finish
sleep 3
done