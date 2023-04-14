
# old cultionet create  --res 0.00008983152841195214829 --project-path /home/ubuntu/training_data --crop-column class --grid-size 100 100 --config-file /home/ubuntu/ym_field_boundaries/4_cultionet_config.yml  --max-crop-class 1 --image-date-format %Y%j


docker run -v /home/ubuntu:/home  -it cultionet_195

cd /home/field_bounds
ln -s training_data/time_series_vars time_series_vars
ln -s training_data/user_train user_train

# cp /home/ubuntu/ym_field_boundaries/4_cultionet_config.yml /home/ubuntu/training_data/config.yml


cultionet create \
        --transforms {fliplr,flipud,rot90,rot180,rot270,tswarp,tsnoise,tsdrift,roll,gaussian,saltpepper,speckle} \
        --res 0.00008983152841195214829 \
        --project-path . \
        --config-file config.yml \
        --crop-column class \
        --grid-size 100 100 \
        --max-crop-class 1 \
        --image-date-format %Y%j \
        --feature-pattern {region}/{image_vi} \
        --start-date 05-01 \
        --end-date 05-01
        
        
cultionet train --project-path . \
                --expected-dim 4 \
                --expected-height 100 \
                --expected-width 100 \
                --delete-mismatches \
                --recalc-zscores\
                --val-frac 0.2 \
                --random-seed 500 \
                --batch-size 4 \
                --epochs 30 \
                --filters 32 \
                --device cpu \
                --patience 5 \
                --learning-rate 0.001 \
                --reset-model
 

