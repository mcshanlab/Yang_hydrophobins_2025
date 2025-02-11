#!/bin/bash

#submit slurm script
for index in {0..6000..500}
do    
  start=$(($index))
  end=$(($start+500))
  echo "submit:"
  echo $start 
  echo $end
  sbatch submit_map_AF.slurm $start $end
  echo "_______"
done

echo "6500"
echo "end"
sbatch submit_map_AF.slurm 6500 end
echo "_______"
