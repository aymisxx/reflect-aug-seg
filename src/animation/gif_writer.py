import imageio


def save_gif(frames, output_path, fps=10):
    imageio.mimsave(output_path, frames, fps=fps)