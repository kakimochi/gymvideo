import subprocess

subprocess.call(['apt', 'update'])
subprocess.call(['apt', 'install', 'xvfb'])
subprocess.call(['pip', 'install', 'pyvirtualdisplay'])

from pyvirtualdisplay import Display

d = Display()
d.start()

import gymnasium as gym
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
from IPython.display import HTML

class GymVideo(gym.Wrapper):
    def __init__(self, env):
        gym.Wrapper.__init__(self, env)
        self.frames = []
     
    def reset(self, reset_frames=False):
        # フレームをリセットする場合はリストを空に
        if reset_frames:
            self.frames = []
            
        return self.env.reset()

    def step(self, ac, monitor_frames=False):
        if monitor_frames:
            self.frames.append(self.env.render())
        return self.env.step(ac)

    def save_video(self, save_name=None, figsize=None, display_inline=False):
        """
        params:
            save_name      : default None. If you set save_name, gif animation will be saved.
            figsize        : default None, If you set figsize (ex:(5, 5)), plt.figure(figsize=figsize) will be executed.
            display_inline : You should use when you set save_name.
                             if you set display_inline True, gif animation will be displayed inline.
        """
        if figsize != None:
            plt.figure(figsize=figsize)
            
        patch = plt.imshow(self.frames[0], cmap='gray')
        plt.axis('off')
        
        def animate(i):
            patch.set_data(self.frames[i])
        
        anim = animation.FuncAnimation(plt.gcf(), animate, frames=len(self.frames), interval=50)

        if save_name != None:
            if display_inline != True:
                anim.save(save_name, writer=PillowWriter(fps=60))
            else:
                anim.save(save_name, writer=PillowWriter(fps=60))
                display(HTML(anim.to_jshtml(default_mode='once')))
        else:
            display(HTML(anim.to_jshtml(default_mode='once')))
        plt.close()
        
    def execute_one_episode(self, model, reset_frames=True):
        # 1エピソードを実行しフレームに格納
        obs = self.reset(reset_frames=reset_frames)

        while True:
            action, _state = model.predict(obs, deterministic=True)
            obs, reward, done, info = self.step(action, monitor_frames=True)
            self.env.render()
            if done:
                break
