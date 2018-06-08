# Q Learning (Marine Builder bot)
Bot that tries to learn to build marines (20 in this case) as fast and as efficiently as possible.
 
- to run my source code file `marine_builder.py` you need to modify the code in `run_loop.py` of pysc2 in the `env` folder
- right before `timesteps = env.step(actions)` add 
```python
 if True in actions:
      break
```
