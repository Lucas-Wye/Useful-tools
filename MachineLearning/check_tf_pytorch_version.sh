#! /bin/sh
###
 # @Author: Lucas Wye
 # @Date: 2020-08-09 09:33:51
 # @Description: This is a script for checking the version of tensorflow and pytorch of All Linux Server's User
### 

for conda in `ls -d /home/*/anaconda3`; do
    py="$conda/bin/python -c"
    list="$conda/bin/conda list"

    torch_version=`$py "import torch;print(torch.__version__);print(torch.cuda.is_available())" 2>/dev/null`
    tf_version=`$py "import tensorflow as tf;print(tf.__version__);" 2>/dev/null`

    if [[ $torch_version != "" || $tf_version != "" ]];then
        echo $conda

        echo -e "\033[36m pytorch: \033[0m" $torch_version
        echo `$list torch | grep torch`

        echo -e "\033[31m tensorflow: \033[0m" $tf_version
        echo `$list tensorflow | grep tensorflow`
        echo
    fi
done
