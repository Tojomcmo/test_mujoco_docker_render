import mujoco
import numpy as np
from PIL import Image


if __name__ == "__main__":
    # Load the MuJoCo model
    model = mujoco.MjModel.from_xml_path("model_xml_files/pendulum.xml")
    data = mujoco.MjData(model)

    # Create a MuJoCo visualization context using OSMesa
    # mujoco.set_mj_gl_context(egl=True)
    context = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150)
    scene = mujoco.MjvScene(model, maxgeom=1000)
    option = mujoco.MjvOption()

    num_steps = 100
    for _ in range(num_steps):
        mujoco.mj_step(model, data)

        # Update the scene and render offscreen
        mujoco.mjv_updateScene(
            model, data, option, None, mujoco.mjtCatBit.mjCAT_ALL, scene
        )
        mujoco.mjr_render(mujoco.MjrRect(0, 0, 640, 480), scene, context)

        # Read the pixels from the offscreen buffer
        rgb_buffer = np.zeros((480, 640, 3), dtype=np.uint8)
        depth_buffer = np.zeros((480, 640), dtype=np.float32)
        mujoco.mjr_readPixels(
            rgb_buffer, depth_buffer, mujoco.MjrRect(0, 0, 640, 480), context
        )

        # Convert the RGB buffer to an image and save it
        image = Image.fromarray(rgb_buffer)
        image.save(f"frame_{_:04d}.png")

    print("Rendering complete. Frames saved as frame_XXXX.png.")
