# Copyright 2026 Canonical Ltd.
# See LICENSE file for licensing details.

import subprocess

import pytest
from charmed_kubeflow_chisme.rock import CheckRock


@pytest.mark.abort_on_fail
def test_rock():
    """Test rock."""
    check_rock = CheckRock("rockcraft.yaml")
    rock_image = check_rock.get_name()
    rock_version = check_rock.get_version()
    LOCAL_ROCK_IMAGE = f"{rock_image}:{rock_version}"

    # assert the rock contains the expected files
    subprocess.run(
        ["docker", "run", "--rm", LOCAL_ROCK_IMAGE, "exec", "ls", "-la", "/keda"],
        check=True,
    )

    # assert the tz database is present (needed by the cron scaler's `timezone` field)
    subprocess.run(
        ["docker", "run", "--rm", LOCAL_ROCK_IMAGE, "exec", "ls", "/usr/share/zoneinfo/Etc/UTC"],
        check=True,
    )
