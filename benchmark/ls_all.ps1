aws s3 ls s3://multimedia-commons/data/images/0 --recursive | %{
    $in_str = $_
    $a = $in_str -split '\s+'
    #write-host in_str=$in_str
    #$in_str.gettype()
    $file_size = $a[2]
    $num_files += 1
    $file_name = $a[3]
    $tot_size += [int]$file_size
    write-host $file_name " size=" $file_size " num_files=" $num_files " tot_size=" $tot_size
}