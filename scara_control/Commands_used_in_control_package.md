**Terminal 1 — build and launch the simulation (Gazebo + RViz):**

```bash
cd ~/ros2_wsv1
colcon build
source install/setup.bash
ros2 launch scara_robot_description scara_gazebo.launch.py
```

**Terminal 2 — build and run the pick cycle:**

```bash
cd ~/ros2_wsv1
colcon build
source install/setup.bash
ros2 run scara_control pick_and_place
```