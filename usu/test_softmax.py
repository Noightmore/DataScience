import numpy as np


def softmax(u):
    """
    vstupem muze byt skalar, vektor, nebo matice
    """
    # Shift input for numerical stability
    u_max = np.max(u, axis=-1, keepdims=True)
    u_shifted = u - u_max

    # Compute softmax
    exp_u = np.exp(u_shifted)
    softmax_output = exp_u / np.sum(exp_u, axis=-1, keepdims=True)

    return softmax_output


def test_softmax():
    # Scalar input
    u_scalar = 1
    output_scalar = softmax(u_scalar)
    assert np.allclose(output_scalar, 1.0)

    # Vector input
    u_vector = np.array([1, 2, 3])
    output_vector = softmax(u_vector)
    expected_output_vector = np.array([0.09003057, 0.24472847, 0.66524096])
    assert np.allclose(output_vector, expected_output_vector)

    # Matrix input
    u_matrix = np.array([[1, 2], [3, 4], [5, 6]])
    output_matrix = softmax(u_matrix)
    expected_output_matrix = np.array([[0.26894142, 0.73105858],
                                       [0.26894142, 0.73105858],
                                       [0.26894142, 0.73105858]])
    assert np.allclose(output_matrix, expected_output_matrix)

    # Large random input
    u_large = np.random.rand(10, 1000)
    output_large = softmax(u_large)
    assert np.allclose(np.sum(output_large, axis=-1), np.ones(10))

    print("All tests pass")


if __name__ == "__main__":
    test_softmax()
