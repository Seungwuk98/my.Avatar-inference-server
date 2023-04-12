#! bin/sh

/bin/bash -c "sudo docker run --rm -it --name inference-server-$1 --gpus ''device=$1'' --network host -v $(pwd):/app -v avatar:/app/my_avatar_ai inference-server /bin/bash"