#!/bin/bash


#blocklist="500,1000,5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,60000,65000,70000,75000,80000,85000,90000,95000,100000,105000,110000,115000"
#blocklist="2015"
startingblock=2015
endblock=167161
maxheight=110427836236357352041769395878404723568785424659630784333489133269811200
steps=2016
max=10
#last_block=$((($startingblock*$max)+1))

while [ $startingblock -lt $endblock ]
do
    blocklist+="$startingblock "
    startingblock=$[$startingblock +2016]
done

last_block=$(echo $blocklist  | tr " " "\n" | tail -n1)


echo -e "["
for i in  $(echo $blocklist | tr " " "\n")
do
	last_count=24
	amount_back=0
	
	echo -e " ["
	echo -e '   "'$(sparks-cli getblockhash $i)'",'
	echo -e "   "$maxheight","
	echo -e "   ["

	for ((count=$amount_back; count<=$last_count; count++))
	do
		block_height=$(($i-$count))
		current_blockhash=$(sparks-cli getblockhash $block_height)
		current_block_head=$(sparks-cli getblock $current_blockhash false | cut -c -160)
#		current_block_head=$(sparks-cli getblockheader $current_blockhash false)

		echo -e "    ["
		echo -e "      "$block_height","
		echo -e '      "'$current_block_head'"'
		if [ $count -eq $last_count ]
		then
			echo  "    ]"
		else
			echo  "    ],"
		fi
	done

	echo -e "   ]"

	if [ $i -eq $last_block ]
	then
		echo -e " ]"
	else
		echo -e " ],"
	fi

done
echo -e "]"
