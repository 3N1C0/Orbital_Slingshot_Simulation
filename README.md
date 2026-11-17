# Orbital Slingshot Simulation

A small Pygame physics simulation of a spacecraft using a gravitational slingshot around a planet. The planet pulls on the ship, and the ship's path bends around it.

## Files

| File | What it is |
|---|---|
| `main.py` | The simulation |
| `main2.py` | A tidier version with constants and asset loading grouped at the top. It also imports `imageio`. |
| `back3.jpg`, `mars.png` | Background and planet artwork |
| `simulation.gif` | A recording of the simulation |

## Skills demonstrated

- **Physics simulation:** gravitational attraction between a planet and a spacecraft, updated each frame.
- **Game loop design:** a fixed-rate loop at 60 FPS that handles input, updates state and draws.
- **Object-oriented code:** separate `Planet` and `Spacecraft` classes.
- **Graphics:** scaling and blitting images in Pygame.

## Run it

```bash
pip install pygame imageio
python main.py
```

Run the command from this folder so the image files are found.
