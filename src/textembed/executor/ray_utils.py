import os
from typing import Optional

import ray
from ray import serve


def initialize_ray_cluster(
    world_size: int,
    ray_address: Optional[str] = None,
):
    """Initialize the distributed cluster with Ray.

    It will connect to the Ray cluster and create a placement group
    for the workers, which includes the specification of the resources
    for each distributed worker.

    Args:
        world_size: world size.
        ray_address: The address of the Ray cluster. If None, uses
            the default Ray cluster address.
    """
    if ray is None:
        raise ImportError(
            "Ray is not installed. Please install Ray to use distributed serving."
        )

    # Connect to a Ray cluster.
    ray.init(address=ray_address, ignore_reinit_error=True)

    # Determine the number of CPU cores per worker
    num_cpus_per_worker = max(1, os.cpu_count() // world_size)

    # Create placement group for worker processes
    current_placement_group = ray.util.get_current_placement_group()
    if current_placement_group:
        # We are in a placement group
        bundles = current_placement_group.bundle_specs
        # Verify that we can use the placement group.
        for bundle in bundles:
            bundle_cpus = bundle.get("CPU", 0)
            if bundle_cpus != num_cpus_per_worker:
                raise ValueError(
                    f"Placement group bundle must have exactly {num_cpus_per_worker} CPU cores."
                )
    else:
        # Create a new placement group
        placement_group_specs = [{"CPU": num_cpus_per_worker}] * world_size
        current_placement_group = ray.util.placement_group(placement_group_specs)
        # Wait until placement group is ready
        ray.get(current_placement_group.ready(), timeout=1800)

    # Set the placement group in the parallel config
    current_placement_group
