import os

trainer_path = './Train.py'

gpcc_codec_path = '~/mpeg-pcc-tmc13/build/tmc3/tmc3'  # path to GPCC codec

num_experiments = 5  # number of independent experiments for each configuration

dataset_configs = {
    'TanksAndTemplates': {
        'dataset_root':  './data',
        'experiments_root': './results/TanksAndTemples',
        'scene': {
            'Train': 'images',
            'Truck': 'images'
        },  # key is scene name, value is image folder name
        'config_path': './Configs/TanksAndTemplates.yaml'
    },
}

model_configs = {
    'Lambda0_001': {
        'override_cfgs': {'gpcc_codec_path': gpcc_codec_path, 'lambda_weight': 0.001}},
    'Lambda0_005': {
        'override_cfgs': {'gpcc_codec_path': gpcc_codec_path, 'lambda_weight': 0.005}},
    'Lambda0_01': {
        'override_cfgs': {'gpcc_codec_path': gpcc_codec_path, 'lambda_weight': 0.01}},
}


if __name__ == '__main__':
    # generate command list
    cmd_list = []
    for dataset_name, dataset_config in dataset_configs.items():
        dataset_root, experiments_root = dataset_config['dataset_root'], dataset_config['experiments_root']
        scene_names = dataset_config['scene']
        config_path = dataset_config['config_path']

        os.makedirs(experiments_root, exist_ok=True)
        for model_name, model_config in model_configs.items():
            for scene_name, image_folder in scene_names.items():
                experiment_folder = os.path.join(experiments_root, scene_name)
                os.makedirs(experiment_folder, exist_ok=True)
                experiment_folder = os.path.join(experiment_folder, model_name)
                os.makedirs(experiment_folder, exist_ok=True)

                cmd = (f'python {trainer_path} --config {config_path} '
                       f'--root={os.path.join(dataset_root, scene_name)} --image_folder={image_folder} --save_directory={experiment_folder}')

                if 'override_cfgs' in model_config:
                    for key, value in model_config['override_cfgs'].items():
                        cmd += f' --{key}={value}'
                for _ in range(num_experiments):
                    cmd_list.append(cmd)

    # write commands to shell script
    if os.name == 'posix':  # linux
        with open('run.sh', 'w') as f:
            for cmd in cmd_list:
                f.write(f'{cmd}/n')
    else:  # windows
        with open('run.bat', 'w') as f:
            for cmd in cmd_list:
                f.write(f'{cmd}/n')
    print('Write commands to shell script successfully, please run it to start experiments.')