def test_something():
    import fiducialreg  # noqa: F401


def test_affine_transform_cpu_respects_voxel_size():
    """A world-coordinate transform must be applied in world units.

    Regression for a bug where the intrinsic->world->intrinsic sampling map was
    computed but discarded, so a translation in microns was applied as if it were
    pixels -- under-applying the transform by the voxel-size factor.
    """
    import numpy as np
    from scipy import ndimage

    from fiducialreg.fiducialreg import affine_transform_cpu

    im = np.zeros((4, 32, 32), dtype="f")
    im[2, 16, 16] = 1.0
    dx = 0.1  # microns / pixel (x, y)

    # pure +1.0 micron translation along x (the last axis), in world coordinates
    tmat = np.eye(4, dtype="f")
    tmat[2, 3] = 1.0

    # with physical voxels the feature must move 1.0 / dx = 10 px, not 1 px
    out = affine_transform_cpu(im, tmat, dzyx=[0.2, dx, dx])
    _, _, x = np.unravel_index(int(np.argmax(out)), out.shape)
    assert abs(abs(x - 16) - 10) <= 1, f"feature moved {x - 16}px, expected ~10"

    # with unit voxel size the result is identical to the plain intrinsic path
    out_unit = affine_transform_cpu(im, tmat, dzyx=[1, 1, 1])
    ref = ndimage.affine_transform(
        im, tmat[:3, :3], offset=tmat[:3, 3], output_shape=im.shape, order=1
    )
    assert np.allclose(out_unit, ref)
