import numpy as np
import scipy.stats
from yupi.analyzing import turning_angles, subsample_trajectory

# relative and cumulative turning angles
def estimate_turning_angles(trajs, accumulate=False, 
                    degrees=False, centered=False):
    theta = [turning_angles(traj) for traj in trajs]
    return np.concatenate(theta)


# Returns measured velocity samples on all the trajectories
# subsampling them at a given stem
def estimate_velocity_samples(trajs, step):
    step = 1
    trajs_ = [subsample_trajectory(traj, step) for traj in trajs]
    return np.concatenate([traj.velocity() for traj in trajs_])


# get position vectors by components
def get_position_vectors(traj):
    # get the components of the position
    r = traj.data[:traj.dim]

    # transpose to have time/dimension as first/second axis
    r = np.transpose(r)
    return r


# get velocity vectors by components
def get_velocity_vectors(traj):
    v = []
    
    # append velocity x-component
    vx = traj.x_velocity()
    v.append(vx)

    # append velocity y-component
    if traj.dim >= 2:
        vy = traj.y_velocity()
        v.append(vy)

    # append velocity z-component
    if traj.dim == 3:
        vz = traj.z_velocity()
        v.append(vz)

    # transpose to have time/dimension as first/second axis
    v = np.transpose(v)
    return v


# get displacements for ensemble average and
# kurtosis for time average
# TODO: Fix this implementation for dim != 2 Traj
def estimate_kurtosis(trajs, time_avg=True, lag=None):
    kurtosis = []
    for traj in trajs:
        if not time_avg:
            dx = traj.x - traj.x[0]
            dy = traj.y - traj.y[0]
            kurt = np.sqrt(dx**2 + dy**2)

        # time average
        else:
            kurt = np.empty(lag)
            for lag_ in range(1, lag + 1):
                dx = traj.x[lag_:] - traj.x[:-lag_]
                dy = traj.y[lag_:] - traj.y[:-lag_]
                dr = np.sqrt(dx**2 + dy**2)
                kurt[lag_ - 1] = scipy.stats.kurtosis(dr, fisher=False)

        kurtosis.append(kurt)

    if not time_avg:
        return scipy.stats.kurtosis(kurtosis, axis=0, fisher=False)
    else:
        return np.mean(kurtosis, axis=0)
