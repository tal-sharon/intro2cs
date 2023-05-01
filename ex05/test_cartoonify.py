import cartoonify

def test_separate_channels():
# TODO separate_channels([[[1, 2]]]) → [[[1]], [[2]]]


def test_combine_channels():
# TODO combine_channels([[[1]], [[2]]]) → [[[1, 2]]]


def test_RGB2grayscale():
# TODO RGB2grayscale ([[[100, 180, 240]]]) → [[163]]


def test_blur_kernel():
# TODO blur_kernel(3) → [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]


def test_apply_kernel():
# TODO apply_kernel([[0, 128, 255]], blur_kernel(3)) → [[14, 128, 241]]


def test_bilinear_interpolation():
# TODO bilinear_interpolation([[0, 64], [128, 255]], 0, 0) → 0
# TODO bilinear_interpolation([[0, 64], [128, 255]], 1, 1) → 255
# TODO bilinear_interpolation([[0, 64], [128, 255]], 0.5, 0.5) → 112
# TODO bilinear_interpolation([[0, 64], [128, 255]], 0.5, 1) → 160


def test_resize():


def test_rotate_90():
# TODO rotate_90([[1, 2, 3], [4, 5, 6]], 'R') → [[4, 1], [5, 2], [6, 3]]
# TODO rotate_90([[1, 2, 3], [4, 5, 6]], 'L') → [[3, 6], [2, 5], [1, 4]]

def test_get_edges():
# TODO get_edges([[200, 50, 200]], 3, 3, 10) → [[255, 0, 255]]


def test_quantize():
# TODO quantize([[0, 50, 100], [150, 200, 250]], 8) → [[0, 32, 96], [128, 191, 223]]

def test_quantize_colored_image():


def test_add_mask():
# TODO add_mask([[50, 50, 50]], [[200, 200, 200]], [[0, 0.5, 1]]) → [[200, 125, 50]]


def test_cartoonify():





