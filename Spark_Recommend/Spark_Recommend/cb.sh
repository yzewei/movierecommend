#!/bin/bash
#!/bin/sh
for((i=0;i<60;i++))
 do
   spark-submit /home/master/movie/CB_tag2.py
   sleep 60s
done

