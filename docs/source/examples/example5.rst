Example 5
=========

Simultaneous tracking of an ant and the camera capturing its movement 
with the reconstruction of the trajectory of the ant respect its 
initial position. Code and multimedia resources are 
available `here <https://github.com/yupidevs/yupi_examples/>`_.

The robot designed in [1] allowed to extend the study of the motion 
of insects for longer times and wider regions. The robot, keeping 
a proper distance from the insect, continuously moves to preserve 
the insect always in the scene recorded by its camera.

However, the fact of having both, the insect and the camera, moving at 
the same time, introduces additional complications while reconstructing 
the trajectory from a video source. yupi handles the motion of the camera 
naturally as part of the TrackingScenario.

In this example, we shown how to reproduce the results of the original paper, 
using one of the videos the authors used to compute the position of an 
ant respect its original position, dealing with the movement of the camera.


The example is structured as follows:
 #. Setup dependencies
 #. Tracking tracking objects
 #. Results
 #. References

1. Setup dependencies
---------------------

Import all the dependencies:

.. code-block:: python

   from yupi.tracking import ROI, ObjectTracker, CameraTracker, TrackingScenario
   from yupi.tracking import RemapUndistorter
   from yupi.tracking import ColorMatching
   from yupi.analyzing import plot_trajectories

Set up the path to multimedia resources:

.. code-block:: python

   video_path = 'resources/videos/Serrano2019.mp4'
   camera_file = 'resources/cameras/gph3+1080-60fps-MEDIUM.npz'


2. Tracking tracking objects
----------------------------

First, we create an instance of an undistorter to correct the distortion 
caused by the camera lens.

.. code-block:: python

   undistorter = RemapUndistorter(camera_file)


Then, we initialize a tracker for the camera:

.. code-block:: python

   camera = CameraTracker(ROI((.65, .65), ROI.CENTER_INIT_MODE))

And a tracker for the ant using ColorMatching algorithm:

.. code-block:: python

   algorithm = ColorMatching((20,20,20), (65,65,65))
   ant = ObjectTracker('ant', algorithm, ROI((120, 120), scale=0.75))

Next, we create a TrackingScenario with the ant Tracker, the CameraTracker and 
the Undistorter:

.. code-block:: python

   scenario = TrackingScenario([ant], camera, undistorter, preview_scale=0.75)

Then, we track the video using the configured scenario. We should notice 
that we will have to initialize the Region-of-Interest (ROI) of the ant tracker 
manually. 

.. code-block:: python

   retval, tl = scenario.track(video_path, pix_per_m=6300)




3. Results
----------
Now, we can produce a plot quite similar to the one of the original paper [1]:

.. code-block:: python

   plot_trajectories(tl)

.. figure:: /images/example5.png
   :alt: Output of example5
   :align: center



4. References
--------------------------

| [1] Serrano-Muñoz, A., et al. "An autonomous robot for continuous tracking of millimetric-sized walkers." Review of Scientific Instruments 90.1 (2019): 014102.