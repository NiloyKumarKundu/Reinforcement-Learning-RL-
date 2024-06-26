import gymnasium as gym
import stable_baselines3
import os
import argparse
import torch


# Create directories to hold models and logs
model_dir = 'models'
log_dir = 'logs'
os.makedirs(model_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# Set the training device
if torch.cuda.is_available(): 
    device = "cuda" 
else: 
    device = "cpu" 
device = torch.device(device)

def train(env, sb3_algo):
    model = sb3_class('MlpPolicy', env, verbose=1, device=device, tensorboard_log=log_dir)
        
    TIMESTEPS = 25000
    iters = 0
    while True:
        iters += 1

        model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False)
        model.save(f'{model_dir}/{sb3_algo}_{TIMESTEPS*iters}')

def test(env, path_to_model, model_name):
    env = gym.wrappers.RecordVideo(env, video_folder="./videos/", name_prefix=f"test-video_{model_name}", episode_trigger=lambda x: x % 2 == 0)

    model = sb3_class.load(path_to_model, env=env)
    obs, _ = env.reset()

    ###
    # Start the recorder
    env.start_video_recorder()

    while True:
        action, _ = model.predict(obs)
        obs, _, terminated, truncated, _ = env.step(action)

        if terminated or truncated:
            break
    ####
    # Don't forget to close the video recorder before the env!
    env.close_video_recorder()



if __name__ == '__main__':
    # Command to train the model
    # python "Pendulum environment testing.py" Pendulum-v1 TD3 -t

    # Command to show the performance in tensorboard
    # tensorboard --logdir logs

    # Parse command line inputs
    parser = argparse.ArgumentParser(description='Train or test model.')
    parser.add_argument('gymenv', help='Gymnasium environment i.e. Pendulum-v1')
    parser.add_argument('sb3_algo', help='StableBaseline3 RL algorithm i.e. A2C, DDPG, DQN, PPO, SAC, TD3')
    parser.add_argument('-t', '--train', action='store_true')
    parser.add_argument('-s', '--test', metavar='path_to_model')
    args = parser.parse_args()

    # Dynamic way to import algorithm. For example, passing in DQN is equivalent to hardcoding:
    # from stable_baseline3 import DQN
    sb3_class = getattr(stable_baselines3, args.sb3_algo)


    if args.train:
        gymenv = gym.make(args.gymenv, render_mode=None)
        train(gymenv, args.sb3_algo)

    # Command to test the model
    # python "Pendulum environment testing.py" Pendulum-v1 SAC -s ./models/SAC_450000.zip 
    if args.test:
        if os.path.isfile(args.test):
            gymenv = gym.make(args.gymenv, render_mode='rgb_array')
            test(gymenv, path_to_model=args.test, model_name=args.sb3_algo)
        else:
            print(f'{args.test} not found.')
