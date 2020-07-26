# =========================================================================

# RunwayML port of White-box-Cartoonization
# https://github.com/SystemErrorWang/White-box-Cartoonization
# https://www.runwayml.com

# =========================================================================

import runway
from runway.data_types import number, text, image, category, boolean
from inpaint_model import PhotoInpaintModel

effect_types = ['dolly-zoom-in', 'zoom-in', 'circle', 'swing']

setup_options = {
    'model_path': text(description='Model path. Empty string = default model.'),
}
@runway.setup(options=setup_options)
def setup(opts):
    model = PhotoInpaintModel()
    return model

@runway.command(name='paint',
        inputs={
            'image': image(),
            'resize': number(default=0.5, min=0, max=1, step=0.1),
            'fps': number(default=24, min=1, max=120, step=1),
            'length_sec': number(default=2, min=1, max=10, step=0.2, description='Output video length in seconds.'),
            'effect_type': category(choices=effect_types, default=effect_types[1], description='Video effect.'),
            'effect_size': number(default=0.5, min=0, max=1, step=0.1),
            'reuse': boolean(default=False, description='Reuse depth map and continue from previous iteration.'),
        },
        outputs={
            'image': image()
        },
        description='Cartoonize.')
def paint(model, args):
    x_shift = 0
    y_shift = 0
    z_shift = 0
    traj_type = 'double-straight-line'
    effect_type = args['effect_type']
    effect_size = args['effect_size']*2

    if effect_type == 'dolly-zoom-in':
        x_shift = 0.00
        y_shift = 0.00
        z_shift = -0.05
        traj_type = 'double-straight-line'
    elif effect_type == 'zoom-in':
        x_shift = 0.00
        y_shift = 0.00
        z_shift = -0.05
        traj_type = 'double-straight-line'
    elif effect_type == 'circle':
        x_shift = -0.02
        y_shift = -0.02
        z_shift = -0.07
        traj_type = 'circle'
    elif effect_type == 'swing':
        x_shift = -0.02
        y_shift = -0.00
        z_shift = -0.07
        traj_type = 'circle'

    output_image = model.paint(args['image'], {
        'resize': args['resize'],
        'fps': args['fps'],
        'num_frames': args['fps'] * args['length_sec'],
        'reuse': args['reuse'],
        'x_shift': x_shift * effect_size,
        'y_shift': y_shift * effect_size,
        'z_shift': z_shift * effect_size,
        'traj_type': traj_type,
        'effect_type': effect_type
    })
    return {
        'image': output_image
    }

if __name__ == '__main__':
    runway.run(host='0.0.0.0', port=8000)
