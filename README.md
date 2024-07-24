#环境配置
bash conda_install.sh
conda activate RSGCBD
bash env_install.sh

#推理
python scripts/blur_inference.py --data_dir /home/agou/vv/ARGCCascade_Test/test1 --out_dir /home/agou/vv/ARGCCascade_Test/haha --model_path /home/agou/vv/Medsegdiff/map/savedmodel050000.pt  --image_size 256 --num_channels 128 --class_cond False --num_res_blocks 2 --num_heads 1 --learn_sigma True --use_scale_shift_norm False --attention_resolutions 16 --diffusion_steps 1000 --noise_schedule linear --rescale_learned_sigmas False --rescale_timesteps False
<!-- /home/agou/vv/Medsegdiff/map/savedmodel050000.pt -->

#调试配置
{
    // 使用 IntelliSense 了解相关属性。 
    // 悬停以查看现有属性的描述。
    // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: 当前文件",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "/home/agou/vv/ARGCCascade_Test/",
            "args": [
                "--data_dir", "/home/agou/vv/ARGCCascade_Test/test1",
                "--out_dir", "/home/agou/vv/ARGCCascade_Test/haha",
                "--image_size", "256",
                "--num_channels", "128",
                "--class_cond", "False",
                "--num_res_blocks", "2",
                "--num_heads", "1",
                "--learn_sigma", "True",
                "--use_scale_shift_norm", "False",
                "--attention_resolutions", "16",
                "--diffusion_steps", "1000",
                "--noise_schedule", "linear",
                "--rescale_learned_sigmas", "False",
                "--rescale_timesteps", "False",
                // "--lr", "1e-4", 
                // "--batch_size", "8"
            ]
        }
    ]
}
