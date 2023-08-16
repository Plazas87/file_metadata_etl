#!/bin/bash

# List information of all block devices, just the NAME
# -d, --nodeps - don't print slaves or holders
# -n, --noheadings - don't print headings
# -o, --output <list>  This time I just want the name
disk_list=$(lsblk -no NAME)

for disk in $disk_list; do
    # -b file - True if file is a Block special device. [[ -b <file_name>]]
    if [[ -b "/dev/$disk" ]]; then

        # verify that the disk is mounted
        # df -h - colums output: Filesystem | Size | Used | Avail | Use% | Mounted on
        # Get the last columns 'Mounted on' -> awk '{print $6}' if the disk is not mounted it return empty 
        mount_point=$(df -h | grep "/dev/$disk" | awk '{print $6}')
        
        # -n String - True if the length of String is nonzero.
        if [[ -n $mount_point ]]; then
            # Check if the disk has partitions
            disk_partitions=$(lsblk -o NAME,TYPE | grep "$disk" | grep "part" | awk '{print $1}')
            if [[ -n $disk_partitions ]]; then
                echo "Disk: '/dev/$disk' has partitions:"
                # loop the partitions and get the information for all of them
                for disk_partition in $disk_partitions; do
                    # Remove special characters
                    clean_disk_partition=$(echo "$disk_partition" | sed 's/[^[:alnum:] ]//g')
                    # get the partition mount point
                    partition_mount_point=$(df -h | grep "/dev/$clean_disk_partition" | awk '{print $6}')
                    echo "-Partition: /dev/$clean_disk_partition"
                    echo "Mount point: $partition_mount_point"
                    # Get the free space for the current block device partition using the fourth column of the df -h colums output
                    free_space=$(df -h | grep "/dev/$clean_disk_partition" | awk '{print $4}')
                    echo "Free space: $free_space"
                    echo "**"
                done
                else
                    echo "Disk: /dev/$disk"
                    echo "Mount point: $mount_point"
                    
                    # Get the free space for the current block device using the fouth column of the df -h colums output
                    free_space=$(df -h | grep "/dev/$disk" | awk '{print $4}')
                    echo "Free space: $free_space"
            fi
            echo "------------------------"
        fi
    fi
done